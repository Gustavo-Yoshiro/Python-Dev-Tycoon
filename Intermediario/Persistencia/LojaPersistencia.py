from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.Loja import Loja

class LojaPersistencia(ABC):

    @abstractmethod
    def salvar(self, loja: Loja):
        pass

    @abstractmethod
    def buscar_por_id(self, id_item: int) -> Loja:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def listar_por_jogador(self, id_jogador: int) -> list:
        pass

    @abstractmethod
    def deletar(self, id_item: int):
        pass

    @abstractmethod
    def atualizar(self, loja: Loja):
        pass

    @abstractmethod
    def listar_em_andamento(self, id_jogador: int) -> list:
        pass

    @abstractmethod
    def concluir_item(self, id_item: int):
        pass
