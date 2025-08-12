from abc import ABC, abstractmethod
from Iniciante.Persistencia.Entidade.Jogador import Jogador

class JogadorPersistencia(ABC):

    @abstractmethod
    def salvar(self, jogador: Jogador):
        pass

    @abstractmethod
    def buscar_por_id(self, id_jogador: int) -> Jogador:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def deletar(self, id_jogador: int):
        pass

    @abstractmethod
    def atualizar(self, jogador: Jogador):
        pass

    @abstractmethod
    def buscar_tipo_fase_atual(self, id_jogador):
        pass

    @abstractmethod
    def avancar_fase_jogador(self, id_jogador: int):
        pass

    @abstractmethod
    def apagar_jogador(self, id_jogador:int):
        pass