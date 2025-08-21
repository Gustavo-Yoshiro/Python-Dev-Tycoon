from Intermediario.Persistencia.ClientePersistencia import ClientePersistencia
from Intermediario.Persistencia.Entidade.Cliente import Cliente
from Iniciante.Persistencia.Impl.Banco import BancoDeDados  # substitui Conexao

class ClientePersistenciaImpl(ClientePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, cliente: Cliente):
        sql = """
            INSERT INTO cliente (nome, area_atuacao, reputacao, descricao)
            VALUES (?, ?, ?, ?) RETURNING id_cliente
        """
        parametros = (
            cliente.get_nome(),
            cliente.get_area_atuacao(),
            cliente.get_reputacao(),
            cliente.get_descricao()
        )
        resultado = self.__bd.executar_query(sql, parametros, fetchone=True)
        cliente.set_id_cliente(resultado[0])

    def buscarPorId(self, id_cliente: int):
        sql = """
            SELECT id_cliente, nome, area_atuacao, reputacao, descricao
            FROM cliente WHERE id_cliente = ?
        """
        resultado = self.__bd.executar_query(sql, (id_cliente,), fetchone=True)
        if resultado:
            return Cliente(*resultado)
        return None

    def listarTodos(self):
        sql = "SELECT id_cliente, nome, area_atuacao, reputacao, descricao FROM cliente"
        resultados = self.__bd.executar_query(sql)
        return [Cliente(*row) for row in resultados]

    def deletar(self, id_cliente: int):
        sql = "DELETE FROM cliente WHERE id_cliente = ?"
        self.__bd.executar(sql, (id_cliente,))