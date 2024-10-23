#Arquivo principal
from threading import Thread
from time import sleep
from modules.database import desconecta_db, conecta_db, keep_alive_db
from modules.mqtt import conecta_mqtt, client
from modules.buffer import process_buffer
# from jsons.monitor import obs_init

try:
    
    sleep(1)

    #Inicia o keep em uma thread paralela
    Thread(target=keep_alive_db, daemon= True).start()

    #Inicia o processamento do buffer em uma thread paralela
    Thread(target=process_buffer, daemon= True).start()

    # Thread(target=obs_init, args= carregaJson, daemon= True).start()

    #Loop do cliente MQTT
    client.loop_forever()

except KeyboardInterrupt:
    desconecta_db()