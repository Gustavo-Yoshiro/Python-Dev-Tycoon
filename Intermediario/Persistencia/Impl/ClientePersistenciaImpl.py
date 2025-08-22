from Intermediario.Persistencia.ClientePersistencia import ClientePersistencia
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados
from typing import Optional
import sqlite3


class ClientePersistenciaImpl(ClientePersistencia):
    def __init__(self) -> None:
        self.__bd = BancoDeDados()

    def salvar(self, cliente: Cliente) -> Cliente:
        sql = """
            INSERT INTO cliente (nome, area_atuacao, reputacao, descricao)
            VALUES (?, ?, ?, ?)
        """
        parametros = (
            cliente.get_nome(),
            cliente.get_area_atuacao(),
            cliente.get_reputacao(),
            cliente.get_descricao()
        )

        try:
            self.__bd.executar(sql, parametros)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao salvar cliente: {e}")
        return cliente

    def atualizar(self, cliente: Cliente) -> None:
        sql = """
            UPDATE cliente
            SET nome = ?, area_atuacao = ?, reputacao = ?, descricao = ?
            WHERE id_cliente = ?
        """
        parametros = (
            cliente.get_nome(),
            cliente.get_area_atuacao(),
            cliente.get_reputacao(),
            cliente.get_descricao(),
            cliente.get_id_cliente()
        )
        try:
            self.__bd.executar(sql, parametros)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao atualizar cliente: {e}")

    def deletar(self, id_cliente: int) -> None:
        sql = "DELETE FROM cliente WHERE id_cliente = ?"
        try:
            self.__bd.executar(sql, (id_cliente,))
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao deletar cliente: {e}")

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        sql = """
            SELECT id_cliente, nome, area_atuacao, reputacao, descricao
            FROM cliente
            WHERE id_cliente = ?
        """
        try:
            resultado = self.__bd.executar_query(sql, (id_cliente,), fetchone=True)
            return Cliente(*resultado) if resultado else None
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar cliente: {e}")
            return None

    def listar_todos(self) -> list[Cliente]:
        sql = """
            SELECT id_cliente, nome, area_atuacao, reputacao, descricao
            FROM cliente
        """
        try:
            resultados = self.__bd.executar_query(sql)
            return [Cliente(*row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar clientes: {e}")
            return []