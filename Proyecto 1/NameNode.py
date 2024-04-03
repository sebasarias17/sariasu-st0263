import os

def dividir_archivo(ruta_archivo, tamaño_bloque):
    nombre_archivo = os.path.basename(ruta_archivo)
    archivos =[]
    
    try:
        with open(ruta_archivo, 'rb') as archivo:
            numero_parte = 0
            while True:
                fragmento = archivo.read(tamaño_bloque)
                if not fragmento:
                    break
                numero_parte += 1
                nombre, extension = os.path.splitext(nombre_archivo)
                nombre_nuevo_archivo = f'{nombre}_{numero_parte}{extension}'
                with open(nombre_nuevo_archivo, 'wb') as archivo_parte:
                    archivo_parte.write(fragmento)
                    archivos.append(fragmento)
                print(f'Creado {nombre_nuevo_archivo}')
            return archivos
    except IOError as error:
        print(f'Error: {error}')
    else:
        print('Particionamiento de archivo completado.')

def juntar_archivo(archivos):
   archivos_content= b""
   for _ in archivos:
       archivos_content += _
   with open('archivo_nuevo.docx', 'wb') as f:
       f.write(archivos_content)


# Uso de la función
RUTA_ARCHIVO = './Archivo1.docx'
TAMAÑO_BLOQUE = 2048 
# RUTA_PARTICIONES = './Particiones'
# RUTA_UNIFICADO = './Archivos Unificados'
array = dividir_archivo(RUTA_ARCHIVO, TAMAÑO_BLOQUE)
juntar_archivo(array)