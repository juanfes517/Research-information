import unicodedata
import bibtexparser
from time import sleep
from selenium import webdriver
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def scrape_ORCID(docentes):
  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre el navegador con la URL
  driver.get('https://orcid.org/')

  # Cierra la ventana emergente de cookies
  cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
  cookies.click()

  tipos_trabajos = np.array([])

  for docente in docentes:
    input = driver.find_element(By.XPATH, '//*[@id="cy-search"]')
    input.clear()

    input.send_keys(docente)
    input.send_keys(Keys.RETURN)

    sleep(2)

    no_match = False

    # Se verifica si el nombre del docente o el nombre de la Universidad de Antioquia aparezca en la primera o segunda fila
    for i in range(1, 3):
      first_name = driver.find_element(By.XPATH, f'//*[@id="main"]/app-results/div/table/tbody/tr[{i}]/td[2]')
      last_name = driver.find_element(By.XPATH, f'//*[@id="main"]/app-results/div/table/tbody/tr[{i}]/td[3]')
      afiliation = driver.find_element(By.XPATH, f'//*[@id="main"]/app-results/div/table/tbody/tr[{i}]/td[5]')

      # Se continua la busqueda si el por lo menos el nombre o apellido del 
      # docente coincide y se tiene la universidad en la afiliación

      match_name = normalizar(first_name.text) in normalizar(docente) or normalizar(last_name.text) in normalizar(docente)
      match_afiliation = normalizar('Universidad de Antioquia') in normalizar(afiliation.text) or normalizar('University of Antioquia') in normalizar(afiliation.text)
      
      if match_afiliation and match_name:
        link = driver.find_element(By.XPATH, f'//*[@id="main"]/app-results/div/table/tbody/tr[{i}]/td[1]/a')
        link.click()
        break
      elif i == 2:
        no_match = True

    if no_match:
      print('No se encontraron coincidencias para:', docente)
      continue

    sleep(2)

    i = 1
    while True:
      try:
        type_html = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[1]/div/div[2]')
        
        # Dividir la cadena en dos partes usando '|'
        partes = type_html.text.split('|')

        # Tomar la parte después de '|'
        type_text = partes[1].strip()

        # tipos_trabajos = np.append(tipos_trabajos, type_text)
        # print(docente, ':', type_text)
        
        # TODO: Hacer algo diferente segun el tipo
      except Exception as e:
        # print(e)
        break

      # Presiona "Show more detail"
      show_details = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[2]/div/a')
      driver.execute_script("arguments[0].scrollIntoView(true);", show_details)
      driver.execute_script("arguments[0].click();", show_details)
      hide_details = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[1]/div/div[2]/div/a')

      sleep(1.5)

      try:
        # Presiona "Show citation"
        show_citation = driver.find_element(By.XPATH, f'//*[@id="cy-citation-toggle-link"]')
        driver.execute_script("arguments[0].click();", show_citation)
      except Exception as e:
        driver.execute_script("arguments[0].click();", hide_details)
        print(f"El trabajo {i} de {docente} no tiene cita")
        print('----------------------------')
        i = i+1
        continue

      try:
        # Presiona "Switch to expanded formatting"
        expanded_formatting = driver.find_element(By.XPATH, f'//*[@id="cy-expanded-citation-toggle-link"]')
        driver.execute_script("arguments[0].click();", expanded_formatting)
      except Exception as e:
        driver.execute_script("arguments[0].click();", hide_details)
        print(f"No se encontro una cita valida para el trabajo: {i} del docente {docente}")
        print('----------------------------')
        i = i+1
        continue

      sleep(1)

      # Para obtener el posible xpath de la cita
      for j in range(1, 6):
        try: 
          xpath = f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[{j}]/div/div[2]/div/pre'
          cita = driver.find_element(By.XPATH, xpath)
          getValues(cita.text)
          break
        except Exception as e:
          if j == 5:
            print(f"ERROR al conseguir la cita en el trabajo: {i} del docente {docente}")
            print('----------------------------')
          continue

      driver.execute_script("arguments[0].click();", hide_details)

      i = i+1
    driver.back()
    sleep(1)
    driver.back()

  print(np.unique(tipos_trabajos))
  driver.quit()


def getValues(text):
  bib_database = bibtexparser.loads(text)

  # Extract the information
  for entry in bib_database.entries:
    doi = quitar_caracteres(entry.get('doi', ''))
    url = quitar_caracteres(entry.get('url', ''))
    year = quitar_caracteres(entry.get('year', ''))
    month = quitar_caracteres(entry.get('month', ''))
    publisher = quitar_caracteres(entry.get('publisher', ''))
    volume = quitar_caracteres(entry.get('volume', ''))
    number = quitar_caracteres(entry.get('number', ''))
    author = quitar_caracteres(entry.get('author', ''))
    title = quitar_caracteres(entry.get('title', ''))
    journal = quitar_caracteres(entry.get('journal', ''))
    
    # Print the extracted information
    print('-------------------------------')
    print(f"DOI: {doi}")
    print(f"URL: {url}")
    print(f"Year: {year}")
    print(f"Month: {month}")
    print(f"Publisher: {publisher}")
    print(f"Volume: {volume}")
    print(f"Number: {number}")
    print(f"Author: {author}")
    print(f"Title: {title}")
    print(f"Journal: {journal}")
    print('-------------------------------')


def normalizar(cadena):
  # Convertir a minúsculas
  cadena = cadena.lower()
  # Reemplazar guiones por espacios en blanco
  cadena = cadena.replace('-', ' ')
  # Eliminar tildes
  cadena = ''.join(
      c for c in unicodedata.normalize('NFD', cadena)
      if unicodedata.category(c) != 'Mn'
  )
  return cadena


# Quita cierto caracteres de un string
def quitar_caracteres(text):
    replacements = {
        '{': '',
        '}': '',
        "'":'',
        "\\":''
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text