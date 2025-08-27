from abc import ABC, abstractmethod

class ChatClienteService(ABC):
    
    @abstractmethod
    def enviar_mensagem(self, chat_cliente):
        pass

    @abstractmethod
    def buscar_historico(self, id_cliente, id_jogador):
        pass
