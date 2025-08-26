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

# ------------------------------------------------------------
# ROTEADOR POR TÍTULO (INICIANTE)
# ------------------------------------------------------------
def get_cobra_content(topic_title: str):
    """
    Retorna (sequencia, distratores_com_why)
      - sequencia: [str, ...]
      - distratores_com_why: [{"txt": str, "why": str}, ...]
    """
    t = _norm(topic_title)

    if "saida de dados" in t or "print" in t:
        return _content_print()
    if "entrada de dados" in t or "input" in t:
        return _content_input()
    if "variaveis" in t or "variavel" in t or "tipos simples" in t:
        return _content_variaveis()
    if "operadores" in t or "relacionais" in t or "aritmeticos" in t:
        return _content_operadores()
    if "condicionais" in t or "if/else" in t or "if else" in t or " if " in t or t.startswith("if"):
        return _content_if()
    if "repeticao (for)" in t or " for)" in t or " for " in t:
        return _content_for()
    if "repeticao (while)" in t or " while)" in t or " while " in t:
        return _content_while()
    if "funcoes" in t or "funções" in t or "funcao" in t or "função" in t:
        return _content_funcoes()

    return _content_print()
