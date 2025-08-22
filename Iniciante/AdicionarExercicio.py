from Iniciante.Persistencia.Entidade.Exercicio import Exercicio
from Iniciante.Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl

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
        dicas="Use o comando print para mostrar a mensagem.",
        pergunta="Dissertativa: Escreva o código Python que imprime na tela: Hello World!",
        tipo="dissertativa", resposta_certa='Hello World!',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=1,
        dicas="A saída deve conter o texto pedido.",
        pergunta="Dissertativa: Escreva um código que exibe: Python é divertido!",
        tipo="dissertativa", resposta_certa='Python é divertido!',
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

    Exercicio(
        id_exercicio=None, id_fase=2,
        dicas="Use input() para ler o nome do usuário e depois imprima Olá, <nome>. Considere que o usuário digita Ana.",
        pergunta="Dissertativa: Peça ao usuário que digite seu nome usando input() e depois imprima: Olá, <nome>. Considere que o usuário digita Ana. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa",
        resposta_certa='Olá, Ana',
        resposta_erradas=None,
        entrada_teste='Ana'
    ),

    Exercicio(
        id_exercicio=None, id_fase=2,
        dicas="Use input() para ler a cor favorita do usuário e depois imprima: Sua cor favorita é <cor>. Considere que o usuário digita azul.",
        pergunta="Dissertativa: Peça ao usuário que digite sua cor favorita usando input() e imprima: Sua cor favorita é <cor>. Considere que o usuário digita azul. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa",
        resposta_certa='Sua cor favorita é azul',
        resposta_erradas=None,
        entrada_teste='azul'
    ),

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
        dicas="Crie a variável e exiba seu valor.",
        pergunta="Dissertativa: Crie uma variável chamada ano, atribua o valor 2025 e mostre o valor dela na tela.",
        tipo="dissertativa", resposta_certa="2025",
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=3,
        dicas="Crie a variável com o valor exato e exiba.",
        pergunta="Dissertativa: Crie uma variável chamada cor e atribua o valor 'azul'. Depois, mostre esse valor na tela.",
        tipo="dissertativa", resposta_certa="azul",
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

    # ========================== FASE 4: Operadores ==========================
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
        dicas="Primeiro resolve multiplicação/divisão, depois soma/subtração.",
        pergunta="Qual o resultado de 3 + 2 * 2 em Python?",
        tipo="objetiva", resposta_certa="7",
        resposta_erradas="10|9|12"),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Use dois input() para receber os números.",
        pergunta="Dissertativa: Peça dois números ao usuário e imprima a soma deles. Considere que o usuário digita 2 e depois 5. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='7',
        resposta_erradas=None,
        entrada_teste='2\n5'
    ),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Use parênteses para alterar a ordem das operações.",
        pergunta="Dissertativa: Escreva um código que imprima o resultado de (5 + 3) * 2.",
        tipo="dissertativa", resposta_certa='16',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=4,
        dicas="Arraste os blocos para montar o comando correto.",
        pergunta="Drag&Drop: Monte o código para ler um número e imprimir o dobro desse valor.",
        tipo="dragdrop",
        resposta_certa="n = int(input())|print(n * 2)",
        resposta_erradas="n = input()|print(n ** 2)|print(n + n)"),

    # ========================== FASE 5: If/Else ==========================
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
        dicas="Use if, elif e else para testar todos os casos.",
        pergunta="Dissertativa: Peça um número ao usuário e imprima 'Positivo' se for maior que zero, 'Zero' se for igual a zero ou 'Negativo' se for menor que zero. Considere que o usuário digita -3. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='Negativo',
        resposta_erradas=None,
        entrada_teste='-3'
    ),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Teste se idade é maior ou igual a 18.",
        pergunta="Dissertativa: Peça a idade do usuário e imprima 'Maior de idade' se for pelo menos 18. Considere que o usuário digita 20. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='Maior de idade',
        resposta_erradas=None,
        entrada_teste='20'
    ),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Arraste para montar o teste de número par.",
        pergunta="Drag&Drop: Monte o código que imprime 'Par' se n for par.",
        tipo="dragdrop",
        resposta_certa="if n % 2 == 0:|    print('Par')",
        resposta_erradas="if n % 2 = 0:|print('Par')|if n % 2:|if n // 2:"),

    Exercicio(id_exercicio=None, id_fase=5,
        dicas="Arraste para montar o teste de número negativo.",
        pergunta="Drag&Drop: Monte o código para imprimir 'Negativo' se n for menor que zero.",
        tipo="dragdrop",
        resposta_certa="if n < 0:|    print('Negativo')",
        resposta_erradas="if n > 0:|print('Negativo')|if n == 0:|if n <= 0:"),

    # ========================== FASE 6: For ==========================
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
        dicas="Use um laço for para resolver.",
        pergunta="Dissertativa: Usando um laço for, imprima os números de 1 até 5, um em cada linha.",
        tipo="dissertativa", resposta_certa='1\n2\n3\n4\n5',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Use o for para percorrer todos os itens.",
        pergunta="Dissertativa: Dada a lista numeros = [2, 4, 6], imprima todos os elementos, um por linha.",
        tipo="dissertativa", resposta_certa='2\n4\n6',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Arraste para montar o for que imprime 0, 1 e 2.",
        pergunta="Drag&Drop: Monte o for que imprime 0, 1 e 2.",
        tipo="dragdrop",
        resposta_certa="for i in range(3):|    print(i)",
        resposta_erradas="for i in range(1,4):|print(i)|for n in [0,1,2]:"),

    Exercicio(id_exercicio=None, id_fase=6,
        dicas="Arraste para montar um for sobre uma lista chamada nomes.",
        pergunta="Drag&Drop: Monte o for para imprimir todos os nomes da lista nomes.",
        tipo="dragdrop",
        resposta_certa="for nome in nomes:|    print(nome)",
        resposta_erradas="for nome in range(nomes):|print(nome)|for n in nomes:"),

    # ========================== FASE 7: While ==========================
    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Observe o incremento para evitar loop infinito.",
        pergunta="O que faz este código? x = 1 while x <= 3: print(x) x += 1",
        tipo="objetiva", resposta_certa="Imprime 1, 2 e 3",
        resposta_erradas="Não faz nada|Imprime infinitamente|Erro de sintaxe"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="O comando break interrompe o laço.",
        pergunta="Como sair do laço antes do fim?",
        tipo="objetiva", resposta_certa="break",
        resposta_erradas="stop|end|exit"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Repita até digitar 0.",
        pergunta="Dissertativa: Peça números ao usuário até ele digitar 0 e mostre a soma total. Considere que o usuário digita 5, depois 3 e depois 0. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='8',
        resposta_erradas=None,
        entrada_teste='5\n3\n0'
    ),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Faça um contador crescente.",
        pergunta="Dissertativa: Usando while, imprima os números de 1 até 5, um em cada linha.",
        tipo="dissertativa", resposta_certa='1\n2\n3\n4\n5',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Arraste para montar o laço que imprime de 0 a 2.",
        pergunta="Drag&Drop: Monte um while que imprime 0, 1 e 2.",
        tipo="dragdrop",
        resposta_certa="x = 0\nwhile x < 3:|    print(x)|    x += 1",
        resposta_erradas="x = 1|while x <= 3:|print(x)|x = x + 1"),

    Exercicio(id_exercicio=None, id_fase=7,
        dicas="Arraste para montar um laço que soma positivos até um negativo.",
        pergunta="Drag&Drop: Monte o código: peça números até digitar um negativo, e some todos os positivos. Considere que o usuário digita 2, 4, -1.",
        tipo="dragdrop",
        resposta_certa="soma = 0|n = int(input())|while n >= 0:|    soma += n|    n = int(input())|print(soma)",
        resposta_erradas="while n > 0:|soma = n|print(n)|if n < 0: break"),

    # ========================== FASE 8: Funções ==========================
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
        pergunta="Dissertativa: Crie uma função que recebe dois números e imprime a soma deles. Considere que os números passados são 3 e 4. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='7',
        resposta_erradas=None,
        entrada_teste='3\n4'
    ),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Defina uma função que retorna se um número é par.",
        pergunta="Dissertativa: Crie uma função que recebe um número e imprime True se for par, ou False caso contrário. Considere que o número passado é 4. Use input() sem texto dentro dos parênteses.",
        tipo="dissertativa", resposta_certa='True',
        resposta_erradas=None,
        entrada_teste='4'
    ),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Arraste para montar uma função que imprime 'Oi'.",
        pergunta="Drag&Drop: Monte a função que imprime 'Oi'.",
        tipo="dragdrop",
        resposta_certa="def oi():|    print('Oi')",
        resposta_erradas="def oi:|print('Oi')|def oi()"),

    Exercicio(id_exercicio=None, id_fase=8,
        dicas="Arraste para montar uma função que retorna o quadrado de x.",
        pergunta="Drag&Drop: Monte a função que retorna o quadrado de x.",
        tipo="dragdrop",
        resposta_certa="def quadrado(x):|    return x * x",
        resposta_erradas="def quadrado(x):|print(x * x)|return x**2|def quadrado:"),
]

persistencia = ExercicioPersistenciaImpl()
for ex in exercicios:
    persistencia.salvar(ex)
