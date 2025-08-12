from abc import ABC, abstractmethod
from Iniciante.Persistencia.Entidade.Exercicio import Exercicio  

class ExercicioPersistencia(ABC):
    
    @abstractmethod
    def salvar(self, exercicio: Exercicio):
        pass

    @abstractmethod
    def buscar_por_id(self, id_exercicio: int) -> Exercicio:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def deletar(self, id_exercicio: int):
        pass

    @abstractmethod
    def atualizar(self, exercicio: Exercicio):
        pass