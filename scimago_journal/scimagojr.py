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

  cuartil_revista = []


  for revista, año in zip(revistas, años):

    if pd.isna(revista):
      cuartil_revista.append('')
      continue

    searchinput = driver.find_element(By.XPATH, '//*[@id="searchinput"]')
    searchinput.clear()

    searchinput.send_keys(revista)
    searchinput.send_keys(Keys.RETURN)

    similarities = []
    journalName = ''
    i=1
    while True:
      try:
        journalName = driver.find_element(By.XPATH, f'/html/body/div[4]/div[2]/a[{i}]/span')
      except Exception as e:
        break
      
      similarities.append(levenshtein_similarity(journalName.text.lower(), revista.lower()))
      i = i+1

    journalName_text = ''
    
    if similarities:
      similarity = max(similarities)
      journal_index = similarities.index(similarity) + 1
      journalName = driver.find_element(By.XPATH, f'/html/body/div[4]/div[2]/a[{journal_index}]/span')
      journalName_text = journalName.text
    else:
      similarity = 0

    if similarity >= 80.0 or caso_especifico(journalName_text, revista):
      if año != 0:
        journalName.click()
        for i in range(1, 16):
          try:
            html_title_quartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[1]/div[1]').text
          except Exception as e:
            if i == 15:
              cuartil_revista.append('')
              reporte.agregar_revista_sin_cuartiles(revista)
            continue

          if html_title_quartil == 'Quartiles':
            mostrar_cuartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[1]/div[2]/div[2]/img')
            driver.execute_script("arguments[0].scrollIntoView(true);", mostrar_cuartil)
            mostrar_cuartil.click()
            reporte.agregar_revista_con_cuartiles(revista)
            
            j = 1
            while True:
              try:
                cuartil_año = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[2]/div[2]/table/tbody/tr[{j}]/td[2]').text
                if cuartil_año == str(año):
                  cuartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[2]/div[2]/table/tbody/tr[{j}]/td[3]').text
                  cuartil_revista.append(cuartil)
                  break
              except Exception as e:
                if int(cuartil_año)+1 == año:
                  cuartil = driver.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[2]/div[2]/table/tbody/tr[{j-1}]/td[3]').text
                  cuartil_revista.append(cuartil)
                else:
                  reporte.agregar_año_sin_cuartil(revista)
                  cuartil_revista.append('')
                break
              j = j+1

            break

        driver.back()
      else:
        cuartil_revista.append('')
        print('El trabajo no tiene año de publicación')
    else:
      cuartil_revista.append('')
      reporte.agregar_revista_no_encontradas(revista)
    
    driver.back()
  
  df['cuartil_revista'] = cuartil_revista


def levenshtein_similarity(text1, text2):
  distance = Levenshtein.distance(text1, text2)
  max_len = max(len(text1), len(text2))
  return (1 - distance / max_len) * 100


def caso_especifico(text_scimago, revista):
  if text_scimago == 'Revista Facultad de Ingenieria' and revista.upper() == 'REVISTA FACULTAD DE INGENIERA UNIVERSIDAD DE ANTIOQUIA':
    return True
  if text_scimago == 'Revista Facultad de Ingenieria' and revista.upper() == 'REVISTA FACULTAD DE INGENIERIA UNIVERSIDAD DE ANTIOQUIA':
    return True
  elif text_scimago == 'Applied Soft Computing Journal' and revista == 'Applied Soft Computing':
    return True
  else:
    return False
