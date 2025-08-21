from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class ProjetoFreelancePersistencia(ABC):

    @abstractmethod
    def salvar(self, projeto: ProjetoFreelance) -> ProjetoFreelance:
        pass

    @abstractmethod
    def atualizar(self, projeto: ProjetoFreelance) -> None:
        pass

    @abstractmethod
    def deletar(self, id_projeto: int) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_projeto: int) -> ProjetoFreelance | None:
        pass

    @abstractmethod
    def listar_disponiveis(self) -> list[ProjetoFreelance]:
        """Lista apenas os projetos disponíveis para o jogador"""
        pass

    @abstractmethod
    def listar_por_cliente(self, id_cliente: int) -> list[ProjetoFreelance]:
        pass
