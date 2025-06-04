import tkinter as tk
from database import criar_tabela, criar_tabela_usuarios
from gui import ProfessorGUI
from login_window import LoginWindow

def iniciar_aplicacao():
    try:
        janela = tk.Tk()
        app = ProfessorGUI(janela)

        janela.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")

def main():
    try:
        criar_tabela()
        criar_tabela_usuarios()

        login_window = LoginWindow(iniciar_aplicacao)
        login_window.mostrar()
        
    except Exception as e:
        print(f"Erro na inicialização: {e}")

if __name__ == "__main__":
    main()