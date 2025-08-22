from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.Cliente import Cliente

class ClienteService(ABC):
    @abstractmethod
    def criar_cliente(self, cliente: Cliente) -> Cliente:
        """Cria um novo cliente no sistema."""
        pass

    @abstractmethod
    def buscar_cliente_por_id(self, id_cliente: int) -> Cliente | None:
        """Busca cliente pelo seu ID."""
        pass

    @abstractmethod
    def listar_clientes(self) -> list[Cliente]:
        """Retorna todos os clientes cadastrados."""
        pass

    @abstractmethod
    def atualizar_cliente(self, cliente: Cliente) -> None:
        """Atualiza os dados de um cliente existente."""
        pass

    @abstractmethod
    def deletar_cliente(self, id_cliente: int) -> None:
        """Remove um cliente pelo seu ID."""
        pass