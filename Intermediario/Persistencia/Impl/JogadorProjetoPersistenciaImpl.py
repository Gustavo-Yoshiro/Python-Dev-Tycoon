from Intermediario.Persistencia.JogadorProjetoPersistencia import JogadorProjetoPersistencia
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Iniciante.Persistencia.Impl.Banco import BancoDeDados
from typing import Optional, List

class JogadorProjetoPersistenciaImpl(JogadorProjetoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def _mapear_resultado_para_objeto(self, row: tuple) -> Optional[JogadorProjeto]:
        """Transforma uma linha do banco em um objeto JogadorProjeto."""
        if not row:
            return None
        return JogadorProjeto(id_jogador=row[0], id_projeto=row[1], status=row[2])

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
        return self._mapear_resultado_para_objeto(resultado)

    def listar_por_jogador(self, id_jogador: int) -> List[JogadorProjeto]:
        sql = """
            SELECT id_jogador, id_projeto, status
            FROM jogador_projeto
            WHERE id_jogador = ?
        """
        resultados = self.__bd.executar_query(sql, (id_jogador,))
        return [self._mapear_resultado_para_objeto(row) for row in resultados]

    def listar_todos(self) -> List[JogadorProjeto]:
        """Lista todas as relações jogador-projeto existentes no banco."""
        sql = "SELECT id_jogador, id_projeto, status FROM jogador_projeto"
        resultados = self.__bd.executar_query(sql)
        return [self._mapear_resultado_para_objeto(row) for row in resultados]

    def atualizar_status(self, id_jogador: int, id_projeto: int, novo_status: str) -> None:
        sql = """
            UPDATE jogador_projeto
            SET status = ?
            WHERE id_jogador = ? AND id_projeto = ?
        """
        parametros = (novo_status, id_jogador, id_projeto)
        self.__bd.executar(sql, parametros)

    def remover(self, id_jogador: int, id_projeto: int) -> None:
        sql = "DELETE FROM jogador_projeto WHERE id_jogador = ? AND id_projeto = ?"
        self.__bd.executar(sql, (id_jogador, id_projeto))