from Intermediario.Service.ProjetoFreelanceService import ProjetoFreelanceService
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class ProjetoFreelanceServiceImpl(ProjetoFreelanceService):
    def __init__(self):
        self.persistencia = ProjetoFreelancePersistenciaImpl()

    def criar_projeto(self, projeto: ProjetoFreelance) -> ProjetoFreelance:
        return self.persistencia.salvar(projeto)

    def atualizar_projeto(self, projeto: ProjetoFreelance) -> None:
        self.persistencia.atualizar(projeto)

    def deletar_projeto(self, id_projeto: int) -> None:
        self.persistencia.deletar(id_projeto)

    def buscar_projeto_por_id(self, id_projeto: int) -> ProjetoFreelance | None:
        return self.persistencia.buscar_por_id(id_projeto)

    def listar_projetos(self) -> list[ProjetoFreelance]:
        return self.persistencia.listar_todos()

    def listar_projetos_disponiveis(self) -> list[ProjetoFreelance]:
        return self.persistencia.listar_disponiveis()