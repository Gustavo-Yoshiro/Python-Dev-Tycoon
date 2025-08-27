# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def popular_clientes(cliente_service: ClienteServiceImpl):
    """
    Insere uma lista extensa de clientes no banco de dados,
    verificando antes se eles já não existem.
    """
    # Verifica se a tabela já está populada para não inserir duplicatas
    if cliente_service.listar_clientes():
        print("Clientes já existem no banco. Pulando a inserção em massa.")
        return

    print("Inserindo uma nova lista de clientes...")

    clientes = [
        # Startups e Tech
        Cliente(id_cliente=None, nome='InovaTech Solutions', area_atuacao='Startups', descricao='Focada em soluções ágeis para o mercado.', reputacao=4.7, personalidade='Direto'),
        Cliente(id_cliente=None, nome='CyberSec Alliance', area_atuacao='Segurança', descricao='Protegendo o mundo digital.', reputacao=4.9, personalidade='Corporativo'),
        Cliente(id_cliente=None, nome='CloudNexus', area_atuacao='Infraestrutura', descricao='Serviços de nuvem escaláveis.', reputacao=4.6, personalidade='Técnico'),
        Cliente(id_cliente=None, nome='AppFactory', area_atuacao='Mobile', descricao='Criamos apps que encantam usuários.', reputacao=4.8, personalidade='Amigável'),

        # Análise de Dados e IA
        Cliente(id_cliente=None, nome='DataSolutions Inc.', area_atuacao='Análise de Dados', descricao='Transformando dados em decisões estratégicas.', reputacao=4.9, personalidade='Corporativo'),
        Cliente(id_cliente=None, nome='QuantumLeap AI', area_atuacao='IA', descricao='Pioneiros em inteligência artificial.', reputacao=5.0, personalidade='Exigente'),
        Cliente(id_cliente=None, nome='MarketMetrics', area_atuacao='Marketing Digital', descricao='Análise de dados para campanhas de marketing.', reputacao=4.4, personalidade='Direto'),

        # Jogos e Entretenimento
        Cliente(id_cliente=None, nome='GameCraft Studios', area_atuacao='Jogos Indie', descricao='Criamos jogos com paixão e criatividade!', reputacao=4.5, personalidade='Amigável'),
        Cliente(id_cliente=None, nome='Pixel Potion', area_atuacao='Jogos Mobile', descricao='Jogos casuais para todos.', reputacao=4.2, personalidade='Amigável'),
        Cliente(id_cliente=None, nome='Epic Worlds RPG', area_atuacao='Jogos RPG', descricao='Construindo universos de fantasia.', reputacao=4.8, personalidade='Exigente'),

        # Comércio e Varejo
        Cliente(id_cliente=None, nome='Café Aconchego', area_atuacao='Pequeno Comércio', descricao='Café e doces caseiros com um toque de tecnologia.', reputacao=5.0, personalidade='Amigável'),
        Cliente(id_cliente=None, nome='VarejoTotal', area_atuacao='E-commerce', descricao='Plataforma de vendas online.', reputacao=4.3, personalidade='Corporativo'),
        Cliente(id_cliente=None, nome='Moda Rápida', area_atuacao='Varejo', descricao='Sistema de gestão de estoque para lojas.', reputacao=4.1, personalidade='Direto')
    ]
    
    for cliente in clientes:
        try:
            cliente_service.criar_cliente(cliente)
        except Exception as e:
            print(f"Erro ao inserir cliente {cliente.get_nome()}: {e}")

    print(f"-> {len(clientes)} novos clientes foram adicionados ao banco de dados.")


if __name__ == "__main__":
    print("Iniciando script de população de clientes...")
    

    # Instancia o serviço necessário
    cliente_service = ClienteServiceImpl()

    # Executa a função de população
    popular_clientes(cliente_service)

    print("\nPopulação de clientes concluída!")
