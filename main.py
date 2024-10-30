import sqlite3
import subprocess
import time

# Parâmetros do monitoramento
intervalo_verificacao = 60  # segundos entre verificações
limite_conexoes = 500       # limite de conexões estabelecidas

# Função para obter a contagem de conexões estabelecidas na porta 5001
def contar_conexoes():
    comando = "netstat -an | grep :5001 | grep ESTABLISHED | wc -l"
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    return int(resultado.stdout.strip())

# Função para registrar a quantidade de conexões no banco de dados
def registrar_alerta(conexoes):
    conn = sqlite3.connect('database/statistics.db')
    cursor = conn.cursor()

    # Criando a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections_statics (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_count INTEGER,
            timestamp        DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Inserindo um registro no banco de dados
    cursor.execute('''
        INSERT INTO connections_statics (connection_count) VALUES (?)
    ''', (conexoes,))

    conn.commit()
    conn.close()

# Loop para monitorar as conexões
if __name__ == "__main__":
    while True:
        conexoes = contar_conexoes()
        print(f"Conexões estabelecidas: {conexoes}")
        
        if conexoes > limite_conexoes:
            print(f"Alerta: Número de conexões ultrapassou o limite de {limite_conexoes}!")
            registrar_alerta(conexoes)
        
        time.sleep(intervalo_verificacao)
