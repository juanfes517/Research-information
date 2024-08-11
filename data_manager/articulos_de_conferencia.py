import os
import pandas as pd

# En este método solo se esta llenando los datos nulos de la columna "año" por ceros
def tratar_articulos_de_conferencia():
  ruta_csv = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/articulos_de_conferencia.csv')
  df_articulos_de_conferencia = pd.read_csv(ruta_csv)

  # Transformación del tipo de la columna "año"
  df_articulos_de_conferencia['año'] = df_articulos_de_conferencia['año'].fillna(0)
  df_articulos_de_conferencia['año'] = df_articulos_de_conferencia['año'].astype(int)

  df_articulos_de_conferencia.to_csv('resultados/tratados/articulos_de_conferencia.csv', index=False)
