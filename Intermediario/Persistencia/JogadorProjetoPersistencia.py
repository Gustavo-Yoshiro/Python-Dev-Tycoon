from abc import ABC, abstractmethod

class JogadorProjetoPersistencia(ABC):
    
    @abstractmethod
    def salvar(self, jogador_projeto):
        pass

    @abstractmethod
    def buscar(self, id_jogador, id_projeto):
        pass

    @abstractmethod
    def listar_por_jogador(self, id_jogador):
        pass

    @abstractmethod
    def atualizar_status(self, id_jogador, id_projeto, novo_status):
        pass

    @abstractmethod
    def atualizar_detalhes(self, id_jogador, id_projeto, novos_detalhes):
        pass

    @abstractmethod
    def buscar_detalhes(self, id_jogador, id_projeto):
        pass