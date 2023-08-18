import time
from all_scrap import ScrapAll
from datetime import datetime

# Instancia a classe dos Scraps
scrap = ScrapAll()
print( "RUNING")
while True:
    # Retorna a o date time
    hora_atual = datetime.now()
    # Quando for 3 horas da manhã
    if hora_atual.hour == 3:
        # Executa todos os Scraps
        scrap.execute_all_scrap()
    # Espera 30 minutos
    time.sleep(1800)
