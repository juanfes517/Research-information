import Levenshtein
import pandas as pd
from time import sleep
from selenium import webdriver
from scimago_journal.Report import Report
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_scimagojr(df_articulos_de_conferencia, df_articulos):
  # Inicializa el driver de Chrome
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)

  # Abre el navegador con la URL
  driver.get('https://www.scimagojr.com/')

  reporte = Report()

  buscar_cuartil(
    df=df_articulos_de_conferencia,
    driver=driver,
    reporte=reporte)
  
  buscar_cuartil(
    df=df_articulos,
    driver=driver,
    reporte=reporte)

  reporte.mostrar_resultados()
  driver.quit()

def buscar_cuartil(df, driver, reporte):
  revistas = df['revista'].to_list()
  años = df['año'].to_list()

  # años = [1,2,3,4,5]

  # revistas = [
  #   "ifmbe proceedings",
  #   "2015 20th symposium on signal processing images and computer vision stsiva 2015 conference proceedings",
  #   "Journal of Physics: Conference Series",
  #   "telematics and informatics",
  #   "the journal of the acoustical society of america"
  # ]

  h_index_revista = []

  for revista, año in zip(revistas, años):

    if pd.isna(revista):
      continue

    searchinput = driver.find_element(By.XPATH, '//*[@id="searchinput"]')
    searchinput.clear()

    searchinput.send_keys(revista)
    searchinput.send_keys(Keys.RETURN)

    i=1
    while True:
      journalName = ''
      try:
        journalName = driver.find_element(By.XPATH, f'/html/body/div[4]/div[2]/a[{i}]/span')
      except Exception as e:
        reporte.agregar_revista_no_encontradas(revista)
        i = i+1
        break
      
      similarity = levenshtein_similarity(journalName.text.lower(), revista.lower())

      if similarity >= 80.0 or caso_especifico(journalName.text, revista):
        if año != 0:
          journalName.click()
          for i in range(1, 15):
            try:
              html_title_quartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[1]/div[1]').text
            except Exception as e:
              if i == 14:
                reporte.agregar_revista_sin_cuartiles(revista)
              continue

            if html_title_quartil == 'Quartiles':
              mostrar_cuartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[1]/div[2]/div[2]/img')
              driver.execute_script("arguments[0].scrollIntoView(true);", mostrar_cuartil)
              mostrar_cuartil.click()
              reporte.agregar_revista_con_cuartiles(revista)
              
              sleep(4)
              break
              
          driver.back()
        else:
          print('El trabajo no tiene año de publicación')
        break

      i = i+1
    
    driver.back()


def levenshtein_similarity(text1, text2):
  distance = Levenshtein.distance(text1, text2)
  max_len = max(len(text1), len(text2))
  return (1 - distance / max_len) * 100


def caso_especifico(text_scimago, revista):
  if text_scimago == 'Revista Facultad de Ingenieria' and revista == 'Revista Facultad de Ingeniería Universidad de Antioquia' or text_scimago == 'Revista Facultad de Ingenieria' and revista == 'REVISTA FACULTAD DE INGENIERIA UNIVERSIDAD DE ANTIOQUIA':
    return True
  elif text_scimago == 'Applied Soft Computing Journal' and revista == 'Applied Soft Computing':
    return True
  else:
    return False
