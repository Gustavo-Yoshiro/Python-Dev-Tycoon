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
        'Difícil': 40
    }

    # --- Cliente: InovaTech Solutions (ID 1 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para InovaTech Solutions ---")
    
    # Projeto: Validador de Senha Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Senha Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Analisando 'Validador de Senha'. Seja direto. O que quer saber?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Detalhes: A função deve receber uma string e retornar True se tiver 8 ou mais caracteres. Nada mais.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. Não negociável para este escopo.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quero os detalhes técnicos.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Voltar.", 1, None))

    # Projeto: Gerador de API Key
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de API Key'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Contrato 'Gerador de API Key'. Preciso de uma solução eficiente. Perguntas?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Detalhes: A função deve usar as bibliotecas `random` e `string` para gerar uma chave de 16 caracteres alfanuméricos.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento base: R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Sua reputação é boa. Posso aumentar para R$ 600.00 se incluir caracteres especiais.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quais os requisitos técnicos?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual a remuneração?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 40] Podemos negociar um valor maior com base na complexidade?", 40, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar por R$ 600.00]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # Projeto: Otimizador de Loop de Busca
    proj = next((p for p in projetos if p.get_titulo() == 'Otimizador de Loop de Busca'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Otimize nosso loop de busca. Use um dicionário para acesso O(1).", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O código atual usa um loop `for` para percorrer uma lista de usuários. A sua solução deve converter a lista para um dicionário para buscas rápidas.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes da implementação atual?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))


    # --- Cliente: CyberSec Alliance (ID 2 - Personalidade: Corporativo) ---
    print("\n--- Populando diálogos para CyberSec Alliance ---")
    
    # Projeto: Verificador de Porta Aberta
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Porta Aberta'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Analisando o contrato '{proj.get_titulo()}'. Por favor, prossiga com suas questões.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O escopo técnico requer uma função que receba um número de porta e uma lista de portas permitidas, retornando um status booleano.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração para este escopo está fixada em R$ {proj.get_recompensa():.2f}, conforme o nosso padrão.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito os detalhes técnicos.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Gostaria de discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Termos]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Informação recebida. Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Retornar.", 1, None))

    # Projeto: Analisador de Logs Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de Logs Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Requeremos uma função que quantifique as ocorrências da string 'ERRO' em nossos logs de sistema para fins de auditoria.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve ser otimizada para performance, processando logs de até 1GB. A contagem deve ser case-sensitive.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor base é R$ {proj.get_recompensa():.2f}. A performance é o nosso principal critério de avaliação.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o escopo técnico completo.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Sanitizador de Input
    proj = next((p for p in projetos if p.get_titulo() == 'Sanitizador de Input'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema apresenta uma vulnerabilidade de SQL Injection. O script de sanitização está incompleto. Solicitamos a correção imediata.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve ser robusta e proteger contra os 10 principais tipos de injeção, não apenas ponto e vírgula. A documentação OWASP é a referência.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}. A segurança é inegociável.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Agradecemos a sua proatividade. A segurança de nossos clientes é primordial. O valor do contrato será ajustado em conformidade.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o briefing técnico.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor do contrato.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 65] Além de corrigir, sugiro implementar um log de tentativas de injeção.", 65, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Excelente iniciativa. Aceito com o escopo expandido.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: CloudNexus (ID 3 - Personalidade: Técnico) ---
    print("\n--- Populando diálogos para CloudNexus ---")

    # Projeto: Calculadora de Custo de VM
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Custo de VM'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Input: `custo_por_hora`. Output: `custo_por_hora * 720`. Alguma dúvida?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Precisão: ponto flutuante, duas casas decimais. Performance: a função deve ser stateless e computacionalmente leve.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Remuneração: R$ {proj.get_recompensa():.2f}. O valor é fixo, baseado na baixa complexidade.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Especificações de precisão e performance?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Especificações recebidas. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))

    # Projeto: Verificador de Status de Serviço
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Status de Serviço'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Input: dicionário de serviços/status. Output: lista de serviços 'offline'.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve iterar sobre os items do dicionário e retornar uma lista contendo as chaves cujo valor é 'offline'.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Interessante. Se a sua solução também retornar o tempo de uptime (um valor mock), posso adicionar um bônus de 20%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes da implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 50] Podemos expandir o escopo para incluir mais métricas?", 50, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com escopo expandido]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # Projeto: Provisionador de Recursos
    proj = next((p for p in projetos if p.get_titulo() == 'Provisionador de Recursos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O script de provisionamento usa `if/elifs` excessivos. Refatore para usar um dicionário.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O objetivo é reduzir a complexidade ciclomática e melhorar a manutenibilidade. O resultado final deve ser funcionalmente idêntico.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o objetivo principal da refatoração?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # --- Cliente: AppFactory (ID 4 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para AppFactory ---")

    # Projeto: Contador de Cliques
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Cliques'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oizinho! Temos um job super rápido pra você, se tiver interesse!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "É só uma função que incrementa uma variável global de cliques. Bem simples pra começar, né?", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Estamos a oferecer R$ 130.00. É um valor fixo para esta tarefa.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Claro, qual é a boa?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual é a recompensa?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Job]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido, parece fácil. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok, obrigado. Voltar.", 1, None))

    # Projeto: Validador de Username
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Username'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi! Nosso app precisa validar usernames. As regras são: entre 4 e 12 caracteres e sem espaços. Topa o desafio?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve retornar `True` se o username for válido e `False` caso contrário. Queremos que a experiência do usuário seja super boa!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Estamos a oferecer R$ {proj.get_recompensa():.2f}. É uma parte importante do nosso app!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Pode detalhar a implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual o valor do projeto?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Gerador de Notificações
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Notificações'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Precisamos de uma função que crie notificações personalizadas com f-strings. Algo bem amigável para os nossos usuários!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve receber o nome do usuário e um item, e gerar algo como 'Olá, [usuário]! O seu item [item] está pronto! ✨'", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}. Uma boa comunicação com o usuário é tudo para nós!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Perfeito! Se você puder adicionar o nome do nosso app ('AppFactory') no final da notificação, seria incrível. Posso dar um bônus por isso.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como deve ser a notificação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Trabalho]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 50] Que tal adicionar um emoji para deixar ainda mais amigável?", 50, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "Ótima ideia! Aceito com o bônus.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: DataSolutions Inc. (ID 5 - Personalidade: Corporativo) ---
    print("\n--- Populando diálogos para DataSolutions Inc. ---")

    # Projeto: Calculadora de Média
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Média'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Prezado(a), analisando o contrato 'Calculadora de Média'. Estamos à disposição para esclarecimentos.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O escopo requer uma função que calcule a média aritmética de uma lista de valores numéricos, tratando casos de lista vazia.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração está fixada em R$ {proj.get_recompensa():.2f}, conforme a complexidade da tarefa.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o escopo técnico.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Proposta]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Compreendido. Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Entendido. Retornar.", 1, None))

    # Projeto: Limpador de Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Limpador de Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O projeto 'Limpador de Dados' está disponível para avaliação. Qual a sua questão?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "É imperativo que a solução utilize List Comprehension para garantir a performance e a legibilidade do código, conforme os nossos padrões.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} foi definido para este contrato.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Há algum requisito de implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Agrupador de Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Agrupador de Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O projeto 'Agrupador de Dados' requer um profissional com sólida experiência em estruturas de dados. Estamos a avaliar o seu perfil.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A solução deve ser escalável, capaz de processar listas com até 1 milhão de registos sem degradação significativa de performance.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração de R$ {proj.get_recompensa():.2f} reflete a natureza crítica deste componente para o nosso sistema.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Compreendemos. Se puder garantir uma otimização de memória de 20% em relação a uma abordagem padrão, podemos aprovar um bônus.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Quais são os critérios de performance?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 75] Dada a criticidade, uma remuneração maior seria apropriada.", 75, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus de performance]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

        # --- Cliente: QuantumLeap AI (ID 6 - Personalidade: Exigente) ---
    print("\n--- Populando diálogos para QuantumLeap AI ---")

    # Projeto: Classificador Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Classificador Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A tarefa é trivial, mas exigimos 100% de acurácia. Uma função que classifique um número como 'Positivo' ou 'Negativo'. Não erre.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve retornar a string 'Positivo' para n > 0 e 'Negativo' para n <= 0. Não há margem para interpretação.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento de R$ {proj.get_recompensa():.2f} é final. A simplicidade da tarefa não justifica negociação.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito as especificações exatas.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Tarefa]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Processador de Dataset
    proj = next((p for p in projetos if p.get_titulo() == 'Processador de Dataset'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nossos modelos de IA requerem dados imutáveis. Converta esta lista de listas em uma lista de tuplas. A performance é crucial.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Use a abordagem mais performática possível. Um loop simples pode ser muito lento para datasets grandes. Considere o uso de `map` ou List Comprehension.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} está alinhado com a expectativa de performance.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a abordagem de implementação preferida?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Validador de Erros de Modelo
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Erros de Modelo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Uma função de cálculo de performance está a causar uma falha crítica (divisão por zero). Implemente um tratamento de erro robusto.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O bloco `try/except` deve capturar especificamente o `ZeroDivisionError` e retornar uma mensagem de erro padronizada: 'Erro: Divisão por zero.'", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} é para a implementação correta do tratamento de exceção.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se você adicionar um log detalhado do erro antes de retornar a mensagem, posso autorizar um bônus de 10%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a mensagem de erro esperada?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 80] E se, além de tratar o erro, eu registar um log?", 80, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus de logging]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: MarketMetrics (ID 7 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para MarketMetrics ---")

    # Projeto: Contador de Palavras-chave
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Palavras-chave'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de uma função que conte a ocorrência de uma palavra-chave em um texto. Simples.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve ser case-sensitive e eficiente. Use o método `.count()` das strings.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento é R$ {proj.get_recompensa():.2f}. Sem bônus.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Requisitos de implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))

    # Projeto: Extrator de Hashtags
    proj = next((p for p in projetos if p.get_titulo() == 'Extrator de Hashtags'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Extrair todas as palavras que começam com '#' de um texto. Retornar uma lista.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve percorrer o texto, identificar as palavras e retorná-las na ordem em que aparecem.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Pagamento?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Analisador de A/B Test
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de A/B Test'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Função para comparar a média de duas listas de resultados (A e B). Retornar 'A' ou 'B'.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve lidar com listas vazias, retornando 'Empate' nesse caso. A precisão do cálculo da média é essencial.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. O valor é baseado na importância do resultado para a nossa tomada de decisão.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Algum caso de borda a considerar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Compreendido. Voltar.", 1, None))

    
    # --- Cliente: GameCraft Studios (ID 8 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para GameCraft Studios ---")

    # Projeto: Verificador de Nível
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Nível'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí! Uma ajudinha rápida: precisamos de uma função que diga se o nível do jogador é alto o suficiente para usar um item. Coisa simples!", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve receber o nível do jogador e o nível do item, e retornar True se `nivel_jogador >= nivel_item`. Bem direto ao ponto!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Para este job rápido, estamos a oferecer R$ {proj.get_recompensa():.2f}. O que acha?", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como deve funcionar exatamente?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Vamos falar da grana.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Quest]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendido! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))

    # Projeto: Contador de Inventário
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Inventário'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Opa! Nosso script de inventário precisa de um upgrade. Queremos uma função que conte quantos itens de um tipo específico o jogador tem na bolsa (uma lista).", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve usar o método `.count()` das listas do Python. É super eficiente para o que precisamos!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor para esta tarefa é de R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Alguma preferência de implementação?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Desafio]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Missões
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Missões'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí, dev! :) Nosso RPG precisa de um sistema pra checar se o jogador completou um grupo de missões. Acha que consegue?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Show! A ideia é usar `sets` do Python. Basicamente, é ver se o conjunto de missões requeridas é um subconjunto das missões que o jogador já fez.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento é R$ {proj.get_recompensa():.2f}. É uma parte crucial da nossa nova expansão!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Boa! Se você manja de `sets`, talvez possa nos ajudar com uma otimização extra. Se conseguir, a gente paga 25% a mais!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Parece divertido! Como pensaram em fazer?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Missão]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendi a lógica. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 60] `Sets` são minha especialidade. Que tipo de otimização têm em mente?", 60, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus de otimização]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: Pixel Potion (ID 9 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para Pixel Potion ---")

    # Projeto: Gerador de Moedas
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Moedas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oizinho! Queremos dar umas moedinhas pros nossos jogadores. Pode fazer uma função que sorteia um número entre 10 e 50? :D", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "É só usar a biblioteca `random` do Python! Bem fácil, né?", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A gente paga R$ {proj.get_recompensa():.2f} por essa ajudinha!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Como eu faria isso?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "E o pagamento?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendi, valeu! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok! Voltar.", 1, None))

    # Projeto: Sistema de Vidas
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Vidas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Socorro! Nossa função de perder vida não tá funcionando, o jogador fica imortal! Hahaha. Pode consertar pra gente?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Parece que a função até subtrai a vida, mas esquece de `retornar` o novo valor. A gente precisa que ela retorne o número de vidas restantes.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor pra caçar esse bug é R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Pode me dar uma pista do bug?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Qual a recompensa?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Tabela de High Scores
    proj = next((p for p in projetos if p.get_titulo() == 'Tabela de High Scores'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queremos mostrar os melhores jogadores! Preciso de uma função que ordene uma lista de jogadores (dicionários) pela maior pontuação ('score').", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve usar o argumento `key` da função `sort()` ou `sorted()` para conseguir ordenar a lista de dicionários corretamente.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento é R$ {proj.get_recompensa():.2f}. Uma tabela de scores bonita é super importante!", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Hmm, boa pergunta. Se for fácil pra você, seria legal mostrar o nome em maiúsculas pra dar destaque. Se não, tudo bem!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a melhor forma de ordenar?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 45] Algum requisito de formatação para os nomes?", 45, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com formatação extra]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: Epic Worlds RPG (ID 10 - Personalidade: Exigente) ---
    print("\n--- Populando diálogos para Epic Worlds RPG ---")

    # Projeto: Rolar Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Rolar Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Exigimos uma simulação de rolagem de um d20. O resultado deve ser um inteiro, precisamente entre 1 e 20, inclusive. Sem desvios.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função não deve ter argumentos e deve usar a biblioteca `random` para garantir a aleatoriedade. A performance não é crítica, mas a precisão é.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} é padrão para tarefas de baixa complexidade.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito as especificações técnicas.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Tarefa]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Calculadora de XP
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de XP'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A lógica de subida de nível está incompleta. O loop `while` precisa ser corrigido para garantir a progressão correta do personagem, sem loops infinitos.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O loop deve continuar enquanto a `xp_atual` for menor que a `xp_necessario`. A cada iteração, o nível deve ser incrementado e a `xp_necessario` deve ser recalculada.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento de R$ {proj.get_recompensa():.2f} reflete a importância desta lógica para a experiência do jogador.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a condição de parada do loop?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Gerador de Loot
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Loot'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de loot precisa de um gerador com pesos. Itens raros devem ter uma chance menor de aparecer. A implementação deve ser eficiente.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A performance é o fator mais importante. O uso de `random.choices` é o padrão esperado pela indústria para esta tarefa.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O pagamento é R$ {proj.get_recompensa():.2f}. Não há espaço para negociação, apenas para excelência.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se você puder garantir que a sua função tem complexidade O(1) e documentar os testes de performance, posso autorizar um bônus de 25%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a abordagem de implementação preferida?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Desafio]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 85] E se eu fornecer um relatório de performance detalhado?", 85, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus de performance]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: Café Aconchego (ID 11 - Personalidade: Amigável) ---
    print("\n--- Populando diálogos para Café Aconchego ---")

    # Projeto: Calculadora de Troco
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Troco'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi, tudo bem? Meus funcionários às vezes se atrapalham com o troco. Pode fazer uma função que ajude eles a calcular direitinho?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função só precisa receber o total da compra e o valor que o cliente pagou, e dizer quanto é o troco. Simples assim!", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"É um trabalho pequeno, então estamos a oferecer R$ {proj.get_recompensa():.2f}. Espero que ajude!", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Pode me dar um exemplo?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "E o pagamento?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Ajudar o Café]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Entendi! Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Ok. Voltar.", 1, None))

    # Projeto: Gerador de Recibo
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Recibo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queria dar um recibo bonitinho para os clientes. Você consegue fazer uma função que formata uma lista de compras num texto de recibo?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A ideia é receber uma lista de itens com seus preços e gerar uma string com cada item numa linha, bem organizado.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Para este trabalho, o valor é R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual o formato esperado?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o pagamento.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Trabalho]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Sistema de Desconto
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Desconto'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Tentei fazer um desconto para compras grandes, mas acho que fiz algo errado e ele só funciona para compras pequenas! Hahaha, pode arrumar?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O bug está na condição `if`. A lógica está invertida. O desconto de 10% deveria ser para compras acima de R$ 50.00.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor para consertar isso é R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Puxa, não consigo aumentar muito, mas se você puder deixar o código bem comentado para eu entender depois, te pago R$ 550.00!", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Pode me dizer onde acha que está o erro?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 60] E se eu deixar o código super comentado?", 60, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: VarejoTotal (ID 12 - Personalidade: Corporativo) ---
    print("\n--- Populando diálogos para VarejoTotal ---")

    # Projeto: Verificador de Estoque
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Estoque'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Prezado(a), o projeto 'Verificador de Estoque' está disponível para análise. Como podemos proceder?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O escopo requer uma função booleana que verifique a disponibilidade de um produto em nosso inventário (quantidade > 0).", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"A remuneração para esta tarefa está fixada em R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito o briefing técnico.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir a remuneração.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Termos]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))

    # Projeto: Calculadora de Frete
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Frete'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O contrato 'Calculadora de Frete' está aberto para propostas. Quais são as suas questões?", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve utilizar um dicionário como tabela de taxas para mapear o estado (string) ao valor do frete (float).", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor de R$ {proj.get_recompensa():.2f} foi alocado para este desenvolvimento.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Solicito detalhes da implementação.", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Processador de Pedidos
    proj = next((p for p in projetos if p.get_titulo() == 'Processador de Pedidos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de processamento de pedidos está a gerar uma exceção não tratada. É imperativo adicionar um bloco try/except.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O bloco deve capturar um `KeyError` e retornar uma mensagem de erro padronizada: 'Erro: Pedido inválido.'. A robustez do sistema é a prioridade.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor para esta correção crítica é de R$ {proj.get_recompensa():.2f}.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Entendido. Se a sua implementação incluir um log do pedido inválido para auditoria futura, podemos aprovar um bônus de 15%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual exceção deve ser tratada?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Tarefa]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 70] Podemos expandir o escopo para incluir logging?", 70, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus]", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    
    # --- Cliente: Moda Rápida (ID 13 - Personalidade: Direto) ---
    print("\n--- Populando diálogos para Moda Rápida ---")

    # Projeto: Conversor de Tamanhos
    proj = next((p for p in projetos if p.get_titulo() == 'Conversor de Tamanhos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de uma função que converta tamanhos de texto (P, M, G) para números (38, 40, 42). Use um dicionário.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve receber a string do tamanho e retornar o número correspondente. Simples.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}. Sem negociação.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Pagamento?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Filtro de Cores
    proj = next((p for p in projetos if p.get_titulo() == 'Filtro de Cores'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A tarefa é filtrar uma lista de roupas por uma cor específica. Use List Comprehension para eficiência.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A entrada será uma lista de dicionários, cada um com uma chave 'cor'. O retorno deve ser uma lista contendo apenas os dicionários que correspondem à cor.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"O valor é R$ {proj.get_recompensa():.2f}.", False))
        
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Qual a estrutura dos dados de entrada?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Contrato]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Voltar.", 1, None))

    # Projeto: Alerta de Estoque Baixo
    proj = next((p for p in projetos if p.get_titulo() == 'Alerta de Estoque Baixo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        req_detalhes = req_social_map.get(proj.get_dificuldade(), 1)
        hub = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Função para percorrer o dicionário de estoque e retornar uma lista de itens com menos de 5 unidades. Rápido.", True))
        no_detalhes = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A função deve ser performática. O dicionário de entrada é no formato {'item': quantidade}.", False))
        no_pagamento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), f"Pagamento: R$ {proj.get_recompensa():.2f}. O prazo é curto.", False))
        no_aumento = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Se a entrega for feita em metade do prazo, autorizo um bônus de 20%.", False))

        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_detalhes.get_id_no(), f"[Social {req_detalhes}] Detalhes da estrutura de dados?", req_detalhes, 'REVELAR_DETALHES'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), no_pagamento.get_id_no(), "Discutir o valor.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, hub.get_id_no(), None, "[Aceitar Tarefa]", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_detalhes.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), hub.get_id_no(), "Retornar.", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_pagamento.get_id_no(), no_aumento.get_id_no(), "[Social 70] E se eu garantir a entrega antecipada?", 70, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no_aumento.get_id_no(), None, "[Aceitar com o bônus de agilidade]", 1, 'ACEITAR_PROJETO_COM_BONUS'))
if __name__ == "__main__":
    print("Iniciando script de população de diálogos...")
    
    db_manager = BancoDeDadosIntermediario()
    db_manager.criarBanco()

    dialogo_service = DialogoServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()
    cliente_service = ClienteServiceImpl()

    popular_dialogos(dialogo_service, projeto_service, cliente_service)

    print("\nPopulação de diálogos concluída!")
