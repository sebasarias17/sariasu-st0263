import grpc
import Service_pb2
import Service_pb2_grpc
import os

REPLICATION_FACTOR = 2  # La cantidad de DataNodes a los que se replicará cada chunk

def dividir_archivo(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)
    peso_archivo = os.path.getsize(ruta_archivo)
    archivos = []
    chunks_bytes = 3 * 1024 * 1024  # Tamaño del chunk en bytes
    espacio_chunk = ((peso_archivo // chunks_bytes) + 1) * 1024 * 1024

    try:
        with open(ruta_archivo, 'rb') as archivo:
            numero_parte = 0
            while True:
                fragmento = archivo.read(espacio_chunk)
                if not fragmento:
                    break
                archivos.append((fragmento, numero_parte))
                numero_parte += 1
        return archivos, nombre_archivo
    except IOError as error:
        print(f'Error: {error}')
        return [], nombre_archivo

def enviar_chunk_a_datanode(chunk, file_name, part_number, data_nodes):
    for i in range(REPLICATION_FACTOR):
        datanode_address = data_nodes[i % len(data_nodes)]  # Selecciona el DataNode

        with grpc.insecure_channel(datanode_address, options=[
            ('grpc.max_send_message_length', 100 * 1024 * 1024),
            ('grpc.max_receive_message_length', 100 * 1024 * 1024)
        ]) as channel:
            stub = Service_pb2_grpc.DataNodeServiceStub(channel)
            response = stub.StoreChunk(Service_pb2.Chunk(
                content=chunk,
                fileName=file_name,
                partNumber=part_number
            ))
            if response.success:
                print(f"Chunk {part_number} replicado en {datanode_address}")
            else:
                print(f"Error al replicar el chunk {part_number} en {datanode_address}: {response.message}")


def consultar_chunks_en_namenode(namenode_address):
     with grpc.insecure_channel(namenode_address) as channel:
         stub = Service_pb2_grpc.NameNodeServiceStub(channel)
         response = stub.ListAllStoredChunks(Service_pb2.Empty())
         return response.chunks
     
def recuperar_chunk_de_datanode(datanode_address, file_name, part_number):
    with grpc.insecure_channel(datanode_address, options=[
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]) as channel:
        stub = Service_pb2_grpc.DataNodeServiceStub(channel)
        chunk_info = Service_pb2.ChunkInfo(fileName=file_name, partNumber=part_number)
        try:
            response = stub.GetChunk(chunk_info)
            return response.content if response else None
        except grpc.RpcError as e:
            print(f"Error al recuperar el chunk: {e}")
            return None

def unificar_chunks(chunks_recuperados, ruta_salida):
    directorio = os.path.dirname(ruta_salida)
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    with open(ruta_salida, 'wb') as archivo_salida:
        for _, chunk in sorted(chunks_recuperados.items()):
            if chunk is not None:
                archivo_salida.write(chunk)
            else:
                print("Advertencia: Se encontró un chunk faltante.")
    
def reconstruir_archivo(file_name, chunks_info):
    chunks_recuperados = {}
    for datanode, chunk_names in chunks_info.items():
        for chunk_name in chunk_names.chunkName:
            if file_name in chunk_name:
                _, part_number_str = chunk_name.rsplit('_', 1)
                part_number = int(part_number_str)
                
                if part_number not in chunks_recuperados:
                    chunk = recuperar_chunk_de_datanode(datanode, file_name, part_number)
                    if chunk is not None:
                        chunks_recuperados[part_number] = chunk
                    else:
                        print(f"No se pudo recuperar el chunk {part_number} desde {datanode}")

    # Unificar y guardar el archivo
    ruta_salida = os.path.join('ruta_para_guardar_archivos', file_name)
    unificar_chunks(chunks_recuperados, ruta_salida)


def main():
    data_nodes = ["54.87.188.179:50052", "44.211.137.11:50053", "34.204.7.252:50054"]

    while True:
        print("\nSeleccione una acción:")
        print("1. Subir un archivo.")
        print("2. Listar chunks almacenados.")
        print("3. Reconstruir un archivo.")
        print("4. Salir.\n")

        choice = input("Ingrese el número de la acción: ")

        if choice == '1':
            file_path = input("Ingrese la ruta del archivo a subir: ")
            chunks, nombre_archivo = dividir_archivo(file_path)

            if len(data_nodes) >= REPLICATION_FACTOR:
                for i, chunk in enumerate(chunks):
                    enviar_chunk_a_datanode(chunk[0], nombre_archivo, chunk[1], data_nodes)
                    data_nodes = data_nodes[REPLICATION_FACTOR:] + data_nodes[:REPLICATION_FACTOR]  # Rota después de replicar cada chunk
            else:
                print(f"Error: Se requieren al menos {REPLICATION_FACTOR} DataNodes para la replicación.")


        elif choice == '2':
            # La lógica para listar los chunks almacenados en los DataNodes
            chunks_info = consultar_chunks_en_namenode('3.82.203.139:50055')
            for datanode, chunk_names in chunks_info.items():
                print(f"DataNode {datanode} tiene los siguientes chunks:")
                for chunk_name in chunk_names.chunkName:
                    print(f" - {chunk_name}")
            
        elif choice == '3':
            file_name = input("Ingrese el nombre del archivo a reconstruir: ")
            chunks_info = consultar_chunks_en_namenode('3.82.203.139:50055')
            reconstruir_archivo(file_name, chunks_info)

        elif choice == '4':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    main()