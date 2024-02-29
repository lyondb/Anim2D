import cv2
import numpy as np
from Core.Color import Color

class Fuentes():
    def __init__(self,ruta_imagen, area, posicion_inicial, posicion_final, numero_imagenes=24):
        self.ruta_imagen= ruta_imagen
        self.area = area
        self.posicion_inicial = posicion_inicial
        self.posicion_final = posicion_final
        self.numero_imagenes=numero_imagenes
        self.imagen = self.leer_imagen()

    def leer_imagen(self):
        imagen = cv2.imread(self.ruta_imagen)
        if imagen is None:
            print("La imagen no existe")
            return None
        return imagen

    def seleccionar_area(self):
        seccion = self.imagen[self.area.yInicial:self.area.yInicial + self.area.alto, self.area.xInicial:self.area.xInicial + self.area.ancho]
        seccion.refinar(Color(255,255,255,255))
        return seccion

    def generar_fuentes(self):
        if self.imagen is None:
            return

        dx = (self.posicion_final.posX - self.posicion_inicial.posX) / (self.numero_imagenes - 1)
        dy = (self.posicion_final.posY - self.posicion_inicial.posY) / (self.numero_imagenes - 1)

        for i in range(self.numero_imagenes):
            imagen_modificada = self.imagen.copy()

            nueva_posicion_x = int(self.posicion_inicial.posX + dx * i)
            nueva_posicion_y = int(self.posicion_inicial.posY + dy * i)

            seccion_desplazada = self.seleccionar_area()

            # Calcular el área efectiva de la sección desplazada que puede ser insertada
            alto_efectivo = min(seccion_desplazada.shape[0], imagen_modificada.shape[0] - nueva_posicion_y)
            ancho_efectivo = min(seccion_desplazada.shape[1], imagen_modificada.shape[1] - nueva_posicion_x)

            if alto_efectivo <= 0 or ancho_efectivo <= 0:
                print("La sección desplazada está fuera de los límites de la imagen.")
                continue

            # Asegurarse de que solo se inserte la parte de la sección desplazada que encaja dentro de la imagen destino
            seccion_para_insertar = seccion_desplazada[:alto_efectivo, :ancho_efectivo]

            imagen_modificada[nueva_posicion_y:nueva_posicion_y + alto_efectivo,
            nueva_posicion_x:nueva_posicion_x + ancho_efectivo] = seccion_para_insertar

            cv2.imwrite(f'imagen_desplazada_{i + 1:02d}.jpg', imagen_modificada)

