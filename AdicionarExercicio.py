from Persistencia.Entidade.Exercicio import Exercicio
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl

exercicios = [
    # ========================== FASE 1: print() ==========================
    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Dica: O comando mais usado para exibir valores na tela.",
        pergunta="Qual comando em Python exibe um texto na tela?",
        tipo="objetiva", resposta_certa="print()",
        resposta_erradas="show()|output()|display()"),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Lembre do comando para separar valores.",
        pergunta="Como exibir os valores de x e y, separados por espaço?",
        tipo="objetiva", resposta_certa="print(x, y)",
        resposta_erradas="print(x + y)|show(x, y)|display(x, y)"),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Digite exatamente o comando pedido.",
        pergunta="Dissertativa: Escreva o comando para exibir o texto 'Bem-vindo!' na tela. (Use aspas duplas)",
        tipo="dissertativa", resposta_certa='print("Bem-vindo!")',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Use print() com uma string e um número.",
        pergunta="Dissertativa: Escreva o comando para exibir 'Idade: 21' usando uma string e o número.",
        tipo="dissertativa", resposta_certa='print("Idade:", 21)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Arraste os blocos para montar o comando correto.",
        pergunta="Drag&Drop: Monte o comando para exibir 'Python é legal!' na tela.",
        tipo="dragdrop", resposta_certa='print("Python é legal!")',
        resposta_erradas='print("Python legal!")|print(Python é legal!)|show("Python é legal!")'),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="Monte um print que some dois valores.",
        pergunta="Drag&Drop: Monte um comando para exibir o resultado da soma de 2 + 2.",
        tipo="dragdrop", resposta_certa='print("Resultado:", 2 + 2)',
        resposta_erradas='print("2 + 2")|print(Resultado, 2+2)|show("Resultado", 2 + 2)'),

    # ========================== FASE 2: input() ==========================
    Exercicio(id_exercicio=None, id_fase=2,
        dicas="Dica: Esse comando aguarda o usuário digitar algo.",
        pergunta="Qual comando em Python lê um texto digitado pelo usuário?",
        tipo="objetiva", resposta_certa="input()",
        resposta_erradas="scan()|read()|get()"),

    Exercicio(id_exercicio=None, id_fase=2,
        dicas="A resposta certa usa input().",
        pergunta="Qual alternativa guarda o nome digitado pelo usuário na variável nome?",
        tipo="objetiva", resposta_certa='nome = input("Digite seu nome: ")',
        resposta_erradas='input(nome)|nome == input()|input("Digite seu nome: ") = nome'),

    Exercicio(id_exercicio=None, id_fase=2,
        dicas="Use input e depois print, igual ao exemplo da fase.",
        pergunta="Dissertativa: Escreva um código para pedir ao usuário seu nome e exibir 'Olá, <nome>' (Exatamente como abaixo)\nResposta esperada:\nnome = input(\"Qual seu nome? \")\nprint(\"Olá,\", nome)",
        tipo="dissertativa", resposta_certa='nome = input("Qual seu nome? ")\nprint("Olá,", nome)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=2,
        dicas="Primeiro input, depois print.",
        pergunta="Dissertativa: Escreva um código para pedir o animal favorito e mostrar na tela.",
        tipo="dissertativa", resposta_certa='animal = input("Animal favorito? ")\nprint(animal)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=2,
        dicas="Arraste os blocos para a ordem correta.",
        pergunta="Drag&Drop: Monte o código para pedir a idade do usuário e exibir 'Idade:', idade.",
        tipo="dragdrop", resposta_certa='idade = input("Idade: ")|print("Idade:", idade)',
        resposta_erradas='idade = print("Idade: ")|input("Idade:", idade)|print(idade)'),

    Exercicio(id_exercicio=None, id_fase=2,
        dicas="Arraste para montar: peça dois números e exiba os dois.",
        pergunta="Drag&Drop: Monte o código para ler dois números (a, b) e exibir ambos na tela.",
        tipo="dragdrop", resposta_certa='a = input("A: ")|b = input("B: ")|print(a, b)',
        resposta_erradas='a = print("A: ")|b = print("B: ")|print("a + b")'),

    # ========================== FASE 3: variáveis ==========================
    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Dica: Variável inteira não tem aspas.",
        pergunta="Qual linha cria uma variável inteira chamada idade?",
        tipo="objetiva", resposta_certa="idade = 20",
        resposta_erradas='idade = "20"|int idade = 20|let idade = 20'),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Só a atribuição correta.",
        pergunta="Qual comando cria uma variável chamada cidade com valor 'São Paulo'?",
        tipo="objetiva", resposta_certa="cidade = 'São Paulo'",
        resposta_erradas="cidade == 'São Paulo'|let cidade = 'São Paulo'|cidade := 'São Paulo'"),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Digite igual ao exemplo.",
        pergunta="Dissertativa: Crie uma variável chamada ano e atribua o valor 2025.",
        tipo="dissertativa", resposta_certa="ano = 2025",
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Dica: o nome pode ser qualquer um, mas use o do exemplo.",
        pergunta="Dissertativa: Crie uma variável chamada cor e atribua o valor 'azul'.",
        tipo="dissertativa", resposta_certa="cor = 'azul'",
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Monte a atribuição correta.",
        pergunta="Drag&Drop: Monte o código para criar a variável nota com valor 8.5.",
        tipo="dragdrop", resposta_certa="nota = 8.5",
        resposta_erradas="nota == 8.5|nota := 8.5|let nota = 8.5"),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Blocos embaralhados.",
        pergunta="Drag&Drop: Crie as variáveis x = 2, y = 4 e exiba a soma.",
        tipo="dragdrop", resposta_certa="x = 2|y = 4|print(x + y)",
        resposta_erradas="x == 2|print(x y)|print(2 + 4)"),

    # Fase 4: operadores
    Exercicio(id_exercicio=None, id_fase=4,
              dicas="== compara se dois valores são iguais.",
              pergunta="Qual operador verifica igualdade entre dois valores em Python?",
              tipo="objetiva", resposta_certa="==",
              resposta_erradas="=|!=|=>"),

    Exercicio(id_exercicio=None, id_fase=4,
              dicas="Lembre-se da ordem de precedência: * antes de +.",
              pergunta="Qual resultado de 3 + 2 * 2 em Python?",
              tipo="objetiva", resposta_certa="7",
              resposta_erradas="10|7 (duplo)|9"),

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
              resposta_erradas="if x > 10 then print(x)|if (x > 10) { print(x) }|if x > 10 do print(x)"),

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
              resposta_erradas="for i = 1 to 3: print(i)|for i in 1..3: print(i)|for (i = 1; i <= 3; i++): print(i)"),

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
              resposta_erradas="Não faz nada|Imprime infinitamente|Erro de sintaxe"),

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
              resposta_erradas="function soma(a, b):|def soma(a, b) end|func soma(a, b):"),

    Exercicio(id_exercicio=None, id_fase=8,
              dicas="Use return para devolver um valor da função.",
              pergunta="Crie uma função que receba dois números e retorne a soma.",
              tipo="dissertativa", resposta_certa="def soma(a, b):\n    return a + b",
              resposta_erradas=None)
]

persistencia = ExercicioPersistenciaImpl()
for ex in exercicios:
    persistencia.salvar(ex)
