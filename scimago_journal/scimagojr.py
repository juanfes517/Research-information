import Levenshtein
from time import sleep
from selenium import webdriver
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

  buscar_h_index(
    df=df_articulos_de_conferencia,
    driver=driver)
  
  buscar_h_index(
    df=df_articulos,
    driver=driver)

  driver.quit()

def buscar_h_index(df, driver):
  revistas = df['revista'].tolist()
  h_index_revista = []

  for revista in revistas:
    
    searchinput = driver.find_element(By.XPATH, '//*[@id="searchinput"]')
    searchinput.clear()

    searchinput.send_keys(revista)
    searchinput.send_keys(Keys.RETURN)

    try:
      i=1
      while True:

        # xpath = ''
        # if i == 0:
        #   xpath = f'/html/body/div[4]/div[2]/a/span'
        # else:
        xpath = f'/html/body/div[4]/div[2]/a[{i}]/span'

        journalName = driver.find_element(By.XPATH, xpath)

        similarity = levenshtein_similarity(journalName.text.lower(), revista.lower())

        print(similarity, journalName.text)
        # if journalName_lower == revista.lower() or caso_especifico(journalName_lower, revista):
        # print(similarity)
        if similarity >= 80.0 or caso_especifico(journalName.text, revista):
          journalName.click()
          try:
            h_index = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[4]/p').text
            h_index_revista.append(h_index)
            print('\n')
          except Exception as e:
            print('La revista no tiene h-index   ', revista)
          driver.back()
          break

        i = i+1

    except Exception as e:
      print('No se encontró la revista: ', revista, '\n')
      h_index_revista.append('')
    
    driver.back()

  print(h_index_revista)
  df['h_index_revista'] = h_index_revista


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
