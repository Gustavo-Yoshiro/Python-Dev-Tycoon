from Intermediario.Persistencia.ChatClientePersistencia import ChatClientePersistencia
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados
import sqlite3
from typing import Optional

class ChatClientePersistenciaImpl(ChatClientePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, chat: ChatCliente):
        sql = """
            INSERT INTO chat_cliente (id_jogador, id_cliente, mensagem, enviado_por, data_envio)
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            chat.get_id_jogador(),
            chat.get_id_cliente(),
            chat.get_mensagem(),
            chat.get_enviado_por(),
            chat.get_data_envio()
        )

        try:
            # Executa e retorna cursor para capturar o lastrowid
            cursor = self.__bd.executar(sql, parametros, return_cursor=True)
            chat.set_id_chat(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao salvar chat_cliente: {e}")

    def buscar_por_id(self, id_chat: int) -> Optional[ChatCliente]:
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente
            WHERE id_chat = ?
        """
        try:
            resultado = self.__bd.executar_query(sql, (id_chat,), fetchone=True)
            return ChatCliente(*resultado) if resultado else None
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar chat_cliente: {e}")
            return None

    def listar_por_jogador(self, id_jogador: int) -> list[ChatCliente]:
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente
            WHERE id_jogador = ?
            ORDER BY data_envio
        """
        try:
            resultados = self.__bd.executar_query(sql, (id_jogador,))
            return [ChatCliente(*row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar chats por jogador: {e}")
            return []

    def listar_por_cliente(self, id_cliente: int) -> list[ChatCliente]:
        sql = """
            SELECT id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio
            FROM chat_cliente
            WHERE id_cliente = ?
            ORDER BY data_envio
        """
        try:
            resultados = self.__bd.executar_query(sql, (id_cliente,))
            return [ChatCliente(*row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar chats por cliente: {e}")
            return []