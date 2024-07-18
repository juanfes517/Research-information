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

  input.send_keys("SALAZAR SANCHEZ MARIA BERNARDA")
  input.send_keys(Keys.RETURN)

  sleep(2)

  elem = driver.find_element(By.XPATH, '//*[@id="main"]/app-results/div/table/tbody/tr[1]/td[1]/a')
  elem.click()

  sleep(2)

  i = 1
  # Obtiene todos los proyectos
  while True:
    try:
      type = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[1]/div/div[2]')

      # TODO: Hacer algo diferente segun el tipo

      show_details = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data/div/div[2]/div/a')
      driver.execute_script("arguments[0].scrollIntoView(true);", show_details)
      driver.execute_script("arguments[0].click();", show_details)
      hide_details = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[1]/div/div[2]/div/a')
      # details.click()

      sleep(1)

      show_citation = driver.find_element(By.XPATH, f'//*[@id="cy-citation-toggle-link"]')
      driver.execute_script("arguments[0].click();", show_citation)

      expanded_formatting = driver.find_element(By.XPATH, f'//*[@id="cy-expanded-citation-toggle-link"]')
      driver.execute_script("arguments[0].click();", expanded_formatting)

      sleep(1)

      cita = driver.find_element(By.XPATH, f'//*[@id="cy-works-panels"]/div[2]/app-work-stack[{i}]/app-panel/div[2]/app-work/app-panel-data[2]/div/div[1]/app-display-attribute[3]/div/div[2]/div/pre')
      print(cita.text)
      print('---------------------------------------')

      driver.execute_script("arguments[0].click();", hide_details)
      # sleep(4)

      i = i+1
    except Exception  as e:
      print(e)
      break

  driver.quit()
