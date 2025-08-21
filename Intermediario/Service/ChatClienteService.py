from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente

class ChatClienteService(ABC):
    @abstractmethod
    def enviar_mensagem(self, chat: ChatCliente):
        pass

    @abstractmethod
    def atualizar_mensagem(self, chat: ChatCliente):
        pass

    @abstractmethod
    def deletar_mensagem(self, id_chat: int):
        pass

    @abstractmethod
    def buscar_mensagem_por_id(self, id_chat: int):
        pass

    @abstractmethod
    def listar_mensagens(self):
        pass

    @abstractmethod
    def listar_conversa(self, id_jogador: int, id_cliente: int):
        pass