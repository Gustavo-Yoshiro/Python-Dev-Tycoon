from Intermediario.Service.ChatClienteService import ChatClienteService
from Intermediario.Persistencia.Impl.ChatClientePersistenciaImpl import ChatClientePersistenciaImpl

class ChatClienteServiceImpl(ChatClienteService):
    def __init__(self):
        self.persistencia = ChatClientePersistenciaImpl()

    def enviar_mensagem(self, chat_cliente):
        """Salva uma nova mensagem no histórico da conversa."""
        # Validações podem ser adicionadas aqui (ex: impedir spam)
        return self.persistencia.salvar(chat_cliente)

    def buscar_historico(self, id_cliente, id_jogador):
        """Busca o histórico completo de mensagens entre um jogador e um cliente."""
        return self.persistencia.listar_por_cliente_e_jogador(id_cliente, id_jogador)
