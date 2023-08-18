import time
import requests
import rarfile
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

# URL que contém um arquivo com registrop dos CAs
url_ca_zip = 'http://www3.mte.gov.br/sistemas/CAEPI_Arquivos/tgg_export_caepi.zip'
# Reccebe as informções da URL para criar arquivo
write_arquive = requests.get(url_ca_zip)
# Cria um arquivo zip comm as informções adquiridas da url
open('ca_data.zip', 'wb').write(write_arquive.content)

# Abra e analise um arquivo RAR
r = rarfile.RarFile('ca_data.zip')
# Extrai tudo dentro do arquivo
r.extractall()
# Fecha o arquivo .rar
r.close()

# Define as colunas no dataFrame
column_names = ['ca', 'data', 'validade', 'tipo']
# Le o arquivo csv e aloca nas devidas colunas do dataframe
df_ca = pd.read_csv('tgg_export_caepi.txt', encoding='Windows-1252', delimiter='|', on_bad_lines='warn', usecols=[0, 1, 2, 7], names=column_names)
# Cria um filtro para as linhas que contém apenas protetores auditivos
filtro = df_ca[df_ca['tipo'].str.contains("AUDITIVO")]
# Cria um arquivo excel a paritir do filtro
# filtro.to_excel('teste01.xlsx', index=False)
# Cria a lista de CAs para consulta
ca_list = filtro.ca.values.tolist()

# URL do site do caepi
url = 'http://caepi.mte.gov.br/internet/ConsultaCAInternet.aspx'
# Instacia do chorme driver
driver = webdriver.Chrome()
# Carrega website da base de dados e espera renderizar o site
driver.get(url=url)
# Confere se a página acessada tem o titulo correto
if driver.title != 'Ministério do Trabalho e Emprego - Certificado de Aprovação de Equipamento de Proteção Individual':
    print("Página não encontrada")

# Encontra o barra de pesquisa do númertodo CA
search_num_ca = driver.find_element(By.NAME, 'ctl00$PlaceHolderConteudo$txtNumeroCA')
time.sleep(5)

# Dicionario de informações obtidas no web scrap
info_data_scrap = {'fabricante': '',
                   'referencia': '',
                   'atenuacao': '',
                   'nrrsf': '',
                   'desvioPadrao': ''
                   }
running = 0
sql_input = []

for i in ca_list:
    listAtenuacao = []
    listDesvioPadrao = []
    running = running + 1
    print(running)
    try:
        search_num_ca = driver.find_element(By.NAME, 'ctl00$PlaceHolderConteudo$txtNumeroCA')
        # Limpa a barra de pesquisa
        search_num_ca.clear()
        # Envia a string
        search_num_ca.send_keys(i)
        # Simula o enter
        search_num_ca.send_keys(Keys.RETURN)
        time.sleep(8)

        try:
            # Encontra o botão de informações/detalhes do ca
            ca_details = driver.find_element(By.NAME, 'ctl00$PlaceHolderConteudo$grdListaResultado$ctl02$btnDetalhar')
            # Abre a aba de detalhes
            ca_details.click()

        except NoSuchElementException:
            ca_details_1 = driver.find_element(By.ID, 'PlaceHolderConteudo_grdListaResultado_btnDetalhar_0')
            no_table = list
            no_table.append(i)
            print("NO ELEMNENT ", i)

        time.sleep(8)
        # Encontra o nome do fabricante
        fabricante = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNORazaoSocial').text
        # Adciona o nome do fabricante ao dicionario de informações
        info_data_scrap['fabricante'] = fabricante

        referencia = driver.find_element(By.ID, 'PlaceHolderConteudo_lblDSReferencia').text
        # Adciona a referencia ao dicionario de informações
        info_data_scrap['referencia'] = referencia

        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao1').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao2').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao3').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao4').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao5').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao6').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao7').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao8').text
        listAtenuacao.append(atenuacao)
        atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao9').text
        listAtenuacao.append(atenuacao)
        info_data_scrap['atenuacao'] = listAtenuacao

        nrrsf = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao10').text
        info_data_scrap['nrrsf'] = nrrsf

        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao1').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao2').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao3').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao4').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao5').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao6').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao7').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao8').text
        listDesvioPadrao.append(desvioPadrao)
        desvioPadrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao9').text
        listDesvioPadrao.append(desvioPadrao)
        info_data_scrap['desvioPadrao'] = listDesvioPadrao

    except ElementClickInterceptedException:

        no_element_clickble.append(i)
        print('No clickble: ', i)

    driver.back()
    time.sleep(8)
    print(info_data_scrap)

    # Lista temporária que será abastecida
    sql_temp = []
    # Para cada valor do dicionário abastecido
    for value in info_data_scrap.values():
        # Adiciona o valor na lista temporária
        sql_temp.append(value)
    # Insere a lista temporária convertida em tupla na lista de que será enviada ao banco de dados
    sql_input.append(tuple(sql_temp))

print(sql_input)
print(no_table)
print(no_element_clickble)
