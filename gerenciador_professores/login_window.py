
import tkinter as tk
from tkinter import messagebox
from database import verificar_login

class LoginWindow:
    def __init__(self, on_success_callback):
        self.on_success_callback = on_success_callback
        self.janela = tk.Tk()
        self.janela.title("Login - Sistema de Professores")
        self.janela.geometry("400x300")
        self.janela.resizable(True, True)

        self.janela.transient()
        self.janela.grab_set()
        
        self.criar_widgets()
        
    def criar_widgets(self):
        tk.Label(self.janela, text="Sistema de Gerenciamento", 
                font=("Arial", 14, "bold")).pack(pady=20)

        frame = tk.Frame(self.janela)
        frame.pack(pady=20)

        tk.Label(frame, text="Usuário:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_usuario = tk.Entry(frame, width=20, bd=2, relief="groove")
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Senha:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_senha = tk.Entry(frame, width=20, bd=2, relief="groove", show="*")
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        tk.Button(frame_botoes, text="Entrar", command=self.fazer_login,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botoes, text="Cancelar", command=self.cancelar,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                 width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(self.janela, text="Login padrão: admin / admin", 
                font=("Arial", 8), fg="gray").pack(pady=5)

        self.janela.bind('<Return>', lambda event: self.fazer_login())

        self.entry_usuario.focus()
    
    def fazer_login(self):
        try:
            usuario = self.entry_usuario.get().strip()
            senha = self.entry_senha.get().strip()
            
            if not usuario or not senha:
                messagebox.showwarning("Campos vazios", "Por favor, preencha usuário e senha.")
                return
            
            if verificar_login(usuario, senha):
                self.janela.destroy()
                self.on_success_callback()
            else:
                messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")
                self.entry_senha.delete(0, tk.END)
                self.entry_usuario.focus()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante o login: {str(e)}")
    
    def cancelar(self):
        self.janela.destroy()
    
    def mostrar(self):
        self.janela.mainloop()