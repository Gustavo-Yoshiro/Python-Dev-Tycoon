from Persistencia.Entidade.ProgressoFase import ProgressoFase
from Persistencia.Impl.Banco import BancoDeDados

class ProgressoFasePersistenciaImpl:
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, progresso: ProgressoFase):
        sql = """
            INSERT INTO progresso_fase
            (id_jogador, id_fase, indice_exercicio, acertos, erros, resposta_parcial, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        parametros = (
            progresso.get_id_jogador(),
            progresso.get_id_fase(),
            progresso.get_indice_exercicio(),
            progresso.get_acertos(),
            progresso.get_erros(),
            progresso.get_resposta_parcial()
        )
        return self.__bd.executar(sql, parametros)

    def buscar_por_id(self, id_progresso: int) -> ProgressoFase:
        sql = "SELECT * FROM progresso_fase WHERE id_progresso = ?"
        resultado = self.__bd.executar_query(sql, (id_progresso,), fetchone=True)
        if resultado:
            return ProgressoFase(*resultado)
        return None

    def buscar_por_jogador_fase(self, id_jogador: int, id_fase: int) -> ProgressoFase:
        sql = "SELECT * FROM progresso_fase WHERE id_jogador = ? AND id_fase = ?"
        resultado = self.__bd.executar_query(sql, (id_jogador, id_fase), fetchone=True)
        if resultado:
            return ProgressoFase(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM progresso_fase"
        resultados = self.__bd.executar_query(sql)
        return [ProgressoFase(*row) for row in resultados]

    def deletar(self, id_progresso: int):
        sql = "DELETE FROM progresso_fase WHERE id_progresso = ?"
        self.__bd.executar(sql, (id_progresso,))

    def atualizar(self, progresso: ProgressoFase):
        sql = """
            UPDATE progresso_fase
            SET id_jogador = ?, id_fase = ?, indice_exercicio = ?, acertos = ?, erros = ?, resposta_parcial = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id_progresso = ?
        """
        parametros = (
            progresso.get_id_jogador(),
            progresso.get_id_fase(),
            progresso.get_indice_exercicio(),
            progresso.get_acertos(),
            progresso.get_erros(),
            progresso.get_resposta_parcial(),
            progresso.get_id_progresso()
        )
        self.__bd.executar(sql, parametros)

    def deletar_por_jogador_fase(self, id_jogador: int, id_fase: int):
        sql = "DELETE FROM progresso_fase WHERE id_jogador = ? AND id_fase = ?"
        self.__bd.executar(sql, (id_jogador, id_fase))

    def buscar_ultima_fase_do_jogador(self, id_jogador: int):
        sql = """
            SELECT id_fase FROM progresso_fase
            WHERE id_jogador = ?
            ORDER BY atualizado_em DESC
            LIMIT 1
        """
        resultado = self.__bd.executar_query(sql, (id_jogador,), fetchone=True)
        if resultado:
            return resultado[0]
        return None

