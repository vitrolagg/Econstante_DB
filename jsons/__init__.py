from ..modules import dynamics, tabela, topicoMQTT
from jsons import load

def recarregaJson():
    with open('../jsons/dynamics.json', 'r') as file:
        dynamics = load(file)
        tabela = dynamics[0]["tabela"]
        topicoMQTT = dynamics[0]["topic"]