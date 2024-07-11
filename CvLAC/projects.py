import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def CvLAC_projects(dataframe, docente):
  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre la página web
  driver.get('https://scienti.minciencias.gov.co/ciencia-war/jsp/enRecurso/IndexRecursoHumano.jsp')

  # Encuentra el elemento usando XPath
  elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/form/table/tbody/tr[6]/td[2]/input')

  # Puedes interactuar con el elemento encontrado, por ejemplo, enviando texto
  elem.send_keys(docente)
  elem.send_keys(Keys.RETURN)

  sleep(2)

  # Se obtiene el elemento en la primera posición de la tabla. 
  # se supone que es la correspondiente al docente
  elem = driver.find_element(By.XPATH, '//*[@id="investigadores_row1"]/td[2]/a')
  elem.click()

  sleep(2)

  # Cambia el foco a la nueva pestaña
  driver.switch_to.window(driver.window_handles[1])

  i = 2

  # Obtiene todos los proyectos
  while True:
    try:
      xpath = f'/html/body/div/div[3]/table/tbody/tr[86]/td/table/tbody/tr[{i}]/td/blockquote'
      proyecto = driver.find_element(By.XPATH, xpath)
      values = getValues(proyecto.text)
      values.insert(0, docente)
      dataframe.loc[len(dataframe)] = values
      i = i+1
    except Exception  as e:
      break

  # for i in proyectos[0].text:
  #   print(i)
  
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

  # # Imprimir los resultados
  # print(f"Tipo de proyecto: {tipo_proyecto}")
  # print(f"Nombre del proyecto: {nombre_proyecto}")
  # print(f"Inicio: {inicio}")
  # print(f"Fin: {fin}")
  # # print(f"Duración: {duracion}")
  # print(f"Resumen: {resumen}")
  # print('---------------------------------------------------------')