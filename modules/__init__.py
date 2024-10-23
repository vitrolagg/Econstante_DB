import os
from json import load

current_dir = os.path.dirname(os.path.abspath(__file__))

sets_path = os.path.join(current_dir, '../jsons/sets.json')

#abre o arquivo json de configurações
with open(sets_path, 'r') as jset:
    sets = load(jset)

dynamics_path = os.path.join(current_dir, '../jsons/dynamics.json')
#Faz o primeiro carregamento do json dinâmico
with open(dynamics_path, 'r') as jdy:
    dynamics = load(jdy)

#Faz o primeiro recarregamento dos valores dinâmicos de tabela (DB) e topico(MQTT)
tabela = dynamics[0]["tabela"]
topicoMQTT = dynamics[0]["topic"]