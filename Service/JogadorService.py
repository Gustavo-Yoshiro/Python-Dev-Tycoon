from abc import ABC, abstractmethod

class JogadorService(ABC):
    @abstractmethod
    def criar_jogador(self, nome, id_fase, social, dinheiro, backend, frontend):
        pass

    @abstractmethod
    def buscar_jogador_por_id(self, id_jogador):
        pass

    @abstractmethod
    def listar_todos_jogadores(self):
        pass

    @abstractmethod
    def deletar_jogador(self, id_jogador):
        pass

    @abstractmethod
    def atualizar_jogador(self, jogador):
        pass

    @abstractmethod
    def premiar_jogador(self, id_jogador, valor):
        pass

    @abstractmethod
    def punir_jogador(self, id_jogador, valor):
        pass

    @abstractmethod
    def evoluir_atributo(self, id_jogador, atributo, valor):
        pass

    @abstractmethod
    def mudar_fase(self, id_jogador, nova_fase):
        pass

    @abstractmethod
    def buscar_progresso(self, id_jogador):
        pass
    # Outros métodos de negócio que quiser!
