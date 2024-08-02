import numpy as np
import unicodedata
from time import sleep
from selenium import webdriver
from ORCID.Report import Report
from ORCID.Extract_info import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scrape_ORCID(df_libros, df_capitulos_de_libros, df_articulos_de_conferencia, df_articulos, docentes):
  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre el navegador con la URL
  driver.get('https://orcid.org/')

  # Cierra la ventana emergente de cookies
  cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
  cookies.click()

  reporte = Report()

  for docente in docentes:
    input = driver.find_element(By.XPATH, '//*[@id="cy-search"]')
    input.clear()

    input.send_keys(docente)
    input.send_keys(Keys.RETURN)

    sleep(3)

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
      reporte.agregar_doncente_no_encontrado(docente)
      continue

    sleep(2)

    i = 1
    while True:

      type_text = ''
      year_text = ''

      try:
        type_html = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[1]/div/div[2]')
        
        # Dividir la cadena en dos partes usando '|'
        partes = type_html.text.split('|')

        # Tomar la parte después de '|'
        type_text = partes[1].strip()

        date_text = partes[0].strip()
        year_text = date_text.split('-')[0].strip()

        reporte.agregar_tipo_de_trabajo(type_text)

        # if type_text != 'Book chapter':
        #   i = i+1
        #   continue

      except Exception as e:
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

        #Extracción de información de elementos sin cita
        if type_text == 'Journal article':
          values = extract_article_without_citation(driver, i, year_text)
          values.insert(0, docente)
          df_articulos.loc[len(df_articulos)] = values
        elif type_text == 'Book chapter':
          values = extract_booksChapter_without_citation(driver, i, year_text)
          values.insert(0, docente)
          df_capitulos_de_libros.loc[len(df_capitulos_de_libros)] = values
        else:
          reporte.agregar_trabajo_sin_cita(nTrabajo=i, tipo_trabajo=type_text, año_trabajo=year_text, docente=docente)
        
        driver.execute_script("arguments[0].click();", hide_details)
        i = i+1
        continue

      try:
        # Presiona "Switch to expanded formatting"
        expanded_formatting = driver.find_element(By.XPATH, f'//*[@id="cy-expanded-citation-toggle-link"]')
        driver.execute_script("arguments[0].click();", expanded_formatting)
      except Exception as e:
        driver.execute_script("arguments[0].click();", hide_details)
        reporte.agregar_cita_no_valida(nTrabajo=i, tipo_trabajo=type_text, año_trabajo=year_text, docente=docente)
        i = i+1
        continue

      sleep(1)

      # Para obtener el posible xpath de la cita
      for j in range(1, 6):
        try: 
          xpath = f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[{j}]/div/div[2]/div/pre'
          cita = driver.find_element(By.XPATH, xpath)

          if type_text == 'Book':
            values = extract_book(cita.text)
            values.insert(0, docente)
            df_libros.loc[len(df_libros)] = values
          elif type_text == 'Book chapter' or ("title" in cita.text and "booktitle" in cita.text) :
            values = extract_booksChapter(cita.text)
            values.insert(0, docente)
            df_capitulos_de_libros.loc[len(df_capitulos_de_libros)] = values
          elif type_text == 'Conference paper':
            values = extract_conferencePaper(cita.text)
            values.insert(0, docente)
            df_articulos_de_conferencia.loc[len(df_articulos_de_conferencia)] = values
          elif type_text == 'Journal article':
            values = extract_article(cita.text)
            values.insert(0, docente)
            df_articulos.loc[len(df_articulos)] = values

          break
        except Exception as e:
          if j == 5:
            reporte.agregar_error_en_cita(nTrabajo=i, tipo_trabajo=type_text, año_trabajo=year_text, docente=docente)
          continue

      driver.execute_script("arguments[0].click();", hide_details)

      i = i+1
    driver.back()
    sleep(1)
    driver.back()

  reporte.mostrar_resultados()
  driver.quit()


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

