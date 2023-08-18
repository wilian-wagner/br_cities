import json
import requests
from datetime import datetime


class CitiesScrap(object):

    def __init__(self):

        # Url da api de requisição
        self.url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/11|12|13|14|15|16|17|21|22|23|24|25|26|27|28|29|31|32|33|35|41|42|43|50|51|52|53/municipios'
        # Dados que serão recebidos da API
        self.data_json = None
        # Dados deserializados e convertidos em objeto do python
        self.data = None
        # Cria o Dicionário com os campos necessários
        self.target_dict = {'mun_id': '',
                            'mun_nome': '',
                            'uf_id': '',
                            'uf_nome': '',
                            'uf_sigla': ''}
        # Cria listas para dar apend nas informções
        self.target_list = []
        # Cria lista para para converter em tuplas no banco e dar insert
        self.sql_input = []
        # List temporária sql
        self.sql_temp = []

    def get_cities(self):
        """
        Este método faz a coleta dos dados na api do IBGE e trata eles para inserção no banco .
        """
        self._get_last_run()
        self._get_json_data()
        # Para cada dicionário no output da API
        for dictionary in self.data:
            # Para cada conjunto chave / valor nos itens do dicionário
            for key, value in dictionary.items():
                # Abastece o target_dict com as condições
                match key:
                    case 'id':
                        self.target_dict['mun_id'] = value
                    case 'nome':
                        self.target_dict['mun_nome'] = value
                    case 'microrregiao':
                        self.target_dict['uf_id'] = dictionary[key]['mesorregiao']['UF']['id']
                        self.target_dict['uf_nome'] = dictionary[key]['mesorregiao']['UF']['nome']
                        self.target_dict['uf_sigla'] = dictionary[key]['mesorregiao']['UF']['sigla']

            # Para cada valor do dicionário abastecido
            for value in self.target_dict.values():
                # Adiciona o valor na lista temporária
                self.sql_temp.append(value)
            # Insere a lista temporária convertida em tupla na lista de que será enviada ao banco de dados
            self.sql_input.append(tuple(self.sql_temp))

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
