import re
from time import sleep
from selenium import webdriver
from CvLAC.Extract_info import *
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
        values = extract_project(proyecto.text)
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
        values = extract_articles(articulo.text)
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
        values = extract_booksChapter(chapter.text)
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