#Arquivo de conexão e interação com o banco de dados
import pymysql
from json import load
from time import sleep

#abre o arquivo json de configurações
with open('sets.json') as jset:
    sets = load(jset)

#Abre o arquivo json de sets dinâmicos
with open('dynamics.json') as jdy:
    jdy = load(jdy)

tabela = str(jdy[0]["tabela"])

#Dados do host de banco de dados
config_db = sets[0]["databaseConfig"]

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

#Função de gravação no banco de dados
def gravaBanco(pacote):

    sql = f'INSERT INTO {tabela} (id , leitura, da_ta, hora) VALUES (%s, %s, %s, %s)'

    for dados in pacote:

        cursor.execute(sql, dados)
    
    conn.commit()

#Keep alive para manter a conexão
def keep_alive_db():

    while True:
        try:
            cursor.execute("SELECT 1")  # Executa uma consulta leve
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Erro ao manter a conexão: {e}")
            desconecta_db()
            sleep(5)
            conecta_db()
        sleep(60)
