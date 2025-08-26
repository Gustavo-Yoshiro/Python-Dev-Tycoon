from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Entidade.Jogador import Jogador # Assumindo a localização da entidade Jogador

class ProjetoFreelanceService(ABC):
    
    @abstractmethod
    def criar_projeto(self, projeto):
        pass

    @abstractmethod
    def listar_projetos_para_jogador(self, jogador):
        pass

    @abstractmethod
    def deletar_todos_projetos(self):
        pass
