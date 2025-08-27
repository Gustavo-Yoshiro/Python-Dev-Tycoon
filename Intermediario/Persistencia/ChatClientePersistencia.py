from abc import ABC, abstractmethod

class ChatClientePersistencia(ABC):
    
    @abstractmethod
    def salvar(self, chat_cliente):
        pass

    @abstractmethod
    def listar_por_cliente_e_jogador(self, id_cliente, id_jogador):
        pass
