from Intermediario.Persistencia.ClientePersistencia import ClientePersistencia
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class ClientePersistenciaImpl(ClientePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, cliente: Cliente):
        sql = """
            INSERT INTO cliente (nome, area_atuacao, descricao, reputacao, personalidade)
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            cliente.get_nome(),
            cliente.get_area_atuacao(),
            cliente.get_descricao(),
            cliente.get_reputacao(),
            cliente.get_personalidade()
        )
        id_gerado = self.__bd.executar_e_retornar_id(sql, parametros)
        cliente.set_id_cliente(id_gerado)
        return cliente

    def atualizar(self, cliente: Cliente):
        sql = """
            UPDATE cliente
            SET nome = ?, area_atuacao = ?, descricao = ?, reputacao = ?, personalidade = ?
            WHERE id_cliente = ?
        """
        parametros = (
            cliente.get_nome(),
            cliente.get_area_atuacao(),
            cliente.get_descricao(),
            cliente.get_reputacao(),
            cliente.get_personalidade(),
            cliente.get_id_cliente()
        )
        self.__bd.executar(sql, parametros)

    def deletar(self, id_cliente: int):
        sql = "DELETE FROM cliente WHERE id_cliente = ?"
        self.__bd.executar(sql, (id_cliente,))

    def buscar_por_id(self, id_cliente: int) -> Cliente:
        sql = "SELECT * FROM cliente WHERE id_cliente = ?"
        resultado = self.__bd.executar_query(sql, (id_cliente,), fetchone=True)
        return Cliente(*resultado) if resultado else None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM cliente ORDER BY nome"
        resultados = self.__bd.executar_query(sql)
        return [Cliente(*row) for row in resultados]