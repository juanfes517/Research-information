import os
import pandas as pd

# Por el momento este tipo de dataset no necesita ningun tratamiento
def tratar_libros():
  ruta_csv = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/libros.csv')
  df_libros = pd.read_csv(ruta_csv)


  df_libros.to_csv('resultados/tratados/libros.csv', index=False)