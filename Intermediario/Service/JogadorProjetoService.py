from abc import ABC, abstractmethod

class JogadorProjetoService(ABC):

    @abstractmethod
    def aceitar_projeto(self, jogador, projeto):
        """
        Aplica a lógica de negócio para um jogador aceitar um projeto.
        """
        pass

    @abstractmethod
    def buscar_projeto_ativo(self, id_jogador):
        """
        Busca o projeto que está atualmente 'em_andamento' para um jogador.
        """
        pass
    
    @abstractmethod
    def desbloquear_detalhes(self, id_jogador, id_projeto, detalhes):
        """
        Salva os detalhes que o jogador descobriu sobre um projeto.
        """
        pass

    @abstractmethod
    def finalizar_projeto(self, jogador, projeto):
        """
        Aplica a lógica de negócio para finalizar um projeto com sucesso.
        """
        pass

    @abstractmethod
    def desistir_projeto(self, jogador, projeto):
        """
        Aplica a lógica de negócio para desistir de um projeto.
        """
        pass

    @abstractmethod
    def solicitar_detalhes_tecnico(self, jogador, projeto, opcao_dialogo):
        """
        Tenta obter detalhes técnicos baseado na opção de diálogo escolhida.
        Retorna uma tupla: (sucesso: bool, detalhe: str ou None, mensagem: str)
        """
        pass

    @abstractmethod
    def get_detalhes_descobertos(self, id_jogador, id_projeto):
        """
        Retorna todos os detalhes técnicos descobertos para um projeto.
        """
        pass

    @abstractmethod
    def atualizar_detalhes(self,id_jogador,id_projeto,novos_detalhes):
        pass

