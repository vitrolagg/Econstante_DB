#Aqruivo de processamento do buffer
from queue import Queue
from database import gravaBanco, desconecta_db, conecta_db
from time import sleep
from pymysql import MySQLError

#Buffer da fila de recebimento de mensagens
global buffer
buffer = Queue()

#Função de processamento do buffer
def process_buffer():

    while True:

        msgs = []

        while not buffer.empty():
            msgs.append(buffer.get())

        if msgs:
            try:
                gravaBanco(msgs)

            except MySQLError  as e:
                print(f"Erro de conexão {e}")

                desconecta_db()
                sleep(5)
                conecta_db()

        sleep(1)
