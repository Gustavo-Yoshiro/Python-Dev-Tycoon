from Intermediario.Persistencia.JogadorProjetoPersistencia import JogadorProjetoPersistencia
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class JogadorProjetoPersistenciaImpl(JogadorProjetoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, jogador_projeto: JogadorProjeto) -> None:
        sql = """
            INSERT INTO jogador_projeto (id_jogador, id_projeto, status)
            VALUES (?, ?, ?)
        """
        parametros = (
            jogador_projeto.get_id_jogador(),
            jogador_projeto.get_id_projeto(),
            jogador_projeto.get_status()
        )
        self.__bd.executar(sql, parametros)

    def buscar(self, id_jogador: int, id_projeto: int) -> JogadorProjeto | None:
        sql = """
            SELECT id_jogador, id_projeto, status
            FROM jogador_projeto
            WHERE id_jogador = ? AND id_projeto = ?
        """
        resultado = self.__bd.executar_query(sql, (id_jogador, id_projeto), fetchone=True)
        if resultado:
            return JogadorProjeto(*resultado)
        return None

    def listar_por_jogador(self, id_jogador: int) -> list[JogadorProjeto]:
        sql = """
            SELECT id_jogador, id_projeto, status
            FROM jogador_projeto
            WHERE id_jogador = ?
        """
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [JogadorProjeto(*row) for row in resultados]

    def atualizar_status(self, id_jogador: int, id_projeto: int, novo_status: str) -> None:
        sql = """
            UPDATE jogador_projeto
            SET status = ?
            WHERE id_jogador = ? AND id_projeto = ?
        """
        parametros = (novo_status, id_jogador, id_projeto)
        self.__bd.executar(sql, parametros)

    def remover(self, id_jogador: int, id_projeto: int) -> None:
        """
        Remove a relação entre um jogador e um projeto.
        """
        sql = "DELETE FROM jogador_projeto WHERE id_jogador = ? AND id_projeto = ?"
        self.__bd.executar(sql, (id_jogador, id_projeto))