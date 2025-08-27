from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Entidade.Jogador import Jogador

class DialogoService(ABC):
    
    @abstractmethod
    def iniciar_conversa(self, id_projeto):
        """Busca o primeiro nó de diálogo para um determinado projeto."""
        pass

    @abstractmethod
    def buscar_opcoes_disponiveis(self, id_no_atual, jogador):
        """Busca as próximas opções de diálogo disponíveis para um jogador, com base em suas skills."""
        pass

    @abstractmethod
    def buscar_proximo_no(self, id_no_destino):
        """Busca o próximo nó da conversa com base na escolha do jogador."""
        pass

    @abstractmethod
    def processar_escolha_dialogo(self, projeto, opcao_escolhida, jogador):
        pass