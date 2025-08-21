from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto

class JogadorProjetoPersistencia(ABC):

    @abstractmethod
    def aceitar_projeto(self, jogador_projeto: JogadorProjeto) -> JogadorProjeto:
        pass

    @abstractmethod
    def atualizar_status(self, id_jogador: int, id_projeto: int, status: str) -> None:
        pass

    @abstractmethod
    def listar_por_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        pass

    @abstractmethod
    def buscar(self, id_jogador: int, id_projeto: int) -> JogadorProjeto | None:
        pass
