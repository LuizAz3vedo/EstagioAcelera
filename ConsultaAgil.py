import datetime
import json

PACIENTES_FILE = 'pacientes.json'
AGENDAMENTOS_FILE = 'agendamentos.json'

pacientes_cadastrados = {}
agendamentos = []

# Função para carregar os pacientes cadastrados a partir do arquivo "pacientes.json"
def carregar_pacientes():
    global pacientes_cadastrados
    try:
        with open("pacientes.json", "r") as file:
            content = file.read()
            if content:
                pacientes_cadastrados = json.loads(content)
            else:
                pacientes_cadastrados = {}
    except FileNotFoundError:
        pacientes_cadastrados = {}

# Função para salvar os pacientes cadastrados no arquivo "pacientes.json"    
def salvar_pacientes():
    with open(PACIENTES_FILE, 'w') as file:
        json.dump(pacientes_cadastrados, file)

# Função para carregar os agendamentos a partir do arquivo "agendamentos.json"
def carregar_agendamentos():
    global agendamentos
    try:
        with open("agendamentos.json", "r") as file:
            content = file.read()
            if content:
                agendamentos = json.loads(content)
            else:
                agendamentos = []
    except FileNotFoundError:
        agendamentos = []

# Função para salvar os agendamentos no arquivo "agendamentos.json"
def salvar_agendamentos():
    with open(AGENDAMENTOS_FILE, 'w') as file:
        json.dump(agendamentos, file)

# Função para cadastrar um novo paciente
def cadastrar_paciente():
    nome = str(input("Digite o nome do paciente: "))
    telefone = input("Digite o telefone do paciente: ")

    if len(telefone) != 11 or not telefone.isdigit():
        print("\nNúmero de telefone inválido! O telefone deve conter 11 dígitos numéricos.")
    elif telefone in pacientes_cadastrados:
        print("\nPaciente já cadastrado!")
    else:
        pacientes_cadastrados[telefone] = nome
        print("\nPaciente cadastrado com sucesso!")
        salvar_pacientes()

# Função para exibir os pacientes cadastrados
def exibir_pacientes_cadastrados():
    if not pacientes_cadastrados:
        print("Não há pacientes cadastrados.")
    else:
        print("Pacientes cadastrados:")
        for i, telefone in enumerate(pacientes_cadastrados, start=1):
            print(f"{i} - Nome: {pacientes_cadastrados[telefone]}, Telefone: {telefone}")

# Função para marcar uma consulta
def marcar_consulta():
    exibir_pacientes_cadastrados()
    escolha = input("Escolha o número correspondente a um paciente: ")

    if escolha.isdigit() and int(escolha) in range(1, len(pacientes_cadastrados) + 1):
        telefone = list(pacientes_cadastrados.keys())[int(escolha) - 1]
        paciente = pacientes_cadastrados[telefone]
        data = input("Digite a data da consulta (DD/MM/AAAA): ")
        hora = input("Digite a hora da consulta (HH:MM): ")
        especialidade = input("Digite a especialidade desejada: ")


        # Verificar se a data está no formato correto
        try:
            data_consulta = datetime.datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            print("\nData inválida! A data deve estar no formato DD/MM/AAAA.")
            return

        # Verificar se a data e hora estão disponíveis
        consulta_disponivel = True
        for agendamento in agendamentos:
            if agendamento['data'] == data and agendamento['hora'] == hora:
                consulta_disponivel = False
                break
                
        # Verificar se a data não é retroativa
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
        data_consulta = datetime.datetime.strptime(data, "%d/%m/%Y")
        if data_consulta < datetime.datetime.strptime(data_atual, "%d/%m/%Y"):
            consulta_disponivel = False

        if consulta_disponivel:
            agendamento = {'paciente': paciente, 'telefone': telefone, 'data': data, 'hora': hora, 'especialidade': especialidade}
            agendamentos.append(agendamento)
            print("\nConsulta marcada com sucesso!")
            salvar_agendamentos()
            salvar_pacientes()
        else:
            print("\nA data e hora selecionadas não estão disponíveis para agendamento.")

    else:
        print("Opção inválida!")

# Função para exibir os agendamento de consulta
def exibir_agendamentos():
    if not agendamentos:
        print("Não há consultas agendadas.")
    else:
        print("Consultas agendadas:")
        for i, agendamento in enumerate(agendamentos, start=1):
            print(f"{i} - Paciente: {agendamento['paciente']}, Data: {agendamento['data']}, Hora: {agendamento['hora']}, Especialidade: {agendamento['especialidade']}")

# Função para cancelar uma consulta
def cancelar_consulta():
    if not agendamentos:
        print("Não há consultas agendadas.")
        return

    exibir_agendamentos()
    escolha = input("Escolha o número correspondente a um agendamento: ")

    if escolha.isdigit() and int(escolha) in range(1, len(agendamentos) + 1):
        agendamento = agendamentos[int(escolha) - 1]
        print("Informações da consulta:")
        print(f"Paciente: {agendamento['paciente']}")
        print(f"Data: {agendamento['data']}")
        print(f"Hora: {agendamento['hora']}")
        print(f"Especialidade: {agendamento['especialidade']}")

        confirmacao = input("Deseja cancelar essa consulta? (S/N): ")
        if confirmacao.lower() == 's':
            agendamentos.remove(agendamento)
            print("Consulta cancelada com sucesso!")
            salvar_agendamentos()
            salvar_pacientes()
        else:
            print("Cancelamento da consulta abortado.")
    else:
        print("Opção inválida!")

# Função do menu principal do programa
def menu_principal():
    carregar_pacientes()
    carregar_agendamentos()
    while True:
        print("\nMenu Principal:")
        print("1 - Cadastrar paciente")
        print("2 - Marcar consulta")
        print("3 - Cancelar consulta")
        print("4 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            cadastrar_paciente()
            
        elif opcao == "2":
            marcar_consulta()
            pass
        elif opcao == "3":
            cancelar_consulta()
        elif opcao == "4":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")

    salvar_pacientes()
    salvar_agendamentos()

# Inicia o programa chamando a função do menu principal
menu_principal()
