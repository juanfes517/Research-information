from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa el driver de Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Abre la página web
driver.get('https://scienti.minciencias.gov.co/ciencia-war/jsp/enRecurso/IndexRecursoHumano.jsp')

# Encuentra el elemento usando XPath
elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/form/table/tbody/tr[6]/td[2]/input')

# Puedes interactuar con el elemento encontrado, por ejemplo, enviando texto
elem.send_keys('diego jose luis botia valderrama')
elem.send_keys(Keys.RETURN)

sleep(2)

# Se obtiene el elemento en la primera posición de la tabla. 
# se supone que es la correspondiente al docente
elem = driver.find_element(By.XPATH, '//*[@id="investigadores_row1"]/td[2]/a')
elem.click()

sleep(2)

# Cambia el foco a la nueva pestaña
driver.switch_to.window(driver.window_handles[1])

proyectos = []
i = 2

# Obtiene todos los proyectos
while True:
  try:
    xpath = f'/html/body/div/div[3]/table/tbody/tr[86]/td/table/tbody/tr[{i}]/td/blockquote'
    proyecto = driver.find_element(By.XPATH, xpath)
    proyectos.append(proyecto)
    i = i+1
  except Exception  as e:
    break


for proyecto in proyectos:
  print(proyecto.text)