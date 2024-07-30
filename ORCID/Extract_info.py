import bibtexparser
from selenium.webdriver.common.by import By

def extract_books(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    juournal = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    
    return [titulo, juournal, año, volumen, paginas, autores]


def extract_chaptersBooks(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    doi = quitar_caracteres(entry.get('doi', ''))
    url = quitar_caracteres(entry.get('url', ''))
    año = quitar_caracteres(entry.get('year', ''))
    editorial = quitar_caracteres(entry.get('publisher', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    nombre_del_capitulo = quitar_caracteres(entry.get('title', ''))
    nombre_del_libro = quitar_caracteres(entry.get('booktitle', ''))
    
    return [doi, url, año, editorial, paginas, autores, nombre_del_capitulo, nombre_del_libro]


def extract_conferencePaper(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    revista = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    
    return [titulo, revista, año, volumen, paginas, autores]


def extract_articles(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    revista = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    mes = quitar_caracteres(entry.get('month', ''))
    doi = quitar_caracteres(entry.get('doi', ''))
    url = quitar_caracteres(entry.get('url', ''))
    editorial = quitar_caracteres(entry.get('publisher', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    numero = quitar_caracteres(entry.get('number', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))

    return [titulo, revista, año, mes, doi, url, editorial, volumen, numero, paginas, autores]


def extract_articles_without_citation(driver, i, year):
  article = []

  # Extracción del titulo
  try:
    titulo = driver.find_element(By.XPATH, f'/html/body/app-root/div/div/app-my-orcid/main/div/div/div/app-main/section/app-work-stack-group/section/app-panels/div[2]/app-work-stack[{i}]/app-panel/div[1]/div[1]/h4')
    article.append(titulo.text)
  except Exception as e:
    article.append('')
  
  # Extracción del nombre de la revista
  try:
    revista = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[1]/div/div[1]/div/div[1]')
    article.append(revista.text)
  except Exception as e:
    article.append('')

  # Año
  article.append(year)

  # La mayoria no tiene mes, entonces no se agrega nada
  article.append('')

  # Extracción del DOI
  try:
    doi = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[1]/div/div[1]/div/app-display-external-ids/app-panel-data-line/div/a')
    article.append(doi.text)
  except Exception as e:
    article.append('')

  # Extracción de la URL
  try:
    url = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[1]/div/div[2]/div/a')
    article.append(url.text)
  except Exception as e:
    try: 
      url = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[2]/div/div[2]/div/a')
      article.append(url.text)
    except Exception as e:
      article.append('')

  # No hay editorial, entonces se deja en blanco
  article.append('')

  # No hay volumen, entonces se deja en blanco
  article.append('')

  # No hay numero, entonces se deja en blanco
  article.append('')

  # No hay paginas, entonces se deja en blanco
  article.append('')

  # Extracción de los autores
  try:
    autores = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[1]/div/div[1]/div/div[3]')
    article.append(autores.text.replace('CONTRIBUTORS: ', ''))
  except Exception as e:
    article.append('')

  return article


# Quita cierto caracteres de un string
def quitar_caracteres(text):
    replacements = {
        '{': '',
        '}': '',
        "'": '',
        "\\": '',
        '~n': 'ñ'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

