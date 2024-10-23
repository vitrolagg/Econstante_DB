#Arquivo de conexão e interação com o broker mqtt
from . import topicoMQTT, sets
import paho.mqtt.client as mqtt
from modules.database import desconecta_db
from modules.buffer import buffer
from time import sleep

client = mqtt.Client(client_id= sets[0]["brokerConfig"]["clientId"])

#Função de callback para conexão com o broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Conectado ao broker com sucesso")
        client.subscribe(topicoMQTT)

    else:
        print(f"Falha ao se conectar com o broker. Código de retorno: {rc}")

#Função de callback para recebimento de mensagem
def on_message(client , userata, msg):

    mensagem = msg.payload.decode().split(";")

    if len(mensagem) == 4:
        usuario_id = mensagem[0]
        usuario_leitura = mensagem[1]
        usuario_data = mensagem[2]
        usuario_hora = mensagem[3]

    buffer.put(
            (
                usuario_id, 
                usuario_leitura, 
                usuario_data, 
                usuario_hora
            )
        )
    
#Função de callback para desconexão com o broker
def on_disconnect(client, userdata, rc):

    print(f"Desconectado com sucesso. Código de retorno {rc}")

    if rc != 0:
        print("Desconectado inesperadamente. Reconectando...")
        client.reconnect()
    
    desconecta_db()


def conecta_mqtt():
    try:

        sleep(1)

        #Objeto cliente
        # global client

        #Autenticação de usuario e senha
        client.username_pw_set(username= sets[0]["brokerConfig"]["user"], password= sets[0]["brokerConfig"]["password"])


        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        #Conexão com o broker
        client.connect(host= sets[0]["brokerConfig"]["broker"], port= sets[0]["brokerConfig"]["port"], keepalive= sets[0]["brokerConfig"]["keepAlive"])

    except KeyboardInterrupt:
        desconecta_db()

conecta_mqtt()