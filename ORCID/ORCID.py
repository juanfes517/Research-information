import numpy as np
import unicodedata
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ORCID.Extract_info import extract_books, extract_chaptersBooks, extract_conferencePaper


def scrape_ORCID(df_books, df_chaptersBooks, df_conferencePaper, docentes):
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

      type_text = ''

      try:
        type_html = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[1]/div/div[2]')
        
        # Dividir la cadena en dos partes usando '|'
        partes = type_html.text.split('|')

        # Tomar la parte después de '|'
        type_text = partes[1].strip()

        date_text = partes[0].strip()
        year_text = date_text.split('-')[0].strip()

        # tipos_trabajos = np.append(tipos_trabajos, type_text)
        # print(docente, ':', type_text)

        if type_text != 'Conference paper':
          i = i+1
          continue
        # else:
        #   print(docente, type_text, '----', year_text)

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

          if type_text == 'Book':
            values = extract_books(cita.text)
            values.insert(0, docente)
            df_books.loc[len(df_books)] = values
          elif type_text == 'Book chapter' or ("title" in cita.text and "booktitle" in cita.text) :
            # print(cita.text)
            values = extract_chaptersBooks(cita.text)
            values.insert(0, docente)
            df_chaptersBooks.loc[len(df_chaptersBooks)] = values
          elif type_text == 'Conference paper':
            values = extract_conferencePaper(cita.text)
            values.insert(0, docente)
            df_conferencePaper.loc[len(df_conferencePaper)] = values
          
          # print(cita.text)

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

