from Intermediario.Service.ProjetoFreelanceService import ProjetoFreelanceService
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl

class ProjetoFreelanceServiceImpl(ProjetoFreelanceService):
    def __init__(self):
        self.persistencia = ProjetoFreelancePersistenciaImpl()

    def criar_projeto(self, projeto):
        return self.persistencia.inserir(projeto)

    def atualizar_projeto(self, projeto):
        return self.persistencia.atualizar(projeto)

    def deletar_projeto(self, id_projeto):
        return self.persistencia.deletar(id_projeto)

    def buscar_projeto_por_id(self, id_projeto):
        return self.persistencia.buscar_por_id(id_projeto)

    def listar_projetos(self):
        return self.persistencia.listar_todos()

    def listar_projetos_disponiveis(self):
        projetos = self.persistencia.listar_todos()
        return [p for p in projetos if p.get_status() == "disponivel"]