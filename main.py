import pandas as pd
from docentes import docentes
from CvLAC.CvLAC import scrape_CvLAC
from ORCID.ORCID import scrape_ORCID

def CvLAC():
  df_proyectos = pd.DataFrame(columns=["docente", "tipo_de_proyecto", "nombre_del_proyecto", "inicio", "fin", "resumen"])
  df_articulos = pd.DataFrame(columns=["docente", "titulo", "pais", "revista", "año", "paginas", "editorial", "DOI", "ISSN"])
  df_capitulos_de_libros = pd.DataFrame(columns=["docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"])

  scrape_CvLAC(
    df_proyectos=df_proyectos,
    df_articulos=df_articulos,
    df_capitulos_de_libros=df_capitulos_de_libros,
    docentes=docentes)

  df_proyectos.to_csv('resultados/CvLAC/proyectos.csv', index=False)
  df_articulos.to_csv('resultados/CvLAC/articulos.csv', index=False)
  df_capitulos_de_libros.to_csv('resultados/CvLAC/capitulos_de_libros.csv', index=False)

# Capitulos de libros de ambas paginas
# ["docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"]
# ["docente", "DOI", "URL", "año", "editorial", "paginas", "autores", "nombre_del_capitulo", "nombre_del_libro"]

# Articulos de ambas paginas
# ["docente", "titulo", "pais", "revista", "año", "paginas", "editorial", "DOI", "ISSN"]
# ["docente", "titulo", "revista", "año", "mes", "DOI", "URL", "editorial", "volumen", "numero", "paginas", "autores"]

def ORCID():

  df_libros = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "autores"])
  df_capitulos_de_libros = pd.DataFrame(columns=["docente", "DOI", "URL", "año", "editorial", "paginas", "autores", "nombre_del_capitulo", "nombre_del_libro"])
  df_articulos_de_conferencia = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "auntores"])
  df_articulos = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "mes", "DOI", "URL", "editorial", "volumen", "numero", "paginas", "autores"])

  scrape_ORCID(
    df_libros=df_libros, 
    df_capitulos_de_libros=df_capitulos_de_libros, 
    df_articulos_de_conferencia=df_articulos_de_conferencia,
    df_articulos = df_articulos, 
    docentes=docentes)

  df_libros.to_csv('resultados/ORCID/libros.csv', index=False)
  df_capitulos_de_libros.to_csv('resultados/ORCID/capitulos_de_libros.csv', index=False)
  df_articulos_de_conferencia.to_csv('resultados/ORCID/articulos_de_conferencia.csv', index=False)
  df_articulos.to_csv('resultados/ORCID/articulos.csv', index=False)


ORCID()
