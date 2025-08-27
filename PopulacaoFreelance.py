# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def popular_projetos(projeto_service: ProjetoFreelanceServiceImpl):
    """
    Insere uma lista extensa e variada de projetos de freelance no banco de dados.
    """
    # Limpa projetos antigos para garantir uma lista sempre nova de desafios
    if projeto_service.listar_projetos_para_jogador(None): # Passa None para simplificar a verificação
        print("Projetos já existem. Limpando a lista antiga...")
        projeto_service.deletar_todos_projetos()

    print("Inserindo uma nova lista de 39 projetos de freelance...")

    projetos = [
        # --- Cliente: InovaTech Solutions (ID 1) ---
        ProjetoFreelance(None, 1, 'Validador de Senha Simples', 'Verifica se uma senha tem mais de 8 caracteres.', 'Iniciante', 180.00, 'disponivel', 2, 1, 1, 'len(), if/else', None, 2, 'completar', 'def senha_e_forte(senha):\n    # Verifique se o comprimento da senha é maior que 8\n    if ...:\n        return True\n    else:\n        return False', '[{"entrada_funcao": ["senha1234"], "saida_esperada": "True"}]'),
        ProjetoFreelance(None, 1, 'Gerador de API Key', 'Cria uma chave de API aleatória com 16 caracteres alfanuméricos.', 'Intermediario', 550.00, 'disponivel', 4, 1, 2, 'random, string', None, 5, 'do_zero', 'import random\nimport string\ndef gerar_api_key():\n    # Gere uma string aleatória de 16 caracteres\n    # SEU CÓDIGO AQUI\n    return ""', '[{"check_type": "length", "expected": 16}]'),
        ProjetoFreelance(None, 1, 'Otimizador de Loop de Busca', 'O código atual para encontrar um usuário é muito lento. Refatore-o para ser mais eficiente.', 'Difícil', 1100.00, 'disponivel', 6, 1, 3, 'Refatoração, Dicionários', None, 7, 'refatorar', 'def encontrar_usuario(lista_usuarios, nome_usuario):\n    # LENTO: Percorre toda a lista sempre\n    for usuario in lista_usuarios:\n        if usuario["nome"] == nome_usuario:\n            return usuario\n    return None', '[{"entrada_funcao": [[{"nome": "ana"}, {"nome": "bruno"}], "bruno"], "saida_esperada": "{\'nome\': \'bruno\'}"}]'),

        # --- Cliente: CyberSec Alliance (ID 2) ---
        ProjetoFreelance(None, 2, 'Verificador de Porta Aberta', 'Script simples que verifica se uma porta está numa lista de portas seguras.', 'Iniciante', 220.00, 'disponivel', 2, 1, 2, 'Listas, in', None, 3, 'completar', 'def porta_e_segura(porta, portas_seguras):\n    # Verifique se a porta está na lista de portas seguras\n    if ...:\n        return "Porta Segura"\n    else:\n        return "ALERTA: Porta Insegura"', '[{"entrada_funcao": [80, [80, 443, 22]], "saida_esperada": "Porta Segura"}]'),
        ProjetoFreelance(None, 2, 'Analisador de Logs Simples', 'Conta quantas vezes a palavra "ERRO" aparece num arquivo de log (string).', 'Intermediario', 650.00, 'disponivel', 4, 1, 3, 'string.count()', None, 6, 'do_zero', 'def contar_erros(log_texto):\n    # SEU CÓDIGO AQUI\n    return 0', '[{"entrada_funcao": ["INFO: Sistema OK. ERRO: Falha na conexão. INFO: ... ERRO: ..."], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 2, 'Sanitizador de Input', 'Corrige uma função que deveria remover caracteres perigosos de um input, mas está incompleta.', 'Difícil', 1300.00, 'disponivel', 6, 2, 4, 'string.replace()', None, 8, 'debug', 'def sanitizar_input(texto):\n    # BUG: Só remove um dos caracteres perigosos\n    texto_seguro = texto.replace(";", "")\n    return texto_seguro', '[{"entrada_funcao": ["SELECT *; FROM users;--"], "saida_esperada": "SELECT * FROM users--"}]'),

        # --- Cliente: CloudNexus (ID 3) ---
        ProjetoFreelance(None, 3, 'Calculadora de Custo de VM', 'Calcula o custo mensal de uma VM (custo_por_hora * 24 * 30).', 'Iniciante', 150.00, 'disponivel', 1, 1, 2, 'Matemática', None, 4, 'do_zero', 'def calcular_custo_mensal(custo_por_hora):\n    # SEU CÓDIGO AQUI\n    return 0.0', '[{"entrada_funcao": [0.10], "saida_esperada": "72.0"}]'),
        ProjetoFreelance(None, 3, 'Verificador de Status de Serviço', 'Recebe um dicionário de serviços e retorna uma lista dos que estão "offline".', 'Intermediario', 480.00, 'disponivel', 3, 1, 3, 'Dicionários, Loops', None, 7, 'completar', 'def verificar_servicos_offline(status_servicos):\n    offline = []\n    for servico, status in status_servicos.items():\n        if ...:\n            offline.append(servico)\n    return offline', '[{"entrada_funcao": [{"API": "online", "DB": "offline", "Auth": "online"}], "saida_esperada": "[\'DB\']"}]'),
        ProjetoFreelance(None, 3, 'Provisionador de Recursos', 'Refatore um script com muitos `if/elifs` para usar um dicionário para mapear tipos de VM a seus custos.', 'Difícil', 950.00, 'disponivel', 5, 2, 3, 'Refatoração, Dicionários', None, 9, 'refatorar', 'def obter_custo_vm(tipo):\n    if tipo == "t2.micro":\n        return 0.01\n    elif tipo == "t3.small":\n        return 0.05\n    # ... (muitos outros elifs)\n    else:\n        return 0.0', '[{"entrada_funcao": ["t3.small"], "saida_esperada": "0.05"}]'),
        
        # --- Cliente: AppFactory (ID 4) ---
        ProjetoFreelance(None, 4, 'Contador de Cliques', 'Cria uma função que incrementa uma variável de contagem.', 'Iniciante', 130.00, 'disponivel', 1, 2, 1, 'Variáveis', None, 2, 'completar', 'cliques = 0\ndef registrar_clique():\n    global cliques\n    # Incremente a variável cliques\n    ...\n    return cliques', '[{"exec_before": "registrar_clique()", "entrada_funcao": [], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 4, 'Validador de Username', 'Verifica se um username tem entre 4 e 12 caracteres e não contém espaços.', 'Intermediario', 450.00, 'disponivel', 3, 3, 2, 'Métodos de string', None, 5, 'do_zero', 'def validar_username(username):\n    # SEU CÓDIGO AQUI\n    return False', '[{"entrada_funcao": ["user_ok"], "saida_esperada": "True"}, {"entrada_funcao": ["bad user"], "saida_esperada": "False"}]'),
        ProjetoFreelance(None, 4, 'Gerador de Notificações', 'Cria uma notificação push formatada usando f-strings.', 'Difícil', 850.00, 'disponivel', 5, 4, 3, 'f-strings, Listas', None, 6, 'do_zero', 'def gerar_notificacao(usuario, item):\n    # Ex: "Olá, ana! Seu item novo item está pronto!"\n    # SEU CÓDIGO AQUI\n    return ""', '[{"entrada_funcao": ["ana", "novo item"], "saida_esperada": "Olá, ana! Seu item novo item está pronto!"}]'),

        # --- Cliente: DataSolutions Inc. (ID 5) ---
        ProjetoFreelance(None, 5, 'Calculadora de Média', 'Calcula a média de uma lista de números.', 'Iniciante', 200.00, 'disponivel', 2, 1, 2, 'Listas, Operadores', None, 3, 'do_zero', 'def calcular_media(numeros):\n    # SEU CÓDIGO AQUI\n    return 0', '[{"entrada_funcao": [[10, 20, 30]], "saida_esperada": "20.0"}]'),
        ProjetoFreelance(None, 5, 'Limpador de Dados', 'Remove valores negativos de uma lista de vendas usando List Comprehension.', 'Intermediario', 600.00, 'disponivel', 4, 1, 3, 'List Comprehensions', None, 6, 'completar', 'def limpar_dados(dados_vendas):\n    # Use List Comprehension para retornar apenas valores >= 0\n    return [...]', '[{"entrada_funcao": [[100, -50, 250, -10]], "saida_esperada": "[100, 250]"}]'),
        ProjetoFreelance(None, 5, 'Agrupador de Dados', 'Agrupa uma lista de dicionários por uma chave (ex: "categoria").', 'Difícil', 1250.00, 'disponivel', 6, 2, 4, 'Dicionários, Loops', None, 9, 'do_zero', 'def agrupar_por_categoria(produtos):\n    # Retorna um dicionário onde as chaves são as categorias\n    # SEU CÓDIGO AQUI\n    return {}', '[{"entrada_funcao": [[{"nome": "A", "cat": "X"}, {"nome": "B", "cat": "Y"}, {"nome": "C", "cat": "X"}]], "saida_esperada": "{\'X\': [{\'nome\': \'A\', \'cat\': \'X\'}, {\'nome\': \'C\', \'cat\': \'X\'}], \'Y\': [{\'nome\': \'B\', \'cat\': \'Y\'}]}"}]'),

        # --- Cliente: QuantumLeap AI (ID 6) ---
        ProjetoFreelance(None, 6, 'Classificador Simples', 'Classifica um número como "Positivo" ou "Negativo".', 'Iniciante', 250.00, 'disponivel', 2, 1, 2, 'if/else', None, 3, 'do_zero', 'def classificar_numero(n):\n    # SEU CÓDIGO AQUI\n    return ""', '[{"entrada_funcao": [10], "saida_esperada": "Positivo"}, {"entrada_funcao": [-5], "saida_esperada": "Negativo"}]'),
        ProjetoFreelance(None, 6, 'Processador de Dataset', 'Converte uma lista de listas em uma lista de tuplas.', 'Intermediario', 700.00, 'disponivel', 4, 1, 3, 'Tuplas, Listas', None, 5, 'completar', 'def processar_dataset(dados):\n    # Use um loop ou list comprehension para converter\n    return [...]', '[{"entrada_funcao": [[[1, "A"], [2, "B"]]], "saida_esperada": "[(1, \'A\'), (2, \'B\')]"}]'),
        ProjetoFreelance(None, 6, 'Validador de Erros de Modelo', 'Usa try/except para lidar com uma divisão por zero em um cálculo de IA.', 'Difícil', 1400.00, 'disponivel', 6, 2, 4, 'Tratamento de Erros', None, 7, 'debug', 'def calcular_performance(acertos, total):\n    # BUG: Quebra se o total for zero\n    return acertos / total', '[{"entrada_funcao": [10, 0], "saida_esperada": "Erro: Divisão por zero."}]'),

        # --- Cliente: MarketMetrics (ID 7) ---
        ProjetoFreelance(None, 7, 'Contador de Palavras-chave', 'Conta quantas vezes uma palavra-chave aparece em um texto.', 'Iniciante', 180.00, 'disponivel', 2, 1, 2, 'string.count()', None, 4, 'do_zero', 'def contar_palavra(texto, palavra):\n    # SEU CÓDIGO AQUI\n    return 0', '[{"entrada_funcao": ["o sol é amarelo e o céu é azul", "o"], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 7, 'Extrator de Hashtags', 'Extrai todas as palavras que começam com # de um texto.', 'Intermediario', 500.00, 'disponivel', 3, 1, 3, 'Métodos de string, Listas', None, 6, 'completar', 'def extrair_hashtags(texto):\n    hashtags = []\n    for palavra in texto.split():\n        if ...:\n            hashtags.append(palavra)\n    return hashtags', '[{"entrada_funcao": ["Adorei o novo #jogo da #gamedev"], "saida_esperada": "[\'#jogo\', \'#gamedev\']"}]'),
        ProjetoFreelance(None, 7, 'Analisador de A/B Test', 'Compara duas listas de resultados de conversão e retorna qual teve a maior média.', 'Difícil', 1000.00, 'disponivel', 5, 2, 4, 'Dicionários, Lógica', None, 8, 'do_zero', 'def analisar_ab_test(resultados_a, resultados_b):\n    # Retorna "A" ou "B"\n    # SEU CÓDIGO AQUI\n    return ""', '[{"entrada_funcao": [[10, 12, 15], [8, 9, 11]], "saida_esperada": "A"}]'),

        # --- Cliente: GameCraft Studios (ID 8) ---
        ProjetoFreelance(None, 8, 'Verificador de Nível', 'Retorna se o jogador pode ou não usar um item com base no nível.', 'Iniciante', 150.00, 'disponivel', 2, 1, 1, 'if/else, Lógica', None, 3, 'do_zero', 'def pode_equipar(nivel_jogador, nivel_item):\n    # SEU CÓDIGO AQUI\n    return False', '[{"entrada_funcao": [10, 5], "saida_esperada": "True"}, {"entrada_funcao": [5, 10], "saida_esperada": "False"}]'),
        ProjetoFreelance(None, 8, 'Contador de Inventário', 'Conta quantos itens de um tipo específico existem no inventário (uma lista).', 'Intermediario', 400.00, 'disponivel', 3, 1, 2, 'Listas, Métodos', None, 5, 'completar', 'def contar_item(inventario, item_procurado):\n    # inventario é uma lista de strings\n    quantidade = ... # COMPLETE AQUI\n    return quantidade', '[{"entrada_funcao": [["poção", "espada", "poção"], "poção"], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 8, 'Sistema de Missões', 'Verifica se um jogador completou todas as missões necessárias para avançar.', 'Difícil', 750.00, 'disponivel', 5, 1, 3, 'Conjuntos (set), Lógica', None, 7, 'do_zero', 'def checar_missoes_completas(missoes_requeridas, missoes_do_jogador):\n    # Use a teoria de conjuntos para verificar se um conjunto está contido em outro.\n    # SEU CÓDIGO AQUI\n    return False', '[{"entrada_funcao": [{"m1", "m2"}, {"m1", "m2", "m3"}], "saida_esperada": "True"}, {"entrada_funcao": [{"m1", "m4"}, {"m1", "m2", "m3"}], "saida_esperada": "False"}]'),

        # --- Cliente: Pixel Potion (ID 9) ---
        ProjetoFreelance(None, 9, 'Gerador de Moedas', 'Cria uma função que retorna um número aleatório de moedas entre 10 e 50.', 'Iniciante', 120.00, 'disponivel', 1, 1, 1, 'random', None, 2, 'do_zero', 'import random\ndef coletar_moedas():\n    # SEU CÓDIGO AQUI\n    return 0', '[{"check_type": "range", "min": 10, "max": 50}]'),
        ProjetoFreelance(None, 9, 'Sistema de Vidas', 'A função de perder vida está com um bug, não diminui as vidas.', 'Intermediario', 380.00, 'disponivel', 3, 2, 2, 'Funções Simples, Debug', None, 4, 'debug', 'def perder_vida(vidas_atuais):\n    # BUG: Não está retornando o novo valor\n    vidas_atuais - 1', '[{"entrada_funcao": [3], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 9, 'Tabela de High Scores', 'Ordena uma lista de dicionários (jogadores) pela pontuação.', 'Difícil', 800.00, 'disponivel', 5, 3, 3, 'Listas de Dicionários, sort', None, 8, 'do_zero', 'def ordenar_scores(lista_jogadores):\n    # Use o argumento key da função sort() ou sorted()\n    # SEU CÓDIGO AQUI\n    return lista_jogadores', '[{"entrada_funcao": [[{"nome": "A", "score": 100}, {"nome": "B", "score": 300}]], "saida_esperada": "[{\'nome\': \'B\', \'score\': 300}, {\'nome\': \'A\', \'score\': 100}]"}]'),

        # --- Cliente: Epic Worlds RPG (ID 10) ---
        ProjetoFreelance(None, 10, 'Rolar Dados', 'Simula a rolagem de um dado de 20 lados (d20).', 'Iniciante', 100.00, 'disponivel', 1, 1, 2, 'random', None, 2, 'do_zero', 'import random\ndef rolar_d20():\n    # SEU CÓDIGO AQUI\n    return 0', '[{"check_type": "range", "min": 1, "max": 20}]'),
        ProjetoFreelance(None, 10, 'Calculadora de XP', 'Usa um loop `while` para subir o nível do jogador até atingir o XP necessário.', 'Intermediario', 500.00, 'disponivel', 3, 1, 3, 'while loop', None, 6, 'completar', 'def subir_de_nivel(xp_atual, xp_necessario):\n    nivel = 1\n    while ...:\n        xp_atual += 10 # Ganha 10 de XP por loop\n        if xp_atual >= xp_necessario:\n            nivel += 1\n            xp_necessario *= 2\n    return nivel', '[{"entrada_funcao": [0, 100], "saida_esperada": "2"}]'),
        ProjetoFreelance(None, 10, 'Gerador de Loot', 'Gera um item aleatório de uma lista de loot com pesos diferentes.', 'Difícil', 900.00, 'disponivel', 5, 2, 4, 'Dicionários, random.choices', None, 9, 'do_zero', 'import random\ndef gerar_loot(tabela_loot):\n    # tabela_loot é um dicionário {"item": peso}\n    # SEU CÓDIGO AQUI\n    return ""', '[{"entrada_funcao": [{"espada": 10, "escudo": 90}], "saida_esperada": "escudo", "check_type": "weighted"}]'),

        # --- Cliente: Café Aconchego (ID 11) ---
        ProjetoFreelance(None, 11, 'Calculadora de Troco', 'Função que calcula o troco a ser dado ao cliente.', 'Iniciante', 120.00, 'disponivel', 1, 1, 1, 'Básico, Matemática', None, 2, 'completar', 'def calcular_troco(total_compra, valor_pago):\n    troco = ... # COMPLETE AQUI\n    return troco', '[{"entrada_funcao": [42.50, 50.00], "saida_esperada": "7.5"}]'),
        ProjetoFreelance(None, 11, 'Gerador de Recibo', 'Cria uma string formatada como um recibo a partir de uma lista de itens.', 'Intermediario', 350.00, 'disponivel', 3, 1, 2, 'f-strings, Loops', None, 5, 'do_zero', 'def gerar_recibo(itens):\n    # itens é uma lista de tuplas (nome, preco)\n    recibo = "--- Café Aconchego ---\\n"\n    # SEU CÓDIGO AQUI\n    return recibo', '[{"entrada_funcao": [[("Café Expresso", 5.00), ("Pão de Queijo", 3.50)]], "saida_esperada": "--- Café Aconchego ---\\nCafé Expresso....R$ 5.00\\nPão de Queijo...R$ 3.50"}]'),
        ProjetoFreelance(None, 11, 'Sistema de Desconto', 'Aplica um desconto de 10% se a compra for acima de R$ 50, mas o bug está na condição.', 'Difícil', 500.00, 'disponivel', 4, 1, 3, 'Lógica, Debug', None, 4, 'debug', 'def aplicar_desconto(total_compra):\n    # BUG: O desconto só é aplicado para valores MENORES que 50.\n    if total_compra < 50:\n        return total_compra * 0.9\n    else:\n        return total_compra', '[{"entrada_funcao": [60.00], "saida_esperada": "54.0"}, {"entrada_funcao": [40.00], "saida_esperada": "40.0"}]'),

        # --- Cliente: VarejoTotal (ID 12) ---
        ProjetoFreelance(None, 12, 'Verificador de Estoque', 'Verifica se a quantidade de um produto em estoque é maior que zero.', 'Iniciante', 160.00, 'disponivel', 2, 2, 1, 'if/else', None, 3, 'do_zero', 'def tem_estoque(qtd_produto):\n    # SEU CÓDIGO AQUI\n    return False', '[{"entrada_funcao": [10], "saida_esperada": "True"}, {"entrada_funcao": [0], "saida_esperada": "False"}]'),
        ProjetoFreelance(None, 12, 'Calculadora de Frete', 'Calcula o frete com base no estado (um dicionário de taxas).', 'Intermediario', 520.00, 'disponivel', 4, 3, 2, 'Dicionários', None, 6, 'completar', 'def calcular_frete(estado, taxas_frete):\n    # taxas_frete é {"SP": 10.0, "RJ": 15.0}\n    frete = ... # COMPLETE AQUI\n    return frete', '[{"entrada_funcao": ["SP", {"SP": 10.0, "RJ": 15.0}], "saida_esperada": "10.0"}]'),
        ProjetoFreelance(None, 12, 'Processador de Pedidos', 'Usa try/except para garantir que um pedido tenha a chave "id_produto".', 'Difícil', 950.00, 'disponivel', 5, 4, 3, 'Tratamento de Erros', None, 8, 'debug', 'def processar_pedido(pedido):\n    # BUG: Quebra se o pedido não tiver "id_produto"\n    return f"Processando pedido para o produto {pedido[\'id_produto\']}"', '[{"entrada_funcao": [{"id_produto": 123}], "saida_esperada": "Processando pedido para o produto 123"}, {"entrada_funcao": [{"nome": "item"}], "saida_esperada": "Erro: Pedido inválido."}]'),

        # --- Cliente: Moda Rápida (ID 13) ---
        ProjetoFreelance(None, 13, 'Conversor de Tamanhos', 'Converte tamanhos de "P", "M", "G" para números (usando um dicionário).', 'Iniciante', 140.00, 'disponivel', 2, 2, 1, 'Dicionários', None, 3, 'do_zero', 'def converter_tamanho(tamanho_str):\n    mapa = {"P": 38, "M": 40, "G": 42}\n    # SEU CÓDIGO AQUI\n    return 0', '[{"entrada_funcao": ["M"], "saida_esperada": "40"}]'),
        ProjetoFreelance(None, 13, 'Filtro de Cores', 'Usa List Comprehension para filtrar uma lista de roupas por uma cor específica.', 'Intermediario', 480.00, 'disponivel', 4, 3, 2, 'List Comprehensions', None, 5, 'completar', 'def filtrar_por_cor(lista_roupas, cor):\n    # lista_roupas é uma lista de dicionários com a chave "cor"\n    return [...]', '[{"entrada_funcao": [[{"cor": "azul"}, {"cor": "vermelho"}], "azul"], "saida_esperada": "[{\'cor\': \'azul\'}]"}]'),
        ProjetoFreelance(None, 13, 'Alerta de Estoque Baixo', 'Percorre um dicionário de estoque e retorna uma lista de itens com menos de 5 unidades.', 'Difícil', 880.00, 'disponivel', 5, 3, 3, 'Loops, Dicionários', None, 7, 'do_zero', 'def alerta_estoque_baixo(estoque):\n    # estoque é {"camiseta": 10, "calça": 3}\n    # SEU CÓDIGO AQUI\n    return []', '[{"entrada_funcao": [{"camiseta": 10, "calça": 3, "meia": 20, "casaco": 1}], "saida_esperada": "[\'calça\', \'casaco\']"}]')
    ]
    
    for projeto in projetos:
        try:
            projeto_service.criar_projeto(projeto)
        except Exception as e:
            print(f"Erro ao inserir projeto {projeto.get_titulo()}: {e}")

    print(f"-> {len(projetos)} novos projetos foram adicionados ao banco de dados.")


if __name__ == "__main__":
    print("Iniciando script de população de projetos...")
    
    db_manager = BancoDeDadosIntermediario()
    db_manager.criarBanco()

    projeto_service = ProjetoFreelanceServiceImpl()

    popular_projetos(projeto_service)

    print("\nPopulação de projetos concluída!")
