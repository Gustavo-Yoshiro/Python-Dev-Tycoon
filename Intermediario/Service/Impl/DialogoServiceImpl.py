# Certifique-se de que os caminhos de importação estão corretos
from Intermediario.Service.DialogoService import DialogoService
from Intermediario.Persistencia.Impl.DialogoPersistenciaImpl import DialogoNoPersistenciaImpl, DialogoOpcaoPersistenciaImpl
from Iniciante.Persistencia.Entidade.Jogador import Jogador

class DialogoServiceImpl(DialogoService):
    def __init__(self):
        self.no_persistencia = DialogoNoPersistenciaImpl()
        self.opcao_persistencia = DialogoOpcaoPersistenciaImpl()

    def iniciar_conversa(self, id_projeto):
        """
        Inicia uma conversa, buscando o primeiro nó de diálogo de um projeto.
        """
        return self.no_persistencia.buscar_no_inicial(id_projeto)

    def buscar_opcoes_disponiveis(self, id_no_atual, jogador):
        """
        Busca todas as opções de um nó e as filtra com base no nível de social do jogador.
        """
        todas_opcoes = self.opcao_persistencia.buscar_opcoes_por_no_origem(id_no_atual)
        opcoes_disponiveis = []
        
        for opcao in todas_opcoes:
            if jogador.get_social() >= opcao.get_req_social():
                opcoes_disponiveis.append(opcao)
                
        return opcoes_disponiveis

    def buscar_proximo_no(self, id_no_destino):
        """
        Busca o próximo nó da conversa com base no ID de destino de uma opção escolhida.
        """
        if id_no_destino is None:
            return None # A conversa terminou
            
        return self.no_persistencia.buscar_por_id(id_no_destino)

