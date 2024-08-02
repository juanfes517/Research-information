import pandas as pd
from docentes import docentes
from CvLAC.CvLAC import scrape_CvLAC
from ORCID.ORCID import scrape_ORCID
from data_manager.libros import tratar_libros
from data_manager.proyectos import tratar_proyectos
from data_manager.articulos_de_conferencia import tratar_articulos_de_conferencia

def main():
  tratar_articulos_de_conferencia()

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

# Capitulos de libros de ambas paginas
# ["docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"]
# ["docente", "DOI", "URL", "año", "editorial", "paginas", "autores", "nombre_del_capitulo", "nombre_del_libro"]

# Articulos de ambas paginas
# ["docente", "titulo", "pais", "revista", "año", "paginas", "editorial", "DOI", "ISSN"]
# ["docente", "titulo", "revista", "año", "mes", "DOI", "URL", "editorial", "volumen", "numero", "paginas", "autores"]

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