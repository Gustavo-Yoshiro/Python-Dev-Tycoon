from Intermediario.Service.ChatClienteService import ChatClienteService
from Persistencia.Impl.ChatClientePersistenciaImpl import ChatClientePersistenciaImpl

class ChatClienteServiceImpl(ChatClienteService):
    def __init__(self):
        self.persistencia = ChatClientePersistenciaImpl()

    def enviar_mensagem(self, chat):
        return self.persistencia.inserir(chat)

    def atualizar_mensagem(self, chat):
        return self.persistencia.atualizar(chat)

    def deletar_mensagem(self, id_chat):
        return self.persistencia.deletar(id_chat)

    def buscar_mensagem_por_id(self, id_chat):
        return self.persistencia.buscar_por_id(id_chat)

    def listar_mensagens(self):
        return self.persistencia.listar_todos()

    def listar_conversa(self, id_jogador, id_cliente):
        mensagens = self.persistencia.listar_todos()
        return [m for m in mensagens if m.get_id_jogador() == id_jogador and m.get_id_cliente() == id_cliente]