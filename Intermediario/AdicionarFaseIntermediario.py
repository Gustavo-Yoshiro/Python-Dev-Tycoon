from Iniciante.Persistencia.Entidade.Fase import Fase
from Iniciante.Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

fases = [
    Fase(None, "intermediario", "f-strings e formatação",
         "As f-strings são como molduras mágicas que transformam variáveis em texto! Elas permitem inserir valores diretamente dentro das strings de forma super simples. Basta colocar um 'f' antes das aspas e usar {chaves} para incluir variáveis ou até fazer contas!\nExemplo:\npreco = 10.5\nquantidade = 3\nprint(f\"O preço é R$ {preco:.2f}\")\nSaída: O preço é R$ 10.50\n\nprint(f\"Total: R$ {preco * quantidade:.2f}\")\nSaída: Total: R$ 31.50\n\nnome = \"Carlos\"\nidade = 30\nprint(f\"{nome} tem {idade} anos e paga R$ {preco} por item\")\nSaída: Carlos tem 30 anos e paga R$ 10.5 por item"),

    Fase(None, "intermediario", "Métodos de string",
         "Strings têm superpoderes especiais chamados métodos! São como ferramentas que transformam e analisam textos. Você pode deixar tudo maiúsculo, minúsculo, trocar palavras, separar frases e muito mais!\nExemplo:\ntexto = \"Python é divertido\"\nprint(texto.upper())\nSaída: PYTHON É DIVERTIDO\n\nprint(texto.replace(\"divertido\", \"incrível\"))\nSaída: Python é incrível\n\nfrase = \"maçã,banana,uva\"\nfrutas = frase.split(\",\")\nprint(frutas)\nSaída: ['maçã', 'banana', 'uva']\n\nlista = [\"Python\", \"Java\", \"C++\"]\nresultado = \" e \".join(lista)\nprint(resultado)\nSaída: Python e Java e C++"),

    Fase(None, "intermediario", "Listas (métodos e slicing)",
         "Listas são como caixas organizadoras que você pode rearrumar! Com métodos especiais, você pode adicionar, remover, ordenar e até pegar pedaços (fatias) da lista. O slicing usa [início:fim:passo] para selecionar partes!\nExemplo:\nnums = [3, 1, 4, 1, 5]\nnums.append(9)  # adiciona no final\nprint(nums)\nSaída: [3, 1, 4, 1, 5, 9]\n\nnums.sort()  # ordena a lista\nprint(nums)\nSaída: [1, 1, 3, 4, 5, 9]\n\nprint(nums[1:4])  # pega do índice 1 ao 3\nSaída: [1, 3, 4]\n\nprint(nums[::2])  # pega cada segundo elemento\nSaída: [1, 4, 9]"),

    Fase(None, "intermediario", "Tuplas e imutabilidade",
         "Tuplas são como listas congeladas - depois de criadas, não podem ser mudadas! São perfeitas para guardar dados que não devem ser alterados, como coordenadas, configurações ou informações fixas.\nExemplo:\ncoordenadas = (10, 20)\nprint(coordenadas[0])\nSaída: 10\n\ncores_rgb = (255, 128, 0)  # laranja\nprint(f\"R: {cores_rgb[0]}, G: {cores_rgb[1]}, B: {cores_rgb[2]}\")\nSaída: R: 255, G: 128, B: 0\n\n# Tentar modificar dá erro:\n# coordenadas[0] = 15  # Isso causaria TypeError!"),

    Fase(None, "intermediario", "Conjuntos (set)",
         "Conjuntos são como sacolas mágicas que não guardam coisas repetidas! Eles automaticamente removem duplicatas e permitem operações matemáticas como união, interseção e diferença.\nExemplo:\na = {1, 2, 3, 3, 2}  # duplicatas são removidas\nprint(a)\nSaída: {1, 2, 3}\n\nb = {3, 4, 5}\nprint(a | b)  # união: todos os elementos\nSaída: {1, 2, 3, 4, 5}\n\nprint(a & b)  # interseção: elementos comuns\nSaída: {3}\n\nprint(a - b)  # diferença: só em A\nSaída: {1, 2}"),

    Fase(None, "intermediario", "Dicionários",
         "Dicionários são como agendas telefônicas - cada nome (chave) tem um número (valor)! São perfeitos para organizar informações com identificadores únicos e acessar dados rapidamente.\nExemplo:\npessoa = {\"nome\": \"Ana\", \"idade\": 25, \"cidade\": \"São Paulo\"}\nprint(pessoa[\"nome\"])\nSaída: Ana\n\npessoa[\"profissão\"] = \"Programadora\"  # adiciona nova chave\nprint(pessoa)\nSaída: {'nome': 'Ana', 'idade': 25, 'cidade': 'São Paulo', 'profissão': 'Programadora'}\n\nfor chave, valor in pessoa.items():\n    print(f\"{chave}: {valor}\")\nSaída:\nnome: Ana\nidade: 25\ncidade: São Paulo\nprofissão: Programadora"),

    Fase(None, "intermediario", "List Comprehensions",
         "List Comprehensions são como receitas expressas para criar listas! Em uma única linha você pode transformar, filtrar e criar listas complexas. É como uma mini-fábrica de listas!\nExemplo:\nnums = [1, 2, 3, 4, 5]\nquadrados = [n * n for n in nums]\nprint(quadrados)\nSaída: [1, 4, 9, 16, 25]\n\npares_quadrados = [n*n for n in nums if n % 2 == 0]\nprint(pares_quadrados)\nSaída: [4, 16]\n\nnomes = [\"ana\", \"carlos\", \"bia\"]\nnomes_maiusculos = [nome.upper() for nome in nomes]\nprint(nomes_maiusculos)\nSaída: ['ANA', 'CARLOS', 'BIA']"),

    Fase(None, "intermediario", "Tratamento de Erros",
         "Tratamento de erros é como um paraquedas para seu programa - impede que ele caia quando algo dá errado! Com try/except, você pode capturar erros e lidar com eles graciosamente, sem travar o programa.\nExemplo:\ntry:\n    numero = int(\"abc\")  # isso vai dar erro!\nexcept ValueError:\n    print(\"Valor inválido! Digite um número.\")\nSaída: Valor inválido! Digite um número.\n\ntry:\n    lista = [1, 2, 3]\n    print(lista[10])  # índice que não existe\nexcept IndexError:\n    print(\"Índice fora da lista!\")\nSaída: Índice fora da lista!\n\ntry:\n    x = 10 / 0  # divisão por zero\nexcept ZeroDivisionError:\n    print(\"Não é possível dividir por zero!\")\nSaída: Não é possível dividir por zero!")
]

persistencia = FasePersistenciaImpl()
for fase in fases:
    persistencia.salvar(fase)