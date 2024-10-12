import paho.mqtt.client as mqtt
import pymysql
from queue import Queue
import threading
import time

#Buffer da fila de recebimento de mensagens
buffer = Queue()

#Dados do host de banco de dados
config_db = {
    'host':'45.148.96.11',
    'user':'econs1214660_pythonGrava',
    'password':'@Vitrola2410',
    'database':'econs1214660_main_db'
}

#Função de conexão com o banco de dados
def conecta_db():
    
    try:
        global conn 
        global cursor 

        conn = pymysql.connect(**config_db)
        cursor = conn.cursor()

        print("Conectado com sucesso ao db")

        print(conn.open)

    except pymysql.MySQLError as e:
        print(f"Erro: {e}")

#Função de desconexão com o banco de dados
def desconecta_db():

    if conn:
        cursor.close()
        conn.close()
        print("Conexão encerrada db")



#Função de callback para conexão com o broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Conectado ao broker com sucesso")
        client.subscribe("leituras")

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

#Função de gravação no banco de dados
def gravaBanco(pacote):
    
    sql = 'INSERT INTO leituras_10_2024 (id , leitura, da_ta, hora) VALUES (%s, %s, %s, %s)'

    for dados in pacote:

        cursor.execute(sql, dados)
    
    conn.commit()

#Função de processamento do buffer
def process_buffer():

    while True:

        msgs = []

        while not buffer.empty():
            msgs.append(buffer.get())

        if msgs:
            try:
                gravaBanco(msgs)

            except pymysql.MySQLError  as e:
                print(f"Erro de conexão {e}")

                desconecta_db()
                time.sleep(5)
                conecta_db()

        time.sleep(1)

#Keep alive para manter a conexão
def keep_alive_db():

    while True:
        try:
            cursor.execute("SELECT 1")  # Executa uma consulta leve
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Erro ao manter a conexão: {e}")
            desconecta_db()
            time.sleep(5)
            conecta_db()
            # break
        time.sleep(60)

try:

    time.sleep(10)
    
    #Conecta ao banco de dados
    conecta_db()

    #Objeto cliente
    client = mqtt.Client(client_id= "Gravador")

    #Autenticação de usuario e senha
    client.username_pw_set("gravador", "gravadorsenha2410")


    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    #Conexão com o broker
    client.connect("177.223.45.160", 1883, 60)

    #Inicia o keep em uma thread paralela
    threading.Thread(target=keep_alive_db, daemon= True).start()

    #Inicia o processamento do buffer em uma thread paralela
    threading.Thread(target=process_buffer, daemon= True).start()

    #Ínicio da conexão em uma thred separada
    client.loop_forever()

except KeyboardInterrupt:
    desconecta_db()