from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def scrape_ORCID():
  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre el navegador con la URL
  driver.get('https://orcid.org/')

  input = driver.find_element(By.XPATH, '//*[@id="cy-search"]')
  input.clear()

  cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
  cookies.click()

  input.send_keys("BOTIA VALDERRAMA DIEGO JOSE LUIS")
  input.send_keys(Keys.RETURN)

  sleep(2)

  #TODO: Verificar que se hayan encontrado resultados para el docente
  elem = driver.find_element(By.XPATH, '//*[@id="main"]/app-results/div/table/tbody/tr[1]/td[1]/a')
  elem.click()

  sleep(2)

  i = 1
  while True:
    try:
      type = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[1]/div/div[2]')
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
      print(f"El trabajo {i} no tiene cita")
      i = i+1
      continue

    try:
      # Presiona "Switch to expanded formatting"
      expanded_formatting = driver.find_element(By.XPATH, f'//*[@id="cy-expanded-citation-toggle-link"]')
      driver.execute_script("arguments[0].click();", expanded_formatting)
    except Exception as e:
      driver.execute_script("arguments[0].click();", hide_details)
      print("No se encontro una cita valida para el trabajo:", i)
      i = i+1
      continue

    sleep(1)

    # Para obtener el posible xpath de la cita
    for j in range(1, 6):
      try: 
        xpath = f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[{j}]/div/div[2]/div/pre'
        cita = driver.find_element(By.XPATH, xpath)
        print(cita.text)
        break
      except Exception as e:
        if j == 5:
          print("Error al conseguir la cita en el trabajo:", i)
        continue

    driver.execute_script("arguments[0].click();", hide_details)

    i = i+1


  driver.quit()
