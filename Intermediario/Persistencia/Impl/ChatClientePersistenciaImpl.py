import sqlite3
from Intermediario.Persistencia.ChatClientePersistencia import ChatClientePersistencia
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class ChatClientePersistenciaImpl(ChatClientePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, chat_cliente):
        sql = "INSERT INTO chat_cliente (id_jogador, id_cliente, mensagem, enviado_por) VALUES (?, ?, ?, ?)"
        parametros = (
            chat_cliente.get_id_jogador(),
            chat_cliente.get_id_cliente(),
            chat_cliente.get_mensagem(),
            chat_cliente.get_enviado_por()
        )
        try:
            self.__bd.executar(sql, parametros)
            return chat_cliente
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao salvar mensagem de chat: {e}")
       

    def listar_por_cliente_e_jogador(self, id_cliente, id_jogador):
        sql = "SELECT * FROM chat_cliente WHERE id_cliente = ? AND id_jogador = ? ORDER BY data_envio ASC"
        try:
            resultados = self.__bd.executar_query(sql)
            return [ChatCliente(*row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar histórico de chat: {e}")
            return []

