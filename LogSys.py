import os
import json
import getpass

def limparConsole():
    os.system("cls")

# Funções dos menus
def menuPrincipal():
    while True:
        limparConsole()
        print("Sistema de login")
        print("----------------")
        print("{:<5} {:<10}".format("Opção", "Descrição"))
        print("----------------")
        print("{:<5} {:<10}".format("1", "Logar"))
        print("{:<5} {:<10}".format("2", "Registrar"))
        print("{:<5} {:<10}".format("3", "Sair"))
        try:
            opcaoMenuPrincipal = int(input("\nSelecione uma opção: "))
            if opcaoMenuPrincipal == 1:
                logarUsuario()
                break
            elif opcaoMenuPrincipal == 2:
                registrarUsuario()
                break
            elif opcaoMenuPrincipal == 3:
                print("\nAté mais!")
                break
            elif opcaoMenuPrincipal == 99:
                listarTodosOsUsuarios()
                input("\nPressione Enter para voltar ao menu.")
                limparConsole()
                continue
            else:
                print("\nOpção inválida. Por favor, selecione uma opção válida.")
        except ValueError:
            print("\nOpção inválida. Por favor, selecione uma opção válida.")
            input("\nPressione Enter para voltar ao menu.")
            limparConsole()

def exibirTabela():
    print("----------------")
    print("{:<5} {:<10}".format("Opção", "Descrição"))
    print("----------------")
    print("{:<5} {:<10}".format("1", "Alterar dados cadastrais"))
    print("{:<5} {:<10}".format("2", "Deletar conta"))
    print("{:<5} {:<10}".format("3", "Sair para login"))

def subMenuLogado(username):
    limparConsole()
    print("Bem-vindo, " + username)
    exibirTabela()
    
    while True:
        try:
            opcaoSubMenuLogado = int(input("\nSelecione uma opção: "))
            if opcaoSubMenuLogado == 1:
                subMenuAlteracaoDeDadosCadastrais(username)
                break
            elif opcaoSubMenuLogado == 2:
                confirmacao = int(input("Deseja realmente deletar sua conta? (1 - Sim, tenho certeza. | 2 - Não, mudei de ideia.)\n"))
                if confirmacao == 1:
                    deleteUserInDataBase(username)
                    menuPrincipal()
                    break
                else:
                    subMenuLogado(username)
            elif opcaoSubMenuLogado == 3:
                menuPrincipal()
                break
            else:
                print("\nOpção inválida. Por favor, selecione uma opção válida.")
        except ValueError:
            print("\nOpção inválida. Por favor, selecione uma opção válida.")
            input("\nPressione Enter para voltar ao menu.")
            limparConsole()
            
        exibirTabela()

def exibirTabelaOpcoes():
    print("----------------")
    print("{:<5} {:<10}".format("Opção", "Descrição"))
    print("----------------")
    print("{:<5} {:<10}".format("1", "Alterar nome de usuário"))
    print("{:<5} {:<10}".format("2", "Alterar senha de usuário"))
    print("{:<5} {:<10}".format("3", "Voltar"))

def subMenuAlteracaoDeDadosCadastrais(username):
    limparConsole()
    exibirTabelaOpcoes()
    
    while True:
        try:
            opcaoAlteracaoDeDadosCadastrais = int(input("\nSelecione uma opção: "))
            if opcaoAlteracaoDeDadosCadastrais == 1:
                alterarDadosCadastrais("username", username)
                break
            elif opcaoAlteracaoDeDadosCadastrais == 2:
                alterarDadosCadastrais("password", username)
                break
            elif opcaoAlteracaoDeDadosCadastrais == 3:
                subMenuLogado(username)
                break
            else:
                print("\nOpção inválida. Por favor, selecione uma opção válida.")
                input("\nPressione Enter para voltar ao menu.")
                limparConsole()
                exibirTabelaOpcoes()
        except ValueError:
            print("\nOpção inválida. Por favor, selecione uma opção válida.")
            input("\nPressione Enter para continuar.")
            limparConsole()
            exibirTabelaOpcoes()

# Funções do sistema
def logarUsuario():
    limparConsole()
    print("\n---- LOGAR ---- ")
    username = input("Digite seu nome de usuário: ")
    if verifyIfExistsInDataBase(username):
        senha = getpass.getpass("Digite sua senha: ")
        if senha == readUser(username)["password"]:
            print("Logado com sucesso!")
            subMenuLogado(username)
        else:
            print("Senha inválida.")
            menuPrincipal()
    else:
        print("Usuário não encontrado no banco de dados.")
        menuPrincipal()

# Registro do usuário no sistema
def registrarUsuario():
    limparConsole()
    print("\n---- REGISTRAR ----")
    dadosDoUsuario = {
        "username": input("\nDigite um nome de usuário: "),
        "password": input("\nDigite uma senha de usuário: ")
    }
    if dadosDoUsuario["password"] != input("\nDigite novamente sua senha de usuário: "):
        print("Você digitou senhas diferentes. Por favor, refaça o processo.")
        menuPrincipal()
    if not verifyIfExistsInDataBase(dadosDoUsuario["username"]):
        createUserInDataBase(dadosDoUsuario)
        menuPrincipal()
    else:
        print("Nome de usuário já existe no banco de dados.")
        menuPrincipal()

# Alteração de senha do usuário
def alterarDadosCadastrais(campo: str, username: str):
    novoDado = getpass.getpass("Informe o novo dado: ")
    if campo == "password":
        updateUserInDataBase(novoDado, campo, username)
        menuPrincipal()
    else:
        if not verifyIfExistsInDataBase(novoDado):
            updateUserInDataBase(novoDado, campo, username)
            menuPrincipal()
        else:
            print("Nome de usuário já existe no banco de dados.")
            menuPrincipal()

# Funções de acesso ao banco de dados (apenas leitura)
def verifyIfExistsInDataBase(nome, field="username"):
    with open("data.txt", "r") as database:
        for linha in database:
            dados = json.loads(linha)
            if dados[field] == nome:
                return True
    return False

# Funções de CRUD - BD
def createUserInDataBase(dadosDoUsuario):
    with open("data.txt", "a") as database:
        json.dump(dadosDoUsuario, database)
        database.write("\n")

def readUser(username: str):     
    with open("data.txt", "r") as database:
        for linha in database:
            dados = json.loads(linha)
            if dados["username"] == username:
                return dados

def updateUserInDataBase(value: str, field: str, username: str):
    updated_users = []
    with open("data.txt", "r") as database:
        for linha in database:
            dados = json.loads(linha)
            if dados["username"] == username:
                dados[field] = value
            updated_users.append(dados)

    with open("data.txt", "w") as database:
        for user in updated_users:
            json.dump(user, database)
            database.write("\n")

# Função delete user in database
def deleteUserInDataBase(username: str):
    with open("data.txt", "r") as database:
        lines = database.readlines()    

    with open("data.txt", "w") as database:
        for line in lines:
            dados = json.loads(line)
            if dados["username"] != username:
                database.write(line)

# Função Master, Admin only
def listarTodosOsUsuarios():
    with open("data.txt", "r") as database:
        for linha in database:
            dados = json.loads(linha)
            print(f"Nome de usuário: {dados['username']}, Senha: {dados['password']}")

# Iniciar o sistema
menuPrincipal()
