from abc import ABC, abstractmethod

class ExercicioService(ABC):
    
    @abstractmethod
    def listar_exercicios_por_fase(self, id_fase: int) -> list:
        """Retorna todos os exercícios ligados à fase especificada."""
        pass

    @abstractmethod
    def verificar_resposta(self, id_exercicio: int, resposta_usuario: str) -> bool:
        """Verifica se a resposta do usuário está correta."""
        pass

    @abstractmethod
    def obter_dicas(self, id_exercicio: int) -> str:
        """Retorna a dica associada ao exercício."""
        pass