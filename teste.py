import schedule
from json import load, dump
from time import sleep

def trocaTabela1():

    global arquivo1

    with open('jsons/dynamics.json', 'r') as file:
        arquivo1 = load(file)
    
    arquivo1[0]["tabela"] = "teste"

    with open('jsons/dynamics.json', 'w') as f:
        dump(arquivo1, f)

def trocatabela2():
    global arquivo2

    with open('jsons/dynamics.json', 'r') as file:
        arquivo2 = load(file)

    arquivo2[0]["tabela"] = "leituras_10_2024"
    with open('jsons/dynamics.json', 'w') as f:     
        dump(arquivo2, f)

schedule.every().hour.at(":36").do(trocaTabela1)
schedule.every().hour.at(":41").do(trocatabela2)

while True:
    schedule.run_pending()
    sleep(1)