#Arquivo de conexão e interação com o banco de dados
from . import sets
import jsons
import pymysql
from time import sleep

#Dados do host de banco de dados
config_db = sets[0]["databaseConfig"]

#Função de conexão com o banco de dados
def conecta_db():
    global conn 
    global cursor 
    
    try:

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

    sql = f'INSERT INTO {jsons.tabela} (id , leitura, da_ta, hora) VALUES (%s, %s, %s, %s)'

    print(jsons.tabela)

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

conecta_db()