#Arquivo principal
from threading import Thread
from time import sleep
from database import desconecta_db, conecta_db, keep_alive_db
from mqtt import conecta_mqtt, client
from buffer import process_buffer

try:
    
    sleep(1)

    conecta_db()
    conecta_mqtt()

    #Inicia o keep em uma thread paralela
    Thread(target=keep_alive_db, daemon= True).start()

    #Inicia o processamento do buffer em uma thread paralela
    Thread(target=process_buffer, daemon= True).start()

    #Ínicio da conexão em uma thred separada
    client.loop_forever()

except KeyboardInterrupt:
    desconecta_db()