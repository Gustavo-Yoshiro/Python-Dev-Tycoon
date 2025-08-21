from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente

class ChatClientePersistencia(ABC):

    @abstractmethod
    def enviar_mensagem(self, chat: ChatCliente) -> ChatCliente:
        pass

    @abstractmethod
    def listar_conversa(self, id_jogador: int, id_cliente: int) -> list[ChatCliente]:
        pass
