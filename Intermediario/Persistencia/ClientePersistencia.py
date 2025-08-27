from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.Cliente import Cliente

class ClientePersistencia(ABC):
    
    @abstractmethod
    def salvar(self, cliente):
        pass

    @abstractmethod
    def atualizar(self, cliente):
        pass

    @abstractmethod
    def deletar(self, id_cliente):
        pass

    @abstractmethod
    def buscar_por_id(self, id_cliente):
        pass

    @abstractmethod
    def listar_todos(self):
        pass
