from abc import ABC, abstractmethod

class ClienteService(ABC):
    @abstractmethod
    def criar_cliente(self, cliente):
        pass

    @abstractmethod
    def buscar_cliente_por_id(self, id_cliente):
        pass

    @abstractmethod
    def listar_clientes(self):
        pass

    @abstractmethod
    def atualizar_cliente(self, cliente):
        pass

    @abstractmethod
    def deletar_cliente(self, id_cliente):
        pass
