from Iniciante.Persistencia.Entidade.Fase import Fase
from Iniciante.Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

fases = [
    Fase(None, "intermediario", "f-strings e formatação",
         "f-strings permitem inserir valores e expressões dentro do texto de forma simples. "
         "Basta colocar um f antes da string e usar {chaves}. Também dá para formatar números "
         "com casas decimais, largura e alinhamento.\n"
         "Exemplos:\n"
         "preco = 10.5\n"
         "print(f\"Preço: R$ {preco:.2f}\")\n"
         "Saída: Preço: R$ 10.50\n\n"
         "quantidade = 3\n"
         "print(f\"Total: R$ {preco * quantidade:.2f}\")\n"
         "Saída: Total: R$ 31.50\n\n"
         "nome = \"Carlos\"; idade = 30\n"
         "print(f\"{nome} tem {idade} anos\")\n"
         "Saída: Carlos tem 30 anos"),

    Fase(None, "intermediario", "Métodos de string",
         "Strings têm métodos úteis para transformar e analisar texto: upper/lower, replace, split, join, startswith, "
         "entre outros. Use-os para padronizar, separar e montar frases.\n"
         "Exemplos:\n"
         "texto = \"Python é divertido\"\n"
         "print(texto.upper())\n"
         "Saída: PYTHON É DIVERTIDO\n\n"
         "frase = \"maçã,banana,uva\"\n"
         "print(frase.split(\",\"))\n"
         "Saída: ['maçã', 'banana', 'uva']\n\n"
         "lings = [\"Python\", \"Java\", \"C++\"]\n"
         "print(\" e \".join(lings))\n"
         "Saída: Python e Java e C++"),

    Fase(None, "intermediario", "Listas (métodos e slicing)",
         "Listas são sequências mutáveis: você pode adicionar, remover e ordenar. "
         "O slicing [inicio:fim:passo] retorna fatias da lista sem alterar o original.\n"
         "Exemplos:\n"
         "nums = [3, 1, 4, 1, 5]\n"
         "nums.append(9); print(nums)\n"
         "Saída: [3, 1, 4, 1, 5, 9]\n\n"
         "nums.sort(); print(nums)\n"
         "Saída: [1, 1, 3, 4, 5, 9]\n\n"
         "print(nums[1:4]); print(nums[::2])\n"
         "Saídas:\n"
         "[1, 3, 4]\n"
         "[1, 4, 9]"),

    Fase(None, "intermediario", "Tuplas e imutabilidade",
         "Tuplas são sequências imutáveis: depois de criadas, não mudam. "
         "São boas para dados fixos (coordenadas, cores) e suportam indexação e desempacotamento.\n"
         "Exemplos:\n"
         "coordenadas = (10, 20)\n"
         "print(coordenadas[0])\n"
         "Saída: 10\n\n"
         "cores = (255, 128, 0)\n"
         "print(f\"R: {cores[0]}, G: {cores[1]}, B: {cores[2]}\")\n"
         "Saída: R: 255, G: 128, B: 0\n\n"
         "# coordenadas[0] = 15  # TypeError (tuplas são imutáveis)"),

    Fase(None, "intermediario", "Conjuntos (set)",
         "Sets guardam elementos sem duplicatas e permitem operações de conjunto como união (|), "
         "interseção (&) e diferença (-). Ótimos para remover repetidos e comparar coleções.\n"
         "Exemplos:\n"
         "a = {1, 2, 3, 3, 2}; print(a)\n"
         "Saída: {1, 2, 3}\n\n"
         "b = {3, 4, 5}\n"
         "print(a | b)  # união\n"
         "Saída: {1, 2, 3, 4, 5}\n\n"
         "print(a & b); print(a - b)\n"
         "Saídas:\n"
         "{3}\n"
         "{1, 2}"),

    Fase(None, "intermediario", "Dicionários",
         "Dicionários mapeiam chaves para valores. Você pode incluir novas chaves, acessar valores, "
         "iterar por itens e copiar/limpar facilmente. Muito usados para dados nomeados.\n"
         "Exemplos:\n"
         "pessoa = {\"nome\": \"Ana\", \"idade\": 25, \"cidade\": \"São Paulo\"}\n"
         "print(pessoa[\"nome\"])\n"
         "Saída: Ana\n\n"
         "pessoa[\"profissão\"] = \"Programadora\"; print(pessoa)\n"
         "Saída: {'nome': 'Ana', 'idade': 25, 'cidade': 'São Paulo', 'profissão': 'Programadora'}\n\n"
         "for k, v in pessoa.items():\n"
         "    print(f\"{k}: {v}\")\n"
         "Saída:\n"
         "nome: Ana\nidade: 25\ncidade: São Paulo\nprofissão: Programadora"),

    Fase(None, "intermediario", "List Comprehensions",
         "List comprehensions criam listas de forma compacta, transformando e filtrando elementos em uma linha, "
         "sem perder legibilidade.\n"
         "Exemplos:\n"
         "nums = [1, 2, 3, 4, 5]\n"
         "print([n*n for n in nums])\n"
         "Saída: [1, 4, 9, 16, 25]\n\n"
         "print([n*n for n in nums if n % 2 == 0])\n"
         "Saída: [4, 16]\n\n"
         "nomes = [\"ana\", \"carlos\", \"bia\"]\n"
         "print([nome.upper() for nome in nomes])\n"
         "Saída: ['ANA', 'CARLOS', 'BIA']"),

    Fase(None, "intermediario", "Tratamento de Erros",
         "Use try/except para capturar exceções e manter o programa estável. "
         "Trate casos previsíveis (ValueError, IndexError, ZeroDivisionError) e informe o usuário.\n"
         "Exemplos:\n"
         "try:\n"
         "    numero = int(\"abc\")\n"
         "except ValueError:\n"
         "    print(\"Valor inválido! Digite um número.\")\n"
         "Saída: Valor inválido! Digite um número.\n\n"
         "try:\n"
         "    lista = [1, 2, 3]\n"
         "    print(lista[10])\n"
         "except IndexError:\n"
         "    print(\"Índice fora da lista!\")\n"
         "Saída: Índice fora da lista!\n\n"
         "try:\n"
         "    x = 10 / 0\n"
         "except ZeroDivisionError:\n"
         "    print(\"Não é possível dividir por zero!\")\n"
         "Saída: Não é possível dividir por zero!")
]

persistencia = FasePersistenciaImpl()
for fase in fases:
    persistencia.salvar(fase)
