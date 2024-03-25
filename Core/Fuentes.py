import cv2
import numpy as np
#import unittest
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
        imagen = cv2.imread(self.ruta_imagen,cv2.IMREAD_UNCHANGED)
        if imagen is None:
            print("La imagen no existe")
            return None
        else:
            if imagen.shape[2] == 3:
                imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2BGRA)
        return imagen

    def generar_background(self, ancho, alto, color):
        imagen = np.full((alto, ancho, 4), color, dtype=np.uint8)
        return imagen
    
    def combinar_con_fondo(self, seccion, fondo):
        fondo_actual = fondo

        for i in range(seccion.shape[0]):
            for j in range(seccion.shape[1]):
                if seccion[i, j][3] != 0 :
                    fondo_actual[i, j] = seccion[i, j]

        return fondo_actual

    def seleccionar_area(self):
        seccion = self.imagen[self.area.yInicial:self.area.yInicial + self.area.alto, self.area.xInicial:self.area.xInicial + self.area.ancho]
        seccion = self.refinar_seccion(seccion, 0, (255, 255, 255, 255))
        return seccion

    def refinar_por_color(self, seccion, color_fondo):
        # Asumiendo color_fondo como una tupla BGR (255,255,255,0) para blanco
        umbral = 240
        # Crear una máscara para píxeles donde los tres canales son mayores que el umbral
        mascara_blanco = cv2.inRange(seccion, (umbral, umbral, umbral,255), color_fondo)
        if seccion.shape[2] == 3:
            # Agregar un canal alpha a la sección, inicialmente opaco (255)
            seccion = cv2.cvtColor(seccion, cv2.COLOR_BGR2BGRA)
        # Invertir la máscara para tener los píxeles objetivo en blanco (255) y el resto en negro (0)
        mascara_invertida = cv2.bitwise_not(mascara_blanco)

        # Aplicar la máscara invertida al canal alpha para hacer transparentes los píxeles coincidentes
        seccion[:, :, 3] = mascara_invertida

        return seccion

    def refinar_por_bordes(self, seccion, bandera):
        # Convertir a escala de grises para la detección de bordes
        gray = cv2.cvtColor(seccion, cv2.COLOR_BGR2GRAY)
        # Detectar bordes
        edges = cv2.Canny(gray, 100, 200)
        # Opcional: convertir los bordes a 3 canales si es necesario para coincidir con la sección original
        edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edges_3ch

    def refinar_por_mascara(self, seccion, mascara):
        # Asegurarse de que la máscara es binaria
        mascara_binaria = cv2.threshold(mascara, 127, 255, cv2.THRESH_BINARY)[1]
        # Aplicar la máscara a la sección
        resultado = cv2.bitwise_and(seccion, seccion, mask=mascara_binaria)
        return resultado

    def refinar_seccion(self, seccion, modo, parametro):
        ## Todo: agregar validaciones de parametro
        ## Si modo es cero, parámetro debe ser un color
        ## Si modo es uno, parámetro debe ser un entero
        ## Si modo es dos, parámetro debe ser una imagen en blanco y negro.
        match modo:
            case 0:
                seccion = self.refinar_por_color(seccion, parametro)
            case 1:
                seccion = self.refinar_por_bordes(seccion, parametro)
            case 2:
                seccion = self.refinar_por_mascara(seccion, parametro)
        return seccion

    def generar_fuentes(self):
        if self.imagen is None:
            return

        dx = (self.posicion_final.posX - self.posicion_inicial.posX) / (self.numero_imagenes - 1)
        dy = (self.posicion_final.posY - self.posicion_inicial.posY) / (self.numero_imagenes - 1)

        imagen_with_no_object = self.imagen.copy()
        ancho_background_inicial = 120
        alto_background_inicial = 120

        if imagen_with_no_object.shape[2] == 3:
                imagen_with_no_object = cv2.cvtColor(imagen_with_no_object, cv2.COLOR_BGR2BGRA)
        background_image = self.generar_background(ancho_background_inicial, alto_background_inicial, (255, 255, 255, 255)) # genera un bg de color blanco

        pos_inicial_x = int(self.posicion_inicial.posX)
        pos_inicial_y = int(self.posicion_inicial.posY)

        imagen_with_no_object[pos_inicial_y:pos_inicial_y + ancho_background_inicial,
            pos_inicial_x:pos_inicial_x + alto_background_inicial, :] = background_image
        
        seccion_desplazada = self.seleccionar_area()

        for i in range(self.numero_imagenes):
            imagen_modificada = imagen_with_no_object.copy()
            if imagen_modificada.shape[2] == 3:
                imagen_modificada = cv2.cvtColor(imagen_modificada, cv2.COLOR_BGR2BGRA)

            nueva_posicion_x = int(self.posicion_inicial.posX + dx * i)
            nueva_posicion_y = int(self.posicion_inicial.posY + dy * i)

            # Calcular el área efectiva de la sección desplazada que puede ser insertada
            alto_efectivo = min(seccion_desplazada.shape[0], imagen_modificada.shape[0] - nueva_posicion_y)
            ancho_efectivo = min(seccion_desplazada.shape[1], imagen_modificada.shape[1] - nueva_posicion_x)

            if alto_efectivo <= 0 or ancho_efectivo <= 0:
                print("La sección desplazada está fuera de los límites de la imagen.")
                continue

            seccion_para_insertar = seccion_desplazada[:alto_efectivo, :ancho_efectivo, :]

            fondo_actual = imagen_modificada[nueva_posicion_y:nueva_posicion_y + alto_efectivo,
            nueva_posicion_x:nueva_posicion_x + ancho_efectivo, :]

            combinado = self.combinar_con_fondo(seccion_para_insertar, fondo_actual)

            # Insertar la sección en la imagen modificada
            imagen_modificada[nueva_posicion_y:nueva_posicion_y + alto_efectivo,
            nueva_posicion_x:nueva_posicion_x + ancho_efectivo, :] = combinado

            cv2.imwrite(f'out/imagen_desplazada_{i + 1:02d}.png', imagen_modificada)


