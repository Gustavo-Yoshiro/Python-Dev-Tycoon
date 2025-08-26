# Intermediario/Content/PythonHeroContent.py
import unicodedata

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _norm(txt: str) -> str:
    if not txt:
        return ""
    t = unicodedata.normalize("NFD", txt)
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return t.lower().strip()

def _q(prompt, ok, *wrong):
    """Monta um item no formato esperado pelo minigame."""
    alts = [{"txt": ok, "ok": True}] + [{"txt": w, "ok": False} for w in wrong]
    return {"prompt": prompt, "alternativas": alts}

# ------------------------------------------------------------
# Pools por tópico — sempre usando só o que já foi visto até ali
# Ordem pedagógica: print → input → variáveis → operadores → if → for → while → funções
# ------------------------------------------------------------
def _pool_print():
    return [
        _q("Imprimir exatamente: Hello",
           "print('Hello')",
           "print(Hello)", "print(\"Hello)", "print('Hello'"),
        _q("Imprimir o número 7 (como número)",
           "print(7)",
           "print('7'+1)", "print('7')", "print(3*3)"),
        _q("Imprimir: Oi, Python!",
           "print('Oi, Python!')",
           "print(Oi, Python!)", "prit('Oi, Python!')", "print('Oi,' 'Python!')"),
        _q("Imprimir aspas: He said \"hi\"",
           "print('He said \"hi\"')",
           "print(\"He said 'hi'\")", "print(He said \"hi\")", "print('He said \"hi')"),
        _q("Imprimir duas linhas",
           "print('Bom dia')\nprint('Boa tarde')",
           "print('Bom dia' 'Boa tarde')", "prit('Bom dia')\nprit('Boa tarde')", "print('Bom dia', 'Boa tarde'')"),
        _q("Imprimir a soma 3+4 (resultado 7)",
           "print(3+4)",
           "print('3+4')", "print(3*4)", "print(7,)"),
    ]

def _pool_input():
    # usa input + print
    return [
        _q("Ler uma linha do usuário em s",
           "s = input()",
           "s = input", "s = input(str)", "input() = s"),
        _q("Ler inteiro para n",
           "n = int(input())",
           "n = input(int())", "n = int(input)", "int = input()"),
        _q("Perguntar nome e imprimir",
           "nome = input('Nome: ')\nprint(nome)",
           "nome = input; print(nome)", "print(input('Nome: ')) = nome", "nome = print(input('Nome: '))"),
        _q("Ler dois inputs separados",
           "a = input()\nb = input()",
           "a, b = input()", "input(); input() = a, b", "a = b = input()"),
        _q("Ler e imprimir direto",
           "print(input())",
           "input(print())", "print = input()", "input(); print()"),
        _q("Ler idade (texto) e mostrar",
           "idade = input('Idade: ')\nprint('Idade:', idade)",
           "idade = input 'Idade:'", "print('Idade:', input)", "print('Idade:' idade)"),
    ]

def _pool_variaveis():
    # usa atribuição + print
    return [
        _q("Guardar 5 em x e imprimir",
           "x = 5\nprint(x)",
           "x == 5\nprint(x)", "x := 5\nprint(x)", "print(x)\nx = 5"),
        _q("Guardar 2.5 em preco e imprimir",
           "preco = 2.5\nprint(preco)",
           "preco = '2.5'\nprint(preco)", "preco = 2,5\nprint(preco)", "print(preco)\npreco = 2.5"),
        _q("Guardar 'Ana' em nome e imprimir",
           "nome = 'Ana'\nprint(nome)",
           "nome : 'Ana'\nprint(nome)", "print('Ana') = nome", "nome = Ana\nprint(nome)"),
        _q("Guardar True em ativo e imprimir",
           "ativo = True\nprint(ativo)",
           "ativo = 'True'\nprint(ativo)", "ativo == True\nprint(ativo)", "print(True) = ativo"),
        _q("Imprimir duas variáveis",
           "x = 3\ny = 'maçã'\nprint(x, y)",
           "x=3; y='maçã'; print(x y)", "print(x)\nprint(y)", "x=3; y='maçã'; print(x+y)"),
        _q("Atribuição e reatribuição",
           "n = 1\nn = 2\nprint(n)",
           "n == 1\nn == 2\nprint(n)", "n = 1,2\nprint(n)", "n = '1'\nn = 2\nprint('n')"),
    ]

def _pool_operadores():
    # usa variáveis + aritméticos/relacionais + print
    return [
        _q("Somar x+y com x=5 e y=2",
           "x = 5\ny = 2\nprint(x + y)",
           "x = 5; y = 2; print(x = y)", "x = 5; y = 2; print(x => y)", "x = 5\ny = 2\nprint(x plus y)"),
        _q("Comparar se 10 é maior que 7",
           "print(10 > 7)",
           "print(10 = 7)", "print(10 => 7)", "print(10 >=< 7)"),
        _q("Resultado de (5+3)*2",
           "print((5 + 3) * 2)",
           "print(5 + 3 * 2)", "print((5 + 3) * 2))", "print(5 + (3 * 2)"),
        _q("Igualdade correta para x e y",
           "x=3\ny=3\nprint(x == y)",
           "x=3; y=3; print(x = y)", "x==3; y==3; print(x == y)", "x=3; y=3; print(x >< y)"),
        _q("Parênteses e soma",
           "a=1\nb=2\nprint(a + (b + 3))",
           "a=1\nb=2\nprint(a + b + )", "a=1; b=2; print(a + (b + 3)", "a=1; b=2; print(a ++ b + 3)"),
        _q("Maior ou igual",
           "x=4\ny=4\nprint(x >= y)",
           "x=4; y=4; print(x => y)", "x=4; y=4; print(x >== y)", "x=4; y=4; print(x = y)"),
    ]

def _pool_if():
    # usa if/elif/else + comparações + print
    return [
        _q("Imprimir 'maior' se idade>=18",
           "idade=18\nif idade>=18:\n    print('maior')\nelse:\n    print('menor')",
           "idade=18\nif idade>=18\n    print('maior')\nelse\n    print('menor')",
           "idade=18\nif idade=>18:\n    print('maior')\nelse:\n    print('menor')",
           "idade=18\nif idade>=18:\nprint('maior')\nelse:\nprint('menor')"),
        _q("if/elif/else válido",
           "n=7\nif n>10:\n    print('alto')\nelif n>5:\n    print('médio')\nelse:\n    print('baixo')",
           "n=7\nif n>10\n    print('alto')\nelif n>5:\n    print('médio')\nelse:\n    print('baixo')",
           "n=7\nif n>10:\n    print('alto')\nelif n>5\n    print('médio')\nelse:\n    print('baixo')",
           "n=7\nelif n>5:\n    print('médio')"),
        _q("if simples correto",
           "x=1\nif x>0:\n    print('ok')",
           "x=1\nif (x>0)\n    print('ok')",
           "x=1\nif x>0: print('ok'", "if x>0: print ok"),
        _q("else correto",
           "flag=False\nif flag:\n    print('sim')\nelse:\n    print('não')",
           "flag=False\nif flag:\n    print('sim')\nelse\n    print('não')",
           "flag=False\nif flag\n    print('sim')\nelse:\n    print('não')",
           "flag=False\nelse:\n    print('não')"),
    ]

def _pool_for():
    # usa for + range/listas + print
    return [
        _q("Imprimir 0..2 (um por linha)",
           "for i in range(3):\n    print(i)",
           "for i in range 3:\n    print(i)", "for(i in range(3)):\n    print(i)", "for i in [3]: print(i)"),
        _q("Loop sobre lista [1,2]",
           "a=[1,2]\nfor x in a:\n    print(x)",
           "a=(1,2)\nfor x in a:\n    print(a)", "for x in [a]:\n    print(x)", "for x in a: print(a[x])"),
        _q("Somar 0..2 em s e imprimir",
           "s=0\nfor i in range(3):\n    s+=i\nprint(s)",
           "s=0\nfor i in range(3):\n    s=s+i\nprint(i)", "for i in range(3): s+=i; print(s)", "s=0; for i in range(3): s+=i"),
        _q("Iterar nas letras de 'Py'",
           "for ch in 'Py':\n    print(ch)",
           "for ch of 'Py':\n    print(ch)", "for 'Py' in ch:\n    print(ch)", "print('Py'[ch])"),
        _q("Usar range com início e fim",
           "for n in range(2,5):\n    print(n)",
           "for n in range 2,5:\n    print(n)", "for n = 2..5:\n    print(n)", "for n in range(2,5) print(n)"),
    ]

def _pool_while():
    # usa while + contador/input + print
    return [
        _q("Contar 0..2 usando while",
           "i=0\nwhile i<3:\n    print(i)\n    i+=1",
           "i=0\nwhile i<3\n    print(i)\n    i+=1", "i=0\nwhile i<3:\n    print(i)\n    i ++", "while i<3:\n    print(i)\n    i+=1"),
        _q("Até digitar 'sair'",
           "txt=''\nwhile txt!='sair':\n    txt = input('> ')\nprint('fim')",
           "txt=''\nwhile txt!='sair'\n    txt = input('> ')\nprint('fim')",
           "while txt!='sair':\n    input('> ')\nprint('fim')",
           "txt=''\nwhile (txt!='sair'):\n    txt = input('> ')\nprint(fim)"),
        _q("De 3 até 1",
           "n=3\nwhile n>0:\n    print(n)\n    n-=1",
           "n=3\nwhile n>0:\n    print(n)\n    n--", "while n>0:\n    n-=1\nprint(n)", "n=3\nwhile n>0:\nprint(n)\nn-=1"),
    ]

def _pool_funcoes():
    # usa def + parâmetros + return + chamada + print
    return [
        _q("Função soma correta",
           "def soma(a,b):\n    return a+b\nprint(soma(2,3))",
           "def soma(a,b)\n    return a+b\nprint(soma(2,3))",
           "def soma: (a,b)\n    return a+b\nprint(soma(2,3))",
           "def soma(a,b):\n    return a+b)\nprint(soma(2,3))"),
        _q("Função eco imprime arg",
           "def eco(s):\n    print(s)\neco('oi')",
           "def eco(s):\n    print s\neco('oi')", "def eco(s)\n    print(s)\neco('oi')", "def eco:\n    print(s)\neco('oi')"),
        _q("Média de dois números",
           "def media(a,b):\n    return (a+b)/2\nprint(media(4,6))",
           "def media(a,b):\n    return a+b/2\nprint(media(4,6))",
           "def media(a,b)\n    return (a+b)/2\nprint(media(4,6))",
           "def media(a,b):\n    return (a+b)/2\nprint(media 4,6)"),
        _q("Chamada que retorna valor",
           "def dobro(x):\n    return 2*x\nr = dobro(5)\nprint(r)",
           "def dobro(x):\n    return 2*x\nprint(r)\nr = dobro(5)",
           "def dobro(x):\n    print(2*x)\nr = dobro(5)\nprint(r)",
           "def dobro(x)\n    return 2*x\nr=dobro(5)"),
    ]

# ------------------------------------------------------------
# Roteador por título (iniciante)
# ------------------------------------------------------------
def get_hero_pool(topic_title: str):
    """
    Retorna uma lista de perguntas/alternativas para o Python Hero
    de acordo com o TÓPICO do iniciante.
    """
    t = _norm(topic_title)

    if "saida de dados" in t or "print" in t:
        return _pool_print()
    if "entrada de dados" in t or "input" in t:
        return _pool_input()
    if "variaveis" in t or "variavel" in t or "tipos simples" in t:
        return _pool_variaveis()
    if "operadores" in t or "relacionais" in t or "aritmeticos" in t:
        return _pool_operadores()
    if "condicionais" in t or "if/else" in t or "if else" in t or "if " in t:
        return _pool_if()
    if "repeticao (for)" in t or " estruturas de repeticao (for" in t or " for)" in t or " for " in t:
        return _pool_for()
    if "repeticao (while)" in t or " estrutura de repeticao (while" in t or " while)" in t or " while " in t:
        return _pool_while()
    if "funcoes" in t or "funções" in t or "funcao" in t or "função" in t:
        return _pool_funcoes()

    # fallback: print
    return _pool_print()
