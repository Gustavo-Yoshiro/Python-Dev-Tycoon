from abc import ABC, abstractmethod
from typing import Optional
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class JogadorProjetoService(ABC):
    @abstractmethod
    def aceitar_projeto(self, jogador_projeto: JogadorProjeto) -> None:
        """Registra que o jogador aceitou um projeto."""
        pass

    @abstractmethod
    def atualizar_status(self, jogador_projeto: JogadorProjeto) -> None:
        """Atualiza o status da relação jogador-projeto."""
        pass

    @abstractmethod
    def remover_relacao(self, id_jogador: int, id_projeto: int) -> None:
        """Remove a relação entre jogador e projeto."""
        pass

    @abstractmethod
    def buscar_relacao(self, id_jogador: int, id_projeto: int) -> Optional[JogadorProjeto]:
        """Busca uma relação específica entre jogador e projeto."""
        pass

    @abstractmethod
    def listar_projetos_do_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        """Lista todos os projetos associados ao jogador."""
        pass

    @abstractmethod
    def buscar_projeto_ativo(self, id_jogador: int) -> Optional[ProjetoFreelance]:
        """Retorna o projeto em andamento do jogador, se houver."""
        pass