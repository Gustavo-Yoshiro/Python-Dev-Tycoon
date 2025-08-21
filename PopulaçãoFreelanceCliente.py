from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance


def popular_clientes(cliente_service: ClienteServiceImpl) -> None:
    clientes = [
        Cliente(nome="Sr. Silva", area_atuacao="Desenvolvimento Web", reputacao=70,
                descricao="Especialista em sites institucionais."),
        Cliente(nome="Dra. Luna", area_atuacao="Ciência de Dados", reputacao=85,
                descricao="Consultora de dados e inteligência artificial."),
        Cliente(nome="Carlos Dev", area_atuacao="Mobile", reputacao=60,
                descricao="Precisa de apps rápidos para startups."),
        Cliente(nome="Maria Code", area_atuacao="Automação", reputacao=75,
                descricao="Focada em bots e scripts para empresas.")
    ]
    for cliente in clientes:
        cliente_service.criar_cliente(cliente)
    print(f"{len(clientes)} clientes inseridos.")


def popular_projetos(projeto_service: ProjetoFreelanceServiceImpl) -> None:
    projetos = [
        ProjetoFreelance(id_cliente=1, titulo="Site em Flask",
                         descricao="Criar site com login e dashboard", dificuldade=2,
                         recompensa=300, habilidade_requerida="Python", status="disponivel"),
        ProjetoFreelance(id_cliente=2, titulo="Análise de Vendas",
                         descricao="Explorar dataset e gerar insights", dificuldade=3,
                         recompensa=500, habilidade_requerida="Pandas", status="disponivel"),
        ProjetoFreelance(id_cliente=3, titulo="Aplicativo Android",
                         descricao="Criar app de lista de tarefas", dificuldade=1,
                         recompensa=200, habilidade_requerida="Kivy", status="disponivel"),
        ProjetoFreelance(id_cliente=4, titulo="Bot de Automação",
                         descricao="Automatizar envio de e-mails", dificuldade=2,
                         recompensa=350, habilidade_requerida="Selenium", status="disponivel")
    ]
    for projeto in projetos:
        projeto_service.criar_projeto(projeto)
    print(f"{len(projetos)} projetos inseridos.")


if __name__ == "__main__":
    # Agora usamos apenas os services diretamente
    cliente_service = ClienteServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()

    popular_clientes(cliente_service)
    popular_projetos(projeto_service)

    print("População inicial concluída com sucesso!")