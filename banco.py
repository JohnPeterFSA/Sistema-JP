# Este é o arquivo que lida com a conexão e a criação do banco de dados SQLite.
# É uma parte fundamental do sistema, garantindo que as tabelas necessárias existam.
import sqlite3
import os

DB = "jpgeo.db"

def conectar():
    """
    Função para conectar ao banco de dados SQLite.
    Cria o arquivo se ele não existir.
    """
    conn = sqlite3.connect(DB)
    return conn

def criar_tabelas():
    """
    Função para criar as tabelas 'usuarios', 'marcos' e 'servicos'
    se elas ainda não existirem no banco de dados.
    """
    conn = conectar()
    c = conn.cursor()
    
    # Tabela de Usuários para gerenciar logins e dados pessoais
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        nome TEXT,
        estado_civil TEXT,
        profissao TEXT,
        documento TEXT,
        email TEXT,
        endereco TEXT,
        cep TEXT,
        senha TEXT
    )''')
    
    # Tabela de Marcos para controle de marcos de fazendas
    c.execute('''CREATE TABLE IF NOT EXISTS marcos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        fazenda TEXT,
        municipio TEXT,
        proprietario TEXT,
        numero_inicial INTEGER,
        numero_final INTEGER
    )''')
    
    # Tabela de Serviços para registrar os serviços prestados
    c.execute('''CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fazenda TEXT,
        cliente TEXT,
        servico TEXT,
        valor TEXT,
        pagamento TEXT,
        data TEXT
    )''')
    
    conn.commit()
    conn.close()

# Verifica se o arquivo do banco de dados já existe.
# Se não existir, ele chama a função para criar as tabelas.
if not os.path.exists(DB):
    criar_tabelas()