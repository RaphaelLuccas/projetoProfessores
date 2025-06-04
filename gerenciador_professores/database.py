import sqlite3
from datetime import datetime

def conectar_banco():
    return sqlite3.connect("professores.db")

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS professores
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    disciplina TEXT NOT NULL,
                    cpf TEXT NOT NULL,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP)
                   ''')
    conn.commit()
    conn.close()

def criar_tabela_usuarios():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS usuarios
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL)
                       ''')

        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ('admin', 'admin'))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar tabela de usuários: {e}")

def verificar_login(usuario, senha):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()[0] > 0
        conn.close()
        return resultado
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return False

def adicionar_professor_db(nome, disciplina, cpf):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO professores (nome, disciplina, cpf) VALUES (?, ?, ?)",
                      (nome, disciplina, cpf))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        raise Exception(f"Erro de integridade: {e}")
    except Exception as e:
        raise Exception(f"Erro ao adicionar professor: {e}")

def remover_professor_db(professor_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professores WHERE id = ?", (professor_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Erro ao remover professor: {e}")

def obter_professores():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, disciplina, cpf, data_criacao FROM professores ORDER BY nome ASC")
        professores = cursor.fetchall()
        conn.close()
        return professores
    except Exception as e:
        raise Exception(f"Erro ao obter professores: {e}")

def obter_professor_por_id(professor_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, disciplina, cpf, data_criacao FROM professores WHERE id = ?", (professor_id,))
        professor = cursor.fetchone()
        conn.close()
        return professor
    except Exception as e:
        raise Exception(f"Erro ao obter professor: {e}")

def atualizar_professor_db(professor_id, nome, disciplina, cpf):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("UPDATE professores SET nome = ?, disciplina = ?, cpf = ? WHERE id = ?",
                      (nome, disciplina, cpf, professor_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Erro ao atualizar professor: {e}")