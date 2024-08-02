import os
import pandas as pd

# En este método solo se estan eliminando los registros con una año menor a 2019 del dataset de libros.
def tratar_libros():
  ruta_csv = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/libros.csv')
  df_libros = pd.read_csv(ruta_csv)

  df_libros['año'] = pd.to_numeric(df_libros['año'])

  df_libros = df_libros[df_libros['año'] >= 2019]
  df_libros = df_libros.reset_index(drop=True)

  df_libros.to_csv('resultados/tratados/libros.csv', index=False)