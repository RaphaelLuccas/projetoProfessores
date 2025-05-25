import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sqlite3
from datetime import datetime

def conectar_banco():

    return sqlite3.connect("professores.db")

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS professores
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome
                       TEXT
                       NOT
                       NULL,
                       disciplina
                       TEXT
                       NOT
                       NULL,
                       cpf
                       TEXT
                       NOT
                       NULL,
                       data_criacao
                       DATETIME
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()


def adicionar_professor():
    nome = entry_nome.get().strip()
    disciplina = entry_disciplina.get().strip()
    cpf_raw = entry_cpf_var.get().replace(".", "").replace("-", "")

    if nome and disciplina and cpf_raw and len(cpf_raw) == 11:
        conn = conectar_banco()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO professores (nome, disciplina, cpf) VALUES (?, ?, ?)",
                           (nome, disciplina, cpf_raw))
            conn.commit()
            messagebox.showinfo("Sucesso", "Professor adicionado com sucesso!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro de CPF",
                                 f"Erro ao adicionar professor: {e}. O CPF pode já existir ou ser inválido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar professor: {str(e)}")
        finally:
            conn.close()

        entry_nome.delete(0, tk.END)
        entry_disciplina.delete(0, tk.END)
        entry_cpf_var.set("")
        atualizar_lista()
    else:
        messagebox.showwarning("Campos vazios ou CPF inválido",
                               "Por favor, preencha Nome, Disciplina e um CPF válido (11 dígitos).")


def atualizar_lista():
    listbox_professores.delete(0, tk.END)

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, disciplina, cpf, data_criacao FROM professores ORDER BY nome ASC")
    for row in cursor.fetchall():
        data_formatada = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
        cpf_formatado = formatar_cpf_display(row[3])
        listbox_professores.insert(tk.END,
                                   f"{row[0]}. {row[1]} - {row[2]} (CPF: {cpf_formatado}) - Criado em: {data_formatada}")
    conn.close()


def remover_professor():
    selecionado = listbox_professores.curselection()
    if selecionado:
        indice = selecionado[0]
        professor_id = listbox_professores.get(indice).split(".")[0]

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o professor ID {professor_id}?"):
            conn = conectar_banco()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM professores WHERE id = ?", (professor_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover professor: {str(e)}")
            finally:
                conn.close()
            atualizar_lista()
    else:
        messagebox.showwarning("Nenhuma seleção", "Selecione um professor para remover.")


def salvar_em_arquivo():
    caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
    if caminho:
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, disciplina, cpf FROM professores")
            professores = cursor.fetchall()
            with open(caminho, "w") as f:
                for nome, disciplina, cpf in professores:
                    f.write(f"{nome},{disciplina},{cpf}\n")  # Salvar CPF sem formatação
            conn.close()
            messagebox.showinfo("Salvo", "Professores salvos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")


def abrir_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    if caminho and os.path.exists(caminho):
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
                            messagebox.showwarning("CPF Inválido na Importação",
                                                   f"CPF '{cpf}' na linha '{linha.strip()}' não tem 11 dígitos. Linha ignorada.")
                    elif len(partes) == 2:
                        nome, disciplina = partes[0], partes[1]
                        messagebox.showwarning("Dados Incompletos",
                                               f"A linha '{linha.strip()}' não contém CPF. Inserindo com CPF '00000000000'. Por favor, edite manualmente.")
                        cursor.execute("INSERT INTO professores (nome, disciplina, cpf) VALUES (?, ?, ?)",
                                       (nome, disciplina, "00000000000"))
                    else:
                        messagebox.showwarning("Formato Inválido",
                                               f"Linha ignorada devido ao formato inválido: '{linha.strip()}'")
                conn.commit()
                conn.close()
                atualizar_lista()
                messagebox.showinfo("Aberto", "Professores importados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir: {str(e)}")


def sair():
    janela.destroy()


def validar_e_formatar_cpf(P):
    cpf_limpo = ''.join(filter(str.isdigit, P))

    if len(cpf_limpo) > 11:
        cpf_limpo = cpf_limpo[:11]

    cpf_formatado = ""
    if len(cpf_limpo) > 0:
        if len(cpf_limpo) > 9:
            cpf_formatado = f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        elif len(cpf_limpo) > 6:
            cpf_formatado = f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:]}"
        elif len(cpf_limpo) > 3:
            cpf_formatado = f"{cpf_limpo[0:3]}.{cpf_limpo[3:]}"
        else:
            cpf_formatado = cpf_limpo

    entry_cpf_var.set(cpf_formatado)
    return True

def formatar_cpf_display(cpf_raw):
    cpf_limpo = ''.join(filter(str.isdigit, cpf_raw))
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf_raw

janela = tk.Tk()
janela.title("Gerenciamento de Professores Substitutos")
janela.geometry("500x550")
janela.resizable(False, False)

criar_tabela()

menu = tk.Menu(janela)
janela.config(menu=menu)

menu_arquivo = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Salvar Dados", command=salvar_em_arquivo)
menu_arquivo.add_command(label="Abrir Dados", command=abrir_arquivo)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=sair)

tk.Label(janela, text="Nome completo do Professor:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
entry_nome = tk.Entry(janela, width=50, bd=2, relief="groove")
entry_nome.pack(pady=2)

tk.Label(janela, text="CPF:", font=("Arial", 10, "bold")).pack(pady=(5, 0))

entry_cpf_var = tk.StringVar()

vcmd = (janela.register(validar_e_formatar_cpf), '%P')
entry_cpf = tk.Entry(janela, width=50, bd=2, relief="groove", textvariable=entry_cpf_var, validate="key",
                     validatecommand=vcmd)
entry_cpf.pack(pady=2)

tk.Label(janela, text="Disciplina:", font=("Arial", 10, "bold")).pack(pady=(5, 0))
entry_disciplina = tk.Entry(janela, width=50, bd=2, relief="groove")
entry_disciplina.pack(pady=2)

tk.Button(janela, text="Adicionar Professor", command=adicionar_professor, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), relief="raised", bd=3).pack(pady=5)
tk.Button(janela, text="Remover Selecionado", command=remover_professor, bg="#f44336", fg="white",
          font=("Arial", 10, "bold"), relief="raised", bd=3).pack(pady=5)

tk.Label(janela, text="Professores Substitutos Cadastrados:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
listbox_professores = tk.Listbox(janela, width=60, height=10, bd=2, relief="sunken", selectmode=tk.SINGLE,
                                 font=("Arial", 9))
listbox_professores.pack(pady=5)

tk.Button(janela, text="Sair", command=sair, fg="white", bg="red", font=("Arial", 10, "bold"), relief="raised",
          bd=3).pack(pady=10)

atualizar_lista()

janela.mainloop()