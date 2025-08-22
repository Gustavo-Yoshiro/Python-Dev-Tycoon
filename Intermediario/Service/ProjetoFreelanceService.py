from abc import ABC, abstractmethod

class ProjetoFreelanceService(ABC):
    @abstractmethod
    def criar_projeto(self, projeto):
        pass

    @abstractmethod
    def atualizar_projeto(self, projeto):
        pass

    @abstractmethod
    def deletar_projeto(self, id_projeto):
        pass

    @abstractmethod
    def buscar_projeto_por_id(self, id_projeto):
        pass

    @abstractmethod
    def listar_projetos(self):
        pass

    @abstractmethod
    def listar_projetos_disponiveis(self):
        pass