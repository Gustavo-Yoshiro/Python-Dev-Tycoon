from abc import ABC, abstractmethod
from Iniciante.Persistencia.Entidade.Fase import Fase

class FasePersistencia(ABC):

    @abstractmethod
    def salvar(self, fase: Fase):
        pass

    @abstractmethod
    def buscar_por_id(self, id_fase: int) -> Fase:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def deletar(self, id_fase: int):
        pass

    @abstractmethod
    def atualizar(self, fase: Fase):
        pass
