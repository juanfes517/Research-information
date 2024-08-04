import os
import pandas as pd

def tratar_capitulos_de_libros():
  ruta_orcid = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/capitulos_de_libros.csv')
  ruta_cvlac = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/CvLAC/capitulos_de_libros.csv')

  df_capitulos_de_libros_orcid = pd.read_csv(ruta_orcid)
  df_capitulos_de_libros_cvlac = pd.read_csv(ruta_cvlac)

  df_capitulos_de_libros_orcid['año'] = df_capitulos_de_libros_orcid['año'].fillna(0)
  df_capitulos_de_libros_orcid['año'] = df_capitulos_de_libros_orcid['año'].astype(int)

  df_capitulos_de_libros_orcid = df_capitulos_de_libros_orcid[df_capitulos_de_libros_orcid['año'] >= 2019]
  df_capitulos_de_libros_orcid = df_capitulos_de_libros_orcid.reset_index(drop=True)
  df_capitulos_de_libros_cvlac = df_capitulos_de_libros_cvlac[df_capitulos_de_libros_cvlac['año'] >= 2019]
  df_capitulos_de_libros_cvlac = df_capitulos_de_libros_cvlac.reset_index(drop=True)

  # Convertir los valores de 'nombre_del_capitulo' a minúsculas
  df_capitulos_de_libros_orcid['nombre_del_capitulo'] = df_capitulos_de_libros_orcid['nombre_del_capitulo'].str.upper()
  df_capitulos_de_libros_cvlac['nombre_del_capitulo'] = df_capitulos_de_libros_cvlac['nombre_del_capitulo'].str.upper()

  # Realizar un merge en función de las columnas 'docente' y 'nombre_del_capitulo'
  df_capitulos_de_libros = pd.merge(df_capitulos_de_libros_orcid, df_capitulos_de_libros_cvlac, on=['docente', 'nombre_del_capitulo'], how='outer', suffixes=('_left', '_right'))

  # Rellenar valores vacíos con los valores del otro DataFrame
  for col in df_capitulos_de_libros_orcid.columns:
      if col in df_capitulos_de_libros_cvlac.columns and col not in ['docente', 'nombre_del_capitulo']:
          df_capitulos_de_libros[col] = df_capitulos_de_libros[f"{col}_left"].combine_first(df_capitulos_de_libros[f"{col}_right"])
          df_capitulos_de_libros.drop(columns=[f"{col}_left", f"{col}_right"], inplace=True)

  # Seleccionar las columnas únicas
  for col in df_capitulos_de_libros_cvlac.columns:
      if col not in df_capitulos_de_libros_orcid.columns:
          df_capitulos_de_libros[col] = df_capitulos_de_libros[col].combine_first(df_capitulos_de_libros[col])

  # Reordenar las columnas
  final_columns = ['docente', 'nombre_del_capitulo', 'nombre_del_libro', 'pais', 'año', 'editorial', 'paginas', 'ISBN', 'DOI', 'URL', 'autores']
  df_capitulos_de_libros = df_capitulos_de_libros[final_columns]

  df_capitulos_de_libros['año'] = df_capitulos_de_libros['año'].astype(int)

  df_capitulos_de_libros.to_csv('resultados/tratados/capitulos_de_libros.csv', index=False)