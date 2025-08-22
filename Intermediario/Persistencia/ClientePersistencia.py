from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.Cliente import Cliente

class ClientePersistencia(ABC):

    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def atualizar(self, cliente: Cliente) -> None:
        pass

    @abstractmethod
    def deletar(self, id_cliente: int) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_cliente: int) -> Cliente | None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Cliente]:
        pass
