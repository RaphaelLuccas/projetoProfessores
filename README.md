Gerenciamento de Professores Substitutos

Este é um aplicativo de desktop simples desenvolvido em Python com Tkinter para gerenciar informações de professores substitutos, incluindo nome, disciplina e CPF. Os dados são armazenados localmente em um banco de dados SQLite.
Funcionalidades

    Adicionar Professor: Permite cadastrar novos professores com seu nome completo, disciplina e CPF.

    Validação e Formatação de CPF: O campo de CPF aceita apenas números, limita a entrada a 11 dígitos e formata automaticamente o CPF (XXX.XXX.XXX-XX) enquanto o usuário digita.

    Remover Professor: Permite remover um professor selecionado da lista.

    Listagem de Professores: Exibe todos os professores cadastrados em uma lista, com seus IDs, nomes, disciplinas, CPFs formatados e a data de criação do registro.

    Salvar Dados: Exporta os dados dos professores (nome, disciplina, CPF) para um arquivo de texto (.txt).

    Abrir Dados: Importa dados de professores de um arquivo de texto (.txt) para o banco de dados. Inclui tratamento para CPFs incompletos ou mal formatados durante a importação.

    Persistência de Dados: Os dados são armazenados em um arquivo professores.db (SQLite) no mesmo diretório do script, garantindo que as informações sejam mantidas entre as sessões.

Como Usar
Pré-requisitos

    Python 3.13 instalado.

Executando o Aplicativo

    Salve o código: Salve o código Python fornecido em um arquivo, por exemplo, app_professores.py.

    Execute o script: Abra um terminal ou prompt de comando, navegue até o diretório onde você salvou o arquivo e execute o comando:

    python app_professores.py

Interface do Usuário

    Campos de Entrada: Preencha "Nome completo do Professor", "CPF" e "Disciplina" nos campos correspondentes.

    Adicionar Professor: Clique no botão "Adicionar Professor" para salvar as informações no banco de dados.

    Remover Selecionado: Selecione um professor na lista e clique em "Remover Selecionado" para excluí-lo. Uma confirmação será solicitada.

    Menu "Arquivo":

        Salvar Dados: Abre uma caixa de diálogo para escolher onde salvar um arquivo de texto com os dados dos professores.

        Abrir Dados: Abre uma caixa de diálogo para selecionar um arquivo de texto e importar os professores para o aplicativo.

        Sair: Fecha o aplicativo.

Estrutura do Projeto

    app_professores.py: O script principal que contém toda a lógica da interface gráfica (Tkinter) e a interação com o banco de dados SQLite.

    professores.db: O arquivo do banco de dados SQLite que será criado automaticamente na primeira execução do aplicativo.

Observações

    O CPF é armazenado no banco de dados apenas com os 11 dígitos numéricos, sem pontos ou traços. A formatação é aplicada apenas na interface do usuário para melhor visualização.

    A importação de arquivos de texto tenta lidar com formatos antigos (apenas nome e disciplina), inserindo um CPF padrão e emitindo um aviso.
e projeto é de código aberto e está disponível sob a licença MIT.
