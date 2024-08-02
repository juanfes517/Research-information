import os
import pandas as pd

def tratar_articulos_de_conferencia():
  ruta_csv = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/articulos_de_conferencia.csv')
  df_articulos_de_conferencia = pd.read_csv(ruta_csv)

  df_articulos_de_conferencia['año'] = df_articulos_de_conferencia['año'].fillna(0)
  df_articulos_de_conferencia['año'] = df_articulos_de_conferencia['año'].astype(int)

  df_articulos_de_conferencia = df_articulos_de_conferencia[df_articulos_de_conferencia['año'] >= 2019]
  df_articulos_de_conferencia = df_articulos_de_conferencia.reset_index(drop=True)

  df_articulos_de_conferencia.to_csv('resultados/tratados/articulos_de_conferencia.csv', index=False)

  # print(df_articulos_de_conferencia['año'])