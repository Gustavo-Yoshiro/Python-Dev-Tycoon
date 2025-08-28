# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.DialogoServiceImpl import DialogoServiceImpl
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Persistencia.Entidade.Dialogo import DialogoNo, DialogoOpcao
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def limpar_dialogos_antigos(dialogo_service):
    """Função auxiliar para limpar as tabelas de diálogo antes de inserir novos dados."""
    # Você precisaria implementar estes métodos na sua camada de persistência/serviço
    # dialogo_service.opcao_persistencia.deletar_todos()
    # dialogo_service.no_persistencia.deletar_todos()
    print("Diálogos antigos foram limpos (simulado).")

def popular_dialogos(dialogo_service: DialogoServiceImpl, projeto_service: ProjetoFreelanceServiceImpl, cliente_service: ClienteServiceImpl):
    """
    Popula as árvores de diálogo para os projetos existentes, com uma estrutura de conversa
    mais desenvolvida, com hub central e opções dinâmicas.
    """
    limpar_dialogos_antigos(dialogo_service)
    
    projetos = projeto_service.persistencia.listar_disponiveis()

    # Mapa de requisitos de social para pedir detalhes
    req_social_map = {
        'Iniciante': 1,
        'Intermediario': 20,
        'Dificil': 40
    }

    # --- Cliente: InovaTech Solutions (ID 1 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para InovaTech Solutions ---")
    
    # Projeto: Validador de Startup
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Startup'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Analisando 'Validador de Startup'. Seja direto. O que quer saber?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Detalhes: A função deve validar se a startup tem pelo menos 2 fundadores e capital inicial > 50k.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Não negociável para este escopo.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quero os detalhes técnicos.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Voltar.", 1, None))

    # Projeto: Gerador de Pitch Deck
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Pitch Deck'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Contrato 'Gerador de Pitch Deck'. Preciso de uma solução eficiente. Perguntas?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Detalhes: Use f-strings para formatar nome, valoração e número de fundadores em um pitch atraente.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento base: R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Sua reputação é boa. Posso aumentar para R$ 600.00 se incluir formatação de moeda.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quais os requisitos técnicos?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual a remuneração?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 40] Podemos negociar um valor maior com base na complexidade?", 40, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar por R$ 600.00]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # Projeto: Sistema de Valuation de Startups
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Valuation de Startups'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Sistema complexo de valuation. Use dicionários, list comprehensions e f-strings.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O sistema deve calcular valuation baseado em faturamento, crescimento e margem, gerando relatório formatado.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes da implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # --- Cliente: CyberSec Alliance (ID 2 - Personalidade: Corporativo) ---
    print("\n--- Populando diálogos para CyberSec Alliance ---")
    
    # Projeto: Verificador de Portas Seguras
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Portas Seguras'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Analisando o contrato '{proj.get_titulo()}'. Por favor, prossiga com suas questões.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O escopo técnico requer uma função que verifique se uma porta está na lista de portas seguras usando operador 'in'.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração para este escopo está fixada em R$ {proj.get_recompensa():.2f}, conforme o nosso padrão.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito os detalhes técnicos.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Gostaria de discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Informação recebida. Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Retornar.", 1, None))

    # Projeto: Sanitizador de Inputs
    proj = next((p for p in projetos if p.get_titulo() == 'Sanitizador de Inputs'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Requeremos uma função robusta de sanitização usando métodos de string para prevenir ataques.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve remover espaços extras, caracteres especiais suspeitos e converter para minúsculas.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor base é R$ {proj.get_recompensa():.2f}. A segurança é nossa principal prioridade.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o escopo técnico completo.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Analisador de Logs de Segurança
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de Logs de Segurança'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de análise de logs precisa ser refatorado. Detectamos padrões de ataques complexos.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A solução deve identificar SQL Injection, XSS e outros padrões de ataque, retornando estatísticas detalhadas.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}. A segurança é inegociável.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Agradecemos a sua proatividade. Se implementar detecção de ataques zero-day, podemos ajustar o valor.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o briefing técnico.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor do contrato.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 65] Posso implementar detecção de ataques mais avançados.", 65, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Excelente iniciativa. Aceito com o escopo expandido.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: CloudNexus (ID 3 - Personalidade: Técnico) ---
    print("\n--- Populando diálogos para CloudNexus ---")

    # Projeto: Calculadora de Uso de CPU
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Uso de CPU'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Input: `tempo_ocioso`, `tempo_total`. Output: `(1 - tempo_ocioso/tempo_total) * 100`. Dúvidas?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Precisão: ponto flutuante, uma casa decimal. Performance: cálculo O(1).", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Remuneração: R$ {proj.get_recompensa():.2f}. Valor fixo pela simplicidade algorítmica.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Especificações de precisão?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Especificações recebidas. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))

    # Projeto: Gerenciador de Recursos
    proj = next((p for p in projetos if p.get_titulo() == 'Gerenciador de Recursos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Input: lista de recursos, índice, novo valor. Output: lista atualizada. Use métodos de lista.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Sugestão: `recursos[indice] = novo_valor` ou métodos como insert/pop se necessário.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual abordagem recomenda?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Otimizador de Alocação de Recursos
    proj = next((p for p in projetos if p.get_titulo() == 'Otimizador de Alocação de Recursos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Identifique recursos subutilizados (<30% uso). Use list comprehension e sets para eficiência.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Retorne lista de recursos com utilização abaixo do threshold. Trate erros de chave.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Complexidade O(n).", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o threshold de utilização?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
    
        # --- Cliente: AppFactory (ID 4 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para AppFactory ---")

    # Projeto: Contador de Downloads
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Downloads'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí! Precisamos contar downloads do nosso app. É rapidinho, pode ajudar?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "É só uma variável global que incrementa quando chamam a função. Super simples!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Te pagamos R$ {proj.get_recompensa():.2f} por essa ajudinha!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como funciona?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual o valor?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Beleza! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok! Voltar.", 1, None))

    # Projeto: Sistema de Coordenadas
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Coordenadas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi! Precisamos calcular distância entre coordenadas na tela. Usa tuplas, tá?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Fórmula: √((x2-x1)² + (y2-y1)²). As coordenadas vêm como tuplas (x, y).", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a fórmula?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Quanto pagam?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendi! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Analytics de App
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Analytics de App'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Opa! Precisamos de analytics pros nossos usuários. Tuplas, dicionários e f-strings!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Recebe lista de tuplas (nome, idade, cidade). Calcula total, média de idade e conta por cidade.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se incluir análise de gênero (adicionando campo nas tuplas), aumento para R$ 1400!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Que dados analisar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Show! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 50] Posso adicionar mais análises?", 50, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Aceito com análise extra!", 1, 'ACEITAR_PROJETO_COM_BONUS'))
    
        # --- Cliente: QuantumLeap AI (ID 6 - Personalidade: Exigente) ---
    print("\n--- Populando diálogos para QuantumLeap AI ---")

    # Projeto: Treinamento de IA
    proj = next((p for p in projetos if p.get_titulo() == 'Treinamento de IA'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Simule treinamento de IA até 95% de precisão. Use while loop com incremento controlado.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Precisão inicial: 0. Incremente 10% por época. Retorne número de épocas necessárias.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Simulação deve ser deterministicamente correta.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Especificações do algoritmo?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Configurador de Hyperparâmetros
    proj = next((p for p in projetos if p.get_titulo() == 'Configurador de Hyperparâmetros'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Atualize dicionário de parâmetros com novos valores. Mantenha parâmetros existentes não sobrescritos.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use método update() ou compreensão de dicionário. Preserve parâmetros originais não especificados nos novos valores.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Valor: R$ {proj.get_recompensa():.2f}. Implementação deve ser eficiente e idiomática.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Estratégia de atualização?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Framework de Validação de Modelos
    proj = next((p for p in projetos if p.get_titulo() == 'Framework de Validação de Modelos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Refatore sistema de validação de modelos. Trate erros robustamente e use list comprehensions.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Para cada modelo, tente validar. Se sucesso: status 'aprovado'. Se erro: status 'erro' com mensagem.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Tolerância zero a falhas não tratadas.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se implementar validação cruzada além do básico, autorizo bônus de 20%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Protocolo de tratamento de erros?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 80] Posso implementar validação cruzada?", 80, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com validação cruzada]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

            # --- Cliente: MarketMetrics (ID 7 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para MarketMetrics ---")

    # Projeto: Relatório de Métricas
    proj = next((p for p in projetos if p.get_titulo() == 'Relatório de Métricas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de relatório formatado com métricas de marketing. Use print().", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Formato: 'Relatório Marketing\\nCliques: X\\nConversões: Y\\nTaxa: Z%'. Calcule taxa = (conversoes/cliques)*100", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Formatação precisa ser exata.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o formato do relatório?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))

    # Projeto: Filtro de Dados de Campanha
    proj = next((p for p in projetos if p.get_titulo() == 'Filtro de Dados de Campanha'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Filtre campanhas com ROI > 1.0. Use list comprehension.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Retorne lista de dicionários onde campanha['roi'] > 1.0. Mantenha estrutura original.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Eficiência é crucial.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o critério de filtro?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Painel de ROI de Campanhas
    proj = next((p for p in projetos if p.get_titulo() == 'Painel de ROI de Campanhas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Analise ROI de múltiplas campanhas. Use métodos de string, dicionários e f-strings.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Calcule ROI = retorno/investimento. Identifique campanha com maior ROI. Formate relatório com f-strings.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Precisão nos cálculos é essencial.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como calcular ROI?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Compreendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Voltar.", 1, None))

        # --- Cliente: GameCraft Studios (ID 8 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para GameCraft Studios ---")

    # Projeto: Criador de Personagem
    proj = next((p for p in projetos if p.get_titulo() == 'Criador de Personagem'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí! Vamos criar um personagem juntos? Precisamos de input() para nome e classe!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use input() duas vezes: para nome e classe. Retorne string formatada: 'Personagem: [nome], Classe: [classe]'", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Te pagamos R$ {proj.get_recompensa():.2f} por essa diversão!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como funciona?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual a recompensa?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Divertido! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Legal! Voltar.", 1, None))

    # Projeto: Sistema de Save/Load
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Save/Load'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de save/load tá bugando! Pode consertar com try/except?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se arquivo contém 'corrompido', levante FileNotFoundError. Use try/except para retornar mensagem amigável.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Jogadores não podem ver tracebacks!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o bug?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Quanto pagam?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendi o bug! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Achievements
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Achievements'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queremos achievements legais! Verifique se jogador cumpriu requisitos usando sets!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use operações de conjunto: missoes_requeridas.issubset(missoes_do_jogador). Retorne lista de conquistas alcançadas.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Vai deixar os jogadores felizes!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se adicionar achievements secretos (requisitos especiais), aumento para R$ 1500!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como verificar conquistas?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Maneiro! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 60] Posso adicionar achievements secretos?", 60, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Aceito com achievements secretos!", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: Pixel Potion (ID 9 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para Pixel Potion ---")

    # Projeto: Sistema de Pontuação
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Pontuação'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oizinho! Soma pontos base + bônus pra gente? É bem simples!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "É só somar pontos_base + bonus e retornar o total. Certifique-se de que são números!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Rapidinho!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como calcular?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual o valor?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Fácil! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok! Voltar.", 1, None))

    # Projeto: Painel de Estatísticas
    proj = next((p for p in projetos if p.get_titulo() == 'Painel de Estatísticas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queremos um painel bonito com f-strings! Formate pontuação, nível e tempo!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use f-strings: pontuação com separador de milhar, tempo em MM:SS. Ex: 'Pontuação: 12,500 | Nível: 7 | Tempo: 01:35'", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Queremos que fique visual!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como formatar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Bonito! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Localização
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Localização'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso jogo vai ser global! Precisamos de tradução multi-idioma com dicionários!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Estrutura: {'text_id': {'en': 'Text', 'pt': 'Texto', 'es': 'Texto'}}. Retorne texto no idioma solicitado.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Vai ajudar jogadores do mundo todo!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se suportar fallback para inglês quando tradução faltar, aumento para R$ 1350!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como estruturar as traduções?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Global! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 45] Posso implementar fallback para inglês?", 45, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Aceito com fallback!", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: Epic Worlds RPG (ID 10 - Personalidade: Exigente) ---
    print("\n--- Populando diálogos para Epic Worlds RPG ---")

    # Projeto: Comparador de Números
    proj = next((p for p in projetos if p.get_titulo() == 'Comparador de Números'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Função trivial: retorne o maior de dois números. Precisão absoluta requerida.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use operadores relacionais. Retorne o valor numérico maior, não uma string. Simples mas deve ser perfeito.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Não justifica negociação.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Especificações exatas?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Sistema de Diálogo
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Diálogo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Processe texto de diálogo RPG. Use métodos de string: strip, lower, capitalize.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Remova espaços extras, converta para minúsculas e capitalize primeira letra. Ex: '  O Reino precisa de você, HERÓI!  ' → 'O reino precisa de você, herói!'", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Diálogos são cruciais para imersão.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quais transformações aplicar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Gerador de Mundo Procedural
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Mundo Procedural'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Refatore gerador procedural de mundos. Use list comprehensions, sets e dicionários para eficiência.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Gere mapa baseado em probabilidades de biomas. Retorne estrutura com mapa e estatísticas de distribuição.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Performance O(n) é mandatória.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se implementar geração baseada em semente (seed) para reproducibilidade, autorizo bônus de 25%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Algoritmo de geração?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 85] Posso implementar suporte a seed?", 85, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com geração por seed]", 1, 'ACEITAR_PROJETO_COM_BONUS'))
    
        # --- Cliente: Café Aconchego (ID 11 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para Café Aconchego ---")

    # Projeto: Calculadora de Pedido
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Pedido'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi! Precisa calcular total do pedido: café + pão de queijo. Pode ajudar?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Café: R$ 5.00, Pão de Queijo: R$ 3.50. Some: (cafe * 5.0) + (pao_de_queijo * 3.5)", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Vai ajudar nossos clientes!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quais os preços?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual o valor?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Delícia! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Obrigada! Voltar.", 1, None))

    # Projeto: Organizador de Pedidos
    proj = next((p for p in projetos if p.get_titulo() == 'Organizador de Pedidos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Os pedidos prioritários devem vir primeiro! Use métodos de lista para organizar.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use métodos como insert, remove, ou sorted com key personalizada. Prioritários primeiro, depois outros.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Agilidade no atendimento!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como priorizar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Organizado! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Gestão de Estoque
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Gestão de Estoque'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de estoque tá com bug! Subtrai vendas mas não retorna valor correto.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Debug: a função precisa retornar o estoque atualizado. Verifique se está retornando o dicionário correto.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Não podemos errar no estoque!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se além de consertar, você adicionar alerta para estoque baixo, pago R$ 1200!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Onde está o bug?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Vou consertar! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 60] Posso adicionar alerta de estoque baixo?", 60, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Aceito com alerta de estoque!", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: VarejoTotal (ID 12 - Personalidade: Corporativo) ---
    print("\n--- Populando diálogos para VarejoTotal ---")

    # Projeto: Verificador de Frete Grátis
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Frete Grátis'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Prezado(a), analisando o contrato 'Verificador de Frete Grátis'. Estamos à disposição.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Frete grátis para: compras ≥ R$ 200 OU (compras ≥ R$ 150 E primeira compra). Use operadores lógicos.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração está fixada em R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito as condições exatas.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Compreendido. Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Retornar.", 1, None))

    # Projeto: Sistema de Logística
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Logística'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O contrato 'Sistema de Logística' está aberto para propostas. Quais são as suas questões?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use tuplas para coordenadas imutáveis. Calcule distância euclidiana: √((x2-x1)² + (y2-y1)²). Some distâncias dos pontos de entrega.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} foi alocado para este desenvolvimento.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito detalhes do cálculo.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Recomendação
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Recomendação'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Sistema de recomendação baseado em histórico de compras. Use list comprehensions e sets.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Analise categoria dos produtos comprados. Recomende produtos da mesma categoria que estejam no catálogo mas não foram comprados.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor para este desenvolvimento é de R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se implementar filtro por popularidade (produtos mais vendidos na categoria), podemos aprovar um bônus.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Estratégia de recomendação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 70] Posso adicionar filtro por popularidade?", 70, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com filtro de popularidade]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: Moda Rápida (ID 13 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para Moda Rápida ---")

    # Projeto: Gerador de Código de Produto
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Código de Produto'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de código de produto formatado: categoria + número com 4 dígitos.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Formato: 'CAT-0042'. Use zfill ou formatação de string para garantir 4 dígitos.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Formatação precisa ser consistente.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o formato?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Analisador de Tendencias
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de Tendencias'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Identifique cores em tendência entre lojas. Use operações de conjunto.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use intersection de sets para encontrar cores comuns entre as lojas. Retorne set com cores em tendência.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Eficiência em grandes volumes.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como identificar tendências?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Previsor de Tendências
    proj = next((p for p in projetos if p.get_titulo() == 'Previsor de Tendências'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preveja tendências de moda baseado em dados históricos. Use dicionários e list comprehensions.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Consulte histórico por temporada. Retorne tendências com confiança baseada em frequência histórica. Trate temporadas não encontradas.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Previsões precisas são vitais.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se implementar previsão baseada em cor (análise de tonalidades), aumento para R$ 1500.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Fonte dos dados históricos?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 75] Posso adicionar análise de tonalidades?", 75, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com análise de cores]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    print("\nDiálogos populados para todos os projetos!")


if __name__ == "__main__":
    print("Iniciando script de população de diálogos...")
    
    db_manager = BancoDeDadosIntermediario()
    db_manager.criarBanco()

    dialogo_service = DialogoServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()
    cliente_service = ClienteServiceImpl()

    popular_dialogos(dialogo_service, projeto_service, cliente_service)

    print("\nPopulação de diálogos concluída!")