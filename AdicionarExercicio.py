from Persistencia.Entidade.Exercicio import Exercicio
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl

exercicios = [
    # Fase 1: print()
    Exercicio(id_exercicio=None, id_fase=1,
              dicas="Dica: É usado para exibir textos ou valores na tela.",
              pergunta="Qual comando em Python exibe um texto na tela?",
              tipo="objetiva", resposta_certa="print()",
              resposta_erradas="show(),output(),display()"),

    Exercicio(id_exercicio=None, id_fase=1,
              dicas="Use o comando correto para mostrar uma saudação.",
              pergunta="Escreva o comando para mostrar 'Bem-vindo!' na tela.",
              tipo="dissertativa", resposta_certa='print("Bem-vindo!")',
              resposta_erradas=None),

    # Fase 2: input()
    Exercicio(id_exercicio=None, id_fase=2,
              dicas="Dica: Esse comando aguarda a digitação do usuário.",
              pergunta="Qual comando lê um texto digitado pelo usuário?",
              tipo="objetiva", resposta_certa="input()",
              resposta_erradas="scan(),read(),get()"),

    Exercicio(id_exercicio=None, id_fase=2,
              dicas="Use input para capturar e print para exibir.",
              pergunta="Peça ao usuário seu nome e exiba uma saudação.",
              tipo="dissertativa", resposta_certa='nome = input("Qual seu nome? ")\nprint("Olá,", nome)',
              resposta_erradas=None),

    # Fase 3: variáveis
    Exercicio(id_exercicio=None, id_fase=3,
              dicas="Cuidado com aspas: número entre aspas é string.",
              pergunta="Qual destas linhas cria uma variável do tipo inteiro em Python?",
              tipo="objetiva", resposta_certa="numero = 5",
              resposta_erradas='numero = "5",int numero = 5,let numero = 5'),

    Exercicio(id_exercicio=None, id_fase=3,
              dicas="Use = para atribuir um valor à variável.",
              pergunta="Crie uma variável chamada idade e atribua o valor 20.",
              tipo="dissertativa", resposta_certa="idade = 20",
              resposta_erradas=None),

    # Fase 4: operadores
    Exercicio(id_exercicio=None, id_fase=4,
              dicas="== compara se dois valores são iguais.",
              pergunta="Qual operador verifica igualdade entre dois valores em Python?",
              tipo="objetiva", resposta_certa="==",
              resposta_erradas="=,!=,=>"),

    Exercicio(id_exercicio=None, id_fase=4,
              dicas="Lembre-se da ordem de precedência: * antes de +.",
              pergunta="Qual resultado de 3 + 2 * 2 em Python?",
              tipo="objetiva", resposta_certa="7",
              resposta_erradas="10,7 (duplo),9"),

    Exercicio(id_exercicio=None, id_fase=4,
              dicas="Você pode usar int(input()) para receber números.",
              pergunta="Some dois números fornecidos pelo usuário e mostre o resultado.",
              tipo="dissertativa", resposta_certa='a = int(input())\nb = int(input())\nprint(a + b)',
              resposta_erradas=None),

    # Fase 5: if/else
    Exercicio(id_exercicio=None, id_fase=5,
              dicas="Python usa dois-pontos ':' ao final do if.",
              pergunta="Qual destas estruturas é correta?",
              tipo="objetiva", resposta_certa="if x > 10: print(x)",
              resposta_erradas="if x > 10 then print(x),if (x > 10) { print(x) },if x > 10 do print(x)"),

    Exercicio(id_exercicio=None, id_fase=5,
              dicas="Use if/elif/else para criar múltiplas condições.",
              pergunta="Peça um número e diga se é positivo, negativo ou zero.",
              tipo="dissertativa", resposta_certa='n = int(input())\nif n > 0:\n    print("Positivo")\nelif n == 0:\n    print("Zero")\nelse:\n    print("Negativo")',
              resposta_erradas=None),

    # Fase 6: for
    Exercicio(id_exercicio=None, id_fase=6,
              dicas="range(início, fim) vai até fim-1.",
              pergunta="Qual destas opções imprime os números de 1 a 3?",
              tipo="objetiva", resposta_certa="for i in range(1, 4): print(i)",
              resposta_erradas="for i = 1 to 3: print(i),for i in 1..3: print(i),for (i = 1; i <= 3; i++): print(i)"),

    Exercicio(id_exercicio=None, id_fase=6,
              dicas="Repita a ação com for e range.",
              pergunta='Imprima a palavra "Python" cinco vezes usando um laço.',
              tipo="dissertativa", resposta_certa='for i in range(5):\n    print("Python")',
              resposta_erradas=None),

    # Fase 7: while
    Exercicio(id_exercicio=None, id_fase=7,
              dicas="Observe o incremento para evitar loop infinito.",
              pergunta="O que faz este código?\n\nx = 1\nwhile x <= 3:\n    print(x)\n    x += 1",
              tipo="objetiva", resposta_certa="Imprime 1, 2 e 3",
              resposta_erradas="Não faz nada,Imprime infinitamente,Erro de sintaxe"),

    Exercicio(id_exercicio=None, id_fase=7,
              dicas="Repita enquanto a entrada for diferente de zero.",
              pergunta="Peça ao usuário números até ele digitar 0 e some todos.",
              tipo="dissertativa", resposta_certa='total = 0\nn = int(input())\nwhile n != 0:\n    total += n\n    n = int(input())\nprint(total)',
              resposta_erradas=None),

    # Fase 8: funções
    Exercicio(id_exercicio=None, id_fase=8,
              dicas="Use def nome(): para declarar uma função.",
              pergunta="Qual comando define uma função em Python?",
              tipo="objetiva", resposta_certa="def soma(a, b):",
              resposta_erradas="function soma(a, b):,def soma(a, b) end,func soma(a, b):"),

    Exercicio(id_exercicio=None, id_fase=8,
              dicas="Use return para devolver um valor da função.",
              pergunta="Crie uma função que receba dois números e retorne a soma.",
              tipo="dissertativa", resposta_certa="def soma(a, b):\n    return a + b",
              resposta_erradas=None)
]

persistencia = ExercicioPersistenciaImpl()
for ex in exercicios:
    persistencia.salvar(ex)