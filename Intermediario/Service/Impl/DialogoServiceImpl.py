import copy
from datetime import datetime
# Certifique-se de que os caminhos de importação estão corretos
from Intermediario.Service.DialogoService import DialogoService
from Intermediario.Persistencia.Impl.DialogoPersistenciaImpl import DialogoNoPersistenciaImpl, DialogoOpcaoPersistenciaImpl
from Intermediario.Persistencia.Impl.ChatClientePersistenciaImpl import ChatClientePersistenciaImpl
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Iniciante.Persistencia.Entidade.Jogador import Jogador

class DialogoServiceImpl(DialogoService):
    def __init__(self):
        self.no_persistencia = DialogoNoPersistenciaImpl()
        self.opcao_persistencia = DialogoOpcaoPersistenciaImpl()
        self.chat_persistencia = ChatClientePersistenciaImpl()

    def iniciar_conversa(self, id_projeto):
        return self.no_persistencia.buscar_no_inicial(id_projeto)

    def buscar_opcoes_disponiveis(self, id_no_atual, jogador):
        todas_opcoes = self.opcao_persistencia.buscar_opcoes_por_no_origem(id_no_atual)
        opcoes_disponiveis = [
            opcao for opcao in todas_opcoes 
            if jogador.get_social() >= opcao.get_req_social()
        ]
        return opcoes_disponiveis

    def buscar_proximo_no(self, id_no_destino):
        if id_no_destino is None:
            return None
        return self.no_persistencia.buscar_por_id(id_no_destino)

    def processar_escolha_dialogo(self, projeto, opcao_escolhida, jogador):
        """
        Processa a escolha do jogador, aplica efeitos, salva o histórico
        e retorna o novo estado da conversa para o GameManager.
        """
        # 1. Salva a escolha do jogador no histórico do chat
        msg_jogador = ChatCliente(
            id_chat=None, id_jogador=jogador.get_id_jogador(), id_cliente=projeto.get_id_cliente(),
            mensagem=opcao_escolhida.get_texto_opcao(), enviado_por='jogador', data_envio=datetime.now()
        )
        self.chat_persistencia.salvar(msg_jogador)

        # 2. Prepara variáveis para o novo estado
        detalhes_extras = None
        projeto_modificado = copy.deepcopy(projeto)
        efeito_final = opcao_escolhida.get_efeito()

        # 3. Aplica a lógica de negócio baseada no efeito da escolha
        if efeito_final == 'ACEITAR_PROJETO_COM_BONUS':
            recompensa_atual = projeto_modificado.get_recompensa()
            projeto_modificado.set_recompensa(recompensa_atual + 20.00)
        
        if "requisitos" in opcao_escolhida.get_texto_opcao().lower():
            detalhes_extras = f"DETALHES TÉCNICOS: O cliente espera uma solução com baixo acoplamento e alta coesão. A performance é um fator crítico."

        # 4. Busca o próximo ponto da conversa
        proximo_no = self.buscar_proximo_no(opcao_escolhida.get_id_no_destino())

        # 5. Se houver uma próxima fala do cliente, salva-a também no histórico
        if proximo_no:
            msg_cliente = ChatCliente(
                id_chat=None, id_jogador=jogador.get_id_jogador(), id_cliente=projeto.get_id_cliente(),
                mensagem=proximo_no.get_texto_npc(), enviado_por='cliente', data_envio=datetime.now()
            )
            self.chat_persistencia.salvar(msg_cliente)

        # 6. Retorna um dicionário com todo o estado atualizado para o GameManager
        return {
            "projeto_atualizado": projeto_modificado,
            "proximo_no": proximo_no,
            "detalhes_adicionais": detalhes_extras,
            "efeito_final": efeito_final
        }
