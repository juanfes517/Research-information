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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein

def main():
  Scimagojr()

def jaccard_similarity(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) * 100



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