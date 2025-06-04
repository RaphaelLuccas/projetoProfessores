import tkinter as tk
from tkinter import messagebox, filedialog
from database import adicionar_professor_db, remover_professor_db, obter_professores
from utils import validar_e_formatar_cpf, formatar_cpf_display, formatar_data
from file_operations import salvar_em_arquivo, abrir_arquivo
from editar_professor import EditarProfessorWindow

class ProfessorGUI:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Gerenciamento de Professores Substitutos")
        self.janela.geometry("500x600")
        self.janela.resizable(True, True)
        
        self.criar_menu()
        self.criar_widgets()
        self.atualizar_lista()
    
    def criar_menu(self):
        menu = tk.Menu(self.janela)
        self.janela.config(menu=menu)
        
        menu_arquivo = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Salvar Dados", command=self.salvar_dados)
        menu_arquivo.add_command(label="Abrir Dados", command=self.abrir_dados)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.sair)
    
    def criar_widgets(self):
        # Entradas
        tk.Label(self.janela, text="Nome completo do Professor:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.entry_nome = tk.Entry(self.janela, width=50, bd=2, relief="groove")
        self.entry_nome.pack(pady=2)

        tk.Label(self.janela, text="CPF:", font=("Arial", 10, "bold")).pack(pady=(5, 0))
        self.entry_cpf_var = tk.StringVar()
        vcmd = (self.janela.register(self.validar_cpf), '%P')
        self.entry_cpf = tk.Entry(self.janela, width=50, bd=2, relief="groove",
                                 textvariable=self.entry_cpf_var, validate="key",
                                 validatecommand=vcmd)
        self.entry_cpf.pack(pady=2)

        tk.Label(self.janela, text="Disciplina:", font=("Arial", 10, "bold")).pack(pady=(5, 0))
        self.entry_disciplina = tk.Entry(self.janela, width=50, bd=2, relief="groove")
        self.entry_disciplina.pack(pady=2)

        # Botões de ação
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        tk.Button(frame_botoes, text="Adicionar Professor", command=self.adicionar_professor,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botoes, text="Editar Selecionado", command=self.editar_professor,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botoes, text="Remover Selecionado", command=self.remover_professor,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(side=tk.LEFT, padx=5)

        # Lista de professores
        tk.Label(self.janela, text="Professores Substitutos Cadastrados:",
                font=("Arial", 12, "bold")).pack(pady=(10, 5))
        self.listbox_professores = tk.Listbox(self.janela, width=60, height=10,
                                            bd=2, relief="sunken", selectmode=tk.SINGLE,
                                            font=("Arial", 9))
        self.listbox_professores.pack(pady=5)

        # Botão Sair
        tk.Button(self.janela, text="Sair", command=self.sair,
                 fg="white", bg="red", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(pady=10)

    def validar_cpf(self, P):
        self.entry_cpf_var.set(validar_e_formatar_cpf(P))
        return True

    def adicionar_professor(self):
        try:
            nome = self.entry_nome.get().strip()
            disciplina = self.entry_disciplina.get().strip()
            cpf_raw = self.entry_cpf_var.get().replace(".", "").replace("-", "")

            if nome and disciplina and cpf_raw and len(cpf_raw) == 11:
                adicionar_professor_db(nome, disciplina, cpf_raw)
                messagebox.showinfo("Sucesso", "Professor adicionado com sucesso!")
                self.limpar_campos()
                self.atualizar_lista()
            else:
                messagebox.showwarning("Campos vazios ou CPF inválido",
                                     "Por favor, preencha Nome, Disciplina e um CPF válido (11 dígitos).")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar professor: {str(e)}")

    def editar_professor(self):
        try:
            selecionado = self.listbox_professores.curselection()
            if selecionado:
                indice = selecionado[0]
                professor_id = self.listbox_professores.get(indice).split(".")[0]
                EditarProfessorWindow(self.janela, professor_id, self.atualizar_lista)
            else:
                messagebox.showwarning("Nenhuma seleção", "Selecione um professor para editar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir janela de edição: {str(e)}")

    def remover_professor(self):
        try:
            selecionado = self.listbox_professores.curselection()
            if selecionado:
                indice = selecionado[0]
                professor_id = self.listbox_professores.get(indice).split(".")[0]
                if messagebox.askyesno("Confirmar Remoção",
                                     f"Tem certeza que deseja remover o professor ID {professor_id}?"):
                    remover_professor_db(professor_id)
                    messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
                    self.atualizar_lista()
            else:
                messagebox.showwarning("Nenhuma seleção", "Selecione um professor para remover.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover professor: {str(e)}")

    def atualizar_lista(self):
        try:
            self.listbox_professores.delete(0, tk.END)
            for prof in obter_professores():
                data_formatada = formatar_data(prof[4])
                cpf_formatado = formatar_cpf_display(prof[3])
                self.listbox_professores.insert(tk.END,
                    f"{prof[0]}. {prof[1]} - {prof[2]} (CPF: {cpf_formatado}) - Criado em: {data_formatada}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista: {str(e)}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_disciplina.delete(0, tk.END)
        self.entry_cpf_var.set("")

    def salvar_dados(self):
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")])
            if caminho and salvar_em_arquivo(caminho):
                messagebox.showinfo("Salvo", "Professores salvos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")

    def abrir_dados(self):
        try:
            caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
            if caminho and abrir_arquivo(caminho):
                self.atualizar_lista()
                messagebox.showinfo("Aberto", "Professores importados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir dados: {str(e)}")

    def sair(self):
        self.janela.destroy()