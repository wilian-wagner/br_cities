import requests
import rarfile
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time
from datetime import datetime


class CaScrap(object):

    def __init__(self):

        # Cria a lista de CAs para consulta
        self.ca_list = None
        # URL que contém um arquivo com registrop dos CAs
        self.url_ca_zip = 'http://www3.mte.gov.br/sistemas/CAEPI_Arquivos/tgg_export_caepi.zip'
        # Define as colunas no dataFrame que irá ser criado a partir da base de dados
        self.column_names = ['ca', 'data', 'validade', 'tipo']
        # URL do site do caepi
        self.url_consulta = 'http://caepi.mte.gov.br/internet/ConsultaCAInternet.aspx'
        # Dicionario de informações obtidas no web scrap
        self.info_data_scrap = {'fabricante': '',
                                'referencia': '',
                                'atenuacao': list(),
                                'nrrsf': '',
                                'desvio_padrao': list()
                                }
        # Contador de loop
        self.running = 0
        # Lista para inserção no banco de dados
        self.sql_input = list()
        # Lista de valores de atenuação
        self.listAtenuacao = list()
        # Lista de valores de desvio padrao
        self.listdesvio_padrao = list()
        # Lista de Cas que não conseguirem obter a tabela de atenuação
        self.no_table = list()
        # Ultiam vez que o programa rodou
        self.last_run = None
        # lista para armazenar os erros
        self.no_element_clickble = list()
        # List temporária sql
        self.sql_temp = []

    def _download_data(self):
        """
        Este método faz a coleta dos dados em forma de zip e descompacta o arquivo .
        """
        # Reccebe as informções da URL para criar arquivo
        write_arquive = requests.get(self.url_ca_zip)
        # Cria um arquivo zip comm as informções adquiridas da url
        open('ca_data.zip', 'wb').write(write_arquive.content)
        # Abra e analise um arquivo RAR
        r = rarfile.RarFile('ca_data.zip')
        # Extrai tudo dentro do arquivo
        r.extractall()
        # Fecha o arquivo .rar
        r.close()

    def _filter_data(self):
        """
        Este método faz o filtro dos dados do arquivo extraído .
        """
        # Le o arquivo csv e aloca nas devidas colunas do dataframe
        df_ca = pd.read_csv('tgg_export_caepi.txt', encoding='Windows-1252', delimiter='|', on_bad_lines='warn',
                            usecols=[0, 1, 2, 7], names=self.column_names)
        # Cria um filtro para as linhas que contém apenas protetores auditivos
        filtro = df_ca[df_ca['tipo'].str.contains("AUDITIVO")]

        # Coloca a lista de filtro numa lista
        self.ca_list = filtro.ca.values.tolist()

    def make_consult(self):
        """
        Este método faz o webscraping usando o filtro como lista .
        """
        self._get_last_run()
        self._download_data()
        self._filter_data()
        # Instacia o chrome driver
        driver = webdriver.Chrome()
        # Carrega website da base de dados e espera renderizar o site
        driver.get(url=self.url_consulta)
        # Confere se a página acessada tem o titulo certo
        if driver.title != 'Ministério do Trabalho e Emprego - Certificado de Aprovação de Equipamento de Proteção Individual':
            print("Página não encontrada")

        for i in self.ca_list:

            # quantidade de vezes que foram feitas consultas
            self.running = self.running + 1
            print(self.running)

            time.sleep(5)

            try:
                # Encontra o barra de pesquisa do númertodo CA
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
                    # Encontra o botão de informações/detalhes do ca
                    ca_details_1 = driver.find_element(By.ID, 'PlaceHolderConteudo_grdListaResultado_btnDetalhar_0')
                    # Abre a aba de detalhes
                    ca_details_1.click()
                    no_table = list()
                    no_table.append(i)
                    print("NO ELEMNENT ", i)

                time.sleep(8)
                # Encontra o nome do fabricante
                fabricante = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNORazaoSocial').text
                # Adciona o nome do fabricante ao dicionario de informações
                self.info_data_scrap['fabricante'] = fabricante

                referencia = driver.find_element(By.ID, 'PlaceHolderConteudo_lblDSReferencia').text
                # Adciona a referencia ao dicionario de informações
                self.info_data_scrap['referencia'] = referencia

                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao1').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao2').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao3').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao4').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao5').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao6').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao7').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao8').text
                self.listAtenuacao.append(atenuacao)
                atenuacao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao9').text
                self.listAtenuacao.append(atenuacao)
                self.info_data_scrap['atenuacao'] = self.listAtenuacao

                nrrsf = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRAtenuacao10').text
                self.info_data_scrap['nrrsf'] = nrrsf

                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao1').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao2').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao3').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao4').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao5').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao6').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao7').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao8').text
                self.listdesvio_padrao.append(desvio_padrao)
                desvio_padrao = driver.find_element(By.ID, 'PlaceHolderConteudo_lblNRDesvioPadrao9').text
                self.listdesvio_padrao.append(desvio_padrao)
                self.info_data_scrap['desvio_padrao'] = self.listdesvio_padrao

            # Exceção Para quando não encontrar objeto clicável
            except ElementClickInterceptedException:

                # Adciona numero do ca que falho a lista
                self.no_element_clickble.append(i)
                print('No clickble: ', i)

            # Retorna a página
            driver.back()
            # Espera carregar
            time.sleep(8)

            # Para cada valor do dicionário abastecido
        for value in self.info_data_scrap.values():

            # Adiciona o valor na lista temporária
            self.sql_temp.append(value)

            # Insere a lista temporária convertida em tupla na lista de que será enviada ao banco de dados
            self.sql_input.append(tuple(self.sql_temp))

            print(self.sql_input)
            print(self.no_table)
            print(self.no_element_clickble)

            # Retorna tubplas para inserção em banco
            return self.sql_input

    def _get_last_run(self):
        """
        Este método informa a data e horario da ultima execução.
        """
        # Pega o dia e hora atual
        now = datetime.now()
        # Organiza o datetime e armazena em uma variável
        self.last_run = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:", self.last_run)
