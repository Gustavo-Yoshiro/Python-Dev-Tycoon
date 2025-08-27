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
# Pools por tópico — INICIANTE
# Ordem: print → input → variáveis → operadores → if → for → while → funções
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
# Pools por tópico — INTERMEDIÁRIO (Fases 9–16)
# ------------------------------------------------------------
def _pool_fstrings_formatacao():
    return [
        _q("Mostrar x com 2 casas decimais usando f-string",
           "x = 3.14159\nprint(f'{x:.2f}')",
           "x = 3.14159\nprint(f'{x:2f}')",
           "x = 3.14159\nprint('{x:.2f}')",
           "x = 3.14159\nprint(format(x, 2))"),
        _q("Interpolar a variável nome corretamente",
           "nome='Ana'\nprint(f'Olá, {nome}')",
           "nome='Ana'\nprint('Olá, {nome}')",
           "nome='Ana'\nprint(f'Olá, {nome')",
           "nome='Ana'\nprint('Olá, {}'.format(nome='Ana'))"),
        _q("Usar chaves literais numa f-string",
           "x=7\nprint(f'{{ok}} {x}')",
           "x=7\nprint(f'{ok} {x}')",
           "x=7\nprint(f'{{ok} {x}')",
           "x=7\nprint('{ok} {}'.format(x))"),
        _q("Alinhar número à direita com largura 5 usando format",
           "print('{:>5}'.format(7))",
           "print('{>5:}'.format(7))",
           "print('{:>5}'.format)",
           "print(f'{7:>5}')  # ok também, mas escolha format aqui"),
        _q("Formatar percentual corretamente",
           "p = 0.275\nprint(f'{p:.0%}')",
           "p = 0.275\nprint(f'{p:%0.0}')",
           "p = 0.275\nprint('{:.0%}'.format())",
           "p = 0.275\nprint('{:p}'.format(p))"),
        _q("Formatar inteiro com zeros à esquerda (largura 4)",
           "n = 7\nprint(f'{n:04d}')",
           "n = 7\nprint(f'{n:04}')",
           "n = 7\nprint('{:04}'.format('7'))",
           "n = 7\nprint('%04d' % '7')"),
    ]

def _pool_metodos_string():
    return [
        _q("Remover espaços das pontas da string s",
           "s = '  py  '\nprint(s.strip())",
           "s = '  py  '\nprint(strip(s))", "s = '  py  '\nprint(s.trim())", "s = 123\nprint(s.strip())"),
        _q("Juntar lista ['a','b'] com vírgula",
           "lst = ['a','b']\nprint(','.join(lst))",
           "lst = ['a','b']\nprint(lst.join(','))",
           "lst = ['a','b']\nprint('-'.join('a','b'))",
           "lst = ['a','b']\nprint(','.join)"),
        _q("Trocar 'b' por 'x' em 'abc'",
           "print('abc'.replace('b','x'))",
           "print('abc'.repl('b','x'))",
           "print(replace('abc','b','x'))",
           "print('abc'.replace('b': 'x'))"),
        _q("Testar prefixo 'py' em 'python'",
           "print('python'.startswith('py'))",
           "print(startswith('python','py'))",
           "print('py' in 'python'[0])",
           "print('python'.startswith)"),
        _q("Dividir 'a-b-c' por '-'",
           "print('a-b-c'.split('-'))",
           "print(split('a-b-c','-'))",
           "print('a-b-c'.split)",
           "print('a-b-c'.split(None, '1'))"),
        _q("Verificar se '123' é número (dígitos)",
           "print('123'.isdigit())",
           "print(isdigit('123'))",
           "print('123'.isnumeric('123'))",
           "print(123.isdigit())"),
    ]

def _pool_listas():
    return [
        _q("Adicionar 3 ao final da lista",
           "l = [1,2]\nl.append(3)",
           "l = [1,2]\nl.add(3)", "l = [1,2]\nappend(l,3)", "l = {1,2}\nl.append(3)"),
        _q("Fazer cópia rasa de l",
            "l = [1,2,3]\nc = l[:]",
            "l = [1,2,3]\nc = l", "l = [1,2,3]\nc = copy(l)", "l = [1,2,3]\nc = list.copy"),
        _q("Ordenar a lista in-place",
           "l=[3,1,2]\nl.sort()",
           "l=[3,1,2]\nsort(l)", "l=[3,1,2]\nprint(sorted=l)", "l=[3,1,2]\nl.sort"),
        _q("Slice dos elementos 1..fim",
           "l=[0,1,2,3]\nprint(l[1:])",
           "l=[0,1,2,3]\nprint(l[1:5:0])",
           "l=[0,1,2,3]\nprint(l[::None])",
           "l=[0,1,2,3]\nprint(l[10])"),
        _q("Estender lista com vários itens",
           "l=[1]\nl.extend([2,3])",
           "l=[1]\nl.append([2,3])  # cria sublista",  # errado no objetivo
           "l=[1]\nl.extend(3)",
           "l=[1]\nl.add(2,3)"),
        _q("Lista reversa sem alterar original",
           "l=[1,2,3]\nr=l[::-1]\nprint(r)",
           "l=[1,2,3]\nr=reversed(l)[:]\nprint(r)",
           "l=[1,2,3]\nl.reverse() e usa como nova",
           "l=[1,2,3]\nprint(l[::0])"),
    ]

def _pool_tuplas():
    return [
        _q("Criar tupla de 1 elemento",
           "t = ('x',)",
           "t = ('x')", "t = tuple['x']", "t = ('x', 'y',)[0]"),
        _q("Desempacotar valores",
           "a,b = (1,2)",
           "a,b = 1,2,3", "a = b = (1,2)", "a b = (1,2)"),
        _q("Acessar primeiro item de tupla",
           "t=(1,2,3)\nprint(t[0])",
           "t=(1,2,3)\nprint(t(0))", "t=(1,2,3)\nprint(t[0]=1)", "t=(1,2,3)\nprint(t.pop())"),
        _q("Converter lista em tupla",
           "t = tuple([1,2])",
           "t = (list(1,2))", "t = tuple{1,2}", "t = tuple[1,2]"),
        _q("Entender imutabilidade",
           "t=(1,2)\n# não alterar itens",
           "t=(1,2)\nt[0]=9",
           "t=(1,2)\nt.append(3)",
           "t=(1,2)\nt.extend((3,))"),
    ]

def _pool_sets():
    return [
        _q("Criar set vazio corretamente",
           "s = set()",
           "s = {}", "s = []", "s = set{}"),
        _q("Adicionar elemento ao set",
           "s={1}\ns.add(2)",
           "s={1}\ns.append(2)", "s={1}\ns.add(2,3)", "s={1}\ns.push(2)"),
        _q("União entre dois sets",
           "a={1,2}; b={2,3}\nprint(a | b)",
           "a={1,2}; b={2,3}\nprint(a + b)",
           "a={1,2}; b={2,3}\nprint(union(a,b))",
           "a={1,2}; b={2,3}\nprint(a || b)"),
        _q("Remover sem erro se não existir",
           "s={1}\ns.discard(9)",
           "s={1}\ns.remove(9)",
           "s={1}\ns.pop(9)",
           "s={1}\ndiscard(s,9)"),
        _q("Evitar itens inhasháveis",
           "s = {1, (2,3)}  # ok",
           "s = {[1,2]}", "s = {{1}}", "s = {set([1])}"),
        _q("Testar pertinência",
           "s={1,2}\nprint(2 in s)",
           "s={1,2}\nprint(in(2,s))",
           "s={1,2}\nprint(s.has(2))",
           "s={1,2}\nprint(2 of s)"),
    ]

def _pool_dicts():
    return [
        _q("Acessar chave 'x' com segurança e default 0",
           "d={'x':1}\nprint(d.get('x',0))",
           "d={'x':1}\nprint(d['x',0])",
           "d={'x':1}\nprint(d.value('x',0))",
           "d={'x':1}\nprint(get(d,'x',0))"),
        _q("Atualizar valor de uma chave",
           "d={'idade':20}\nd['idade']=21",
           "d={'idade':20}\nd.idade=21",
           "d={'idade':20}\nupdate(d,{'idade':21})",
           "d={'idade':20}\nd['idade']->21"),
        _q("Iterar por itens k,v",
           "d={'a':1,'b':2}\nfor k,v in d.items():\n    print(k,v)",
           "d={'a':1,'b':2}\nfor k,v in items(d):\n    print(k,v)",
           "d={'a':1,'b':2}\nfor (k:v) in d:\n    print(k,v)",
           "d={'a':1,'b':2}\nfor k in d.items():\n    print(k,v)"),
        _q("Unir dicionários (3.9+)",
           "d1={'a':1}; d2={'b':2}\nprint(d1 | d2)",
           "print(merge(d1,d2))",
           "print(dict.add(d1,d2))",
           "print(d1 + d2)"),
        _q("Evitar KeyError em acesso inexistente",
           "d={}\nprint(d.get('k'))",
           "d={}\nprint(d['k'])",
           "d={}\nprint(d.k)",
           "d={}\nprint(d['k'] or None)"),
        _q("Chaves devem ser imutáveis",
           "d = {(1,2): 'ok'}",
           "d = {['a']: 1}",
           "d = {{1}: 2}",
           "d = {set(): 3}"),
    ]

def _pool_list_comprehensions():
    return [
        _q("Quadrados de 0..4 com list comprehension",
           "squares = [i*i for i in range(5)]",
           "squares = [i**2: i in range(5)]",
           "squares = (i*i for i in range(5))  # generator",
           "squares = {i*i for i in range(5)}  # set"),
        _q("Filtrar pares de 0..9",
           "pares = [i for i in range(10) if i%2==0]",
           "[i if i%2==0 for i in range(10)]",
           "[i for i in 10 if i%2==0]",
           "[i for i in range(10) if]"),
        _q("Flatten de lista de listas",
           "flat = [x for row in [[1,2],[3]] for x in row]",
           "flat = [for x in row for row in m]",
           "flat = [x for x in row for row in m]",
           "flat = [x for row in [[1,2],[3]] x in row]"),
        _q("Comprehension com if-else na expressão",
           "pos = [x if x>0 else 0 for x in a]",
           "[x for x in a if x>0 else 0]",
           "pos = [if x>0 then x else 0 for x in a]",
           "pos = [x else 0 if x>0 for x in a]"),
        _q("Comprehension de set (diferença para lista)",
           "s = {x for x in [1,1,2]}",
           "s = [x for x in {1,1,2}]",
           "s = (x for x in [1,1,2])",
           "s = {{x} for x in [1,1,2]}"),
        _q("Usar enumerate em comprehension",
           "idxs = [i for i,_ in enumerate(a)]",
           "idxs = [enumerate(a)]",
           "idxs = [i,_ in enumerate(a)]",
           "idxs = [for i,_ in enumerate(a)]"),
    ]

def _pool_tratamento_erros():
    return [
        _q("Capturar uma ZeroDivisionError corretamente",
           "try:\n    x = 1/0\nexcept ZeroDivisionError:\n    print('erro')",
           "try:\n    x = 1/0\ncatch ZeroDivisionError:\n    print('erro')",
           "try:\n    x = 1/0\nexcept:\nprint('erro')",
           "try:\n    x = 1/0\nexcept ZeroDivisionError as:\n    print('erro')"),
        _q("Usar finally que sempre executa",
           "try:\n    f()\nfinally:\n    print('sempre')",
           "try:\n    f()\nfinally\n    print('sempre')",
           "try:\n    f()\nfinal:\n    print('sempre')",
           "try:\n    f()\nelse:\n    print('sempre')"),
        _q("Levantar exceção corretamente",
           "raise ValueError('msg')",
           "raise('msg')",
           "throw ValueError('msg')",
           "raise NotAnError('msg')"),
        _q("Captura genérica com apelido (cuidado)",
           "try:\n    f()\nexcept Exception as e:\n    print(e)",
           "try:\n    f()\nexcept e:\n    print(e)",
           "try:\n    f()\nexcept(Exception):\nprint(e)",
           "try:\n    f()\ncatch Exception as e:\n    print(e)"),
        _q("Bloco else quando não ocorre exceção",
           "try:\n    x = int('3')\nexcept ValueError:\n    x = 0\nelse:\n    print('ok')",
           "try:\n    x = int('3')\nelse:\n    print('ok')",
           "try:\n    x = int('a')\nelse:\n    print('ok')",
           "try:\n    x = int('3')\nexcept:\n    pass\nelse print('ok')"),
        _q("Re-lançar exceção atual dentro de except",
           "try:\n    f()\nexcept:\n    raise",
           "try:\n    f()\nexcept:\n    raise e",
           "try:\n    f()\nexcept e:\n    raise e",
           "try:\n    f()\ncatch:\n    raise"),
    ]

# ------------------------------------------------------------
# Roteador — nomes EXATOS normalizados (mesmo padrão da Cobrinha/BugSquash)
# ------------------------------------------------------------
def get_hero_pool(topic_title: str):
    """
    Retorna a lista de perguntas/alternativas do Python Hero
    de acordo com o TÓPICO (iniciante + intermediário).
    """
    t = _norm(topic_title)

    ROUTER = {
        # Iniciante
        _norm("Saída de dados com print()"): _pool_print,
        _norm("Entrada de dados com input()"): _pool_input,
        _norm("Variáveis e Tipos Simples"): _pool_variaveis,
        _norm("Operadores Aritméticos e Relacionais"): _pool_operadores,
        _norm("Estruturas Condicionais (if/else)"): _pool_if,
        _norm("Estruturas de Repetição (for)"): _pool_for,
        _norm("Estrutura de Repetição (while)"): _pool_while,
        _norm("Funções Simples"): _pool_funcoes,

        # Intermediário (Fases 9–16)
        _norm("f-strings e formatação"): _pool_fstrings_formatacao,
        _norm("Métodos de string"): _pool_metodos_string,
        _norm("Listas (métodos e slicing)"): _pool_listas,
        _norm("Tuplas e imutabilidade"): _pool_tuplas,
        _norm("Conjuntos (set)"): _pool_sets,
        _norm("Dicionários"): _pool_dicts,
        _norm("List Comprehensions"): _pool_list_comprehensions,
        _norm("Tratamento de Erros"): _pool_tratamento_erros,
    }

    fn = ROUTER.get(t)
    if fn:
        return fn()
    # fallback: print
    return _pool_print()
