from abc import ABC, abstractmethod

class JogadorProjetoService(ABC):

    @abstractmethod
    def aceitar_projeto(self, jogador_projeto):
        pass

    @abstractmethod
    def buscar_projeto_ativo(self, id_jogador):
        pass
