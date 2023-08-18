from cnae_scrapping import CnaeScrap
from ca_scrapping import CaScrap
from br_cities import CitiesScrap


class ScrapAll(object):

    def __init__(self):

        self.cnaes = CnaeScrap()
        self.cas = CaScrap()
        self.cities = CitiesScrap()
    
    def execute_all_scrap(self):
        
        print(self.cnaes.get_cnae() )
        print(self.cities.get_cities())
        self.cas.make_consult()
