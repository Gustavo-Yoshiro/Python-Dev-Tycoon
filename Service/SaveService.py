from abc import ABC, abstractmethod
from Persistencia.Entidade.Save import Save

class SaveService(ABC):

    @abstractmethod
    def adicionar_save(self, save: Save):
        pass

    @abstractmethod
    def buscar_save(self, id_save: int) -> Save:
        pass

    @abstractmethod
    def listar_saves(self) -> list:
        pass

    @abstractmethod
    def atualizar_save(self, save: Save):
        pass

    @abstractmethod
    def remover_save(self, id_save: int):
        pass

    @abstractmethod
    def listar_saves_do_jogador(self, id_jogador: int) -> list:
        pass