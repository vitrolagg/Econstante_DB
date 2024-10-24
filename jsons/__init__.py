#arquivo de inicialização do pacote jsons
from json import load
import os

#Salva o diretório atual deste arquivo em dydir
current_dir = os.path.dirname(os.path.abspath(__file__))

#Concatena pasta e arquivo no caminho do diretorio para criar o caminho absoluto para dynamics.json
dynamics_path = os.path.join(current_dir, '../jsons/dynamics.json')

#Função para recarrear o json após modificação
def recarregaJson():

    global tabela, topicoMQTT

    with open(dynamics_path, 'r') as file:
        dynamics = load(file)
        tabela = dynamics[0]["tabela"]
        topicoMQTT = dynamics[0]["topic"]

#Faz o primeiro carregamento 
recarregaJson()