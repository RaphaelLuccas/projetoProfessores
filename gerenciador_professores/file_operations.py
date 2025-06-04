from tkinter import messagebox
from database import conectar_banco

def salvar_em_arquivo(caminho):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, disciplina, cpf FROM professores")
        professores = cursor.fetchall()
        with open(caminho, "w") as f:
            for nome, disciplina, cpf in professores:
                f.write(f"{nome},{disciplina},{cpf}\n")
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
        return False

def abrir_arquivo(caminho):
    try:
        with open(caminho, "r") as f:
            linhas = f.readlines()
            conn = conectar_banco()
            cursor = conn.cursor()
            for linha in linhas:
                partes = linha.strip().split(",")
                if len(partes) == 3:
                    nome, disciplina, cpf = partes[0], partes[1], partes[2]
                    cpf_limpo = ''.join(filter(str.isdigit, cpf))
                    if len(cpf_limpo) == 11:
                        cursor.execute("INSERT INTO professores (nome, disciplina, cpf) VALUES (?, ?, ?)",
                                     (nome, disciplina, cpf_limpo))
                    else:
                        messagebox.showwarning("CPF Inválido",
                            f"CPF '{cpf}' na linha '{linha.strip()}' não tem 11 dígitos. Linha ignorada.")
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir: {str(e)}")
        return False
