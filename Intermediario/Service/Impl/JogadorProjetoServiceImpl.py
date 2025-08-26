from Intermediario.Service.JogadorProjetoService import JogadorProjetoService
from Intermediario.Persistencia.Impl.JogadorProjetoPersistenciaImpl import JogadorProjetoPersistenciaImpl
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl

class JogadorProjetoServiceImpl(JogadorProjetoService):
    def __init__(self):
        self.persistencia = JogadorProjetoPersistenciaImpl()
        self.projeto_persistencia = ProjetoFreelancePersistenciaImpl() 

    def aceitar_projeto(self, jogador_projeto):
        # A lógica de negócio (verificar se já tem projeto, etc.) fica no GameManager
        # O serviço aqui apenas executa a ação de salvar.
        self.persistencia.salvar(jogador_projeto)

    def buscar_projeto_ativo(self, id_jogador):
        projetos_do_jogador = self.persistencia.listar_por_jogador(id_jogador)
        for relacao in projetos_do_jogador:
            if relacao.get_status() == "em_andamento":
                return self.projeto_persistencia.buscar_por_id(relacao.get_id_projeto())
        return None
