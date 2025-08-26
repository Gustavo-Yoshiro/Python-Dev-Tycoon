from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class ProjetoFreelancePersistencia(ABC):
    
    @abstractmethod
    def salvar(self, projeto):
        pass

    @abstractmethod
    def atualizar(self, projeto):
        pass

    @abstractmethod
    def deletar(self, id_projeto):
        pass

    @abstractmethod
    def buscar_por_id(self, id_projeto):
        pass

    @abstractmethod
    def listar_disponiveis(self):
        pass

    @abstractmethod
    def deletar_todos(self):
        pass
