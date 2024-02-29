from Core.Fuentes import Fuentes
from Core.Area import Area
from Core.Posicion2D import Posicion2D

fuentes = Fuentes("prueba.jpg", Area(25,105,100,100), Posicion2D(25,105), Posicion2D(425,105))
fuentes.generar_fuentes()