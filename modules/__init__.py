#Arquivo de inicialização do pacote modules
import os
from json import load

current_dir = os.path.dirname(os.path.abspath(__file__))

sets_path = os.path.join(current_dir, '../jsons/sets.json')

#abre o arquivo json de configurações
with open(sets_path, 'r') as jset:
    sets = load(jset)