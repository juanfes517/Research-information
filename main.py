import pandas as pd
from docentes import docentes
from CvLAC.CvLAC import scrape_CvLAC
from ORCID.ORCID import scrape_ORCID

def CvLAC():
  df_projects = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])
  df_articles = pd.DataFrame(columns=["Docente", "Titulo_del_articulo", "pais", "revista", "año_de_publicacion", "paginas", "editorial", "DOI", "ISSN"])
  df_chaptersBooks = pd.DataFrame(columns=["Docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"])

  scrape_CvLAC(df_projects=df_projects, df_articles=df_articles, df_chaptersBooks=df_chaptersBooks, docentes=docentes)

  df_projects.to_csv('resultados/CvLAC/projects.csv', index=False)
  df_articles.to_csv('resultados/CvLAC/articles.csv', index=False)
  df_chaptersBooks.to_csv('resultados/CvLAC/chaptersBooks.csv', index=False)


def ORCID():

  df_books = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "autores"])
  df_chaptersBooks = pd.DataFrame(columns=["docente", "DOI", "URL", "año", "editorial", "paginas", "autores", "nombre_del_capitulo", "nombre_del_libro"])
  df_conferencePaper = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "volumen", "paginas", "auntores"])
  df_articles = pd.DataFrame(columns=["docente", "titulo", "revista", "año", "mes", "DOI", "URL", "editorial", "volumen", "numero", "paginas", "autores"])

  scrape_ORCID(
    df_books=df_books, 
    df_chaptersBooks=df_chaptersBooks, 
    df_conferencePaper=df_conferencePaper,
    df_articles = df_articles, 
    docentes=docentes)

  df_books.to_csv('resultados/ORCID/books.csv', index=False)
  df_chaptersBooks.to_csv('resultados/ORCID/chaptersBooks.csv', index=False)
  df_conferencePaper.to_csv('resultados/ORCID/conferencePaper.csv', index=False)
  df_articles.to_csv('resultados/ORCID/articles.csv', index=False)


ORCID()
