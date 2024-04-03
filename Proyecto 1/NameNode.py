import os

def dividir_archivo(ruta_archivo, tamaño_bloque, carpeta_particiones='Particiones'):
    nombre_archivo = os.path.basename(ruta_archivo)
    archivos = []

    # Verificar si la carpeta de particiones existe, si no, crearla
    if not os.path.exists(carpeta_particiones):
        os.makedirs(carpeta_particiones)

    try:
        with open(ruta_archivo, 'rb') as archivo:
            numero_parte = 0
            while True:
                fragmento = archivo.read(tamaño_bloque)
                if not fragmento:
                    break
                numero_parte += 1
                nombre, extension = os.path.splitext(nombre_archivo)
                nombre_nuevo_archivo = f'{carpeta_particiones}/{nombre}_{numero_parte}{extension}'
                with open(nombre_nuevo_archivo, 'wb') as archivo_parte:
                    archivo_parte.write(fragmento)
                    archivos.append(nombre_nuevo_archivo)
                print(f'Creado {nombre_nuevo_archivo}')
        return archivos
    except IOError as error:
        print(f'Error: {error}')
    else:
        print('Particionamiento de archivo completado.')

def juntar_archivo(archivos, carpeta_uni = 'Archivos Unificados'):

    if not os.path.exists(carpeta_uni):
        os.makedirs(carpeta_uni)

    archivos_content = b""
    for ruta_archivo in archivos:
        try:
            with open(ruta_archivo, 'rb') as archivo:
                fragmento = archivo.read()
                archivos_content += fragmento
        except IOError as error:
            print(f'Error al leer el archivo {ruta_archivo}: {error}')
            return
    
    ruta_salida = os.path.join(carpeta_uni, 'archivo_nuevo.docx')
    with open(ruta_salida, 'wb') as f:
        f.write(archivos_content)


# Uso de la función
RUTA_ARCHIVO = './Archivo1.docx'
TAMAÑO_BLOQUE = 2048 
# RUTA_UNIFICADO = './Archivos Unificados'
array = dividir_archivo(RUTA_ARCHIVO, TAMAÑO_BLOQUE)
juntar_archivo(array)