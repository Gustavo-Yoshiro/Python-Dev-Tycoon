# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def popular_projetos(projeto_service: ProjetoFreelanceServiceImpl):
    """
    Insere uma lista extensa e variada de projetos de freelance no banco de dados.
    """
    if projeto_service.listar_projetos_para_jogador(None):
        print("Projetos já existem. Limpando a lista antiga...")
        projeto_service.deletar_todos_projetos()

    print("Inserindo uma nova lista de 39 projetos de freelance...")

    projetos = [
        # --- Cliente: InovaTech Solutions (ID 1) ---
        ProjetoFreelance(None, 1, 'Validador de Startup', 'Valide se uma startup tem pelo menos 2 fundadores e capital inicial > 50k.', 'Iniciante', 200.00, 'disponivel', 2, 1, 1, 'if/else, operadores', None, 2, 'do_zero', 
                         'def validar_startup(num_fundadores, capital):\n    return False', 
                         '[{"entrada_funcao": [3, 75000], "saida_esperada": "True"}, {"entrada_funcao": [1, 60000], "saida_esperada": "False"}]'),
        ProjetoFreelance(None, 1, 'Gerador de Pitch Deck', 'Formate dados da startup em um pitch atraente usando f-strings.', 'Intermediario', 550.00, 'disponivel', 12, 2, 3, 'f-strings', None, 5, 'do_zero', 
                         'def gerar_pitch(nome, valoracao, fundadores):\n    return ""', 
                         '[{"entrada_funcao": ["TechSolve", 2500000, 3], "saida_esperada": "PITCH: TechSolve | Valoração: $2.500.000 | Fundadores: 3"}]'),
        ProjetoFreelance(None, 1, 'Sistema de Valuation de Startups', 'Calcule valuation com múltiplos critérios e gere relatório formatado.', 'Difícil', 1200.00, 'disponivel', 20, 4, 6, 'dicionários, list comprehensions, f-strings', None, 12, 'do_zero', 
                         'def calcular_valuation(dados_startup):\n    return {"valuation": 0, "relatorio": ""}', 
                         '[{"entrada_funcao": [{"faturamento": 500000, "crescimento": 20, "margem": 30}], "saida_esperada": "{\'valuation\': 2500000, \'relatorio\': \'Valuation: $2.500.000 | Multiplicador: 5.0x\'}"}]'),

        # --- Cliente: CyberSec Alliance (ID 2) ---
        ProjetoFreelance(None, 2, 'Verificador de Portas Seguras', 'Verifique se uma porta está na lista de portas seguras.', 'Iniciante', 250.00, 'disponivel', 3, 1, 2, 'Listas, in', None, 3, 'completar', 
                         'def porta_e_segura(porta, portas_seguras):\n    if ...:\n        return "Porta Segura"\n    else:\n        return "ALERTA: Porta Insegura"', 
                         '[{"entrada_funcao": [443, [80, 443, 22]], "saida_esperada": "Porta Segura"}]'),
        ProjetoFreelance(None, 2, 'Sanitizador de Inputs', 'Implemente métodos de string para limpar entradas suspeitas.', 'Intermediario', 650.00, 'disponivel', 13, 2, 4, 'string methods', None, 6, 'do_zero', 
                         'def sanitizar_input(texto):\n    return texto', 
                         '[{"entrada_funcao": ["  ALERTA; DROP TABLE; --  "], "saida_esperada": "alerta droptable"}]'),
        ProjetoFreelance(None, 2, 'Analisador de Logs de Segurança', 'Processe logs complexos identificando padrões de ataques.', 'Difícil', 1500.00, 'disponivel', 22, 5, 7, 'try/except, string methods, dicionários', None, 14, 'refatorar', 
                         'def analisar_logs_seguranca(logs):\n    # Código complexo existente com problemas\n    return {"alertas": [], "estatisticas": {}}', 
                         '[{"entrada_funcao": ["ERRO: SQL Injection attempt from 192.168.1.1\\nALERTA: XSS detected\\nINFO: Normal request"], "saida_esperada": "{\'alertas\': [\'SQL Injection\', \'XSS\'], \'estatisticas\': {\'tentativas_ataque\': 2}}"}'),

        # --- Cliente: CloudNexus (ID 3) ---
        ProjetoFreelance(None, 3, 'Calculadora de Uso de CPU', 'Calcule o uso percentual de CPU com base no tempo ocioso.', 'Iniciante', 180.00, 'disponivel', 2, 1, 2, 'Matemática', None, 3, 'do_zero', 
                         'def calcular_uso_cpu(tempo_ocioso, tempo_total):\n    return 0', 
                         '[{"entrada_funcao": [20, 100], "saida_esperada": "80.0"}]'),
        ProjetoFreelance(None, 3, 'Gerenciador de Recursos', 'Use métodos de lista para gerenciar recursos alocados.', 'Intermediario', 600.00, 'disponivel', 14, 3, 4, 'list methods, slicing', None, 7, 'completar', 
                         'def redistribuir_recursos(recursos, indice, novo_valor):\n    # Use métodos de lista aqui\n    return recursos', 
                         '[{"entrada_funcao": [[10, 20, 30], 1, 25], "saida_esperada": "[10, 25, 30]"}]'),
        ProjetoFreelance(None, 3, 'Otimizador de Alocação de Recursos', 'Otimize alocação em nuvem identificando recursos subutilizados.', 'Difícil', 1400.00, 'disponivel', 21, 4, 6, 'list comprehensions, sets, error handling', None, 13, 'do_zero', 
                         'def otimizar_recursos(recursos, utilizacao):\n    return []', 
                         '[{"entrada_funcao": [["vm1", "vm2", "vm3"], {"vm1": 15, "vm2": 80, "vm3": 25}], "saida_esperada": "[\'vm1\', \'vm3\']"}]'),

        # --- Cliente: AppFactory (ID 4) ---
        ProjetoFreelance(None, 4, 'Contador de Downloads', 'Conte quantos downloads nosso app teve hoje.', 'Iniciante', 150.00, 'disponivel', 1, 2, 1, 'Variáveis', None, 2, 'completar', 
                         'downloads = 0\ndef registrar_download():\n    global downloads\n    ...\n    return downloads', 
                         '[{"exec_before": "registrar_download()", "entrada_funcao": [], "saida_esperada": "3"}]'),
        ProjetoFreelance(None, 4, 'Sistema de Coordenadas', 'Use tuplas para representar coordenadas de elementos na tela.', 'Intermediario', 580.00, 'disponivel', 13, 2, 3, 'tuplas', None, 6, 'do_zero', 
                         'def calcular_distancia(coord1, coord2):\n    return 0', 
                         '[{"entrada_funcao": [(10, 20), (13, 24)], "saida_esperada": "5.0"}]'),
        ProjetoFreelance(None, 4, 'Sistema de Analytics de App', 'Analise dados de usuários e gere relatórios performáticos.', 'Difícil', 1300.00, 'disponivel', 19, 4, 5, 'dicionários, tuplas, f-strings', None, 11, 'completar', 
                         'def gerar_relatorio_usuarios(dados_usuarios):\n    # Complete esta função complexa\n    return ""', 
                         '[{"entrada_funcao": [[("Ana", 25, "SP"), ("João", 30, "RJ"), ("Maria", 25, "SP")]], "saida_esperada": "Total: 3 usuários | Idade média: 26.7 | SP: 2, RJ: 1"}]'),

        # --- Cliente: DataSolutions Inc. (ID 5) ---
        ProjetoFreelance(None, 5, 'Calculadora de Média de Vendas', 'Calcule a média de vendas diárias.', 'Iniciante', 220.00, 'disponivel', 2, 1, 2, 'for, listas', None, 3, 'do_zero', 
                         'def calcular_media(vendas_diarias):\n    return 0', 
                         '[{"entrada_funcao": [[100, 200, 300]], "saida_esperada": "200.0"}]'),
        ProjetoFreelance(None, 5, 'Analisador de Clientes Únicos', 'Use sets para identificar clientes únicos em diferentes regiões.', 'Intermediario', 700.00, 'disponivel', 15, 3, 4, 'sets', None, 8, 'do_zero', 
                         'def clientes_unicos(regiao_norte, regiao_sul):\n    return set()', 
                         '[{"entrada_funcao": [["A", "B", "C"], ["B", "C", "D"]], "saida_esperada": "{\'A\', \'D\'}"}]'),
        ProjetoFreelance(None, 5, 'Processador de Big Data', 'Processe grandes conjuntos de dados encontrando insights.', 'Difícil', 1600.00, 'disponivel', 23, 5, 7, 'list comprehensions, sets, dicionários', None, 15, 'do_zero', 
                         'def encontrar_insights(dataset):\n    return {"comum": set(), "estatisticas": {}}', 
                         '[{"entrada_funcao": [[{"idade": 25, "cidade": "SP"}, {"idade": 30, "cidade": "RJ"}, {"idade": 25, "cidade": "SP"}]], "saida_esperada": "{\'comum\': {\'idade\': 25, \'cidade\': \'SP\'}, \'estatisticas\': {\'media_idade\': 26.7}}"}'),

        # --- Cliente: QuantumLeap AI (ID 6) ---
        ProjetoFreelance(None, 6, 'Treinamento de IA', 'Simule o treinamento de IA até atingir 95% de precisão.', 'Iniciante', 280.00, 'disponivel', 3, 1, 2, 'while', None, 4, 'completar', 
                         'def treinar_ia():\n    precisao = 0\n    epocas = 0\n    while ...:\n        precisao += 10\n        epocas += 1\n    return epocas', 
                         '[{"saida_esperada": "10"}]'),
        ProjetoFreelance(None, 6, 'Configurador de Hyperparâmetros', 'Use dicionários para configurar parâmetros de modelo de IA.', 'Intermediario', 750.00, 'disponivel', 16, 4, 5, 'dicionários', None, 9, 'completar', 
                         'def atualizar_parametros(parametros, novos_valores):\n    # Atualize o dicionário aqui\n    return parametros', 
                         '[{"entrada_funcao": [{"lr": 0.01, "batch_size": 32}, {"lr": 0.02, "epochs": 10}], "saida_esperada": "{\'lr\': 0.02, \'batch_size\': 32, \'epochs\': 10}"}]'),
        ProjetoFreelance(None, 6, 'Framework de Validação de Modelos', 'Valide múltiplos modelos de IA com tratamento robusto de erros.', 'Difícil', 1800.00, 'disponivel', 25, 5, 8, 'error handling, dicionários, list comprehensions', None, 17, 'refatorar', 
                         'def validar_modelos(modelos, dados_teste):\n    # Código complexo que precisa ser refatorado\n    return {}', 
                         '[{"entrada_funcao": [{"modelo_a": {"acuracia": 0.95}, "modelo_b": {"erro": "falha"}}, [1, 2, 3]], "saida_esperada": "{\'modelo_a\': {\'status\': \'aprovado\', \'acuracia\': 0.95}, \'modelo_b\': {\'status\': \'erro\', \'mensagem\': \'falha\'}}"}'),

        # --- Cliente: MarketMetrics (ID 7) ---
        ProjetoFreelance(None, 7, 'Relatório de Métricas', 'Gere um relatório formatado com as métricas de marketing.', 'Iniciante', 170.00, 'disponivel', 2, 1, 1, 'print()', None, 2, 'do_zero', 
                         'def gerar_relatorio(cliques, conversoes):\n    print("")\n    print("")\n    print("")', 
                         '[{"entrada_funcao": [150, 15], "saida_esperada": "Relatório Marketing\\nCliques: 150\\nConversões: 15\\nTaxa: 10.0%"}]'),
        ProjetoFreelance(None, 7, 'Filtro de Dados de Campanha', 'Use list comprehension para filtrar campanhas com ROI positivo.', 'Intermediario', 650.00, 'disponivel', 14, 2, 4, 'list comprehensions', None, 7, 'do_zero', 
                         'def filtrar_campanhas_lucrativas(campanhas):\n    return []', 
                         '[{"entrada_funcao": [[{"nome": "A", "roi": 1.5}, {"nome": "B", "roi": 0.8}, {"nome": "C", "roi": 2.0}]], "saida_esperada": "[{\'nome\': \'A\', \'roi\': 1.5}, {\'nome\': \'C\', \'roi\': 2.0}]"}]'),
        ProjetoFreelance(None, 7, 'Painel de ROI de Campanhas', 'Analise ROI de múltiplas campanhas com relatório detalhado.', 'Difícil', 1450.00, 'disponivel', 21, 4, 6, 'string methods, dicionários, f-strings', None, 13, 'do_zero', 
                         'def analisar_campanhas(campanhas):\n    return {"melhor_campanha": "", "relatorio": ""}', 
                         '[{"entrada_funcao": [{"campanha_a": {"investimento": 1000, "retorno": 3000}, "campanha_b": {"investimento": 2000, "retorno": 5000}}], "saida_esperada": "{\'melhor_campanha\': \'campanha_b\', \'relatorio\': \'Melhor ROI: 2.5x | Retorno Total: $8000\'}"}]'),

        # --- Cliente: GameCraft Studios (ID 8) ---
        ProjetoFreelance(None, 8, 'Criador de Personagem', 'Crie um personagem com nome e classe escolhidos pelo jogador.', 'Iniciante', 160.00, 'disponivel', 2, 1, 1, 'input()', None, 2, 'do_zero', 
                         'def criar_personagem():\n    return ""', 
                         '[{"entrada_funcao": [], "input_simulado": "Ana\nGuerreira", "saida_esperada": "Personagem: Ana, Classe: Guerreira"}]'),
        ProjetoFreelance(None, 8, 'Sistema de Save/Load', 'Implemente tratamento de erros para carregamento de jogos salvos.', 'Intermediario', 620.00, 'disponivel', 13, 2, 3, 'try/except', None, 6, 'debug', 
                         'def carregar_jogo(nome_arquivo):\n    # Simula carregamento que pode falhar\n    if "corrompido" in nome_arquivo:\n        raise FileNotFoundError("Arquivo corrompido")\n    return "Jogo carregado"', 
                         '[{"entrada_funcao": ["save1.sav"], "saida_esperada": "Jogo carregado"}, {"entrada_funcao": ["corrompido.sav"], "saida_esperada": "Erro: Arquivo corrompido"}]'),
        ProjetoFreelance(None, 8, 'Sistema de Achievements', 'Implemente sistema complexo de conquistas com verificação de progresso.', 'Difícil', 1350.00, 'disponivel', 20, 4, 5, 'sets, list comprehensions, error handling', None, 12, 'completar', 
                         'def verificar_conquistas(progresso_jogador, conquistas):\n    # Complete o sistema de verification\n    return []', 
                         '[{"entrada_funcao": [{"nivel": 10, "inimigos_derrotados": 50}, {"nivel_5": {"requisito": "nivel >= 5"}, "matador": {"requisito": "inimigos_derrotados >= 30"}}], "saida_esperada": "[\'nivel_5\', \'matador\']"}]'),

        # --- Cliente: Pixel Potion (ID 9) ---
        ProjetoFreelance(None, 9, 'Sistema de Pontuação', 'Calcule a pontuação final do jogo com bônus.', 'Iniciante', 140.00, 'disponivel', 1, 1, 1, 'Variáveis, Tipos', None, 2, 'do_zero', 
                         'def calcular_pontuacao(pontos_base, bonus):\n    return 0', 
                         '[{"entrada_funcao": [100, 25], "saida_esperada": "125"}]'),
        ProjetoFreelance(None, 9, 'Painel de Estatísticas', 'Formate estatísticas de jogo com f-strings para visualização clara.', 'Intermediario', 580.00, 'disponivel', 12, 2, 3, 'f-strings, formatação', None, 5, 'do_zero', 
                         'def formatar_estatisticas(pontuacao, nivel, tempo_jogado):\n    return ""', 
                         '[{"entrada_funcao": [12500, 7, 95], "saida_esperada": "Pontuação: 12,500 | Nível: 7 | Tempo: 01:35"}]'),
        ProjetoFreelance(None, 9, 'Sistema de Localização', 'Implemente sistema de tradução multi-idioma para jogos mobile.', 'Difícil', 1250.00, 'disponivel', 18, 3, 5, 'dicionários, tuplas, string methods', None, 10, 'do_zero', 
                         'def traduzir_jogo(textos, idioma):\n    return {}', 
                         '[{"entrada_funcao": [{"play": {"en": "Play", "pt": "Jogar", "es": "Jugar"}}, "es"], "saida_esperada": "{\'play\': \'Jugar\'}"}]'),

        # --- Cliente: Epic Worlds RPG (ID 10) ---
        ProjetoFreelance(None, 10, 'Comparador de Números', 'Compare dois números e retorne o maior.', 'Iniciante', 190.00, 'disponivel', 2, 1, 1, 'Operadores', None, 3, 'do_zero', 
                         'def maior_numero(a, b):\n    return 0', 
                         '[{"entrada_funcao": [10, 20], "saida_esperada": "20"}]'),
        ProjetoFreelance(None, 10, 'Sistema de Diálogo', 'Processe texto de diálogo com métodos de string para RPG.', 'Intermediario', 720.00, 'disponivel', 15, 3, 4, 'string methods', None, 8, 'completar', 
                         'def processar_dialogo(dialogo):\n    # Aplique métodos de string aqui\n    return dialogo', 
                         '[{"entrada_funcao": ["  O Reino precisa de você, HERÓI!  "], "saida_esperada": "O reino precisa de você, herói!"}]'),
        ProjetoFreelance(None, 10, 'Gerador de Mundo Procedural', 'Crie geração procedural de mundos para RPG com múltiplos biomas.', 'Difícil', 1700.00, 'disponivel', 24, 5, 7, 'list comprehensions, sets, dicionários', None, 16, 'refatorar', 
                         'def gerar_mundo(tamanho, biomas):\n    # Refatore este código complexo\n    return []', 
                         '[{"entrada_funcao": [5, {"floresta": 0.4, "deserto": 0.3, "montanha": 0.3}], "check_type": "complex", "expected_keys": ["mapa", "estatisticas_biomas"]}]'),

        # --- Cliente: Café Aconchego (ID 11) ---
        ProjetoFreelance(None, 11, 'Calculadora de Pedido', 'Calcule o total de um pedido de café e doces.', 'Iniciante', 120.00, 'disponivel', 1, 1, 1, 'Funções', None, 2, 'do_zero', 
                         'def calcular_total(cafe, pao_de_queijo):\n    return 0.0', 
                         '[{"entrada_funcao": [2, 3], "saida_esperada": "19.5"}]'),
        ProjetoFreelance(None, 11, 'Organizador de Pedidos', 'Use métodos de lista para organizar pedidos por prioridade.', 'Intermediario', 550.00, 'disponivel', 12, 2, 3, 'list methods', None, 5, 'do_zero', 
                         'def organizar_pedidos(pedidos, prioritarios):\n    return []', 
                         '[{"entrada_funcao": [["Café", "Suco", "Chá"], ["Chá", "Suco"]], "saida_esperada": "[\'Chá\', \'Suco\', \'Café\']"}]'),
        ProjetoFreelance(None, 11, 'Sistema de Gestão de Estoque', 'Gerencie estoque com alertas e relatórios formatados.', 'Difícil', 1100.00, 'disponivel', 17, 3, 4, 'error handling, dicionários, f-strings', None, 9, 'debug', 
                         'def gerenciar_estoque(estoque_atual, vendas):\n    # Debug deste código com problemas\n    for item, quantidade in vendas.items():\n        estoque_atual[item] -= quantidade\n    return estoque_atual', 
                         '[{"entrada_funcao": [{"cafe": 50, "pao": 30}, {"cafe": 10, "pao": 5}], "saida_esperada": "{\'cafe\': 40, \'pao\': 25}"}]'),

        # --- Cliente: VarejoTotal (ID 12) ---
        ProjetoFreelance(None, 12, 'Verificador de Frete Grátis', 'Verifique se o cliente tem direito a frete grátis.', 'Iniciante', 210.00, 'disponivel', 2, 1, 2, 'if/elif/else', None, 3, 'do_zero', 
                         'def tem_frete_gratis(valor_compra, eh_primeira_compra):\n    return False', 
                         '[{"entrada_funcao": [150, True], "saida_esperada": "True"}, {"entrada_funcao": [199, False], "saida_esperada": "False"}]'),
        ProjetoFreelance(None, 12, 'Sistema de Logística', 'Use tuplas para representar coordenadas de entrega imutáveis.', 'Intermediario', 680.00, 'disponivel', 14, 3, 4, 'tuplas', None, 7, 'do_zero', 
                         'def calcular_rota(origem, destino, pontos_entrega):\n    return 0', 
                         '[{"entrada_funcao": [(0, 0), (10, 10), [(2, 3), (5, 7)]], "saida_esperada": "26.5"}]'),
        ProjetoFreelance(None, 12, 'Sistema de Recomendação', 'Implemente sistema de recomendação baseado em histórico de compras.', 'Difícil', 1550.00, 'disponivel', 22, 4, 6, 'list comprehensions, sets, string methods', None, 14, 'do_zero', 
                         'def recomendar_produtos(historico, catalogo):\n    return []', 
                         '[{"entrada_funcao": [[{"produto": "camiseta", "categoria": "roupas"}, {"produto": "tenis", "categoria": "calcados"}], ["jaqueta", "meias", "sapato"]], "saida_esperada": "[\'jaqueta\', \'meias\']"}]'),

        # --- Cliente: Moda Rápida (ID 13) ---
        ProjetoFreelance(None, 13, 'Gerador de Código de Produto', 'Gere um código de produto formatado.', 'Iniciante', 170.00, 'disponivel', 2, 1, 1, 'Strings', None, 2, 'do_zero', 
                         'def gerar_codigo(categoria, numero):\n    return ""', 
                         '[{"entrada_funcao": ["CAM", 42], "saida_esperada": "CAM-0042"}]'),
        ProjetoFreelance(None, 13, 'Analisador de Tendencias', 'Use sets para identificar cores em tendência entre diferentes lojas.', 'Intermediario', 630.00, 'disponivel', 13, 2, 3, 'sets', None, 6, 'do_zero', 
                         'def cores_em_tendencia(loja_a, loja_b):\n    return set()', 
                         '[{"entrada_funcao": [["azul", "preto", "vermelho"], ["preto", "verde", "amarelo"]], "saida_esperada": "{\'preto\'}"}]'),
        ProjetoFreelance(None, 13, 'Previsor de Tendências', 'Preveja tendências de moda baseado em dados históricos.', 'Difícil', 1400.00, 'disponivel', 21, 4, 5, 'dicionários, list comprehensions, error handling', None, 13, 'completar', 
                         'def prever_tendencias(dados_historicos, temporada):\n    # Complete esta previsão complexa\n    return {"tendencias": [], "confianca": 0}', 
                         '[{"entrada_funcao": [{"verao": ["amarelo", "floral"], "inverno": ["preto", "lã"]}, "verao"], "saida_esperada": "{\'tendencias\': [\'amarelo\', \'floral\'], \'confianca\': 0.85}"}]')
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