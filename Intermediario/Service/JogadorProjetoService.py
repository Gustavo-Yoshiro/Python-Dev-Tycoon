from abc import ABC, abstractmethod

class JogadorProjetoService(ABC):
    @abstractmethod
    def aceitar_projeto(self, jogador_projeto):
        pass

    @abstractmethod
    def atualizar_status(self, jogador_projeto):
        pass

    @abstractmethod
    def remover_relacao(self, id_jogador, id_projeto):
        pass

    @abstractmethod
    def buscar_relacao(self, id_jogador, id_projeto):
        pass

    @abstractmethod
    def listar_projetos_do_jogador(self, id_jogador):
        pass