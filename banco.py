import sqlite3

def conectar():
    return sqlite3.connect("banc.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        saldo REAL,
        usuario_id INTEGER           
    )
""")
    
    conn.commit()
    conn.close()


def criar_conta(nome, usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contas (nome, saldo, usuario_id) VALUES (?, ?, ?)",
        (nome, 0, usuario_id)
    )

    conn.commit()
    conn.close()


def listar_contas(usuario_id):
    conn = conectar()
    cursor = conn.cursor()    

    cursor.execute("SELECT * FROM contas WHERE usuario_id = ?", (usuario_id,))
    contas = cursor.fetchall()

    conn.close()
    return contas

def depositar(id, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, id))
    
    conn.commit()
    conn.close()

def sacar(id, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT saldo FROM contas WHERE id = ?", (id,))
    resultado = cursor.fetchone()

    if resultado:
        saldo = resultado[0]

        if saldo >= valor:
            cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, id))
        else:
            print("Saldo insuficiente!")
    else:
        print("Conta não encontrada!")

    conn.commit()
    conn.close()
        
def total_saldo():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(saldo) FROM contas")
    total = cursor.fetchone()[0]

    conn.close()
    return total if total else 0


def total_contas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contas")
    total = cursor.fetchone()[0]

    conn.close()
    return total

def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        senha TEXT
    )
    """)

    conn.commit()
    conn.close()

def criar_usuario(nome, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))

    conn.commit()
    conn.close()


def login_usuario(nome, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    user = cursor.fetchone()

    conn.close()
    return user