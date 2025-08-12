from abc import ABC, abstractmethod
from Iniciante.Persistencia.Entidade.Save import Save

class SavePersistencia(ABC):
    @abstractmethod
    def salvar(self, save: Save):
        pass

    @abstractmethod
    def buscar_por_id(self, id_save: int) -> Save:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def deletar(self, id_save: int):
        pass

    @abstractmethod
    def atualizar(self, save: Save):
        pass

    @abstractmethod
    def pode_salvar(self, id_jogador: int):
        pass