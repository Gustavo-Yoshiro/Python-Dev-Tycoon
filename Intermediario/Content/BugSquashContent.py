# Intermediario/Content/BugSquashContent.py
import random
import unicodedata
from typing import List, Dict, Tuple

Row = Dict[str, str]  # {"code": str, "bug": "0|1", "why": str}

# ----------------------------- Utils -----------------------------

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

def _dedup_rows(rows: List[Row]) -> List[Row]:
    """Remove duplicados por 'code' preservando o primeiro 'why'."""
    seen, out = set(), []
    for r in rows:
        c = r.get("code", "").strip()
        if c not in seen:
            out.append(r)
            seen.add(c)
    return out

def _sample_mix(pool: List[Row], size: int, min_bugs: int = 2) -> List[Row]:
    """
    Amostra 'size' itens do pool, garantindo ao menos 'min_bugs' bugs
    e uma proporção razoável (~30%-60%) de bugs quando possível.
    """
    pool = list(pool)
    bugs = [r for r in pool if r["bug"] == "1"]
    oks  = [r for r in pool if r["bug"] == "0"]

    if not pool:
        return []

    # alvo mínimo de bugs ~ max(min_bugs, 1/3 do size)
    nb_target = max(min_bugs, size // 3)
    nb = min(len(bugs), nb_target)
    no = min(len(oks), size - nb)

    chosen = _pick(bugs, nb) + _pick(oks, no)

    # completa se ainda faltar (com o que tiver)
    if len(chosen) < size:
        rest = [r for r in pool if r not in chosen]
        chosen += _pick(rest, size - len(chosen))

    random.shuffle(chosen)
    return chosen[:size]

# ----------------------------- Geradores por tópico -----------------------------
# Cada gerador devolve (pool, hint). O pool é grande e variado.
# Limite: mantemos snippets curtos (1–3 linhas) para caber no balão das cobras.

def _pool_print() -> Tuple[List[Row], str]:
    hint = "Foque em print(): parênteses/aspas corretos; nada de misturar str com int sem conversão."
    base = [
        _row("print('Olá')", False, "OK."),
        _row("print(1+2)", False, "OK."),
        _row("print('Fim')", False, "OK."),
        _row("print('a', 1)", False, "OK."),
        _row("print('Resposta:', 42)", False, "OK."),
        _row("prit('Olá')", True, "Nome da função errado."),
        _row("print(Olá)", True, "Strings precisam de aspas."),
        _row("print('Ola)", True, "Aspas não fechadas."),
        _row("printf('Hello')", True, "Não existe printf() em Python."),
        _row("print('7'+1)", True, "Concatenação str + int."),
        _row("print 'x'", True, "Sintaxe do Python 2."),
        _row("print('x') )", True, "Parêntese extra."),
    ]
    words = ["fim", "ok", "python", "teste", "sucesso"]
    nums  = [0, 1, 2, 3, 7, 42]
    for w in words:
        base.append(_row(f"print('{w}')", False, "OK."))
        base.append(_row(f"print('{w.upper()}')", False, "OK."))
        base.append(_row(f"print({len(w)}+{nums[len(w)%len(nums)]})", False, "OK."))
        base.append(_row(f"print({w})", True, "Variável indefinida; texto precisa de aspas."))
        base.append(_row(f"print('{w}", True, "Aspas não fechadas."))
    for a in nums:
        b = random.choice(nums)
        base.append(_row(f"print({a}+{b})", False, "OK."))
        base.append(_row(f"print('{a}'+{b})", True, "str + int."))
    return _dedup_rows(base), hint


def _pool_input() -> Tuple[List[Row], str]:
    hint = "input() usa parênteses; converta para int/float quando precisar de número."
    base = [
        _row("nome = input('Nome: ')", False, "OK."),
        _row("x = input('Digite: ')", False, "OK."),
        _row("idade = int(input('Idade: '))", False, "Conversão correta."),
        _row("peso = float(input('Peso: '))", False, "Conversão correta."),
        _row("a = input('A: ')\nb = input('B: ')", False, "Duas leituras (strings)."),
        _row("nome = input 'Nome: '", True, "Faltam parênteses."),
        _row("imput('Cidade: ')", True, "input() escrito errado."),
        _row("n = int(input('n: ')", True, "Parêntese não fechado."),
        _row("total = input('t: ')\ntotal = total + 1", True, "str + int."),
        _row("soma = input('a: ') + input('b: ')", True, "Concatena strings sem conversão."),
        _row("x = floatinput('x: ')", True, "Função inexistente."),
        _row("idade = int input('Idade: ')", True, "Sintaxe inválida."),
    ]
    return _dedup_rows(base), hint


def _pool_variaveis() -> Tuple[List[Row], str]:
    hint = "Atribuição usa '='; nomes válidos; cuidado com tipos."
    base = [
        _row("x = 5", False, "OK."),
        _row("y = 'Python'", False, "OK."),
        _row("x, y = 1, 2", False, "OK."),
        _row("ativo = True", False, "OK."),
        _row("saldo = 0", False, "OK."),
        _row("x == 5", True, "Comparação, não atribuição."),
        _row("1x = 3", True, "Nome inválido."),
        _row("class = 3", True, "Palavra reservada."),
        _row("y = 3 + '2'", True, "str + int."),
        _row("saldo += 1", True, "Variável possivelmente indefinida."),
        _row("x := 5", True, "Não use ':=' para definir isoladamente aqui."),
        _row("z", True, "Referência sem atribuição."),
        _row("total = 0; total = total + '1'", True, "str + int."),
    ]
    return _dedup_rows(base), hint


def _pool_operadores() -> Tuple[List[Row], str]:
    hint = ">=, ==, !=; nada de '=>' ou '=' para comparar."
    base = [
        _row("print(3 + 5 * 2)", False, "OK."),
        _row("print(10 // 3)", False, "OK."),
        _row("print(5 % 2)", False, "OK."),
        _row("print(3 >= 2)", False, "OK."),
        _row("print(True and False)", False, "OK."),
        _row("print(3 => 2)", True, "Use '>='."),
        _row("print(3 = 2)", True, "Use '==' para comparar."),
        _row("print('3' - 1)", True, "str - int."),
        _row("print(> 3)", True, "Falta operando."),
        _row("print(3 >== 2)", True, "Operador inválido."),
    ]
    return _dedup_rows(base), hint


def _pool_if() -> Tuple[List[Row], str]:
    hint = "if/else: termine cabeçalho com ':'; indentação obrigatória; parênteses são opcionais."
    base = [
        _row("if 10 > 5:\n    print('ok')", False, "OK."),
        _row("if 'py'.startswith('p'):\n    print('sim')", False, "OK."),
        _row("if 0:\n    print('nunca')", False, "OK (condição falsa)."),
        _row("if idade >= 18", True, "Falta ':' no cabeçalho."),
        _row("if x = 3:\n    print('ok')", True, "Use '==' para comparar."),
        _row("iff x>0:", True, "Palavra-chave errada."),
        _row("else:", True, "else sem if correspondente."),
        _row("if (x == 3):\nprint('ok')", True, "Sem indentação do corpo."),
        _row("if True: print 'x'", True, "print sem parênteses."),
    ]
    return _dedup_rows(base), hint


def _pool_for() -> Tuple[List[Row], str]:
    hint = "for + range(): use parênteses e ':'; corpo indentado na linha de baixo."
    base = [
        _row("for i in range(3):\n    print(i)", False, "OK."),
        _row("for c in 'py':\n    print(c)", False, "OK."),
        _row("for i in range(1, 4):\n    print(i)", False, "OK."),
        _row("for i in range 3:", True, "Faltam parênteses em range()."),
        _row("for i = 0..2:", True, "Sintaxe não-Python."),
        _row("for(i in range(3)):", True, "Mistura com C."),
        _row("for i in range(3)", True, "Falta ':' no cabeçalho."),
        _row("for i in 3:\n    print(i)", True, "Não se itera inteiro."),
    ]
    return _dedup_rows(base), hint


def _pool_while() -> Tuple[List[Row], str]:
    hint = "while ...: termine com ':'; corpo indentado na linha de baixo."
    base = [
        _row("while True:\n    break", False, "OK (exemplo mínimo)."),
        _row("while 1:\n    break", False, "OK."),
        _row("while i < 3", True, "Falta ':' no cabeçalho."),
        _row("i ++", True, "Não existe '++' em Python."),
        _row("whille i < 3:\n    pass", True, "Palavra-chave errada."),
        _row("while i = 3:\n    pass", True, "Use '==' para comparar."),
    ]
    return _dedup_rows(base), hint


def _pool_funcoes() -> Tuple[List[Row], str]:
    hint = "def nome(args): e return; corpo indentado na linha de baixo."
    base = [
        _row("def f():\n    return 1", False, "OK."),
        _row("def soma(a,b):\n    return a+b", False, "OK."),
        _row("def eco(s):\n    return s", False, "OK."),
        _row("def soma(a, b)", True, "Falta ':' no cabeçalho."),
        _row("def f(x):\nreturn x", True, "Falta indentação no corpo."),
        _row("def soma: (a,b)", True, "Sintaxe inválida."),
        _row("retun 1", True, "Ortografia de 'return'."),
        _row("print soma(2,3)", True, "Chamada sem parênteses."),
    ]
    return _dedup_rows(base), hint


def _pool_fstrings_formatacao() -> Tuple[List[Row], str]:
    hint = "f-strings: f'...{expr}...'; .format(...); especificadores (:.2f, :>5); chaves devem fechar."
    base = [
        _row("nome = 'Ana'; print(f'Olá, {nome}')", False, "OK."),
        _row("x = 3.14159; print(f'{x:.2f}')", False, "OK."),
        _row("a, b = 2, 3; print(f'{a}+{b}={a+b}')", False, "OK."),
        _row("print('Olá, {}'.format('mundo'))", False, "OK."),
        _row("print('{:>5}'.format(7))", False, "OK."),
        _row("x = 10; print(f'{{ok}} {x}')", False, "Chaves literais."),
        _row("print(f'Olá, {nome')", True, "Chave não fechada."),
        _row("x = 3.14; print(f'{x:2f}')", True, "Formato inválido; use :.2f."),
        _row("print('Olá, {nome}'.format())", True, "Placeholder sem argumento."),
        _row("print('{:d}'.format('3'))", True, "Tipo errado para {:d}."),
        _row("print('%d' % '3')", True, "Tipo errado para %d."),
        _row("a, b = 1, 2; print(f'Total: {a+b')", True, "Falta fechar }."),
        _row("x = 5; print(f'{x:}')", True, "Especificador incompleto."),
    ]
    return _dedup_rows(base), hint


def _pool_metodos_string() -> Tuple[List[Row], str]:
    hint = "Principais métodos: lower/upper/strip/split/join/replace/startswith/endswith/isdigit."
    base = [
        _row("s = ' Py '\nprint(s.strip())", False, "strip() remove espaços nas pontas."),
        _row("print('py'.upper())", False, "OK."),
        _row("print('PY'.lower())", False, "OK."),
        _row("print('a-b-c'.split('-'))", False, "OK."),
        _row("print('-'.join(['a','b','c']))", False, "OK."),
        _row("print('abc'.replace('b','x'))", False, "OK."),
        _row("print('python'.startswith('py'))", False, "OK."),
        _row("print('file.txt'.endswith('.txt'))", False, "OK."),
        _row("print('123'.isdigit())", False, "OK."),
        _row("s = 123; print(s.lower())", True, "lower() em int."),
        _row("print('a-b'.split)", True, "Faltou chamar split()."),
        _row("lista = ['a','b']; print(lista.join('-'))", True, "join é de string."),
        _row("print('-'.join('a','b'))", True, "join aceita 1 iterável."),
        _row("print('abc'.repl('b','x'))", True, "Método inexistente."),
        _row("print('abc'.split(None, '1'))", True, "maxsplit deve ser int."),
        _row("print('abc'.find('a') = 0)", True, "Atribuição em chamada."),
    ]
    return _dedup_rows(base), hint


def _pool_listas() -> Tuple[List[Row], str]:
    hint = "Listas: [], append/extend/insert/pop/remove, sort/reverse, slicing."
    base = [
        _row("l = [1,2]; l.append(3)", False, "OK."),
        _row("print([1,2,3][1:])", False, "Slicing."),
        _row("print([1,2,3][::-1])", False, "Reverse por slicing."),
        _row("l = [1,2]; l.extend([3,4])", False, "OK."),
        _row("l = [3,1,2]; l.sort()", False, "OK."),
        _row("l = [1,2]; l.insert(1,'x')", False, "OK."),
        _row("x = [1,2,3]; y = x[:]", False, "Cópia por slicing."),
        _row("l = {}; l.append(1)", True, "{} cria dict, não lista."),
        _row("l = [1]; l.add(2)", True, "Lista não tem add()."),
        _row("print([1,2,3][1:5:0])", True, "step=0 inválido."),
        _row("print([1,2,3][10])", True, "IndexError provável."),
        _row("l = [3,2]; sort(l)", True, "Use l.sort()."),
        _row("l = [1,2]; l.extend(3)", True, "extend espera iterável."),
        _row("print([1,2][::None])", True, "step None inválido."),
    ]
    return _dedup_rows(base), hint


def _pool_tuplas() -> Tuple[List[Row], str]:
    hint = "Tuplas são imutáveis; 1 elemento precisa de vírgula: ('x',)."
    base = [
        _row("t = (1,2,3); print(t[0])", False, "OK."),
        _row("a, b = (1, 2)", False, "OK."),
        _row("t = ('x',)", False, "OK."),
        _row("t = tuple([1,2])", False, "OK."),
        _row("t = (1); print(type(t))", True, "(1) é int; faltou vírgula."),
        _row("t = (1,2); t[0] = 9", True, "Imutável."),
        _row("t = (1,2); t.append(3)", True, "Tupla não tem append."),
        _row("a, b = (1,2,3)", True, "Tamanhos diferentes."),
    ]
    return _dedup_rows(base), hint


def _pool_sets() -> Tuple[List[Row], str]:
    hint = "Conjuntos: set(), {1,2}; add/remove/discard; união |, interseção &."
    base = [
        _row("s = {1,2,3}; s.add(4)", False, "OK."),
        _row("print(2 in {1,2,3})", False, "OK."),
        _row("print({1,2} | {2,3})", False, "União."),
        _row("print({1,2,3} & {2,3})", False, "Interseção."),
        _row("print(set([1,2,2,3]))", False, "Dedup."),
        _row("s = {1}; s.discard(99)", False, "OK."),
        _row("s = {}; s.add(1)", True, "{} é dict, não set()."),
        _row("s = set(); s.append(1)", True, "Set não tem append()."),
        _row("s = {1,2}; s.remove(3)", True, "remove erra se não existir."),
        _row("s = {{1}}", True, "Itens devem ser hashable."),
        _row("s = {[1,2]}", True, "Lista não é hashable."),
        _row("print({1,2} + {3})", True, "Use '|', não '+'."),
    ]
    return _dedup_rows(base), hint


def _pool_dicts() -> Tuple[List[Row], str]:
    hint = "Dicts: {'k':v}; d['k'], get(), update(); chaves imutáveis."
    base = [
        _row("d = {'nome':'Ana','idade':20}; print(d['nome'])", False, "OK."),
        _row("d = {'n':1}; print(d.get('x',0))", False, "OK."),
        _row("d = {'idade':20}; d['idade'] = 21", False, "OK."),
        _row("d = {'a':1}; d.update({'b':2})", False, "OK."),
        _row("print(list({'x':1}.items()))", False, "OK."),
        _row("d = {'x':1}; print(d.x)", True, "Use d['x']."),
        _row("d = [('a',1)]; print(d['a'])", True, "Lista não indexa por chave."),
        _row("d = {'a':1}; print(d['b'])", True, "KeyError provável."),
        _row("d = {['a']:1}", True, "Lista não é hashable."),
        _row("print({1:'a', 1:'b'})", True, "Chave duplicada sobrescreve."),
    ]
    return _dedup_rows(base), hint


def _pool_list_comprehensions() -> Tuple[List[Row], str]:
    hint = "List comps: [expr for x in seq if cond]; não confundir com set/dict/generator."
    base = [
        _row("nums = [1,2,3]; quad = [n*n for n in nums]", False, "OK."),
        _row("pares = [n for n in range(6) if n%2==0]", False, "OK."),
        _row("flat = [x for sub in [[1,2],[3]] for x in sub]", False, "OK."),
        _row("doubles = [x*2 for x in (1,2,3)]", False, "OK."),
        _row("[n for n in range(3) if]", True, "if sem condição."),
        _row("[x for in range(3)]", True, "Faltou variável antes de in."),
        _row("[x for x range(3)]", True, "Faltou 'in'."),
        _row("{x for x in [1,1,2]}", True, "Isto é set, não lista."),
        _row("(x for x in [1,2])", True, "Isto é generator, não lista."),
        _row("[n* for n in range(3)]", True, "Expressão incompleta."),
    ]
    return _dedup_rows(base), hint


def _pool_tratamento_erros() -> Tuple[List[Row], str]:
    hint = "try/except/else/finally; 'except Tipo as e'; 'raise ValueError(...)'; sem 'catch'."
    base = [
        _row("raise ValueError('msg')", False, "OK."),
        _row("int('3')", False, "Conversão válida."),
        _row("try:\n    1/0", True, "try sem except/finally."),
        _row("try:\n    pass", True, "try sem except/finally."),
        _row("catch Exception:", True, "Não existe 'catch' em Python."),
        _row("raise NotAnError('x')", True, "Classe de exceção inexistente."),
        _row("try:\n    pass\n", True, "Bloco incompleto."),  # ainda 2 linhas úteis
        _row("except ValueError, e: pass", True, "Sintaxe Python 2."),
    ]
    return _dedup_rows(base), hint

# ----------------------------- Roteador -----------------------------

def get_bug_squash_pool(topic_title: str) -> Tuple[List[Row], str]:
    """
    Retorna o POOL COMPLETO (grande) para o tópico, + hint textual.
    Roteamento por NOME EXATO normalizado (mesmo padrão da Cobrinha/PyFoot).
    """
    t = _norm(topic_title)

    ROUTER = {
        _norm("Saída de dados com print()"): _pool_print,
        _norm("Entrada de dados com input()"): _pool_input,
        _norm("Variáveis e Tipos Simples"): _pool_variaveis,
        _norm("Operadores Aritméticos e Relacionais"): _pool_operadores,
        _norm("Estruturas Condicionais (if/else)"): _pool_if,
        _norm("Estruturas de Repetição (for)"): _pool_for,
        _norm("Estrutura de Repetição (while)"): _pool_while,
        _norm("Funções Simples"): _pool_funcoes,

        # Fases 9–16
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

    # fallback seguro: se vier título errado, cai no "print"
    return _pool_print()

    # ----- NOVOS TÓPICOS (Fases 9–16) -----
    # Fase 9: f-strings e formatação
    if ("f-strings" in t or "f strings" in t or "fstring" in t or
        "formatacao" in t or ".format(" in t or "formatacao de strings" in t or "formatacao" in t):
        return _pool_fstrings_formatacao()

    # Fase 10: Métodos de string
    if ("metodos de string" in t or "metodo de string" in t or
        "string methods" in t or "strings (metodos" in t or "strings metodos" in t):
        return _pool_metodos_string()

    # Fase 15: List Comprehensions (checar ANTES de 'listas' genérico)
    if ("list comprehension" in t or "list comprehensions" in t or
        "comprehension" in t or "comprehensions" in t):
        return _pool_list_comprehensions()

    # Fase 11: Listas (métodos e slicing)
    if ("listas" in t or "lista" in t or "slicing" in t):
        return _pool_listas()

    # Fase 12: Tuplas e imutabilidade
    if ("tuplas" in t or "tupla" in t or "imutabilidade" in t or "imutavel" in t):
        return _pool_tuplas()

    # Fase 13: Conjuntos (set)
    if ("conjuntos" in t or "conjunto" in t or "set " in t or t.startswith("set")):
        return _pool_sets()

    # Fase 14: Dicionários
    if ("dicionarios" in t or "dicionario" in t or "dicion\u00E1rio" in t or "dict" in t):
        return _pool_dicts()

    # Fase 16: Tratamento de Erros
    if ("tratamento de erros" in t or "excecoes" in t or "excecao" in t or
        "exceptions" in t or "try" in t or "except" in t or "raise" in t):
        return _pool_tratamento_erros()

    # fallback
    return _pool_print()

def get_bug_squash_content(topic_title: str, lanes: int = 7, min_bugs: int = 2) -> Tuple[List[Row], str]:
    """
    Retorna (rows, hint).
    Agora 'rows' é um conjunto AMPLIADO (não só 'lanes'): amostramos um
    subconjunto grande do pool para dar VARIEDADE ao minigame por várias rodadas.
    """
    pool, hint = get_bug_squash_pool(topic_title)

    # tamanho alvo: proporcional às lanes (p/ diversidade), mas limitado pelo pool
    target_size = min(len(pool), max(24, lanes * 6))
    rows = _sample_mix(pool, size=target_size, min_bugs=min_bugs)

    return _dedup_rows(rows), hint
