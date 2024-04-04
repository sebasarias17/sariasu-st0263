import grpc
import Service_pb2
import Service_pb2_grpc
from concurrent import futures
import os

def dividir_archivo(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)
    archivos = []
    peso_archivo = os.path.getsize(ruta_archivo)
    print(peso_archivo)
    chunks_bytes = 3 * 1024 * 1024
    espacio_chunk = ((peso_archivo // chunks_bytes) +1 )* 1024 * 1024
    print(espacio_chunk)
    try:
        with open(ruta_archivo, 'rb') as archivo:
            numero_parte = 0
            while True:
                fragmento = archivo.read(espacio_chunk)
                archivos.append(fragmento)
                if not fragmento:
                    break
                numero_parte += 1
        return archivos
    except IOError as error:
        print(f'Error: {error}')

with grpc.insecure_channel('localhost:50051', options=[
    ('grpc.max_send_message_length', 100 * 1024 * 1024),
    ('grcp.max_receive_message_length', 100 * 1024 * 1024)
    ]) as channel:

    stub = Service_pb2_grpc.ClientCallServiceStub(channel)
    arreglo = dividir_archivo('./image.jpg')
    response = stub.sendPartitionFile(Service_pb2.File(content = arreglo))
    print(response.requestFile)

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