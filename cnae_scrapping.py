import json
import requests
from datetime import datetime


class CnaeScrap(object):

    def __init__(self):

        # Url da api de requisição
        self.url = 'https://servicodados.ibge.gov.br/api/v2/cnae/subclasses'
        # Dados que serão recebidos da API
        self.data_json = None
        # Dados deserializados e convertidos em objeto do python
        self.data = None
        # Cria o Dicionário com os campos necessários
        self.target_dict = {'classe_id': '',
                            'classe_descricao': '',
                            'subclass_id': '',
                            'subclass_descricao': ''
                            }
        # Cria listas para dar apend nas informções
        self.target_list = []
        # Cria lista para para converter em tuplas no banco e dar insert 
        self.sql_input = []

    def get_cnae(self):
        """
        Este método faz a coleta dos dados na api do IBGE e trata eles para inserção no banco .
        """
        self._get_last_run()
        self._get_json_data()
        # Iteração dos dados transformandos eles de lista em dicionario 
        for dictionary in self.data:
            # Para cada chave e valor no dicionario
            for key, value in dictionary.items():
                # Abastece o target_dict com as condições
                match key:
                    case 'id':
                        # adiciona o valor da chave no target dict
                        self.target_dict['subclass_id'] = value
                    case 'descricao':
                        # adiciona o valor da chave no target dict
                        self.target_dict['subclass_descricao'] = value
                    case 'ca_scrapping.py':
                        # adiciona o valor da chave no target dict
                        self.target_dict['classe_id'] = dictionary['ca_scrapping.py']['id']
                        # adiciona o valor da chave no target dict
                        self.target_dict['classe_descricao'] = dictionary['ca_scrapping.py']['descricao']
            # Lista temporária que será abastecida
            sql_temp = []
            # Para cada valor do dicionário abastecido
            for value in self.target_dict.values():
                # Adiciona o valor na lista temporária
                sql_temp.append(value)
            # Insere a lista temporária convertida em tupla na lista de que será enviada ao banco de dados
            self.sql_input.append(tuple(sql_temp))

            self.target_list.append(self.target_dict)

        return self.sql_input

    def _get_json_data(self):
        """
        Este método faz a coleta dos dados na api do IBGE
        """
        # Chama a API
        self.data_json = requests.get(url=self.url).text
        # Deserializa o json para um objeto em python
        self.data = json.loads(self.data_json)

    def _get_last_run(self):
        """
        Este método informa a data e horario da ultima execução.
        """
        # Pega o dia e hora atual
        now = datetime.now()
        # Organiza o datetime e armazena em uma variável
        self.last_run = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:", self.last_run)
