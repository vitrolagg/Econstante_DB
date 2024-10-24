#Arquivo principal
from threading import Thread
from time import sleep
from modules.database import desconecta_db, keep_alive_db
from modules.mqtt import client
from modules.buffer import process_buffer
from jsons.monitor import WatchdogHandler, Watchdog
import os

try:
    
    sleep(1)

    #Salva o diretório atual deste arquivo em dydir
    dydir = os.path.dirname(os.path.abspath(__file__))

    #Concatena pasta e arquivo no caminho do diretorio para criar o caminho absoluto para dynamics.json
    caminho = os.path.join(dydir, 'jsons', 'dynamics.json')

    #Instância da classe watchdog para monitorar mudanças no arquivo json
    wdg = Watchdog(handler= WatchdogHandler(watchPath= caminho))

    #Inicia o keep em uma thread paralela
    Thread(target=keep_alive_db, daemon= True).start()

    #Inicia o processamento do buffer em uma thread paralela
    Thread(target=process_buffer, daemon= True).start()

    #inicia o monitoramento de dynamics.json
    Thread(target=wdg.start, daemon= True).start()

    #Loop do cliente MQTT
    client.loop_forever()

except KeyboardInterrupt:
    desconecta_db()