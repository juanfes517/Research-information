import pandas as pd
from docentes import docentes
from CvLAC.CvLAC import scrape_CvLAC
from ORCID.ORCID import scrape_ORCID
from data_manager.libros import tratar_libros
from data_manager.articulos import tratar_articulos
from data_manager.proyectos import tratar_proyectos
from scimago_journal.scimagojr import scrape_scimagojr
from data_manager.capitulos_de_libros import tratar_capitulos_de_libros
from data_manager.articulos_de_conferencia import tratar_articulos_de_conferencia

import Levenshtein

def main():
  Scimagojr()

  # text1 = 'ICASSP, IEEE International Conference on Acoustics, Speech and Signal Processing - Proceedings'
  # text2 = 'Proceedings - ICASSP, IEEE International Conference on Acoustics, Speech and Signal Processing'
  
  # text1 = '2015 20th symposium on signal processing images and computer vision stsiva'
  # text2 = '2015 20th Symposium on Signal Processing, Images and Computer Vision, STSIVA 2015 - Conference Proceedings'
  
  # text1 = 'Physical Review B'
  # text2 = 'PHYSICAL REVIEW D'
  
  # score = levenshtein_similarity(text1.lower(), text2.lower())
  # print(score)

def levenshtein_similarity(text1, text2):
  distance = Levenshtein.distance(text1, text2)
  max_len = max(len(text1), len(text2))
  return (1 - distance / max_len) * 100

def Scimagojr():
  df_articulos_de_conferencia = pd.read_csv('resultados/tratados/articulos_de_conferencia.csv')
  df_articulos = pd.read_csv('resultados/tratados/articulos.csv')

  scrape_scimagojr(
    df_articulos_de_conferencia=df_articulos_de_conferencia,
    df_articulos=df_articulos
  )

  df_articulos_de_conferencia.to_csv('resultados/tratados/articulos_de_conferencia.csv', index=False)
  df_articulos.to_csv('resultados/tratados/articulos.csv', index=False)

def CvLAC():
  df_proyectos = pd.DataFrame(columns=["docente", "tipo_de_proyecto", "nombre_del_proyecto", "inicio", "fin", "resumen"])
  df_articulos = pd.DataFrame(columns=["docente", "titulo", "pais", "revista", "año", "paginas", "editorial", "DOI", "ISSN"])
  df_capitulos_de_libros = pd.DataFrame(columns=["docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"])

  scrape_CvLAC(
    df_proyectos=df_proyectos,
    df_articulos=df_articulos,
    df_capitulos_de_libros=df_capitulos_de_libros,
    docentes=docentes)

  df_proyectos.to_csv('resultados/sin_tratar/CvLAC/proyectos.csv', index=False)
  df_articulos.to_csv('resultados/sin_tratar/CvLAC/articulos.csv', index=False)
  df_capitulos_de_libros.to_csv('resultados/sin_tratar/CvLAC/capitulos_de_libros.csv', index=False)

def ORCID():

  df_libros = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "autores"])
  df_capitulos_de_libros = pd.DataFrame(columns=["docente", "DOI", "URL", "año", "editorial", "paginas", "autores", "nombre_del_capitulo", "nombre_del_libro"])
  df_articulos_de_conferencia = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "autores"])
  df_articulos = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "mes", "DOI", "URL", "editorial", "volumen", "numero", "paginas", "autores"])

  scrape_ORCID(
    df_libros=df_libros, 
    df_capitulos_de_libros=df_capitulos_de_libros, 
    df_articulos_de_conferencia=df_articulos_de_conferencia,
    df_articulos = df_articulos, 
    docentes=docentes)

  df_libros.to_csv('resultados/sin_tratar/ORCID/libros.csv', index=False)
  df_capitulos_de_libros.to_csv('resultados/sin_tratar/ORCID/capitulos_de_libros.csv', index=False)
  df_articulos_de_conferencia.to_csv('resultados/sin_tratar/ORCID/articulos_de_conferencia.csv', index=False)
  df_articulos.to_csv('resultados/sin_tratar/ORCID/articulos.csv', index=False)


if __name__ == "__main__":
  main()