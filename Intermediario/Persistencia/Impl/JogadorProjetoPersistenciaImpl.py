from Intermediario.Persistencia.JogadorProjetoPersistencia import JogadorProjetoPersistencia
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Iniciante.Persistencia.Impl.Banco import BancoDeDados  # substitui Conexao

class JogadorProjetoPersistenciaImpl(JogadorProjetoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, jogador_projeto: JogadorProjeto):
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

    def buscar(self, id_jogador: int, id_projeto: int):
        sql = """
            SELECT id_jogador, id_projeto, status
            FROM jogador_projeto
            WHERE id_jogador = ? AND id_projeto = ?
        """
        resultado = self.__bd.executar_query(sql, (id_jogador, id_projeto), fetchone=True)
        if resultado:
            return JogadorProjeto(*resultado)
        return None

    def listarPorJogador(self, id_jogador: int):
        sql = """
            SELECT id_jogador, id_projeto, status
            FROM jogador_projeto
            WHERE id_jogador = ?
        """
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [JogadorProjeto(*row) for row in resultados]

    def atualizarStatus(self, id_jogador: int, id_projeto: int, novo_status: str):
        sql = """
            UPDATE jogador_projeto
            SET status = ?
            WHERE id_jogador = ? AND id_projeto = ?
        """
        parametros = (novo_status, id_jogador, id_projeto)
        self.__bd.executar(sql, parametros)