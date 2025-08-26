# Certifique-se de que os caminhos de importação estão corretos
from Intermediario.Service.ProjetoFreelanceService import ProjetoFreelanceService
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Entidade.Jogador import Jogador

class ProjetoFreelanceServiceImpl(ProjetoFreelanceService):
    def __init__(self):
        self.persistencia = ProjetoFreelancePersistenciaImpl()

    def listar_projetos_para_jogador(self, jogador):
        """
        Busca todos os projetos disponíveis e enriquece cada um com um status
        indicando se o jogador possui os requisitos para aceitá-lo.
        """
        projetos_disponiveis = self.persistencia.listar_disponiveis()
        projetos_com_status = []

        for projeto in projetos_disponiveis:
            pode_aceitar = (
                jogador.get_backend() >= projeto.get_req_backend() and
                jogador.get_frontend() >= projeto.get_req_frontend() and
                jogador.get_social() >= projeto.get_req_social()
            )
            projetos_com_status.append({
                "projeto": projeto,
                "pode_aceitar": pode_aceitar
            })
        
        return projetos_com_status

    # --- Outros métodos do serviço ---

    def criar_projeto(self, projeto):
        """Cria um novo projeto de freelance."""
        return self.persistencia.salvar(projeto)

    def deletar_todos_projetos(self):
        """Deleta todos os projetos. Usado para repopular o banco."""
        return self.persistencia.deletar_todos()
