import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_CvLAC(df_proyectos, df_articulos, df_capitulos_de_libros, docentes):

  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre el navegador con la URL
  driver.get('https://scienti.minciencias.gov.co/ciencia-war/jsp/enRecurso/IndexRecursoHumano.jsp')

  for docente in docentes:
    # Encuentra el elemento usando XPath
    input = driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/form/table/tbody/tr[6]/td[2]/input')
    input.clear()

    # Escribe en el input y presiona enter
    input.send_keys(docente)
    input.send_keys(Keys.RETURN)

    # Obtiene las dos primers filas de las tablas
    row_1 = driver.find_element(By.XPATH, '//*[@id="investigadores_row1"]/td[2]/a')
    row_2 = driver.find_element(By.XPATH, '//*[@id="investigadores_row2"]/td[2]/a')

    # Verifica si una de las dos filas tomadas tiene el nombre del docente
    if row_1.text == docente:
      elem = row_1
    elif row_2.text == docente:
      elem = row_2
    else:
      print('No se encontraron coincidencias de', docente)
      driver.back()
      continue
  
    elem.click()
    
    # Se guarda la pestaña original y se cambia el foco a la nueva
    original_window = driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])
    
    i = 2
    # Obtiene todos los proyectos
    while True:
      try:
        xpath = f'/html/body/div/div[3]/table/tbody/tr[86]/td/table/tbody/tr[{i}]/td/blockquote'
        proyecto = driver.find_element(By.XPATH, xpath)
        values = getValuesProjects(proyecto.text)
        values.insert(0, docente)
        df_proyectos.loc[len(df_proyectos)] = values
        i = i+1
      except Exception  as e:
        break

    i = 3
    # Obtiene todos los articulos
    while True:
      try:
        xpath = f'/html/body/div/div[3]/table/tbody/tr[37]/td/table/tbody/tr[{i}]/td/blockquote'
        articulo = driver.find_element(By.XPATH, xpath)
        values = getValuesArticles(articulo.text)
        values.insert(0, docente)
        df_articulos.loc[len(df_articulos)] = values
        i = i+2
      except Exception  as e:
        break
    
    i = 2
    # Obtiene todos los capitulos de libros
    while True:
      try:
        xpath = f'/html/body/div/div[3]/table/tbody/tr[39]/td/table/tbody/tr[{i}]/td/li/blockquote'
        chapter = driver.find_element(By.XPATH, xpath)
        values = getValuesChapters(chapter.text)
        values.insert(0, docente)
        df_capitulos_de_libros.loc[len(df_capitulos_de_libros)] = values
        i = i+1
      except Exception  as e:
        break
    
    #Se cierra la ventana actual, se cambia el foco a la pestaña original y se regresa a la pagina anterior
    driver.close()
    driver.switch_to.window(original_window)
    driver.back()
  
  driver.quit()

def getValuesProjects(text):
  # Expresiones regulares para extraer cada parte
  regex_tipo_proyecto = r"Tipo de proyecto:\s*(.*)"
  regex_nombre_proyecto = r"Tipo de proyecto:.*?\n(.*)"
  regex_inicio = r"Inicio:\s*([a-zA-Z]+\s*\d{4})"
  regex_fin = r"Fin:\s*([a-zA-Z]+\s*\d{4})"
  regex_duracion = r"Duración\s*([\w\s]+)"
  regex_resumen = r"Resumen\s*(.*)"

  # Buscar coincidencias
  tipo_proyecto = re.search(regex_tipo_proyecto, text)
  nombre_proyecto = re.search(regex_nombre_proyecto, text)
  inicio = re.search(regex_inicio, text)
  fin = re.search(regex_fin, text)
  duracion = re.search(regex_duracion, text)
  resumen = re.search(regex_resumen, text, re.DOTALL)  # re.DOTALL para que . coincida con \n

  # Guardar en variables (si hay coincidencias)
  tipo_proyecto = tipo_proyecto.group(1) if tipo_proyecto else ""
  nombre_proyecto = nombre_proyecto.group(1) if nombre_proyecto else ""
  inicio = inicio.group(1) if inicio else ""
  fin = fin.group(1) if fin else ""
  resumen = resumen.group(1).strip() if resumen else ""

  return [tipo_proyecto, nombre_proyecto, inicio, fin, resumen]


def getValuesArticles(text):
  # Encontrar el índice de "Palabras:"
  indice = text.find('Palabras:')

  # Si "Palabras:" está en el texto, cortarlo hasta ese punto
  if indice != -1:
      text = text[:indice]

  # Patrón para encontrar el nombre del artículo (entre comillas)
  article_title_pattern = r'"(.*?)"'
  # Patrón para encontrar el país (después de "En:" y antes del nombre de la revista, opcional)
  country_pattern = r'En:\s*(\w+\s*)?(?=\n)'
  # Patrón para encontrar el nombre de la revista (entre "En:" opcional país y "ISSN:")
  journal_name_pattern = r'En:\s*(?:\w+\s*)?\n(.*?)\s*ISSN:'
  # Patrón para encontrar el año de publicación (después del número de páginas y la coma)
  year_pattern = r',(\d{4}),'
  # Patrón para encontrar las páginas (entre "p." y la coma)
  pages_pattern = r'p\.(.*?)\s*,'
  # Patrón para encontrar la editorial (entre "ed:" y "v.")
  editorial_pattern = r'ed:\s*(.*?)\s*v\.'
  # Patrón para encontrar el DOI (después de "DOI:" o "doi:")
  doi_pattern = r'DOI:\s*(.*)'
  # Patrón para encontrar el ISSN (entre "ISSN:" y "ed:")
  issn_pattern = r'ISSN:\s*(.*?)\s*ed:'

  # Buscar los patrones en la citación
  article_title_match = re.search(article_title_pattern, text)
  country_match = re.search(country_pattern, text)
  journal_name_match = re.search(journal_name_pattern, text)
  year_match = re.search(year_pattern, text)
  pages_match = re.search(pages_pattern, text)
  editorial_match = re.search(editorial_pattern, text)
  doi_match = re.search(doi_pattern, text)
  issn_match = re.search(issn_pattern, text)

  # Extraer los valores si los patrones se encontraron
  article_title = article_title_match.group(1) if article_title_match else None
  country = country_match.group(1).strip() if country_match and country_match.group(1) else None
  journal_name = journal_name_match.group(1).strip() if journal_name_match else None
  publication_year = year_match.group(1) if year_match else None
  pages = pages_match.group(1).strip() if pages_match else None
  editorial = editorial_match.group(1).strip() if editorial_match else None
  doi = doi_match.group(1).strip() if doi_match else None
  issn = issn_match.group(1).strip() if issn_match else None

  return [article_title, country, journal_name, publication_year, pages, editorial, doi, issn]


def getValuesChapters(text):
  # Patrón para encontrar el nombre del capítulo (entre comillas)
  chapter_title_pattern = r'"(.*?)"'
  # Patrón para encontrar el nombre del libro (entre el capítulo y "En:")
  book_name_pattern = r'"[^"]*"\s*(.*?)\s*En:'
  # Patrón para encontrar el país (después de "En:" y antes de "ISBN:")
  country_pattern = r'En:\s*(.*?)\s*ISBN:'
  # Patrón para encontrar el año de publicación (después de la coma y antes de la palabra "ed")
  year_pattern = r',(\d{4})'
  # Patrón para encontrar la editorial (después de "ed:" y antes de "v.")
  editorial_pattern = r'ed:\s*(.*?)\s*,'
  # Patrón para encontrar las páginas (entre "p." y la coma)
  pages_pattern = r'p\.(.*?)\s*,'
  # Patrón para encontrar el ISBN (entre "ISBN:" y "ed:")
  isbn_pattern = r'ISBN:\s*([^ ]+)'

  # Buscar los patrones en la citación
  chapter_title_match = re.search(chapter_title_pattern, text)
  book_name_match = re.search(book_name_pattern, text)
  country_match = re.search(country_pattern, text)
  year_match = re.search(year_pattern, text)
  editorial_match = re.search(editorial_pattern, text)
  pages_match = re.search(pages_pattern, text)
  isbn_match = re.search(isbn_pattern, text)

  # Extraer los valores si los patrones se encontraron
  chapter_title = chapter_title_match.group(1) if chapter_title_match else None
  book_name = book_name_match.group(1).strip() if book_name_match else None
  country = country_match.group(1).strip() if country_match else None
  publication_year = year_match.group(1) if year_match else None
  editorial = editorial_match.group(1).strip() if editorial_match else None
  pages = pages_match.group(1).strip() if pages_match else None
  isbn = isbn_match.group(1).strip() if isbn_match else None

  return [chapter_title, book_name, country, publication_year, editorial, pages, isbn]