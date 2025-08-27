# Intermediario/Content/CobraContent.py
import random
import unicodedata

# ------------------------------------------------------------
# Normalização básica (remove acento e baixa)
# ------------------------------------------------------------
def _norm(txt: str) -> str:
    if not txt:
        return ""
    t = unicodedata.normalize("NFD", txt)
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return t.lower().strip()

# helper para distrator com explicação
def _d(txt, why): 
    return {"txt": str(txt), "why": str(why)}

# ------------------------------------------------------------
# Pequenas pools para variar um pouco as sequências
# (mantém tudo simples e dentro do conteúdo já estudado)
# ------------------------------------------------------------
_NAMES = ["x", "y", "z", "n", "a", "b"]
_TXTS  = ["Olá", "Bem-vindo", "Python", "Dev Tycoon", "Oi", "Hello"]
_NUMS  = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def _pick2(seq):
    a, b = random.sample(seq, 2)
    return a, b

def _ok(seq, dist):
    # seq = lista de strings (passos corretos)
    # dist = lista de dicts {"txt": str, "why": str}
    seq = [str(s) for s in seq if s and str(s).strip()]
    dist2 = []
    for d in dist:
        if isinstance(d, dict):
            txt = str(d.get("txt","")).strip()
            why = str(d.get("why","")).strip()
            if txt:
                dist2.append({"txt": txt, "why": why or "—"})
        else:
            # aceita tupla/lista (txt, why)
            try:
                txt = str(d[0]).strip(); why = str(d[1]).strip()
                if txt:
                    dist2.append({"txt": txt, "why": why or "—"})
            except Exception:
                pass
    return seq, dist2

# ------------------------------------------------------------
# MAPEAMENTO — INICIANTE (com why nos distratores)
# ------------------------------------------------------------
def _content_print():
    a, b = _pick2(_NUMS)
    t1 = random.choice(_TXTS)
    seq = [
        f"print('{t1}')",
        f"print({a}+{b})",
        "print('Fim')",
    ]
    dist = [
        _d("prit('Olá')",            "Função correta é print()."),
        _d("print(Olá)",             "Strings precisam de aspas."),
        _d("print('Ola)",            "Aspas não fechadas."),
        _d("printf('Hello')",        "printf() não existe em Python."),
        _d("print('7'+1)",           "Não misture str com int."),
        _d("print ('x') )",          "Parêntese extra."),
    ]
    return _ok(seq, dist)

def _content_input():
    name = random.choice(_NAMES)
    ask  = random.choice(["Nome", "Cidade", "Curso"])
    seq = [
        f"{name} = input('{ask}: ')",
        f"print({name})",
        "print('Pronto')",
    ]
    dist = [
        _d(f"{name} = input '{ask}: '", "Faltam parênteses em input()."),
        _d("imput('Digite: ')",         "input() escrito errado."),
        _d(f"print({name}) )",          "Parêntese extra."),
        _d(f"print({name}+1)",          "Concatenação str + int."),
        _d("input(print('x'))",         "Chamada aninhada desnecessária."),
    ]
    return _ok(seq, dist)

def _content_variaveis():
    name1, name2 = _pick2(_NAMES)
    a, b = _pick2(_NUMS)
    seq = [
        f"{name1} = {a}",
        f"{name2} = '{random.choice(_TXTS)}'",
        f"print({name1})",
    ]
    dist = [
        _d(f"{name1} == {a}",          "Comparação (==) não faz atribuição."),
        _d(f"{name2} = {a}+ '{b}'",    "Mistura int e str."),
        _d(f"print({name1}",           "Parêntese não fechado."),
        _d(f"{name1} := {a}",          "':=' não substitui '=' nessa forma."),
        _d(f"{name2} =+ {name1}",      "Operador invertido; seria '+='."),
        _d("print(z)",                 "Variável z não foi definida."),
    ]
    return _ok(seq, dist)

def _content_operadores():
    a, b = _pick2(_NUMS)
    seq = [
        f"x = {a}",
        f"y = {b}",
        "print(x + y)",
        "print(x >= y)",
    ]
    dist = [
        _d("x == 5",            "Expressão solta; não imprime nada."),
        _d("y = '3' + 2",       "Mistura str e int."),
        _d("print(x => y)",     "Operador inválido: use '>='."),
        _d("print(x = y)",      "Use '==' para comparar."),
        _d("print(x >== y)",    "Operador inválido."),
        _d("print(x > )",       "Falta operando."),
    ]
    return _ok(seq, dist)

def _content_if():
    a, b = _pick2(_NUMS)
    seq = [
        f"idade = {a + b}",
        "if idade >= 18:",
        "print('maior')",
        "else:",
        "print('menor')",
    ]
    dist = [
        _d("if idade >= 18",    "Falta ':' no if."),
        _d("if idade => 18:",   "Operador inválido (use '>=')."),
        _d("print 'maior'",     "print() precisa de parênteses."),
        _d("else",              "Falta ':' no else."),
        _d("iff idade >= 18:",  "Palavra-chave errada (iff)."),
    ]
    return _ok(seq, dist)

def _content_for():
    seq = [
        "for i in range(3):",
        "print(i)",
        "print('FIM')",
    ]
    dist = [
        _d("for i in range 3:",     "Faltam parênteses em range()."),
        _d("for i = 0..2:",         "Sintaxe não-Python."),
        _d("for(i in range(3)):",   "Mistura com C."),
        _d("print i",               "print() precisa de parênteses."),
        _d("for i in range(3)",     "Falta ':' no for."),
    ]
    return _ok(seq, dist)

def _content_while():
    seq = [
        "i = 0",
        "while i < 3:",
        "print(i)",
        "i += 1",
    ]
    dist = [
        _d("while i < 3",    "Falta ':' no while."),
        _d("i = i + '1'",    "Mistura int e str."),
        _d("print(i))",      "Parêntese extra."),
        _d("i ++",           "Não existe operador ++ em Python."),
        _d("whille i < 3:",  "Palavra-chave errada."),
    ]
    return _ok(seq, dist)

def _content_funcoes():
    a, b = _pick2(_NUMS)
    seq = [
        "def soma(a, b):",
        "return a + b",
        f"print(soma({a}, {b}))",
    ]
    dist = [
        _d("def soma(a, b)",     "Falta ':' após a assinatura da função."),
        _d("return a + b)",      "Parêntese extra."),
        _d("print soma(2,3)",    "Faltam parênteses na chamada."),
        _d("def soma: (a,b)",    "Sintaxe inválida."),
        _d("retun a+b",          "'return' escrito errado."),
    ]
    return _ok(seq, dist)

# ===================== NOVOS TÓPICOS (Fases 9–16) =====================

def _content_fstrings_formatacao():
    nome = random.choice(["Ana", "Joao", "Py"])
    seq = [
        f"nome = '{nome}'",
        "x = 3.14159",
        "print(f'Olá, {nome} {x:.2f}')",
    ]
    dist = [
        _d("print(f'Olá, {nome')", "Chave não fechada em f-string."),
        _d("print('{nome}')", "Sem o prefixo f: vira literal."),
        _d("print(f'{x:2f}')", "Especificador inválido (use :.2f)."),
        _d("print('Olá, {}'.format())", "format() sem argumento."),
        _d("print('{:d}'.format('3'))", "Tipo errado para {:d}."),
        _d("formt('x={}'.format(1))", "format() escrito errado."),
    ]
    return _ok(seq, dist)

def _content_metodos_string():
    seq = [
        "s = '  Python  '",
        "s = s.strip()",
        "print(s.upper())",
    ]
    dist = [
        _d("s = 123; s.lower()", "Método de string em int."),
        _d("print('py'.upper)", "Faltou chamar: upper()."),
        _d("['a','b'].join('-')", "join é de string: '-'.join(lista)."),
        _d("'-'.join('a','b')", "join recebe 1 iterável, não 2 args."),
        _d("print('abc'.repl('b','x'))", "Método inexistente: replace()."),
    ]
    return _ok(seq, dist)

def _content_listas():
    a, b = _pick2(_NUMS)
    seq = [
        f"l = [{a}, {b}, 3]",
        "l.append(4)",
        "print(l[1:])",
    ]
    dist = [
        _d("l = {}; l.append(1)", "{} cria dict, não lista."),
        _d("l.add(2)", "Lista não tem add()."),
        _d("print(l[1:5:0])", "step=0 é inválido."),
        _d("print(l[10])", "Provável IndexError."),
        _d("extend(l, [1])", "extend é método: l.extend([1])."),
    ]
    return _ok(seq, dist)

def _content_tuplas():
    seq = [
        "t = (1, 2)",
        "a, b = t",
        "print(a)",
    ]
    dist = [
        _d("t = (1)", "(1) é int; para tupla use (1,)."),
        _d("t[0] = 9", "Tuplas são imutáveis."),
        _d("t.append(3)", "Tupla não tem append()."),
        _d("a, b = (1,2,3)", "Tamanhos diferentes no desempacote."),
    ]
    return _ok(seq, dist)

def _content_sets():
    seq = [
        "s = {1, 2}",
        "s.add(3)",
        "print(2 in s)",
    ]
    dist = [
        _d("s = {}; s.add(1)", "{} é dict; use set()."),
        _d("s = set(); s.append(1)", "Set não tem append()."),
        _d("s = {1,2}; s.remove(3)", "remove erra se não existir (use discard)."),
        _d("s = {{1}}", "set dentro de set é inhashável."),
        _d("s = {[1,2]}", "Lista é inhashável como chave de set."),
        _d("{1,2} + {3}", "Use união com |, não +."),
    ]
    return _ok(seq, dist)

def _content_dicts():
    seq = [
        "d = {'n': 1}",
        "d['n'] = 2",
        "print(d.get('x', 0))",
    ]
    dist = [
        _d("print(d.x)", "Acesso por atributo não lê chave."),
        _d("d = [('a',1)]; d['a']", "Lista não indexa por chave string."),
        _d("print({'a':1}['b'])", "KeyError provável."),
        _d("d = {['a']:1}", "Lista é inhashável como chave."),
        _d("{1:'a',1:'b'}", "Chave duplicada sobrescreve anterior."),
    ]
    return _ok(seq, dist)

def _content_list_comprehensions():
    seq = [
        "nums = [1, 2, 3]",
        "quad = [n*n for n in nums]",
        "print(quad)",
    ]
    dist = [
        _d("[n for n in range(3) if]", "if sem condição é inválido."),
        _d("[x for in range(3)]", "Faltou variável antes de in."),
        _d("[x for x range(3)]", "Faltou 'in'."),
        _d("{x for x in [1,1,2]}", "Isto cria set, não lista."),
        _d("(x for x in [1,2])", "Isto é generator, não lista."),
        _d("[n* for n in range(3)]", "Expressão incompleta antes do for."),
    ]
    return _ok(seq, dist)

def _content_tratamento_erros():
    seq = [
        "try:",
        "x = 1/0",
        "except ZeroDivisionError:",
        "print('erro')",
        "finally:",
        "print('fim')",
    ]
    dist = [
        _d("try: pass; catch Exception: pass", "Não existe catch em Python."),
        _d("try: x=1; except e: print(e)", "Use 'except Tipo as e'."),
        _d("try: pass; finally print('x')", "Falta ':' após finally."),
        _d("raise NotAnError('x')", "Classe de exceção não definida."),
        _d("except ValueError, e:", "Sintaxe do Python 2; use 'as e'."),
    ]
    return _ok(seq, dist)

# ------------------------------------------------------------
# ROTEADOR POR TÍTULO (INICIANTE)
# ------------------------------------------------------------
def get_cobra_content(topic_title: str):
    t = _norm(topic_title)  # minúsculo + sem acento

    ROUTER = {
        # ----- EXISTENTES -----
        "saida de dados com print()": _content_print,
        "entrada de dados com input()": _content_input,
        "variaveis e tipos simples": _content_variaveis,
        "operadores aritmeticos e relacionais": _content_operadores,
        "estruturas condicionais (if/else)": _content_if,
        "estruturas de repeticao (for)": _content_for,
        "estrutura de repeticao (while)": _content_while,
        "funcoes simples": _content_funcoes,

        # ----- Fases 9–16 -----
        "f-strings e formatacao": _content_fstrings_formatacao,
        "metodos de string": _content_metodos_string,
        "listas (metodos e slicing)": _content_listas,
        "tuplas e imutabilidade": _content_tuplas,
        "conjuntos (set)": _content_sets,
        "dicionarios": _content_dicts,
        "list comprehensions": _content_list_comprehensions,
        "tratamento de erros": _content_tratamento_erros,
    }

    fn = ROUTER.get(t)
    if fn:
        return fn()
    return _content_print()  # fallback

