import tkinter as tk
from tkinter import messagebox
from database import obter_professor_por_id, atualizar_professor_db
from utils import validar_e_formatar_cpf, formatar_cpf_display

class EditarProfessorWindow:
    def __init__(self, parent, professor_id, callback_atualizar):
        self.parent = parent
        self.professor_id = professor_id
        self.callback_atualizar = callback_atualizar
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Editar Professor")
        self.janela.geometry("400x300")
        self.janela.resizable(True, True)
        self.janela.transient(parent)
        self.janela.grab_set()

        self.janela.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.carregar_dados()
        self.criar_widgets()
    
    def carregar_dados(self):
        try:
            self.professor_data = obter_professor_por_id(self.professor_id)
            if not self.professor_data:
                messagebox.showerror("Erro", "Professor não encontrado!")
                self.janela.destroy()
                return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
            self.janela.destroy()
    
    def criar_widgets(self):
        tk.Label(self.janela, text=f"Editando Professor ID: {self.professor_id}", 
                font=("Arial", 12, "bold")).pack(pady=10)

        frame = tk.Frame(self.janela)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(frame, text="Nome completo:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_nome = tk.Entry(frame, width=50, bd=2, relief="groove")
        self.entry_nome.pack(fill="x", pady=(0, 10))
        self.entry_nome.insert(0, self.professor_data[1])  # nome

        tk.Label(frame, text="CPF:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_cpf_var = tk.StringVar()
        vcmd = (self.janela.register(self.validar_cpf), '%P')
        self.entry_cpf = tk.Entry(frame, width=50, bd=2, relief="groove",
                                 textvariable=self.entry_cpf_var, validate="key",
                                 validatecommand=vcmd)
        self.entry_cpf.pack(fill="x", pady=(0, 10))
        cpf_formatado = formatar_cpf_display(self.professor_data[3])
        self.entry_cpf_var.set(cpf_formatado)

        tk.Label(frame, text="Disciplina:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_disciplina = tk.Entry(frame, width=50, bd=2, relief="groove")
        self.entry_disciplina.pack(fill="x", pady=(0, 20))
        self.entry_disciplina.insert(0, self.professor_data[2])  # disciplina

        frame_botoes = tk.Frame(frame)
        frame_botoes.pack(fill="x")
        
        tk.Button(frame_botoes, text="Salvar Alterações", command=self.salvar_alteracoes,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_botoes, text="Cancelar", command=self.cancelar,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                 relief="raised", bd=3).pack(side=tk.LEFT)

        self.janela.bind('<Return>', lambda event: self.salvar_alteracoes())
    
    def validar_cpf(self, P):
        self.entry_cpf_var.set(validar_e_formatar_cpf(P))
        return True
    
    def salvar_alteracoes(self):
        try:
            nome = self.entry_nome.get().strip()
            disciplina = self.entry_disciplina.get().strip()
            cpf_raw = self.entry_cpf_var.get().replace(".", "").replace("-", "")
            
            if not nome or not disciplina or not cpf_raw or len(cpf_raw) != 11:
                messagebox.showwarning("Campos inválidos", 
                    "Por favor, preencha todos os campos com dados válidos.")
                return

            atualizar_professor_db(self.professor_id, nome, disciplina, cpf_raw)
            
            messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
            self.callback_atualizar()
            self.janela.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alterações: {str(e)}")
    
    def cancelar(self):
        if messagebox.askyesno("Cancelar", "Deseja cancelar as alterações?"):
            self.janela.destroy()