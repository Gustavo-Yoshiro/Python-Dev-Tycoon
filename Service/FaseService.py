from abc import ABC, abstractmethod

class FaseService(ABC):

    @abstractmethod
    def criar_fase(self, tipo_fase, topico, introducao):
        pass

    @abstractmethod
    def buscar_fase_por_id(self, id_fase):
        pass

    @abstractmethod
    def listar_todas_fases(self):
        pass

    @abstractmethod
    def deletar_fase(self, id_fase):
        pass

    @abstractmethod
    def atualizar_fase(self, fase):
        pass
