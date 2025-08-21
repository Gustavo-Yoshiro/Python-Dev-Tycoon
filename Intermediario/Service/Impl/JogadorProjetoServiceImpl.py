from Intermediario.Service.JogadorProjetoService import JogadorProjetoService
from Persistencia.Impl.JogadorProjetoPersistenciaImpl import JogadorProjetoPersistenciaImpl

class JogadorProjetoServiceImpl(JogadorProjetoService):
    def __init__(self):
        self.persistencia = JogadorProjetoPersistenciaImpl()

    def aceitar_projeto(self, jogador_projeto):
        return self.persistencia.inserir(jogador_projeto)

    def atualizar_status(self, jogador_projeto):
        return self.persistencia.atualizar(jogador_projeto)

    def remover_relacao(self, id_jogador, id_projeto):
        return self.persistencia.deletar(id_jogador, id_projeto)

    def buscar_relacao(self, id_jogador, id_projeto):
        return self.persistencia.buscar_por_id(id_jogador, id_projeto)

    def listar_projetos_do_jogador(self, id_jogador):
        return self.persistencia.listar_todos_do_jogador(id_jogador)