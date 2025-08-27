# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.DialogoServiceImpl import DialogoServiceImpl
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.Dialogo import DialogoNo, DialogoOpcao
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def limpar_dialogos_antigos(dialogo_service):
    """Função auxiliar para limpar as tabelas de diálogo antes de inserir novos dados."""
    # Você precisaria implementar estes métodos na sua camada de persistência/serviço
    # Exemplo:
    # dialogo_service.opcao_persistencia.deletar_todos()
    # dialogo_service.no_persistencia.deletar_todos()
    print("Diálogos antigos foram limpos (simulado).")

def popular_dialogos(dialogo_service: DialogoServiceImpl, projeto_service: ProjetoFreelanceServiceImpl):
    """
    Popula as árvores de diálogo para os projetos existentes, com base na
    personalidade do cliente e com opções dependentes de skills.
    """
    limpar_dialogos_antigos(dialogo_service)
    
    # Busca todos os projetos para podermos associar os diálogos
    projetos = projeto_service.persistencia.listar_disponiveis()

    # --- Cliente: InovaTech Solutions (Personalidade: Direto) ---

    # Projeto: Validador de Senha Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Senha Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de um validador de senhas. Mínimo de 8 caracteres. Cumpra o prazo.", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Não há mais detalhes. A especificação é clara. Apenas execute.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. Aceito o trabalho.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 30] Poderia me dar mais detalhes sobre a complexidade?", 30, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Compreendido. Aceito o desafio.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Gerador de API Key
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de API Key'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Gerador de chaves de API. 16 caracteres. Alfanumérico. Entregue.", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Segurança é fundamental. A inclusão de caracteres especiais aumentaria o valor do contrato em 20%.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Simples e direto. Aceito.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 40] Podemos discutir a inclusão de caracteres especiais para maior segurança?", 40, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Excelente. Aceito com o bônus de segurança.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # Projeto: Otimizador de Loop de Busca
    proj = next((p for p in projetos if p.get_titulo() == 'Otimizador de Loop de Busca'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso loop de busca está lento. Otimize-o. Use um dicionário para acesso O(1).", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Refatoração é minha especialidade. Aceito.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: CyberSec Alliance (Personalidade: Corporativo) ---

    # Projeto: Verificador de Porta Aberta
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Porta Aberta'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Prezado(a), solicitamos um script para validar se uma porta de rede consta em nossa lista de portas seguras, conforme as diretrizes de segurança.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Compreendido. Procederei com o desenvolvimento.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Não possuo a expertise necessária no momento.", 1, 'RECUSAR_PROJETO'))

    # Projeto: Analisador de Logs Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de Logs Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Requeremos uma função que quantifique as ocorrências da string 'ERRO' em nossos logs de sistema para fins de auditoria.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Tarefa recebida. Iniciarei a implementação.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Sanitizador de Input
    proj = next((p for p in projetos if p.get_titulo() == 'Sanitizador de Input'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema apresenta uma vulnerabilidade de SQL Injection. O script de sanitização está incompleto. Solicitamos a correção imediata.", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Agradecemos a sua proatividade. A segurança de nossos clientes é primordial. O valor do contrato será ajustado em conformidade.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Segurança é prioridade. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 65] Além de corrigir, sugiro implementar um log de tentativas de injeção.", 65, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Excelente iniciativa. Aceito com o escopo expandido.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: CloudNexus (Personalidade: Técnico) ---

    # Projeto: Calculadora de Custo de VM
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Custo de VM'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Necessito de uma função para calcular o custo mensal de uma VM. A fórmula é `custo_por_hora * 720`.", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A precisão é fundamental. Use ponto flutuante e garanta que o arredondamento seja de duas casas decimais.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Lógica recebida. Aceito a tarefa.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 25] Alguma consideração sobre a precisão do cálculo?", 25, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Entendido. A precisão será garantida. Aceito.", 1, 'ACEITAR_PROJETO'))
        
    # Projeto: Verificador de Status de Serviço
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Status de Serviço'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Input: um dicionário de serviços e seus status. Output: uma lista com os nomes dos serviços 'offline'.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Especificação clara. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Provisionador de Recursos
    proj = next((p for p in projetos if p.get_titulo() == 'Provisionador de Recursos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O script de provisionamento usa `if/elifs` excessivos. Refatore para usar um dicionário como um dispatcher para otimizar a performance.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. A refatoração será feita. Aceito.", 1, 'ACEITAR_PROJETO'))

        # Projeto: Contador de Cliques
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Cliques'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oizinho! Precisamos de uma função super simples que conte os cliques no nosso novo app. É só incrementar uma variável!", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Que legal! Adoraria ajudar. Aceito!", 1, 'ACEITAR_PROJETO'))

    # Projeto: Validador de Username
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Username'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi! Nosso app precisa validar usernames. As regras são: entre 4 e 12 caracteres, sem espaços. Topa?", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Claro! Parece um desafio interessante. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Gerador de Notificações
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Notificações'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Precisamos de uma função que crie notificações personalizadas com f-strings. Algo bem amigável para nossos usuários!", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Perfeito! Se você puder adicionar o nome do app ('AppFactory') no final da notificação, seria incrível. Posso te dar um bônus por isso.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Adoro trabalhar com formatação de texto. Aceito!", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 50] Que tal adicionar um emoji para deixar ainda mais amigável?", 50, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Ótima ideia! Aceito com o bônus.", 1, 'ACEITAR_PROJETO_COM_BONUS'))

    # --- Cliente: DataSolutions Inc. (Personalidade: Corporativo) ---

    # Projeto: Calculadora de Média
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Média'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Solicitamos o desenvolvimento de uma função para calcular a média aritmética de uma lista de valores numéricos.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Recebido. Iniciarei o desenvolvimento. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Limpador de Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Limpador de Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "O dataset de vendas contém entradas negativas espúrias. Requeremos uma função que as remova, utilizando List Comprehension para eficiência.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Compreendido. A solução será implementada. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Agrupador de Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Agrupador de Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Necessitamos de uma função que agrupe uma lista de dicionários por uma chave categórica, retornando um dicionário de listas.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: QuantumLeap AI (Personalidade: Exigente) ---

    # Projeto: Classificador Simples
    proj = next((p for p in projetos if p.get_titulo() == 'Classificador Simples'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A tarefa é trivial, mas exigimos 100% de acurácia. Uma função que classifique um número como 'Positivo' ou 'Negativo'. Não erre.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Apesar da simplicidade, garanto a qualidade. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Processador de Dataset
    proj = next((p for p in projetos if p.get_titulo() == 'Processador de Dataset'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nossos modelos de IA requerem dados imutáveis. Converta esta lista de listas em uma lista de tuplas. A performance é crucial.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. A imutabilidade e a performance serão garantidas. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Validador de Erros de Modelo
    proj = next((p for p in projetos if p.get_titulo() == 'Validador de Erros de Modelo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Uma função de cálculo de performance está a causar uma falha crítica (divisão por zero). Implemente um tratamento de erro robusto.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "A robustez do código é minha prioridade. Aceito.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: MarketMetrics (Personalidade: Direto) ---

    # Projeto: Contador de Palavras-chave
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Palavras-chave'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de uma função que conte a ocorrência de uma palavra-chave em um texto. Simples.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Extrator de Hashtags
    proj = next((p for p in projetos if p.get_titulo() == 'Extrator de Hashtags'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Extrair todas as palavras que começam com '#' de um texto. Retornar uma lista.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Compreendido. Aceito o trabalho.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Analisador de A/B Test
    proj = next((p for p in projetos if p.get_titulo() == 'Analisador de A/B Test'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Função para comparar a média de duas listas de resultados (A e B). Retornar 'A' ou 'B'.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Lógica clara. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))

     # --- Cliente: GameCraft Studios (Personalidade: Amigável) ---
    
    # Projeto: Verificador de Nível
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Nível'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí! Uma ajudinha rápida: precisamos de uma função que diga se o nível do jogador é alto o suficiente para usar um item. Coisa simples!", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Pode deixar, lógica de jogo é comigo mesmo. Aceito!", 1, 'ACEITAR_PROJETO'))

    # Projeto: Contador de Inventário
    proj = next((p for p in projetos if p.get_titulo() == 'Contador de Inventário'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Opa! Nosso script de inventário precisa de um upgrade. Queremos uma função que conte quantos itens de um tipo específico o jogador tem na bolsa (uma lista).", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Trabalhar com listas é tranquilo. Aceito o desafio.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Sistema de Missões
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Missões'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "E aí, dev! :) Nosso RPG precisa de um sistema pra checar se o jogador completou um grupo de missões. Acha que consegue?", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Show! A ideia é usar `sets` do Python, que são super eficientes pra isso. Basicamente, é ver se o conjunto de missões requeridas é um subconjunto das missões que o jogador já fez.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "Parece divertido! Como vocês pensaram em fazer?", 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Entendi a lógica. Pode deixar comigo!", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: Pixel Potion (Personalidade: Amigável) ---

    # Projeto: Gerador de Moedas
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Moedas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oizinho! Queremos dar umas moedinhas pros nossos jogadores. Pode fazer uma função que sorteia um número entre 10 e 50? :D", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Claro, uma função de sorteio é moleza. Aceito!", 1, 'ACEITAR_PROJETO'))

    # Projeto: Sistema de Vidas
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Vidas'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Socorro! Nossa função de perder vida não tá funcionando, o jogador fica imortal! Hahaha. Pode consertar pra gente?", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Um bug de imortalidade? Interessante. Deixa eu ver isso. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Tabela de High Scores
    proj = next((p for p in projetos if p.get_titulo() == 'Tabela de High Scores'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queremos mostrar os melhores jogadores! Preciso de uma função que ordene uma lista de jogadores (dicionários) pela maior pontuação ('score').", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Hmm, boa pergunta. Se for fácil pra você, seria legal mostrar o nome em maiúsculas pra dar destaque. Se não, tudo bem!", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Ordenar dados é uma tarefa importante. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 45] Algum requisito de formatação para os nomes na tabela final?", 45, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Sem problemas, posso formatar os nomes. Aceito.", 1, 'ACEITAR_PROJETO'))


    # --- Cliente: Epic Worlds RPG (Personalidade: Exigente) ---

    # Projeto: Rolar Dados
    proj = next((p for p in projetos if p.get_titulo() == 'Rolar Dados'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Exigimos uma simulação de rolagem de um d20. O resultado deve ser um inteiro, precisamente entre 1 e 20, inclusive. Sem desvios.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "A precisão será garantida. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Calculadora de XP
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de XP'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A lógica de subida de nível está incompleta. O loop `while` precisa ser corrigido para garantir a progressão correta do personagem.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Lógica de progressão é crítica. Aceito a responsabilidade.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Gerador de Loot
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Loot'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de loot precisa de um gerador com pesos. Itens raros devem ter uma chance menor de aparecer. A implementação deve ser eficiente.", True))
        n2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A performance é o fator mais importante. O uso de `random.choices` é o padrão esperado pela indústria para esta tarefa.", False))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Um sistema de loot ponderado é um desafio interessante. Aceito.", 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), n2.get_id_no(), "[Social 55] Qual a prioridade: performance ou facilidade de manutenção do código?", 55, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n2.get_id_no(), None, "Entendido. Focarei na performance. Aceito.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: Café Aconchego (Personalidade: Amigável) ---

    # Projeto: Calculadora de Troco
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Troco'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Oi, tudo bem? Meus funcionários às vezes se atrapalham com o troco. Pode fazer uma função que ajude eles a calcular direitinho?", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Claro, posso ajudar com isso! Aceito o trabalho.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Gerador de Recibo
    proj = next((p for p in projetos if p.get_titulo() == 'Gerador de Recibo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Queria dar um recibo bonitinho para os clientes. Você consegue fazer uma função que formata uma lista de compras num texto de recibo?", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Com certeza! Um recibo bem formatado faz toda a diferença. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Sistema de Desconto
    proj = next((p for p in projetos if p.get_titulo() == 'Sistema de Desconto'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Tentei fazer um desconto para compras grandes, mas acho que fiz algo errado e ele só funciona para compras pequenas! Hahaha, pode arrumar?", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Acontece! Vou corrigir a lógica para você. Aceito.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: VarejoTotal (Personalidade: Corporativo) ---

    # Projeto: Verificador de Estoque
    proj = next((p for p in projetos if p.get_titulo() == 'Verificador de Estoque'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Prezado(a), necessitamos de uma função booleana para verificar a disponibilidade de um produto em nosso inventário (quantidade > 0).", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. A função será desenvolvida conforme solicitado. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Calculadora de Frete
    proj = next((p for p in projetos if p.get_titulo() == 'Calculadora de Frete'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Solicitamos a implementação de uma função que calcule o valor do frete com base no estado de destino, utilizando uma tabela de taxas (dicionário).", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Compreendido. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Processador de Pedidos
    proj = next((p for p in projetos if p.get_titulo() == 'Processador de Pedidos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Nosso sistema de processamento de pedidos está a gerar uma exceção não tratada para pedidos malformados. É imperativo adicionar um bloco try/except.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "A robustez do sistema é fundamental. Aceito a tarefa.", 1, 'ACEITAR_PROJETO'))

    # --- Cliente: Moda Rápida (Personalidade: Direto) ---

    # Projeto: Conversor de Tamanhos
    proj = next((p for p in projetos if p.get_titulo() == 'Conversor de Tamanhos'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Preciso de uma função que converta tamanhos de texto (P, M, G) para números (38, 40, 42). Use um dicionário.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Entendido. Aceito.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Filtro de Cores
    proj = next((p for p in projetos if p.get_titulo() == 'Filtro de Cores'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "A tarefa é filtrar uma lista de roupas por uma cor específica. Use List Comprehension.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Compreendido. Aceito o trabalho.", 1, 'ACEITAR_PROJETO'))

    # Projeto: Alerta de Estoque Baixo
    proj = next((p for p in projetos if p.get_titulo() == 'Alerta de Estoque Baixo'), None)
    if proj:
        print(f"Criando diálogo para: {proj.get_titulo()}")
        n1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj.get_id_projeto(), "Função para percorrer o dicionário de estoque e retornar uma lista de itens com menos de 5 unidades. Rápido.", True))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, n1.get_id_no(), None, "Lógica clara. Aceito o contrato.", 1, 'ACEITAR_PROJETO'))


if __name__ == "__main__":
    print("Iniciando script de população de diálogos...")
    

    # Instancia os serviços necessários
    dialogo_service = DialogoServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()

    # Executa a função de população
    popular_dialogos(dialogo_service, projeto_service)

    print("\nPopulação de diálogos concluída!")
