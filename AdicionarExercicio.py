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

    # Fase 4: Operadores
    Exercicio(id_exercicio=None, id_fase=4,
        dicas="== compara se dois valores são iguais.",
        pergunta="Qual operador verifica igualdade entre dois valores em Python?",
        tipo="objetiva", resposta_certa="==",
        resposta_erradas="=|!=|=>"),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="O operador != verifica se dois valores são diferentes.",
        pergunta="Qual operador é usado para 'diferente de' em Python?",
        tipo="objetiva", resposta_certa="!=",
        resposta_erradas="=/=|==|<>"),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Dica: Primeiro resolve multiplicação/divisão, depois soma/subtração.",
        pergunta="Qual resultado de 3 + 2 * 2 em Python?",
        tipo="objetiva", resposta_certa="7",
        resposta_erradas="10|9|12"),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Você pode usar int(input()) para receber números do usuário.",
        pergunta="Some dois números fornecidos pelo usuário e mostre o resultado.\nDigite o código exatamente como esperado.",
        tipo="dissertativa", resposta_certa='a = int(input())\nb = int(input())\nprint(a + b)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="A ordem dos operadores pode alterar o resultado.",
        pergunta="Mostre o resultado de (5 + 3) * 2 usando print().",
        tipo="dissertativa", resposta_certa='print((5 + 3) * 2)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Arraste os blocos para montar uma expressão que imprima o dobro do valor digitado pelo usuário.",
        pergunta="Monte a expressão para imprimir o dobro do número digitado.",
        tipo="dragdrop",
        resposta_certa="n = int(input())|print(n * 2)",
        resposta_erradas="n = input()|print(n ** 2)|print(n + n)"),


    # Fase 5: If/Else
    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Python usa dois-pontos ':' ao final do if.",
        pergunta="Qual destas estruturas é correta?",
        tipo="objetiva", resposta_certa="if x > 10: print(x)",
        resposta_erradas="if x > 10 then print(x)|if (x > 10) { print(x) }|if x > 10 do print(x)"),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="O comando else cobre todos os casos não tratados por if e elif.",
        pergunta="Como se escreve o bloco else em Python?",
        tipo="objetiva", resposta_certa="else:",
        resposta_erradas="else|else {}|else then:"),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Use if/elif/else para criar múltiplas condições.",
        pergunta="Peça um número e diga se é positivo, negativo ou zero. Escreva o código exato.",
        tipo="dissertativa", resposta_certa='n = int(input())\nif n > 0:\n    print("Positivo")\nelif n == 0:\n    print("Zero")\nelse:\n    print("Negativo")',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Atenção à indentação após if.",
        pergunta="Como imprime 'Maior de idade' se a variável idade for pelo menos 18?",
        tipo="dissertativa", resposta_certa='if idade >= 18:\n    print("Maior de idade")',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Arraste para montar um teste de número par.",
        pergunta="Monte o código que imprime 'Par' se n for par.",
        tipo="dragdrop",
        resposta_certa="if n % 2 == 0:|    print('Par')",
        resposta_erradas="if n % 2 = 0:|print('Par')|if n % 2:|if n // 2:"),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Arraste para montar um teste de número negativo.",
        pergunta="Arraste para montar o teste: se n < 0, imprimir 'Negativo'",
        tipo="dragdrop",
        resposta_certa="if n < 0:|    print('Negativo')",
        resposta_erradas="if n > 0:|print('Negativo')|if n == 0:|if n <= 0:"),


    # Fase 6: For
    Exercicio(id_exercicio=None, id_fase=6,
        dicas="range(início, fim) vai até fim-1.",
        pergunta="Qual destas opções imprime os números de 1 a 3?",
        tipo="objetiva", resposta_certa="for i in range(1, 4): print(i)",
        resposta_erradas="for i = 1 to 3: print(i)|for i in 1..3: print(i)|for (i = 1; i <= 3; i++): print(i)"),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Use for para repetir uma ação várias vezes.",
        pergunta="Qual comando repete 5 vezes?",
        tipo="objetiva", resposta_certa="for i in range(5):",
        resposta_erradas="for i in 5:|for i in range(1,5):|for i = 1 to 5:"),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Repita a ação com for e range.",
        pergunta='Imprima a palavra "Python" cinco vezes usando um laço. Escreva exatamente.',
        tipo="dissertativa", resposta_certa='for i in range(5):\n    print("Python")',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="For permite iterar sobre listas também.",
        pergunta="Imprima todos os elementos da lista numeros = [2, 4, 6]",
        tipo="dissertativa", resposta_certa='numeros = [2, 4, 6]\nfor n in numeros:\n    print(n)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Arraste para montar o for que imprime 0 a 2.",
        pergunta="Monte o for que imprime 0, 1 e 2.",
        tipo="dragdrop",
        resposta_certa="for i in range(3):|    print(i)",
        resposta_erradas="for i in range(1,4):|print(i)|for n in [0,1,2]:"),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Arraste para montar um for sobre uma lista chamada nomes.",
        pergunta="Monte o for para imprimir todos os nomes.",
        tipo="dragdrop",
        resposta_certa="for nome in nomes:|    print(nome)",
        resposta_erradas="for nome in range(nomes):|print(nome)|for n in nomes:"),

    # Fase 7: While
    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Observe o incremento para evitar loop infinito.",
        pergunta="O que faz este código?\n\nx = 1\nwhile x <= 3:\n    print(x)\n    x += 1",
        tipo="objetiva", resposta_certa="Imprime 1, 2 e 3",
        resposta_erradas="Não faz nada|Imprime infinitamente|Erro de sintaxe"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="O comando break interrompe o laço.",
        pergunta="Como sair do laço antes do fim?",
        tipo="objetiva", resposta_certa="break",
        resposta_erradas="stop|end|exit"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Repita enquanto a entrada for diferente de zero.",
        pergunta="Peça ao usuário números até ele digitar 0 e some todos.\nDigite o código exato.",
        tipo="dissertativa", resposta_certa='total = 0\nn = int(input())\nwhile n != 0:\n    total += n\n    n = int(input())\nprint(total)',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="While pode ser usado para contagem crescente.",
        pergunta="Imprima os números de 1 a 5 usando while.",
        tipo="dissertativa", resposta_certa='x = 1\nwhile x <= 5:\n    print(x)\n    x += 1',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Arraste para montar o laço que imprime de 0 a 2.",
        pergunta="Monte um while que imprime 0, 1 e 2.",
        tipo="dragdrop",
        resposta_certa="x = 0\nwhile x < 3:|    print(x)|    x += 1",
        resposta_erradas="x = 1|while x <= 3:|print(x)|x = x + 1"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Arraste para montar um laço que para quando encontra um valor negativo.",
        pergunta="Monte o código: peça números até digitar negativo, e some todos os positivos.",
        tipo="dragdrop",
        resposta_certa="soma = 0|n = int(input())|while n >= 0:|    soma += n|    n = int(input())|print(soma)",
        resposta_erradas="while n > 0:|soma = n|print(n)|if n < 0: break"),


    # Fase 8: Funções
    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Use def nome(): para declarar uma função.",
        pergunta="Qual comando define uma função em Python?",
        tipo="objetiva", resposta_certa="def soma(a, b):",
        resposta_erradas="function soma(a, b):|def soma(a, b) end|func soma(a, b):"),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Uma função pode receber parâmetros e retornar valor.",
        pergunta="Como declarar uma função que retorna o dobro de x?",
        tipo="objetiva", resposta_certa="def dobro(x): return x * 2",
        resposta_erradas="def dobro(x): print(x * 2)|def dobro(): return x * 2|function dobro(x): return x * 2"),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Use return para devolver o valor.",
        pergunta="Crie uma função que receba dois números e retorne a soma. Escreva exatamente.",
        tipo="dissertativa", resposta_certa="def soma(a, b):\n    return a + b",
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Defina uma função que retorna se um número é par.",
        pergunta="Defina uma função que recebe n e retorna True se for par, False caso contrário.",
        tipo="dissertativa", resposta_certa='def eh_par(n):\n    return n % 2 == 0',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Arraste para montar uma função que imprime 'Oi'.",
        pergunta="Monte a função que imprime 'Oi'.",
        tipo="dragdrop",
        resposta_certa="def oi():|    print('Oi')",
        resposta_erradas="def oi:|print('Oi')|def oi()"),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Arraste para montar uma função que retorna o quadrado de x.",
        pergunta="Monte a função que retorna o quadrado de x.",
        tipo="dragdrop",
        resposta_certa="def quadrado(x):|    return x * x",
        resposta_erradas="def quadrado(x):|print(x * x)|return x**2|def quadrado:"),

]

persistencia = ExercicioPersistenciaImpl()
for ex in exercicios:
    persistencia.salvar(ex)
