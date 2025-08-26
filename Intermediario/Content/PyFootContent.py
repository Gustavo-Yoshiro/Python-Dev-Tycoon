import random
import unicodedata
from typing import List, Dict, Tuple

# Cada pergunta:
# {
#   "prompt": str,
#   "opts": [str, str, str],
#   "correct": int,   # 0/1/2
#   "why": [str, str, str]
# }

Row = Dict[str, str]  # {"code": str, "bug": "0|1", "why": str}

# -------------------------- Utils --------------------------

def _norm(txt: str) -> str:
    if not txt:
        return ""
    t = unicodedata.normalize("NFD", txt)
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return t.lower().strip()

def _row(code: str, bug: bool, why: str = "") -> Row:
    return {"code": code, "bug": "1" if bug else "0", "why": why or ("OK" if not bug else "Bug")}

def _pick(seq, k):
    if k >= len(seq):
        return list(seq)
    return random.sample(seq, k)

# -------------------------- Pools (robustos) --------------------------

def _pool_print() -> Tuple[List[Row], str]:
    hint = "print(): parênteses/aspas corretos; evite misturar str com int."
    pool = [
        _row("print('Olá, mundo!')", False, "Sintaxe correta."),
        _row("print(1+2)", False, "Expressão válida."),
        _row("print('Fim')", False, "OK."),
        _row("print('x', 3)", False, "Vários argumentos."),
        _row("print('7' * 2)", False, "Repetição de string."),
        _row("prit('Olá')", True, "Função correta é print()."),
        _row("printf('Oi')", True, "printf() não existe em Python."),
        _row("print(Olá)", True, "Strings precisam de aspas."),
        _row("print('7'+1)", True, "Mistura str com int."),
        _row("print ('x') )", True, "Parêntese extra."),
        _row("print('Ola)", True, "Aspas não fechadas."),
    ]
    return pool, hint

def _pool_input() -> Tuple[List[Row], str]:
    hint = "input(): sempre com parênteses; prompt em aspas."
    pool = [
        _row("nome = input('Nome: ')", False, "OK."),
        _row("x = input('Digite um número: ')", False, "OK."),
        _row("print('Olá,', nome)", False, "OK."),
        _row("nome = input 'Nome: '", True, "Faltam parênteses."),
        _row("imput('Cidade: ')", True, "input() escrito errado."),
        _row("print(nome))", True, "Parêntese extra."),
        _row("print(nome+1)", True, "Concatenação str + int."),
        _row("input(print('x'))", True, "Chamada aninhada desnecessária."),
    ]
    return pool, hint

def _pool_variaveis() -> Tuple[List[Row], str]:
    hint = "Atribuição com '='; cuidado com tipos e nomes."
    pool = [
        _row("x = 5", False, "OK."),
        _row("y = 'Python'", False, "OK."),
        _row("print(x)", False, "OK."),
        _row("x == 5", True, "Comparação, não atribuição."),
        _row("y = 3 + '2'", True, "Mistura int e str."),
        _row("print(x", True, "Parêntese não fechado."),
        _row("x := 5", True, "':=' não substitui '=' nessa forma."),
        _row("y =+ x", True, "Operador invertido; seria '+='."),
        _row("print(z)", True, "Variável indefinida."),
    ]
    return pool, hint

def _pool_operadores() -> Tuple[List[Row], str]:
    hint = "Comparações: '==', '>=', '<='; evite '=>' ou '=' sozinho."
    pool = [
        _row("x = 3; y = 5", False, "OK."),
        _row("print(x + y)", False, "Soma correta."),
        _row("print(x >= y)", False, "Comparação válida."),
        _row("print(x => y)", True, "Operador inválido: use '>='."),
        _row("print(x = y)", True, "Use '==' para comparar."),
        _row("print(x >== y)", True, "Operador inválido."),
        _row("y = '3' + 2", True, "Mistura str e int."),
        _row("print(x > )", True, "Falta operando."),
    ]
    return pool, hint

def _pool_if() -> Tuple[List[Row], str]:
    hint = "If/else: dois pontos ':' e print() correto."
    pool = [
        _row("idade = 18", False, "OK."),
        _row("if idade >= 18:", False, "OK."),
        _row("print('maior')", False, "OK."),
        _row("else:", False, "OK."),
        _row("print('menor')", False, "OK."),
        _row("if idade >= 18", True, "Falta ':' no if."),
        _row("if idade => 18:", True, "Operador inválido."),
        _row("print 'maior'", True, "Faltam parênteses."),
        _row("else", True, "Falta ':' no else."),
        _row("iff idade >= 18:", True, "Palavra-chave errada."),
    ]
    return pool, hint

def _pool_for() -> Tuple[List[Row], str]:
    hint = "for + range(): parênteses e ':'; print() com parênteses."
    pool = [
        _row("for i in range(3):", False, "OK."),
        _row("print(i)", False, "OK."),
        _row("print('FIM')", False, "OK."),
        _row("for i in range 3:", True, "Faltam parênteses."),
        _row("for i = 0..2:", True, "Sintaxe não-Python."),
        _row("for(i in range(3)):", True, "Mistura com C."),
        _row("print i", True, "print() precisa de parênteses."),
        _row("for i in range(3)", True, "Falta ':' no for."),
    ]
    return pool, hint

def _pool_while() -> Tuple[List[Row], str]:
    hint = "while ...: com incremento; não existe 'i ++' em Python."
    pool = [
        _row("i = 0", False, "OK."),
        _row("while i < 3:", False, "OK."),
        _row("print(i)", False, "OK."),
        _row("i += 1", False, "OK."),
        _row("while i < 3", True, "Falta ':' no while."),
        _row("i = i + '1'", True, "Mistura int e str."),
        _row("print(i))", True, "Parêntese extra."),
        _row("i ++", True, "Não existe operador ++."),
        _row("whille i < 3:", True, "Palavra-chave errada."),
    ]
    return pool, hint

def _pool_funcoes() -> Tuple[List[Row], str]:
    hint = "def ...: + return; chamadas com parênteses; ortografia correta."
    pool = [
        _row("def soma(a, b):", False, "OK."),
        _row("return a + b", False, "OK."),
        _row("print(soma(2, 3))", False, "OK."),
        _row("def soma(a, b)", True, "Falta ':' em def."),
        _row("return a + b)", True, "Parêntese extra."),
        _row("print soma(2,3)", True, "Faltam parênteses."),
        _row("def soma: (a,b)", True, "Sintaxe inválida."),
        _row("retun a+b", True, "Return escrito errado."),
    ]
    return pool, hint

# -------------------------- Roteador --------------------------

def _pool_by_topic(topic_title: str) -> Tuple[List[Row], str]:
    t = _norm(topic_title)

    if "saida de dados" in t or "saída de dados" in t or "print" in t:
        return _pool_print()
    if "entrada de dados" in t or "input" in t:
        return _pool_input()
    if "variaveis" in t or "variáveis" in t or "variavel" in t or "variável" in t or "tipos simples" in t:
        return _pool_variaveis()
    if "operadores" in t or "relacionais" in t or "aritmeticos" in t or "aritméticos" in t:
        return _pool_operadores()
    if "condicionais" in t or "if/else" in t or "if else" in t or " if " in t or t.startswith("if"):
        return _pool_if()
    if "repeticao (for)" in t or "repetição (for)" in t or " for)" in t or " for " in t:
        return _pool_for()
    if "repeticao (while)" in t or "repetição (while)" in t or " while)" in t or " while " in t:
        return _pool_while()
    if "funcoes" in t or "funções" in t or "funcao" in t or "função" in t:
        return _pool_funcoes()

    return _pool_print()

# -------------------------- Gerador de perguntas --------------------------

def _make_question_from_pool(pool: List[Row]) -> Dict:
    oks  = [r for r in pool if r["bug"] == "0"]
    bugs = [r for r in pool if r["bug"] == "1"]
    if not oks:
        oks = [random.choice(pool)]
    while len(bugs) < 2:
        bugs.append(random.choice(pool))

    ok = random.choice(oks)
    wrongs = random.sample(bugs, 2)

    opts = [ok["code"], wrongs[0]["code"], wrongs[1]["code"]]
    why  = [ok["why"],  wrongs[0]["why"],  wrongs[1]["why"]]

    idxs = [0,1,2]
    random.shuffle(idxs)
    opts = [opts[i] for i in idxs]
    why  = [why[i]  for i in idxs]
    correct = idxs.index(0)

    return {
        "prompt": "Passe para a opção CORRETA.",
        "opts": opts,
        "correct": correct,
        "why": why
    }

def get_pyfoot_questions(topic_title: str, rounds: int = 12) -> List[Dict]:
    pool, _hint = _pool_by_topic(topic_title)
    qs = []
    for _ in range(max(1, int(rounds))):
        qs.append(_make_question_from_pool(pool))
    return qs
