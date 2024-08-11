import numpy as np

class Report:
  
  def __init__(self):
    self.revistas_no_encontradas = np.array([])
    self.revistas_sin_cuartiles = np.array([])
    self.revistas_con_cuatiles = np.array([])

  def agregar_revista_no_encontradas(self, revista):
    self.revistas_no_encontradas = np.append(self.revistas_no_encontradas, revista)

  def agregar_revista_sin_cuartiles(self, revista):
    self.revistas_sin_cuartiles = np.append(self.revistas_sin_cuartiles, revista)

  def agregar_revista_con_cuartiles(self, revista):
    self.revistas_con_cuatiles = np.append(self.revistas_con_cuatiles, revista)

  def mostrar_resultados(self):
    # Reporte de doncentes no encontrados
    print('____________________________________________________________')
    print('Revistas no encontradas')
    print('Las siguientes revistas no fueron encontradas en scimagoJr\n')
    for revista in self.revistas_no_encontradas:
      print('-',revista)
    print('____________________________________________________________\n\n')


    print('____________________________________________________________')
    print('Revistas sin cuartiles')
    print('Las siguientes revistas no tienen el indice de cuartiles\n')
    for revista in self.revistas_sin_cuartiles:
      print('-',revista)
    print('____________________________________________________________\n\n')


    print('____________________________________________________________')
    print('Revistas con cuartiles')
    print('Las siguientes revistas tienen el indice de cuartiles\n')
    for revista in self.revistas_con_cuatiles:
      print('-',revista)
    print('____________________________________________________________\n\n')

