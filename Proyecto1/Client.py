import grpc
import Service_pb2
import Service_pb2_grpc
import os

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

with grpc.insecure_channel('localhost:50051', options=[
    ('grpc.max_send_message_length', 100 * 1024 * 1024),
    ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]) as channel:

    stub = Service_pb2_grpc.ClientCallServiceStub(channel)
    chunks, nombre_archivo = dividir_archivo('./image.jpg')
    for chunk, numero_parte in chunks:
        response = stub.sendPartitionFile(Service_pb2.File(
            content=chunk,
            fileName=nombre_archivo,
            partNumber=numero_parte
        ))
        print(response.requestFile)

    stored_chunks = stub.ListStoredChunks(Service_pb2.Empty())
    print("Chunks almacenados:", stored_chunks.chunks)

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