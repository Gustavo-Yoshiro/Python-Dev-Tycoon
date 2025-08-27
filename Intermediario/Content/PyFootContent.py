# Intermediario/Content/PyFootContent.py
# Banco de perguntas do PyFoot — Iniciante + Intermediário num arquivo só.
# - get_pyfoot_questions(topic_title, rounds)
# - get_topic_for_fase(fase_id)  → mapeia Fases 1..16
#
# Fase  1: Saída de dados (print)
# Fase  2: Entrada de dados (input)
# Fase  3: Variáveis e tipos simples
# Fase  4: Operadores aritméticos e relacionais
# Fase  5: Condicionais (if/else)
# Fase  6: Repetição (for)
# Fase  7: Repetição (while)
# Fase  8: Funções
# Fase  9: f-strings e formatação
# Fase 10: Métodos de string
# Fase 11: Listas (métodos e slicing)
# Fase 12: Tuplas e imutabilidade
# Fase 13: Conjuntos (set)
# Fase 14: Dicionários
# Fase 15: List Comprehensions
# Fase 16: Tratamento de Erros

import random
import unicodedata
from typing import List, Dict, Tuple

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

# =====================================================================
# =========================  INICIANTE  ================================
# =====================================================================

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
    hint = "input(): sempre com parênteses; converta se precisar de número."
    pool = [
        _row("nome = input('Nome: ')", False, "OK."),
        _row("idade = int(input('Idade: '))", False, "Converte para int."),
        _row("altura = float(input('Altura: '))", False, "Converte para float."),
        _row("soma = int(input('A: ')) + int(input('B: '))", False, "Soma numérica com conversão."),
        _row("texto = input('Digite algo: ')", False, "Lê string."),

        _row("nome = input 'Nome: '", True, "Faltam parênteses."),
        _row("imput('Cidade: ')", True, "input() escrito errado."),
        _row("idade = int 'Idade: '", True, "int() precisa envolver input(...)."),
        _row("soma = input('A: ') + input('B: ')", True, "Sem conversão, concatena strings."),
        _row("altura = float(input('Altura: ')", True, "Parêntese não fechado."),
        _row("int(input('x')) = idade", True, "Atribuição invertida."),
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
    hint = "If/else em 1 linha com ternário quando couber."
    pool = [
        _row("idade = 18; print('maior') if idade >= 18 else print('menor')", False, "Expressão condicional."),
        _row("x = 7; print('par') if x % 2 == 0 else print('impar')", False, "Paridade em uma linha."),
        _row("n = 10; print('verdadeiro') if n else print('falso')", False, "Truthiness."),

        _row("if idade >= 18 print('maior')", True, "Falta ':' após a condição."),
        _row("if idade => 18: print('maior')", True, "Operador inválido; use '>='."),
        _row("print 'maior' if True else print('menor')", True, "print precisa de parênteses."),
        _row("else: print('menor')", True, "else sem if."),
        _row("iff x > 0: print('ok')", True, "Palavra-chave errada."),
        _row("if x = 3: print('ok')", True, "Use '==' para comparar."),
    ]
    return pool, hint

def _pool_for() -> Tuple[List[Row], str]:
    hint = "for + range(): ':' e parênteses; corpo NUNCA na mesma linha (imprima em 2 linhas)."
    pool = [
        _row("for i in range(3):\n    print(i)", False, "Itera 0..2 e imprime."),
        _row("for c in 'py':\n    print(c)", False, "Itera sobre string."),
        _row("for i in range(1,4):\n    print(i)", False, "Faixa 1..3."),

        _row("for i in range 3:", True, "Faltam parênteses em range()."),
        _row("for(i in range(3)):", True, "Sintaxe estilo C não vale."),
        _row("for i = 0..2:", True, "Sintaxe não-Python."),
        _row("for i in range(3)", True, "Falta ':' no for."),
        _row("for i in 3:\n    print(i)", True, "Inteiro não é iterável."),
        _row("for i in range(3):\n    print i", True, "print precisa de parênteses."),
    ]
    return pool, hint

def _pool_while() -> Tuple[List[Row], str]:
    hint = "while ...: termine com ':'; corpo NUNCA na mesma linha; garanta atualizar a variável."
    pool = [
        _row("i = 0\nwhile i < 3:\n    i += 1", False, "Incrementa até 3."),
        _row("i = 3\nwhile i:\n    i -= 1", False, "Decrementa até 0."),

        _row("while i < 3", True, "Falta ':' no while."),
        _row("i = i + '1'", True, "Mistura int e str."),
        _row("i ++", True, "Não existe ++ em Python."),
        _row("whille i < 3:", True, "Palavra-chave errada."),
        _row("while i = 3:\n    i += 1", True, "Use '==' para comparar."),
    ]
    return pool, hint



def _pool_funcoes() -> Tuple[List[Row], str]:
    hint = "def nome(args): return ... ; chame com parênteses."
    pool = [
        _row("def soma(a,b): return a+b", False, "Função e retorno em uma linha."),
        _row("def eco(s): print(s)", False, "Sem retorno explícito (None)."),
        _row("def dobro(x=2): return x*2", False, "Parâmetro com default."),

        _row("def soma(a,b) return a+b", True, "Falta ':' em def."),
        _row("print soma(2,3)", True, "Chamada sem parênteses."),
        _row("def soma: (a,b)", True, "Sintaxe inválida."),
        _row("def f(x): retun x", True, "return escrito errado."),
        _row("def f x: return x", True, "Parênteses dos parâmetros faltando."),
    ]
    return pool, hint

# =====================================================================
# =======================  INTERMEDIÁRIO  ==============================
# =====================================================================

def _pool_fstrings() -> Tuple[List[Row], str]:
    hint = "f-strings: f\"...{expr:spec}...\"; formatação com : (., largura, alinhamento, % etc.)"
    pool = [
        _row("nome = 'Ana'; print(f\"Olá, {nome}\")", False, "Interpolação direta com f-string."),
        _row("x = 3.14159; print(f\"{x:.2f}\")", False, "Duas casas decimais .2f."),
        _row("s = 'py'; print(f\"{s:<10}\")", False, "Alinhamento à esquerda em largura 10."),
        _row("n = 7; print(f\"{n:04d}\")", False, "Zeros à esquerda com tipo inteiro d."),
        _row("p = 0.275; print(f\"{p:.0%}\")", False, "Percentual sem casas."),
        _row("x = 42; print(f\"{x=}\")", False, "Debug format: nome=valor."),
        _row("d = {'x': 10}; print(f\"{d['x']}\")", False, "Index por chave dentro da f-string."),
        _row("print(f\"{{}}\")", False, "Chaves literais são escapadas como {{ }}."),
        _row("n = 12000; print(f\"{n:,}\")", False, "Separador de milhar padrão."),
        _row("from datetime import datetime; dt = datetime(2020,1,2); print(f\"{dt:%Y-%m-%d}\")", False, "Formatação de data com %Y-%m-%d."),
        _row("n = 5; print(f\"{n:^6}\")", False, "Centraliza em 6 de largura."),
        _row("n = 5; print(f\"{n:+d}\")", False, "Mostra sinal sempre (+)."),

        _row("nome='Ana'; print(\"Olá, {}\" % nome)", True, "Operador % não é f-string (estilo antigo)."),
        _row("print(\"Olá, {}\".format{nome})", True, "Sintaxe de .format inválida (faltam parênteses)."),
        _row("x=3.14; print(f\"{x:.2}\")", True, "Falta o tipo numérico (ex.: .2f)."),
        _row("n=7; print(f\"{n:04}\")", True, "Em inteiros, use :04d para tipo inteiro."),
        _row("d={'x':10}; print(f\"{d.x}\")", True, "dict não tem atributo .x; use d['x']."),
        _row("from datetime import datetime; dt = datetime(2020,1,2); print(f\"{dt:YYYY-mm-dd}\")", True, "Spec de data inválida (use %Y-%m-%d)."),
        _row("n=12000; print(f\"{n:; ,}\")", True, "Spec inválido; use ',' após ':'."),
    ]
    return pool, hint

def _pool_metodos_string() -> Tuple[List[Row], str]:
    hint = "Principais: strip/lstrip/rstrip, upper/lower/casefold, startswith, split, join, replace, find/count."
    pool = [
        _row("s = '  py  '; print(s.strip())", False, "Remove espaços nas pontas."),
        _row("s = 'abc'; print(s.upper())", False, "Maiúsculas."),
        _row("s = 'python'; print(s.startswith('py'))", False, "Teste de prefixo."),
        _row("lst = ['a','b']; print(','.join(lst))", False, "Join é no separador."),
        _row("s = 'a,b,c'; print(s.split(','))", False, "Split por vírgula."),
        _row("s = 'a1a'; print(s.replace('a','b'))", False, "Substituição de substring."),
        _row("s = 'xyz'; print(s.find('x'))", False, "find retorna índice ou -1."),
        _row("s = 'banana'; print(s.count('a'))", False, "Conta ocorrências."),
        _row("s = 'um titulo'; print(s.title())", False, "Title case."),
        _row("s = '１２３'; print(s.isnumeric())", False, "isnumeric considera numerais largos também."),
        _row("s = 'Straße'; print(s.casefold())", False, "casefold forte p/ comparações."),

        _row("s = 'a b '; print(s.trim())", True, "trim() não existe em Python."),
        _row("s = 'abc'; print(upper(s))", True, "upper é método, não função livre."),
        _row("s = 'python'; print('py' in s[0])", True, "Index único; não testa prefixo."),
        _row("s = 'a,b'; print(split(',', s))", True, "Assinatura errada; use s.split(',')."),
        _row("s = 'abc'; print(s.swap('a','b'))", True, "swap() não existe."),
        _row("s = 'xyz'; print(s.index('x') if 'x' in s else -1)", False, "Também funciona (cuidado com ValueError em index)."),
        _row("s = 'ABC'; print(s.lowercase())", True, "lowercase() não existe; use lower() ou casefold()."),
        _row("s = ' abc '; print(s.stripleft())", True, "stripleft() não existe; use lstrip()."),
    ]
    return pool, hint

def _pool_listas() -> Tuple[List[Row], str]:
    hint = "Lista: append/extend/insert/remove/clear/sort; slicing [:] cópia rasa; sorted() retorna nova."
    pool = [
        _row("l = [1]; l.append(2)", False, "Adiciona 1 item."),
        _row("l = [1]; l.extend([2,3])", False, "Extende com vários."),
        _row("l = [1]; l.insert(0, 9)", False, "Insere na posição 0."),
        _row("l = [1,2,3]; print(l[-1])", False, "Último item com índice negativo."),
        _row("l = [1,2]; c = l[:]", False, "Cópia rasa com slice."),
        _row("l = [1,2,3]; r = l[::-1]", False, "Reverso sem alterar original."),
        _row("l = [3,1,2]; s = sorted(l)", False, "sorted cria nova lista ordenada."),
        _row("l = [3,1,2]; l.sort()", False, "Ordena in-place."),
        _row("l = [0,1,2,3]; print(l[:3])", False, "Primeiros 3 itens."),
        _row("l = [1,2,2,3]; l.remove(2)", False, "Remove primeira ocorrência."),
        _row("l = [1,2]; l.clear()", False, "Esvazia a lista."),
        _row("zeros = [0]*5", False, "Repete elemento 0 cinco vezes."),

        _row("l = []; l.add(1)", True, "List não tem add(); use append()."),
        _row("l = [1]; l.append([2,3])  # vira sublista", False, "append com lista cria sublista (às vezes intencional)."),
        _row("l=[1,2,3]; print(l[len(l)])", True, "Off-by-one; último é len(l)-1."),
        _row("l=[1,2,3]; reversed(l)[:]", True, "reversed retorna iterador; não indexa assim."),
        _row("l=[3,1,2]; sort(l)", True, "sort é método: l.sort()."),
        _row("print([i%2==0 for i in range(6)])", True, "Isso gera lista de bool; não é filtro de elementos."),
    ]
    return pool, hint

def _pool_tuplas() -> Tuple[List[Row], str]:
    hint = "Tupla é imutável; (1,) é tupla de 1 item; desempacotar a,b = (1,2)."
    pool = [
        _row("t = (1,)", False, "Tupla de 1 item precisa da vírgula."),
        _row("a,b = (1,2)", False, "Desempacotar em duas variáveis."),
        _row("t = (1,2,3); print(t[0])", False, "Index em tupla."),
        _row("a,b=(1,2); a,b=b,a", False, "Swap idiomático com tupla."),
        _row("l = [1,2]; t = tuple(l)", False, "Converte lista em tupla."),
        _row("t = tuple(range(3))", False, "Gera (0,1,2)."),
        _row("t = (1,2); u = (3,4); print(t+u)", False, "Concatena tuplas."),
        _row("print(2 in (1,2,3))", False, "Teste de pertinência."),
        _row("t = (1,2,2); print(t.count(2))", False, "Conta ocorrências."),
        _row("t = (1,2,3); print(len(t))", False, "Tamanho da tupla."),

        _row("t = (1,2); t[0] = 9", True, "Tupla é imutável; não pode atribuir item."),
        _row("(1)", True, "Sem vírgula vira int, não tupla."),
        _row("t.extend((3,))", True, "Tupla não tem extend()."),
    ]
    return pool, hint

def _pool_sets() -> Tuple[List[Row], str]:
    hint = "set sem duplicatas; operações: | união, & interseção, - diferença, ^ dif. simétrica."
    pool = [
        _row("s = set([1,1,2])  # {1,2}", False, "Constrói set removendo duplicatas."),
        _row("s = {1,2}; s.add(3)", False, "Adiciona elemento."),
        _row("s = {1,2}; print(2 in s)", False, "Pertinência."),
        _row("a = {1,2}; b = {2,3}; print(a | b)", False, "União."),
        _row("a = {1,2}; b = {2,3}; print(a & b)", False, "Interseção."),
        _row("a = {1,2}; b = {2,3}; print(a - b)", False, "Diferença."),
        _row("a = {1,2}; b = {2,3}; print(a ^ b)", False, "Diferença simétrica."),
        _row("s = {1,2}; s.discard(9)", False, "Remove sem erro se não existir."),
        _row("s = set()", False, "Set vazio."),
        _row("s = set([1,2,3])", False, "Lista -> set."),

        _row("s = {1,1,2}", False, "{} com itens iguais resulta {1,2} (ok)."),
        _row("s = []; s.add(1)", True, "Lista não tem add()."),
        _row("a={1}; b={2}; print(a + b)", True, "Soma não une sets; use |."),
        _row("s = {1}; s.remove(9)", True, "KeyError se não existir; prefira discard()."),
        _row("s = {1,2}; s.pop(1)", True, "pop() em set não aceita argumento."),
        _row("{}", True, "{} é dict vazio; set vazio é set()."),
    ]
    return pool, hint

def _pool_dicts() -> Tuple[List[Row], str]:
    hint = "dict: get/keys/values/items/setdefault/pop/clear; união 3.9+: d1|d2; comp {k:v for ...}. Em laços, corpo em 2 linhas."
    pool = [
        _row("d = {'x':1}; print(d.get('x',0))", False, "get com default sem erro."),
        _row("for k,v in {'a':1,'b':2}.items():\n    print(k,v)", False, "Itera pares k,v."),
        _row("d = {'x':1}; print(list(d.values()))", False, "Só valores."),
        _row("'x' in {'x':1}", False, "Teste de chave."),
        _row("d = {'k':1}; d.pop('k', None)", False, "Remove com default, sem erro."),
        _row("d1 = {'a':1}; d2 = {'b':2}; print(d1 | d2)", False, "União de dicts (3.9+)."),
        _row("d = {}; d.setdefault('k', []).append(1)", False, "Cria lista se faltar e usa."),
        _row("pares = [('a',1),('b',2)]; print({k:v for k,v in pares})", False, "Comprehension de dict."),
        _row("d = {'x':1}; c = d.copy()", False, "Cópia rasa de dict."),
        _row("d = {}; print(list(d.keys()))", False, "Lista de chaves."),
        _row("d = {'x':1}; d.clear()", False, "Limpa o dict."),

        _row("d = {}; d['x'] or 0", True, "Pode dar KeyError; use get()."),
        _row("merge(d1,d2)", True, "merge não é built-in."),
        _row("d.value('x',1)", True, "value() não existe; use get()."),
        _row("d.keys[]", True, "Sintaxe inválida; use list(d.keys())."),
        _row("d = {}.clear()", True, "{}.clear() retorna None; você perde o dict."),
    ]
    return pool, hint

def _pool_list_comprehensions() -> Tuple[List[Row], str]:
    hint = "Comprehensions: [expr for x in it if cond]; ordem correta em aninhadas."
    pool = [
        _row("squares = [i*i for i in range(5)]", False, "Quadrados 0..4."),
        _row("pares = [i for i in range(10) if i%2==0]", False, "Filtro no final."),
        _row("pos = [x if x>0 else 0 for x in a]", False, "if-else na expressão."),
        _row("flat = [x for row in m for x in row]", False, "Flatten em ordem correta."),
        _row("s = {x for x in a}", False, "Set comprehension."),
        _row("aplic = [f(x) for x in a]", False, "Equivalente a map em muitos casos."),
        _row("vazia = []", False, "Lista vazia (não é comp, mas é ok)."),
        _row("idxs = [i for i,_ in enumerate(a)]", False, "Usa enumerate."),

        _row("[i**2: i in range(5)]", True, "Sintaxe inválida de comp."),
        _row("[i if i%2==0 for i in range(10)]", True, "Ordem errada do if."),
        _row("[x for x in 10]", True, "10 não é iterável."),
        _row("[x for x in row for row in m]", True, "Ordem das cláusulas invertida."),
        _row("map(f,a)[]", True, "Index inválido em map; converta com list(map(...))."),
        _row("[map(f,a)]", True, "Isso cria lista com um iterador dentro."),
        _row("[ for x in a ]", True, "Comp vazia inválida."),
        _row("[x if x>0 and x%2==0 in a]", True, "Condição mal posicionada."),
    ]
    return pool, hint

def _pool_tratamento_erros() -> Tuple[List[Row], str]:
    hint = "try/except/finally em até 2 linhas; raise ValueError('msg')."
    pool = [
        _row("try: x = int('3')\nexcept ValueError: print('value')", False, "Captura específica."),
        _row("try: x = 1/0\nexcept ZeroDivisionError: x = 0", False, "Fallback em divisão por zero."),
        _row("try: f()\nfinally: print('sempre')", False, "finally sempre executa."),
        _row("raise ValueError('msg')", False, "Lança exceção explícita."),
        _row("try: f()\nexcept Exception as e: print(e)", False, "Captura genérica (use com cuidado)."),

        _row("try: f()\ncatch Exception: pass", True, "Em Python é 'except', não 'catch'."),
        _row("except()", True, "Sintaxe inválida de except."),
        _row("raise('msg')", True, "raise exige uma exceção, não string."),
        _row("except ValueError as:", True, "Falta o nome após 'as'."),
        _row("try: pass", True, "try sem except/finally."),
    ]
    return pool, hint

# =====================================================================
# ========================  ROTEADOR / API  ============================
# =====================================================================

# Tópicos de Fase — nomes EXATOS (após os ':')
_FASES = [
    None,  # índice 0 não usado
    "Saída de dados com print()",
    "Entrada de dados com input()",
    "Variáveis e Tipos Simples",
    "Operadores Aritméticos e Relacionais",
    "Estruturas Condicionais (if/else)",
    "Estruturas de Repetição (for)",
    "Estrutura de Repetição (while)",
    "Funções Simples",
    "f-strings e formatação",
    "Métodos de string",
    "Listas (métodos e slicing)",
    "Tuplas e imutabilidade",
    "Conjuntos (set)",
    "Dicionários",
    "List Comprehensions",
    "Tratamento de Erros",
]


def get_topic_for_fase(fase_id: int) -> str:
    """Retorna o título de tópico (string) para a fase 1..16."""
    try:
        if 1 <= int(fase_id) <= 16:
            return _FASES[int(fase_id)]
    except Exception:
        pass
    return _FASES[1]

def _pool_by_topic(topic_title: str) -> Tuple[List[Row], str]:
    """Roteia por título EXATO (normalizado) — mesmo padrão da Cobrinha."""
    t = _norm(topic_title or "")

    ROUTER = {
        _norm("Saída de dados com print()"): _pool_print,
        _norm("Entrada de dados com input()"): _pool_input,
        _norm("Variáveis e Tipos Simples"): _pool_variaveis,
        _norm("Operadores Aritméticos e Relacionais"): _pool_operadores,
        _norm("Estruturas Condicionais (if/else)"): _pool_if,
        _norm("Estruturas de Repetição (for)"): _pool_for,
        _norm("Estrutura de Repetição (while)"): _pool_while,
        _norm("Funções Simples"): _pool_funcoes,

        _norm("f-strings e formatação"): _pool_fstrings,
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
    # fallback seguro (igual cobrinha cai no print se o título vier errado)
    return _pool_print()

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

# opcional: atalho por fase, se quiser usar direto
def get_pyfoot_questions_by_fase(fase_id: int, rounds: int = 12) -> List[Dict]:
    return get_pyfoot_questions(get_topic_for_fase(fase_id), rounds)
