import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from docentes import docentes

def scrape_CvLAC(df_projects, df_articles, df_chaptersBooks, docentes):

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
        values = getValues(proyecto.text)
        values.insert(0, docente)
        df_projects.loc[len(df_projects)] = values
        i = i+1
      except Exception  as e:
        break
    
    #Se cierra la ventana actual, se cambia el foco a la pestaña original y se regresa a la pagina anterior
    driver.close()
    driver.switch_to.window(original_window)
    driver.back()
  
  driver.quit()

def getValues(text):
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
  # duracion = duracion.group(1).strip() if duracion else ""
  resumen = resumen.group(1).strip() if resumen else ""

  values = [tipo_proyecto, nombre_proyecto, inicio, fin, resumen]

  return values