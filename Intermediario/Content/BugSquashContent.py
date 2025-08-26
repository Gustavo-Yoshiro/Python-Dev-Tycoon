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
        _row("print('Olá')", False, "Sintaxe correta."),
        _row("print(1+2)", False, "Expressão válida."),
        _row("print('Fim')", False, "OK."),
        _row("print('a', 1)", False, "Múltiplos argumentos são válidos."),
        _row("print('Resposta:', 42)", False, "OK."),

        _row("prit('Olá')", True, "Função errada: 'print'."),
        _row("print(Olá)", True, "Strings requerem aspas."),
        _row("print('Ola)", True, "Aspas não fechadas."),
        _row("printf('Hello')", True, "Não existe printf() em Python."),
        _row("print('7'+1)", True, "Mistura str com int sem conversão."),
        _row("print ('x') )", True, "Parêntese extra."),
    ]

    # variações programáticas simples
    words = ["fim", "ok", "python", "teste", "sucesso", "start", "end", "resultado"]
    nums  = [0, 1, 2, 3, 5, 7, 10, 42]
    for w in words:
        base.append(_row(f"print('{w.upper()}')", False, "OK."))
        base.append(_row(f"print('{w}')", False, "OK."))
        base.append(_row(f"print({len(w)}+{nums[len(w)%len(nums)]})", False, "OK."))
        base.append(_row(f"print({w})", True, "Variável não definida; use aspas se for texto."))
        base.append(_row(f"print('{w}", True, "Aspas não fechadas."))
    for a in nums:
        b = random.choice(nums)
        base.append(_row(f"print({a}+{b})", False, "Soma numérica válida."))
        base.append(_row(f"print('{a}'+{b})", True, "Concatenação str + int causa erro."))

    # pequenos multi-linhas
    base += [
        _row("msg = 'oi'\nprint(msg)", False, "Variável definida e usada corretamente."),
        _row("msg = 'oi\nprint(msg)", True, "Aspas não fechadas quebram o código."),
    ]

    return _dedup_rows(base), hint

def _pool_input() -> Tuple[List[Row], str]:
    hint = "input() usa parênteses; converta para int/float quando for somar números."
    base = [
        _row("nome = input('Nome: ')", False, "OK."),
        _row("print(nome)", False, "OK."),
        _row("x = input('Digite: ')", False, "OK."),
        _row("idade = int(input('Idade: '))", False, "Conversão para int correta."),
        _row("a = float(input('A: '))\nb = float(input('B: '))\nprint(a+b)", False, "Soma de floats OK."),

        _row("nome = input 'Nome: '", True, "Faltam parênteses."),
        _row("imput('Cidade: ')", True, "input() escrito errado."),
        _row("print(nome))", True, "Parêntese extra."),
        _row("print(nome+1)", True, "Concatenação str + int."),
        _row("input(print('x'))", True, "Chamada aninhada desnecessária."),
        _row("soma = input('a: ') + input('b: ')", True, "Sem conversão: concatena strings."),
        _row("idade = int(input('Idade: '))\nprint('Idade: ' + idade)", True, "Concatenação str + int."),
    ]
    return _dedup_rows(base), hint

def _pool_variaveis() -> Tuple[List[Row], str]:
    hint = "Atribuição usa '='; cuidado com tipos e nomes válidos."
    base = [
        _row("x = 5", False, "OK."),
        _row("y = 'Python'", False, "OK."),
        _row("x, y = 1, 2", False, "Atribuição múltipla válida."),
        _row("print(x)", False, "OK."),
        _row("x += 3", False, "Atribuição composta válida (após definir x)."),

        _row("x == 5", True, "Comparação, não atribuição."),
        _row("y = 3 + '2'", True, "Mistura int e str."),
        _row("print(x", True, "Parêntese não fechado."),
        _row("x := 5", True, "Walrus não substitui '=' na definição isolada."),
        _row("y =+ 2", True, "Provável erro: queria '+='."),
        _row("print(z)", True, "Variável indefinida."),
        _row("class = 3", True, "Palavra reservada não pode ser nome."),
    ]
    # variações
    names = ["total", "contador", "msg", "ativo", "saldo"]
    for n in names:
        base.append(_row(f"{n} = 0\n{n} = {n} + 1", False, "Atualização de variável OK."))
        base.append(_row(f"{n} = {n} + '1'", True, "Mistura str e int."))
    return _dedup_rows(base), hint

def _pool_operadores() -> Tuple[List[Row], str]:
    hint = "Use '>=', '==', '!='; nada de '=>' ou '=' para comparar."
    base = [
        _row("x = 3\ny = 5\nprint(x + y)", False, "Soma correta."),
        _row("print(3 * 2 + 1)", False, "Precedência OK."),
        _row("print(10 // 3)", False, "Divisão inteira OK."),
        _row("print(5 % 2)", False, "Módulo OK."),
        _row("print(3 >= 2)", False, "Comparação válida."),
        _row("print(3 == 3)", False, "Comparação válida."),
        _row("print(True and False)", False, "Operador lógico válido."),

        _row("print(3 => 2)", True, "Operador inválido: use '>='."),
        _row("print(3 = 2)", True, "Use '==' para comparar."),
        _row("print(3 >== 2)", True, "Operador inválido."),
        _row("print('3' - 1)", True, "Subtração entre str e int não existe."),
        _row("print(> 3)", True, "Falta operando."),
    ]
    return _dedup_rows(base), hint

def _pool_if() -> Tuple[List[Row], str]:
    hint = "if/else: termine cabeçalho com ':'; parênteses são opcionais; use print() correto."
    base = [
        _row("idade = 18\nif idade >= 18:\n    print('maior')\nelse:\n    print('menor')", False, "Estrutura if/else correta."),
        _row("x = 7\nif x % 2 == 0:\n    print('par')\nelse:\n    print('impar')", False, "Uso de % e if/else OK."),
        _row("n = 10\nif n:\n    print('verdadeiro')", False, "Qualquer não zero é True."),

        _row("if idade >= 18", True, "Falta ':' no cabeçalho."),
        _row("if idade => 18:", True, "Operador inválido, use '>='."),
        _row("print 'maior'", True, "print() precisa de parênteses."),
        _row("else", True, "Falta ':' e bloco após else."),
        _row("iff idade >= 18:", True, "Palavra-chave errada."),
        _row("if (x == 3):\nprint('ok')", True, "Indentação obrigatória dentro do bloco."),
        _row("if x = 3:\n    print('ok')", True, "Use '==' para comparar."),
    ]
    return _dedup_rows(base), hint

def _pool_for() -> Tuple[List[Row], str]:
    hint = "for + range(): use parênteses e ':'; lembre de print() com parênteses."
    base = [
        _row("for i in range(3):\n    print(i)\nprint('FIM')", False, "Laço for com range e print OK."),
        _row("for c in 'py':\n    print(c)", False, "Iterando sobre string OK."),
        _row("for i in range(1, 4):\n    print(i)", False, "Faixa 1..3 OK."),

        _row("for i in range 3:", True, "Faltam parênteses em range()."),
        _row("for i = 0..2:", True, "Sintaxe não-Python."),
        _row("for(i in range(3)):", True, "Mistura com C."),
        _row("print i", True, "print() precisa de parênteses."),
        _row("for i in range(3)", True, "Falta ':' no cabeçalho."),
        _row("for i in 3:\n    print(i)", True, "Não se itera inteiro."),
    ]
    return _dedup_rows(base), hint

def _pool_while() -> Tuple[List[Row], str]:
    hint = "while ...: termine com ':'; atualize a variável para não travar; nada de 'i ++'."
    base = [
        _row("i = 0\nwhile i < 3:\n    print(i)\n    i += 1", False, "Laço com incremento OK."),
        _row("i = 3\nwhile i:\n    print(i)\n    i -= 1", False, "Condição verdade: qualquer não zero."),

        _row("while i < 3", True, "Falta ':' no cabeçalho."),
        _row("i = i + '1'", True, "Mistura int e str."),
        _row("print(i))", True, "Parêntese extra."),
        _row("i ++", True, "Não existe ++ em Python."),
        _row("whille i < 3:", True, "Palavra-chave errada."),
        _row("i = 0\nwhile i < 3:\n    print(i)", True, "Sem incremento: laço infinito."),
        _row("while i = 3:\n    print(i)", True, "Use '==' para comparar."),
    ]
    return _dedup_rows(base), hint

def _pool_funcoes() -> Tuple[List[Row], str]:
    hint = "def nome(args): e return; chamadas com parênteses; escreva 'return' corretamente."
    base = [
        _row("def soma(a, b):\n    return a + b\nprint(soma(2, 3))", False, "Definição e chamada corretas."),
        _row("def eco(s):\n    print(s)\neco('oi')", False, "Função sem retorno explícito é OK."),
        _row("def dobro(x=2):\n    return x*2\nprint(dobro())", False, "Default em parâmetro OK."),

        _row("def soma(a, b)", True, "Falta ':' no cabeçalho."),
        _row("return a + b)", True, "Parêntese extra; e 'return' deve estar dentro da função."),
        _row("print soma(2,3)", True, "Chamada sem parênteses."),
        _row("def soma: (a,b)", True, "Sintaxe inválida para parâmetros."),
        _row("retun a+b", True, "Erro de ortografia em 'return'."),
        _row("def f(x):\nreturn x", True, "Indentação obrigatória no corpo."),
    ]
    return _dedup_rows(base), hint

# ----------------------------- Roteador -----------------------------

def get_bug_squash_pool(topic_title: str) -> Tuple[List[Row], str]:
    """
    Retorna o POOL COMPLETO (grande) para o tópico, + hint textual.
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

    if "condicionais" in t or "if/else" in t or "if else" in t or " if " in t or t.startswith("if"):
        return _pool_if()

    if "repeticao (for)" in t or "estrutura de repeticao (for" in t or " for)" in t or " for " in t or t.startswith("for"):
        return _pool_for()

    if "repeticao (while)" in t or "estrutura de repeticao (while" in t or " while)" in t or " while " in t or t.startswith("while"):
        return _pool_while()

    if "funcoes" in t or "funcoes" in t or "funções" in t or "funcao" in t or "função" in t or "def " in t:
        return _pool_funcoes()

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
