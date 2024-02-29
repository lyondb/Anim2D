class Area():
    def __init__(self, xInicial, yInicial, ancho, alto):
        self.xInicial = xInicial
        self.yInicial = yInicial
        self.ancho = ancho
        self.alto = alto


    def refinarPorColor(self, color):
        pass
        #agregar código para definir el color transparente
        #Recorrer matríz que representa el área
        #Si el color del punto es igual al color pasado como parámetro
        #Ese punto debe ser transparente
        #si no, ese punto se mueve

    def refinarPorBorde(self, bandera = 0):
        pass
        #agregar el código para seleccionar los puntos a partir de los bordes
        #si bandera es cero, se seleccionan los puntos dentro de los bordes
        #si bandera es uno, se seleccionan los puntos fuera de los bordes
        #Definir los puntos que forman los bordes
        #Si el punto está dentro o fuera del borde, de acuerdo con la bandera
        #Se mueve.
    
    def refinarPorMascara(self):
        pass
        #Convertir el área de la imagen a blancos y negros y guardarla como máscara
        #Utilizar la operación lógica AND sobre el área y la máscara
        #si el resultado es cero se mueve
        #si el resultado es uno no se mueve (dependendiendo la operación lógica)
