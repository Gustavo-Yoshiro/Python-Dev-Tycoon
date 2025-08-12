from abc import ABC, abstractmethod
from Iniciante.Persistencia.Entidade.ProgressoFase import ProgressoFase

class ProgressoFasePersistencia(ABC):
    @abstractmethod
    def salvar(self, progresso: ProgressoFase):
        pass

    @abstractmethod
    def buscar_por_id(self, id_progresso: int) -> ProgressoFase:
        pass

    @abstractmethod
    def buscar_por_jogador_fase(self, id_jogador: int, id_fase: int) -> ProgressoFase:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def deletar(self, id_progresso: int):
        pass

    @abstractmethod
    def atualizar(self, progresso: ProgressoFase):
        pass

    @abstractmethod
    def deletar_por_jogador_fase(self, id_jogador: int, id_fase: int):
        pass

    @abstractmethod
    def buscar_ultima_fase_do_jogador(self, id_jogador: int):
        pass

