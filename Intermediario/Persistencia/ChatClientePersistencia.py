from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente

class ChatClientePersistencia(ABC):

    @abstractmethod
    def salvar(self, chat: ChatCliente) -> None:
        """Insere uma nova mensagem de chat."""
        pass

    @abstractmethod
    def buscar_por_id(self, id_chat: int) -> ChatCliente | None:
        """Busca uma mensagem específica pelo seu ID."""
        pass

    @abstractmethod
    def listar_por_jogador(self, id_jogador: int) -> list[ChatCliente]:
        """Lista todas as mensagens enviadas/recebidas por um jogador."""
        pass

    @abstractmethod
    def listar_por_cliente(self, id_cliente: int) -> list[ChatCliente]:
        """Lista todas as mensagens enviadas/recebidas por um cliente."""
        pass