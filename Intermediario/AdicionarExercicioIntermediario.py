from Iniciante.Persistencia.Entidade.Exercicio import Exercicio
from Iniciante.Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl

exercicios = [
    # ========================== FASE 9: f-strings e formatação ==========================
    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Dica: Coloque um 'f' antes das aspas e use { } para inserir variáveis.",
        pergunta="Qual destas opções usa f-string corretamente para exibir a variável nome?",
        tipo="objetiva", resposta_certa='print(f"Olá, {nome}")',
        resposta_erradas='print("Olá, {nome}")|print(f"Olá, nome")|print("fOlá, {nome}")'),

    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Use f-strings para formatar com 2 casas decimais.",
        pergunta="Como exibir a variável preco com duas casas decimais usando f-string?",
        tipo="objetiva", resposta_certa='print(f"Preço: {preco:.2f}")',
        resposta_erradas='print("Preço: {preco:.2f}")|print(f"Preço: preco.2f")|print(f"Preço: {preco:2}")'),

    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Use f-string e substitua o ponto por vírgula se necessário.",
        pergunta="Dissertativa: Receba um número decimal via input() e exiba no formato R$ valor, com vírgula. Considere que o usuário digita 10.5.",
        tipo="dissertativa", resposta_certa='R$ 10.50',
        resposta_erradas=None, entrada_teste='10.5'),

    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Exiba texto e resultado na mesma linha usando f-string.",
        pergunta="Dissertativa: Receba dois números e exiba 'Soma: <resultado>' usando f-string. Considere que o usuário digita 3 e 4.",
        tipo="dissertativa", resposta_certa='Soma: 7',
        resposta_erradas=None, entrada_teste='3\n4'),

    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Arraste para formar a f-string correta.",
        pergunta="Drag&Drop: Monte a f-string para exibir 'Idade: <idade>'.",
        tipo="dragdrop", resposta_certa="print(f'Idade: {idade}')",
        resposta_erradas="print('Idade: {idade}')|print(f'Idade: idade')|print(f'Idade {idade}')"),

    Exercicio(id_exercicio=None, id_fase=9,
        dicas="Arraste para formatar com 2 casas decimais.",
        pergunta="Drag&Drop: Monte a f-string para exibir 'Valor: <v>' com 2 casas.",
        tipo="dragdrop", resposta_certa="print(f'Valor: {v:.2f}')",
        resposta_erradas="print('Valor: {v:.2f}')|print(f'Valor: v.2f')|print(f'Valor {v:2}')"),

    # ========================== FASE 10: Métodos de string ==========================
    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Método para deixar tudo maiúsculo.",
        pergunta="Qual método deixa todo o texto em maiúsculas?",
        tipo="objetiva", resposta_certa="upper()",
        resposta_erradas="capitalize()|title()|max()"),

    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Método para separar em lista por espaços.",
        pergunta="Qual método divide a string em uma lista de palavras?",
        tipo="objetiva", resposta_certa="split()",
        resposta_erradas="join()|replace()|separate()"),

    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Combine strip() e title().",
        pergunta="Dissertativa: Receba um nome com espaços extras e exiba com a primeira letra maiúscula. Considere que o usuário digita '  maria silva  '.",
        tipo="dissertativa", resposta_certa='Maria Silva',
        resposta_erradas=None, entrada_teste='  maria silva  '),

    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Use replace() para trocar partes da string.",
        pergunta="Dissertativa: Receba um texto e troque 'Python' por 'Java'. Considere que o usuário digita 'Eu gosto de Python'.",
        tipo="dissertativa", resposta_certa='Eu gosto de Java',
        resposta_erradas=None, entrada_teste='Eu gosto de Python'),

    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Arraste para juntar lista em string separada por vírgulas.",
        pergunta="Drag&Drop: Monte o código para unir lista nomes em string separada por ', '.",
        tipo="dragdrop", resposta_certa="', '.join(nomes)",
        resposta_erradas="' '.join(nomes)|', '.split(nomes)|join(nomes)"),

    Exercicio(id_exercicio=None, id_fase=10,
        dicas="Arraste para remover espaços extras nas pontas.",
        pergunta="Drag&Drop: Monte o código para remover espaços no início e fim da string s.",
        tipo="dragdrop", resposta_certa="s.strip()",
        resposta_erradas="strip(s)|s.remove()|trim(s)"),

    # ========================== FASE 11: Listas (métodos e slicing) ==========================
    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Adiciona item ao final da lista.",
        pergunta="Qual método adiciona um item ao final da lista?",
        tipo="objetiva", resposta_certa="append()",
        resposta_erradas="add()|push()|insert()"),

    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Ordena lista em ordem crescente.",
        pergunta="Qual método ordena a lista em ordem crescente?",
        tipo="objetiva", resposta_certa="sort()",
        resposta_erradas="order()|reverse()|sorted()"),

    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Use slicing para pegar primeiros 3 elementos.",
        pergunta="Dissertativa: Receba uma lista nums e exiba apenas os 3 primeiros elementos. Considere nums = [1,2,3,4,5].",
        tipo="dissertativa", resposta_certa='[1, 2, 3]',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Remova elemento da lista.",
        pergunta="Dissertativa: Receba uma lista nums e remova o valor 3. Considere nums = [1,3,5].",
        tipo="dissertativa", resposta_certa='[1, 5]',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Arraste para inverter a lista.",
        pergunta="Drag&Drop: Monte o código para inverter a lista nums.",
        tipo="dragdrop", resposta_certa="nums.reverse()",
        resposta_erradas="reverse(nums)|nums.invert()|nums[::-2]"),

    Exercicio(id_exercicio=None, id_fase=11,
        dicas="Arraste para ordenar lista de trás para frente.",
        pergunta="Drag&Drop: Monte o código para ordenar nums em ordem decrescente.",
        tipo="dragdrop", resposta_certa="nums.sort(reverse=True)",
        resposta_erradas="nums.sort(desc=True)|sort(nums, rev=True)|nums[::-1].sort()"),

    # ========================== FASE 12: Tuplas e imutabilidade ==========================
    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Usa parênteses para criar.",
        pergunta="Qual comando cria uma tupla com 1 e 2?",
        tipo="objetiva", resposta_certa="(1, 2)",
        resposta_erradas="[1, 2]|{1, 2}|tuple[1, 2]"),

    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Método para contar ocorrências em tupla.",
        pergunta="Qual método conta quantas vezes um valor aparece em uma tupla?",
        tipo="objetiva", resposta_certa="count()",
        resposta_erradas="index()|len()|find()"),

    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Troque valores usando tupla.",
        pergunta="Dissertativa: Troque os valores de a e b usando tupla. Considere a=1, b=2.",
        tipo="dissertativa", resposta_certa='2 1',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Acesse elemento pelo índice.",
        pergunta="Dissertativa: Crie tupla t=(10,20,30) e exiba o valor no índice 1.",
        tipo="dissertativa", resposta_certa='20',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Arraste para criar tupla com único valor 5.",
        pergunta="Drag&Drop: Monte o código para criar tupla com um único elemento 5.",
        tipo="dragdrop", resposta_certa="(5,)",
        resposta_erradas="(5)|tuple(5)|[5]"),

    Exercicio(id_exercicio=None, id_fase=12,
        dicas="Arraste para acessar elemento 0 da tupla t.",
        pergunta="Drag&Drop: Monte o código para acessar primeiro elemento da tupla t.",
        tipo="dragdrop", resposta_certa="t[0]",
        resposta_erradas="t.get(0)|t.index(0)|first(t)"),

    # ========================== FASE 13: Conjuntos (set) ==========================
    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Usa chaves e valores únicos.",
        pergunta="Qual comando cria um conjunto com 1,2,3?",
        tipo="objetiva", resposta_certa="{1, 2, 3}",
        resposta_erradas="[1, 2, 3]|(1, 2, 3)|set[1, 2, 3]"),

    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Operador para união de conjuntos.",
        pergunta="Qual operador representa a união de dois conjuntos?",
        tipo="objetiva", resposta_certa="|",
        resposta_erradas="&|-|+" ),

    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Use & para interseção.",
        pergunta="Dissertativa: Dado A={1,2} e B={2,3}, exiba a interseção.",
        tipo="dissertativa", resposta_certa='{2}',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Use - para diferença.",
        pergunta="Dissertativa: Dado A={1,2,3} e B={2}, exiba A-B.",
        tipo="dissertativa", resposta_certa='{1, 3}',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Arraste para adicionar elemento 5 no set s.",
        pergunta="Drag&Drop: Monte o código para adicionar 5 ao conjunto s.",
        tipo="dragdrop", resposta_certa="s.add(5)",
        resposta_erradas="add(s,5)|s.push(5)|s.append(5)"),

    Exercicio(id_exercicio=None, id_fase=13,
        dicas="Arraste para remover elemento 2 do set s.",
        pergunta="Drag&Drop: Monte o código para remover 2 do conjunto s.",
        tipo="dragdrop", resposta_certa="s.remove(2)",
        resposta_erradas="s.del(2)|remove(s,2)|s.pop(2)"),

    # ========================== FASE 14: Dicionários ==========================
    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Usa chaves e pares chave:valor.",
        pergunta="Qual comando cria dicionário com nome='Ana'?",
        tipo="objetiva", resposta_certa="{'nome': 'Ana'}",
        resposta_erradas="{nome: 'Ana'}|[nome:'Ana']|dict(nome='Ana')"),

    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Método para acessar apenas as chaves.",
        pergunta="Qual método retorna as chaves de um dicionário?",
        tipo="objetiva", resposta_certa="keys()",
        resposta_erradas="values()|items()|get_keys()"),

    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Acesse valor pela chave.",
        pergunta="Dissertativa: Crie dict pessoa={'idade':30} e exiba idade.",
        tipo="dissertativa", resposta_certa='30',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Itere sobre itens.",
        pergunta="Dissertativa: Dado dict cores={'a':'azul'}, exiba chave e valor.",
        tipo="dissertativa", resposta_certa='a azul',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Arraste para adicionar chave 'cidade' com valor 'SP'.",
        pergunta="Drag&Drop: Monte o código para adicionar ao dict d.",
        tipo="dragdrop", resposta_certa="d['cidade'] = 'SP'",
        resposta_erradas="d.add('cidade','SP')|add(d,'cidade','SP')|d.cidade='SP'"),

    Exercicio(id_exercicio=None, id_fase=14,
        dicas="Arraste para remover chave 'idade' do dict d.",
        pergunta="Drag&Drop: Monte o código para remover 'idade' do d.",
        tipo="dragdrop", resposta_certa="del d['idade']",
        resposta_erradas="d.remove('idade')|remove(d,'idade')|d.popitem('idade')"),

    # ========================== FASE 15: List Comprehensions ==========================
    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Usa colchetes e for dentro.",
        pergunta="Qual list comprehension cria lista de 0 a 4?",
        tipo="objetiva", resposta_certa="[x for x in range(5)]",
        resposta_erradas="[x in range(5)]|list(x) for x in range(5)|[for x in range(5)]"),

    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Adicione condicional no final.",
        pergunta="Qual list comprehension cria lista com números pares até 5?",
        tipo="objetiva", resposta_certa="[x for x in range(6) if x % 2 == 0]",
        resposta_erradas="[x if x%2==0 for x in range(6)]|[x for x in range(6) where x%2==0]|[x for x in range(6) && x%2==0]"),

    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Filtre números maiores que 3.",
        pergunta="Dissertativa: Crie lista [1,2,3,4,5] e gere outra só com >3.",
        tipo="dissertativa", resposta_certa='[4, 5]',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Eleve ao quadrado usando list comprehension.",
        pergunta="Dissertativa: Crie lista com quadrados de 1 a 3.",
        tipo="dissertativa", resposta_certa='[1, 4, 9]',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Arraste para criar lista com dobro dos números de nums.",
        pergunta="Drag&Drop: Monte a list comprehension.",
        tipo="dragdrop", resposta_certa="[x*2 for x in nums]",
        resposta_erradas="[x for x in nums*2]|[x*2 in nums]|[for x in nums: x*2]"),

    Exercicio(id_exercicio=None, id_fase=15,
        dicas="Arraste para criar lista com letras maiúsculas de lista letras.",
        pergunta="Drag&Drop: Monte a list comprehension.",
        tipo="dragdrop", resposta_certa="[l.upper() for l in letras]",
        resposta_erradas="[upper(l) for l in letras]|[l.upper(letras)]|[l for letras.upper()]"),

    # ========================== FASE 16: Tratamento de Erros ==========================
    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Captura exceções.",
        pergunta="Qual palavra-chave inicia um bloco de tratamento de erros?",
        tipo="objetiva", resposta_certa="try",
        resposta_erradas="catch|except|error"),

    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Captura exceção específica.",
        pergunta="Qual sintaxe captura especificamente ValueError?",
        tipo="objetiva", resposta_certa="except ValueError:",
        resposta_erradas="catch ValueError:|except(ValueError)|except ValueError"),

    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Capture erro de conversão.",
        pergunta="Dissertativa: Receba um valor e tente converter para int, exibindo 'Erro' se falhar. Considere entrada 'abc'.",
        tipo="dissertativa", resposta_certa='Erro',
        resposta_erradas=None, entrada_teste='abc'),

    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Use finally para sempre executar.",
        pergunta="Dissertativa: Exiba 'Fim' no bloco finally, independentemente de erro.",
        tipo="dissertativa", resposta_certa='Fim',
        resposta_erradas=None),

    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Arraste para capturar qualquer erro e exibir mensagem.",
        pergunta="Drag&Drop: Monte o try/except para capturar erro genérico e imprimir 'Erro'.",
        tipo="dragdrop", resposta_certa="try:|    ...|except:|    print('Erro')",
        resposta_erradas="try:|    print('Erro')|except|..."),

    Exercicio(id_exercicio=None, id_fase=16,
        dicas="Arraste para capturar ZeroDivisionError e exibir 'Divisão inválida'.",
        pergunta="Drag&Drop: Monte o código.",
        tipo="dragdrop", resposta_certa="try:|    ...|except ZeroDivisionError:|    print('Divisão inválida')",
        resposta_erradas="try|except ZeroDivisionError|print('Divisão inválida')|..."),
]

# Inserção no banco
persistencia = ExercicioPersistenciaImpl()
for e in exercicios:
    persistencia.salvar(e)
