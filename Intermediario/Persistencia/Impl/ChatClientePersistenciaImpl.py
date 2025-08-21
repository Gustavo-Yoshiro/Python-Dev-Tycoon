from Intermediario.Persistencia.ChatClientePersistencia import ChatClientePersistencia
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados  # substitui Conexao

class ChatClientePersistenciaImpl(ChatClientePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, chat: ChatCliente):
        sql = """
            INSERT INTO chat_cliente (id_jogador, id_cliente, mensagem, enviado_por, data_envio)
            VALUES (?, ?, ?, ?, ?) RETURNING id_chat
        """
        parametros = (
            chat.get_id_jogador(),
            chat.get_id_cliente(),
            chat.get_mensagem(),
            chat.get_enviado_por(),
            chat.get_data_envio()
        )
        resultado = self.__bd.executar_query(sql, parametros, fetchone=True)
        chat.set_id_chat(resultado[0])

    def buscarPorId(self, id_chat: int):
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente WHERE id_chat = ?
        """
        resultado = self.__bd.executar_query(sql, (id_chat,), fetchone=True)
        if resultado:
            return ChatCliente(*resultado)
        return None

    def listarPorJogador(self, id_jogador: int):
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente
            WHERE id_jogador = ?
            ORDER BY data_envio
        """
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [ChatCliente(*row) for row in resultados]

    def listarPorCliente(self, id_cliente: int):
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente
            WHERE id_cliente = ?
            ORDER BY data_envio
        """
        resultados = self.__bd.executar_query(sql, (id_cliente,))
        return [ChatCliente(*row) for row in resultados]