# Importe as classes de Serviço, Entidade e o gerenciador do Banco
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def popular_dados_base(cliente_service):
    """Popula os dados essenciais como clientes e o jogador de teste."""
    # Clientes
    if not cliente_service.listar_clientes():
        clientes = [
            Cliente(id_cliente=None, nome='Tech_Inova', area_atuacao='Startups', descricao='Focada em soluções ágeis.', reputacao=4.7, personalidade='Direto'),
            Cliente(id_cliente=None, nome='DataSolutions', area_atuacao='Análise de Dados', descricao='Transformando dados em decisões.', reputacao=4.9, personalidade='Corporativo'),
            Cliente(id_cliente=None, nome='GameCraft', area_atuacao='Jogos Indie', descricao='Criamos jogos com paixão!', reputacao=4.5, personalidade='Amigável'),
            Cliente(id_cliente=None, nome='Café Aconchego', area_atuacao='Pequeno Comércio', descricao='Café e doces caseiros.', reputacao=5.0, personalidade='Amigável')
        ]
        for cliente in clientes:
            cliente_service.criar_cliente(cliente)
        print(f"{len(clientes)} clientes inseridos.")
    else:
        print("Clientes já existem no banco.")

def popular_projetos(projeto_service):
    """Popula os projetos de freelance (desafios) no banco de dados."""
    # Limpa projetos antigos para garantir uma lista nova
    projeto_service.deletar_todos_projetos()
    
    projetos = [
        ProjetoFreelance(id_projeto=None, id_cliente=4, titulo='Calculadora de Café', descricao='Função que multiplica preço pela quantidade.', dificuldade='Iniciante', recompensa=100.00, status='disponivel', req_backend=1, req_frontend=1, req_social=1, tags='Básico, Matemática', data_postagem=None, prazo_dias=2, tipo_desafio='completar',
                         codigo_base='def calcular_total(preco_unitario, quantidade):\n    total = ... # COMPLETE AQUI\n    return f"Total a pagar: R$ {total:.2f}"',
                         testes='[{"entrada_funcao": [3.50, 4], "saida_esperada": "Total a pagar: R$ 14.00"}]'),
        
        ProjetoFreelance(id_projeto=None, id_cliente=3, titulo='Medidor de Dano', descricao='A função de dano crítico está com um bug.', dificuldade='Iniciante', recompensa=300.00, status='disponivel', req_backend=2, req_frontend=1, req_social=2, tags='Lógica, Condicionais', prazo_dias=3, tipo_desafio='debug',
                         codigo_base='def calcular_dano(dano_base, tipo_ataque):\n    if tipo_ataque == "critico":\n        return dano_base / 2\n    else:\n        return dano_base',
                         testes='[{"entrada_funcao": [100, "critico"], "saida_esperada": "200.0"}]')
    ]

    for projeto in projetos:
        projeto_service.criar_projeto(projeto)
    print(f"{len(projetos)} projetos inseridos com sucesso.")


if __name__ == "__main__":
    print("Iniciando a população de Clientes e Projetos...")
    
    db_manager = BancoDeDadosIntermediario()

    cliente_service = ClienteServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()


    popular_dados_base(cliente_service)
    popular_projetos(projeto_service)

    print("\nPopulação de Clientes e Projetos concluída!")
