from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto

class JogadorProjetoPersistencia(ABC):

    @abstractmethod
    def salvar(self, jogador_projeto: JogadorProjeto) -> None:
        """Insere um novo registro de jogador-projeto."""
        pass

    @abstractmethod
    def buscar(self, id_jogador: int, id_projeto: int) -> JogadorProjeto | None:
        """Retorna o vínculo entre jogador e projeto, se existir."""
        pass

    @abstractmethod
    def listar_por_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        """Lista todos os projetos associados a um jogador."""
        pass

    @abstractmethod
    def atualizar_status(self, id_jogador: int, id_projeto: int, novo_status: str) -> None:
        """Atualiza o status de um jogador-projeto específico."""
        pass

    @abstractmethod
    def remover(self, id_jogador: int, id_projeto: int) -> None:
        """Remove a relação entre um jogador e um projeto pelo par de IDs."""
        pass