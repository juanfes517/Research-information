import os
import pandas as pd

def tratar_articulos():
  ruta_orcid = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/ORCID/articulos.csv')
  ruta_cvlac = os.path.join(os.path.dirname(__file__), '../resultados/sin_tratar/CvLAC/articulos.csv')

  df_articulos_orcid = pd.read_csv(ruta_orcid)
  df_articulos_cvlac = pd.read_csv(ruta_cvlac)

  df_articulos_orcid['año'] = df_articulos_orcid['año'].fillna(0)
  df_articulos_orcid['año'] = df_articulos_orcid['año'].astype(int)

  # Se eliminan los registros con una año menor a 2019
  df_articulos_orcid = df_articulos_orcid[df_articulos_orcid['año'] >= 2019]
  df_articulos_orcid = df_articulos_orcid.reset_index(drop=True)
  df_articulos_cvlac = df_articulos_cvlac[df_articulos_cvlac['año'] >= 2019]
  df_articulos_cvlac = df_articulos_cvlac.reset_index(drop=True)

  titulo_orcid = df_articulos_orcid['titulo'].tolist()
  titulo_cvlac = df_articulos_cvlac['titulo'].tolist()

  # Convertir los títulos a minúsculas
  df_articulos_orcid['titulo'] = df_articulos_orcid['titulo'].str.upper()
  df_articulos_cvlac['titulo'] = df_articulos_cvlac['titulo'].str.upper()

  # Realizar un merge en función de las columnas 'docente' y 'titulo'
  df_articulos = pd.merge(df_articulos_orcid, df_articulos_cvlac, on=['docente', 'titulo'], how='outer', suffixes=('_left', '_right'))

  # Rellenar valores vacíos con los valores del otro DataFrame
  for col in df_articulos_orcid.columns:
    if col in df_articulos_cvlac.columns and col not in ['docente', 'titulo']:
      df_articulos[col] = df_articulos[f"{col}_left"].combine_first(df_articulos[f"{col}_right"])
      df_articulos.drop(columns=[f"{col}_left", f"{col}_right"], inplace=True)

  # Seleccionar las columnas únicas
  for col in df_articulos_cvlac.columns:
    if col not in df_articulos_orcid.columns:
      df_articulos[col] = df_articulos[col].combine_first(df_articulos[col])

  # Reordenar las columnas
  final_columns = ['docente', 'titulo', 'pais', 'revista', 'año', 'mes', 'paginas', 'editorial', 'DOI', 'ISSN', 'URL', 'volumen', 'numero', 'autores']
  df_articulos = df_articulos[final_columns]

  df_articulos['año'] = df_articulos['año'].astype(int)

  df_articulos.to_csv('resultados/tratados/articulos.csv', index=False)
    