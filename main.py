from CvLAC.CvLAC import scrape_CvLAC
import pandas as pd
from docentes import docentes

df_projects = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])
df_articles = pd.DataFrame(columns=["Docente", "Titulo_del_articulo", "pais", "revista", "año_de_publicacion", "paginas", "editorial", "DOI", "ISSN"])
df_chaptersBooks = pd.DataFrame(columns=["Docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"])

scrape_CvLAC(df_projects=df_projects, df_articles=df_articles, df_chaptersBooks=df_chaptersBooks, docentes=docentes)
df_projects.to_csv('projects.csv', index=False)
df_articles.to_csv('articles.csv', index=False)
df_chaptersBooks.to_csv('chaptersBooks.csv', index=False)
