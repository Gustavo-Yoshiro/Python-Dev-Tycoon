from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto

class JogadorProjetoService(ABC):
    @abstractmethod
    def aceitar_projeto(self, jogador_projeto: JogadorProjeto) -> None:
        pass

    @abstractmethod
    def atualizar_status(self, jogador_projeto: JogadorProjeto) -> None:
        pass

    @abstractmethod
    def remover_relacao(self, id_jogador: int, id_projeto: int) -> None:
        pass

    @abstractmethod
    def buscar_relacao(self, id_jogador: int, id_projeto: int) -> JogadorProjeto | None:
        pass

    @abstractmethod
    def listar_projetos_do_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        pass