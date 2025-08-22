from abc import ABC, abstractmethod

class ProgressoFaseService(ABC):
    @abstractmethod
    def criar_progresso(self, id_jogador, id_fase, indice_exercicio=0, acertos=0, erros=0, resposta_parcial=""):
        pass

    @abstractmethod
    def buscar_progresso_por_id(self, id_progresso):
        pass

    @abstractmethod
    def buscar_progresso_por_jogador_fase(self, id_jogador, id_fase):
        pass

    @abstractmethod
    def listar_todos_progresso(self):
        pass

    @abstractmethod
    def deletar_progresso(self, id_progresso):
        pass

    @abstractmethod
    def atualizar_progresso(self, progresso):
        pass

    @abstractmethod
    def fase_ja_concluida(self, id_jogador, id_fase, total_exercicios):
        pass

    # Outros métodos específicos, se desejar
