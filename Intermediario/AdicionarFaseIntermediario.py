from Iniciante.Persistencia.Entidade.Fase import Fase
from Iniciante.Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

fases = [
    Fase(None, "intermediario", "f-strings e formatação",
         "As f-strings permitem inserir variáveis e expressões diretamente dentro de strings de forma simples e legível. Você coloca um f antes das aspas e usa { } para incluir variáveis ou expressões.\nExemplo:\npreco = 10.5\nprint(f\"O preço é R$ {preco:.2f}\")"),

    Fase(None, "intermediario", "Métodos de string",
         "Strings possuem métodos úteis para modificar ou analisar textos. Por exemplo: upper() para deixar tudo maiúsculo, lower() para minúsculo, replace() para trocar partes, split() para separar em lista e join() para juntar listas em uma string.\nExemplo:\ntexto = \"Python é divertido\"\nprint(texto.upper())"),

    Fase(None, "intermediario", "Listas (métodos e slicing)",
         "Listas são coleções que podem ser modificadas. Métodos como append() adicionam, remove() retira, sort() ordena e reverse() inverte. Também é possível acessar fatias com slicing usando colchetes.\nExemplo:\nnums = [3, 1, 4]\nnums.sort()\nprint(nums[0:2])"),

    Fase(None, "intermediario", "Tuplas e imutabilidade",
         "Tuplas são como listas, mas não podem ser alteradas após criadas (imutáveis). São criadas com parênteses e usadas para agrupar dados que não mudarão.\nExemplo:\ncoordenadas = (10, 20)\nprint(coordenadas[0])"),

    Fase(None, "intermediario", "Conjuntos (set)",
         "Sets armazenam valores únicos e não ordenados. Permitem operações de união (|), interseção (&) e diferença (-).\nExemplo:\na = {1, 2, 3}\nb = {3, 4, 5}\nprint(a | b)"),

    Fase(None, "intermediario", "Dicionários",
         "Dicionários armazenam pares chave-valor. É possível acessar valores pela chave, adicionar e remover itens e percorrer com .keys(), .values() ou .items().\nExemplo:\npessoa = {\"nome\": \"Ana\", \"idade\": 25}\nprint(pessoa[\"nome\"])"),

    Fase(None, "intermediario", "List Comprehensions",
         "List Comprehensions permitem criar listas de forma compacta, com ou sem condição. São úteis para transformar e filtrar dados em uma única linha.\nExemplo:\nnums = [1, 2, 3, 4]\npares_quadrados = [n*n for n in nums if n % 2 == 0]\nprint(pares_quadrados)"),

    Fase(None, "intermediario", "Tratamento de Erros",
         "O tratamento de erros permite que o programa lide com situações inesperadas sem parar de funcionar. Usamos try/except para capturar erros, else para executar caso não haja erro e finally para executar sempre.\nExemplo:\ntry:\n    x = int(\"abc\")\nexcept ValueError:\n    print(\"Valor inválido\")")
]

persistencia = FasePersistenciaImpl()
for fase in fases:
    persistencia.salvar(fase)
