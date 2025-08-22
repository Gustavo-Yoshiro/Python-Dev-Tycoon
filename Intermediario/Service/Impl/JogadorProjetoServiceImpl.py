from Intermediario.Service.JogadorProjetoService import JogadorProjetoService
from Intermediario.Persistencia.Impl.JogadorProjetoPersistenciaImpl import JogadorProjetoPersistenciaImpl
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto

class JogadorProjetoServiceImpl(JogadorProjetoService):
    def __init__(self):
        self.persistencia = JogadorProjetoPersistenciaImpl()

    def aceitar_projeto(self, jogador_projeto: JogadorProjeto) -> None:
        self.persistencia.salvar(jogador_projeto)

    def atualizar_status(self, jogador_projeto: JogadorProjeto) -> None:
        self.persistencia.atualizar_status(jogador_projeto)

    def remover_relacao(self, id_jogador: int, id_projeto: int) -> None:
        self.persistencia.remover(id_jogador, id_projeto)

    def buscar_relacao(self, id_jogador: int, id_projeto: int) -> JogadorProjeto | None:
        return self.persistencia.buscar(id_jogador, id_projeto)

    def listar_projetos_do_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        return self.persistencia.listar_por_jogador(id_jogador)