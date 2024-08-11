import os
import pandas as pd

# Tanto la columna 'inicio' y 'fin' tienen este formato <mes  año>, por lo tanto, 
# con este método, se estan separando en columnas difentes
def tratar_proyectos():

  ruta_csv = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/CvLAC/proyectos.csv')
  df_proyectos = pd.read_csv(ruta_csv)

  fechas_de_inicio = df_proyectos['inicio'].tolist()
  fechas_de_fin = df_proyectos['fin'].tolist()

  mes_inicio = []
  año_inicio = []
  mes_fin = []
  año_fin = []

  for fecha_inicio in fechas_de_inicio:
    if pd.isnull(fecha_inicio):
      mes_inicio.append(None)
      año_inicio.append(0)
    else:
      partes = fecha_inicio.split('  ')
      mes_inicio.append(partes[0].strip())
      año_inicio.append(partes[1].strip())

  for fecha_fin in fechas_de_fin:
    if pd.isnull(fecha_fin):
      mes_fin.append(None)
      año_fin.append(0)
    else:
      partes = fecha_fin.split('  ')
      mes_fin.append(partes[0].strip())
      año_fin.append(partes[1].strip())
  
  df_proyectos = df_proyectos.drop(columns=['inicio', 'fin'])
  
  df_proyectos['mes_inicio'] = mes_inicio
  df_proyectos['año_inicio'] = pd.to_numeric(año_inicio)
  df_proyectos['mes_fin'] = mes_fin
  df_proyectos['año_fin'] = pd.to_numeric(año_fin)

  df_proyectos.to_csv('resultados/tratados/proyectos.csv', index=False)


