
import os 
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import time


# caminho do diretório de download da tabbela
BASE_DIR = Path(__file__).resolve().parent.parent
download_path = os.path.join(BASE_DIR, "downloads")


# Criar o diretório de download, se ele não existir
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Obtém a lista de arquivos antes do download
files_before = set(os.listdir(download_path))

# setup para baixar a planilha direto na pasta download
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("prefs", {
  "download.default_directory": download_path,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
service = Service(ChromeDriverManager().install())


# Página de download da tabela cmed
browser = webdriver.Chrome(service=service, options=options)
print('Entrando na página...')
browser.get("https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos")
sleep(.5)

# Fechar o popup que abre quando entra no site
popup_button = browser.find_element('xpath', '/html/body/header/div[1]')
popup_button.click()
sleep(.5)

# Scrollar para o fim da página e achar o botão de download
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(.2)



# botao de download + clique
print('Procurando botão de download...')
# Encontra o botão e clica em baixar
download_button = browser.find_element('xpath', '//*[@id="db63c5be-7407-4436-aa28-4c16db6b6162"]/div/div/div/div[2]/a')
download_button.click()
print('Download iniciado')
sleep(1)


# Esperar o arquivo ser baixado
file_downloaded = False
timeout = 60
start = time.time()
while not file_downloaded and time.time() - start < timeout:

   
    try:
        files_after = set(os.listdir(download_path))
        try:
            newly_downloaded_file = files_after - files_before
        except:
            print('Não foi possível extrair o novo arquivo de download')
            sleep(.5)
        if newly_downloaded_file:
            # O nome do arquivo baixado é o primeiro item da lista
            downloaded_file_name = list(newly_downloaded_file)[0]
            if 'crdownload'  in downloaded_file_name:
                raise Exception('download não finalizado')

            print('filename: ', downloaded_file_name)
            file_downloaded = True
            
              
    except:
        #print(time.time() - start)
        time.sleep(20)

# Verificar se o arquivo foi baixado
if file_downloaded:
    
    print('arquivo baixado')
else:
    print("Tempo de download expirado")


