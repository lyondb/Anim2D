import cv2
import os

# Directorio donde se encuentran tus imágenes
directorio_imagenes = 'D:\PycharmProjects\Anim2D'
# Nombre del archivo de salida
nombre_video_salida = 'video_desplazamiento.avi'
# Tasa de cuadros por segundo (FPS)
fps = 24

# Obtener la lista de archivos de imagen en el directorio
archivos_imagenes = [img for img in os.listdir(directorio_imagenes) if img.endswith(".jpg")]
archivos_imagenes.sort()  # Asegurarse de que las imágenes estén en orden secuencial

# Leer la primera imagen para obtener las dimensiones
imagen_ejemplo = cv2.imread(os.path.join(directorio_imagenes, archivos_imagenes[0]))
altura, ancho, capas = imagen_ejemplo.shape

# Configurar el objeto VideoWriter
# El codec 'DIVX' es común, pero puedes cambiarlo según tus necesidades
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video_salida = cv2.VideoWriter(nombre_video_salida, fourcc, fps, (ancho, altura))

# Añadir imágenes al video
for archivo in archivos_imagenes:
    imagen = cv2.imread(os.path.join(directorio_imagenes, archivo))
    video_salida.write(imagen)

# Finalizar y guardar el video
video_salida.release()

print("El video ha sido creado exitosamente.")
