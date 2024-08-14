import numpy as np

class Report:
  
  def __init__(self):
    self.revistas_no_encontradas = np.array([])
    self.revistas_sin_cuartiles = np.array([])
    self.revistas_con_cuatiles = np.array([])
    self.año_sin_cuartil = np.array([])

  def agregar_revista_no_encontradas(self, revista):
    self.revistas_no_encontradas = np.append(self.revistas_no_encontradas, revista)

  def agregar_revista_sin_cuartiles(self, revista):
    self.revistas_sin_cuartiles = np.append(self.revistas_sin_cuartiles, revista)

  def agregar_revista_con_cuartiles(self, revista):
    self.revistas_con_cuatiles = np.append(self.revistas_con_cuatiles, revista)

  def agregar_año_sin_cuartil(self, revista):
    self.año_sin_cuartil = np.append(self.año_sin_cuartil, revista)

  def mostrar_resultados(self):
    print('____________________________________________________________')
    print('Revistas no encontradas')
    print('Las siguientes revistas no fueron encontradas en scimagoJr\n')
    for revista in list(set(self.revistas_no_encontradas)):
      print('-',revista)
    print('____________________________________________________________\n\n')


    print('____________________________________________________________')
    print('Revistas sin cuartiles')
    print('Las siguientes revistas NO tienen el indice de cuartiles\n')
    for revista in list(set(self.revistas_sin_cuartiles)):
      print('-',revista)
    print('____________________________________________________________\n\n')


    print('____________________________________________________________')
    print('Revistas con cuartiles')
    print('Las siguientes revistas tienen el indice de cuartiles\n')
    for revista in list(set(self.revistas_con_cuatiles)):
      print('-',revista)
    print('____________________________________________________________\n\n')


    print('____________________________________________________________')
    print('Cuartil no definido en el año de publicación')
    print('Las siguientes revistas NO tienen cuartil en el año de publicación del articulo\n')
    for revista in list(set(self.año_sin_cuartil)):
      print('-',revista)
    print('____________________________________________________________\n\n')