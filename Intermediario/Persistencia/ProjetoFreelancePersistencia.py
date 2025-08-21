from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class ProjetoFreelancePersistencia(ABC):
    @abstractmethod
    def salvar(self, projeto: ProjetoFreelance) -> ProjetoFreelance:
        """Persiste um novo projeto e retorna o objeto com ID atualizado."""
        pass

    @abstractmethod
    def atualizar(self, projeto: ProjetoFreelance) -> None:
        """Atualiza as informações de um projeto existente."""
        pass

    @abstractmethod
    def deletar(self, id_projeto: int) -> None:
        """Remove um projeto pelo seu ID."""
        pass

    @abstractmethod
    def buscar_por_id(self, id_projeto: int) -> ProjetoFreelance | None:
        """Busca um projeto pelo ID, retornando None se não existir."""
        pass

    @abstractmethod
    def listar_disponiveis(self) -> list[ProjetoFreelance]:
        """Lista todos os projetos com status 'disponivel'."""
        pass

    @abstractmethod
    def listar_por_cliente(self, id_cliente: int) -> list[ProjetoFreelance]:
        """Lista todos os projetos de um cliente específico."""
        pass

    @abstractmethod
    def listar_todos(self) -> list[ProjetoFreelance]:
        """Lista todos os projetos, independentemente do status."""
        pass