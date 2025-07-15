from Persistencia.Entidade.Exercicio import Exercicio
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl

persistencia = ExercicioPersistenciaImpl()

def inserir_direto():
    # Objetivo
    ex1 = Exercicio(
        id_exercicio=None,
        id_fase=1,
        dicas="Use estruturas condicionais como if/else.",
        tipo="objetivo",
        resposta_certa="if x > 0:\n    print('positivo')",
        resposta_erradas=[
            {"texto": "if x > 0 then print('positivo')", "correta": False},
            {"texto": "if x > 0 { print('positivo') }", "correta": False},
            {"texto": "x > 0 ? print('positivo')", "correta": False}
        ]
    )

    # Subjetivo
    ex2 = Exercicio(
        id_exercicio=None,
        id_fase=1,
        dicas="Explique como a função print funciona.",
        tipo="subjetivo",
        resposta_certa="A função print() exibe dados no console.",
        resposta_erradas=[]
    )

    persistencia.salvar(ex1)
    persistencia.salvar(ex2)
    print("Exercícios inseridos diretamente com sucesso.")

def inserir_por_terminal():
    print("\nInserir exercício manual")
    id_fase = int(input("ID da fase: "))
    dicas = input("Dicas: ")
    tipo = input("Tipo (objetivo/subjetivo): ").strip().lower()
    resposta_certa = input("Resposta correta: ")

    if tipo == "objetivo":
        alternativas = []
        print("Informe alternativas incorretas:")
        while True:
            texto_alt = input("Texto da alternativa (ou ENTER para finalizar): ")
            if not texto_alt:
                break
            alternativas.append({"texto": texto_alt, "correta": False})
        resposta_erradas = alternativas
    else:
        resposta_erradas = []

    exercicio = Exercicio(
        id_exercicio=None,
        id_fase=id_fase,
        dicas=dicas,
        tipo=tipo,
        resposta_certa=resposta_certa,
        resposta_erradas=resposta_erradas
    )

    persistencia.salvar(exercicio)
    print("Exercício inserido com sucesso.")

def menu():
    while True:
        print("\nMenu de Inserção de Exercício")
        print("1 - Inserir pré-definidos")
        print("2 - Inserir manualmente")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            inserir_direto()
        elif opcao == "2":
            inserir_por_terminal()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

menu()