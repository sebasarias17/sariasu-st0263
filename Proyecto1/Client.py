import grpc
import Service_pb2
import Service_pb2_grpc
import os

def main():
    while True:
        print("\n")
        print("Seleccione una acción:")
        print("1. Subir un archivo.")
        print("2. Listar chunks almacenados.")
        print("3. Salir.")
        print("\n")

        choice = input("Ingrese el número de la acción: ")
        print("\n")

        if choice == '1':
            # Aquí el código para subir el archivo...

            def dividir_archivo(ruta_archivo):
                nombre_archivo = os.path.basename(ruta_archivo)
                archivos = []
                peso_archivo = os.path.getsize(ruta_archivo)
                chunks_bytes = 3 * 1024 * 1024
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

            def enviar_chunk_a_datanode(chunk, datanode_address, file_name, part_number):
                with grpc.insecure_channel(datanode_address,options=[
                ('grpc.max_send_message_length', 100 * 1024 * 1024),
                ('grpc.max_receive_message_length', 100 * 1024 * 1024)
                ] ) as channel:
                    stub = Service_pb2_grpc.DataNodeServiceStub(channel)
                    response = stub.StoreChunk(Service_pb2.Chunk(
                        content=chunk,
                        fileName=file_name,
                        partNumber=part_number
                    ))
                    return response
    
            # Lista de DataNodes
            data_nodes = ["localhost:50052", "localhost:50053", "localhost:50054"]
            chunks, nombre_archivo = dividir_archivo(input("Ingrese el arhcivo a subir: "))
            print("\n")

            # Envío de chunks utilizando Round-Robin
            for i, chunk in enumerate(chunks):
                datanode_address = data_nodes[i % len(data_nodes)]
                response = enviar_chunk_a_datanode(chunk[0], datanode_address, nombre_archivo, chunk[1])
                print(f"Chunk {i} enviado a {datanode_address}: {response.message}")
                print("\n")


        elif choice == '2':
            # Aquí el código para listar los chunks...

            def consultar_chunks_en_namenode(namenode_address):
                with grpc.insecure_channel(namenode_address) as channel:
                    stub = Service_pb2_grpc.NameNodeServiceStub(channel)
                    response = stub.ListAllStoredChunks(Service_pb2.Empty())
                    return response.chunks

            # Uso en el cliente
            chunks_info = consultar_chunks_en_namenode('localhost:50055')
            for datanode, chunk_names in chunks_info.items():
                print(f"DataNode {datanode} tiene los siguientes chunks:")
                for chunk_name in chunk_names.chunkName:
                    print(f" - {chunk_name}")
                print("\n")

        elif choice == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    main()

#    chunk_details = stub.GetChunkDetails(Service_pb2.Empty())
#    for chunk_key, size in chunk_details.chunkInfo.items(): 
#        print(f"Chunk: {chunk_key}, Tamaño: {size} bytes")


# def juntar_archivo(archivos, carpeta_uni = 'Archivos Unificados'):

#     if not os.path.exists(carpeta_uni):
#         os.makedirs(carpeta_uni)

#     archivos_content = b""
#     for ruta_archivo in archivos:
#         try:
#             with open(ruta_archivo, 'rb') as archivo:
#                 fragmento = archivo.read()
#                 archivos_content += fragmento
#         except IOError as error:
#             print(f'Error al leer el archivo {ruta_archivo}: {error}')
#             return
    
#     ruta_salida = os.path.join(carpeta_uni, 'archivo_nuevo.docx')
#     with open(ruta_salida, 'wb') as f:
#         f.write(archivos_content)


# Uso de la función
# array = dividir_archivo(RUTA_ARCHIVO)
# juntar_archivo(array)