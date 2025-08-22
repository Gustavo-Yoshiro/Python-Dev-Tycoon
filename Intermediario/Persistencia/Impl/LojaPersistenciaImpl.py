from Intermediario.Persistencia.LojaPersistencia import LojaPersistencia
from Intermediario.Persistencia.Entidade.Loja import Loja
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class LojaPersistenciaImpl(LojaPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, loja: Loja):
        sql = """
            INSERT INTO loja (id_jogador, nome, categoria, preco, duracao_segundos, status, duracao_total)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        parametros = (
            loja.get_id_jogador(),
            loja.get_nome(),
            loja.get_categoria(),
            loja.get_preco(),
            loja.get_duracao_segundos(),
            loja.get_status(),
            loja.get_duracao_total()   # 👈 novo campo
        )
        return self.__bd.executar(sql, parametros)


    def buscar_por_id(self, id_item: int) -> Loja:
        sql = "SELECT * FROM loja WHERE id_item = ?"
        resultado = self.__bd.executar_query(sql, (id_item,), fetchone=True)
        if resultado:
            return Loja(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM loja"
        resultados = self.__bd.executar_query(sql)
        return [Loja(*row) for row in resultados]

    def listar_por_jogador(self, id_jogador: int) -> list:
        sql = "SELECT * FROM loja WHERE id_jogador = ?"
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [Loja(*row) for row in resultados]

    def deletar(self, id_item: int):
        sql = "DELETE FROM loja WHERE id_item = ?"
        self.__bd.executar(sql, (id_item,))

    def atualizar(self, loja: Loja):
        sql = """
            UPDATE loja
            SET id_jogador = ?, nome = ?, categoria = ?, preco = ?, duracao_segundos = ?, 
                status = ?, duracao_total = ?
            WHERE id_item = ?
        """
        parametros = (
            loja.get_id_jogador(),
            loja.get_nome(),
            loja.get_categoria(),
            loja.get_preco(),
            loja.get_duracao_segundos(),
            loja.get_status(),
            loja.get_duracao_total(),  # 👈 novo campo
            loja.get_id_item()
        )
        self.__bd.executar(sql, parametros)


    def listar_em_andamento(self, id_jogador: int) -> list:
        sql = "SELECT * FROM loja WHERE id_jogador = ? AND status = 'andamento'"
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [Loja(*row) for row in resultados]

    def concluir_item(self, id_item: int):
        sql = "UPDATE loja SET status = 'concluido' WHERE id_item = ?"
        self.__bd.executar(sql, (id_item,))
