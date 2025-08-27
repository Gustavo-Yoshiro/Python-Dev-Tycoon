from Intermediario.Persistencia.JogadorProjetoPersistencia import JogadorProjetoPersistencia
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Iniciante.Persistencia.Impl.Banco import BancoDeDados
import sqlite3

class JogadorProjetoPersistenciaImpl(JogadorProjetoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def criar(self, id_jogador, id_projeto):
        return JogadorProjeto(id_jogador, id_projeto, "Em andamento")

    def salvar(self, jogador_projeto: JogadorProjeto):
        sql = "INSERT INTO jogador_projeto (id_jogador, id_projeto, status) VALUES (?, ?, ?)"
        parametros = (
            jogador_projeto.get_id_jogador(),
            jogador_projeto.get_id_projeto(),
            jogador_projeto.get_status()
        )
        try:
            self.__bd.executar(sql, parametros)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao salvar jogador-projeto: {e}")
            raise e

    def listar_por_jogador(self, id_jogador: int) -> list:
        sql = "SELECT id_jogador, id_projeto, status FROM jogador_projeto WHERE id_jogador = ?"
        try:
            resultados = self.__bd.executar_query(sql, (id_jogador,))
            return [JogadorProjeto(*row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar projetos do jogador: {e}")
            return []

    def atualizar_status(self, id_jogador: int, id_projeto: int, novo_status: str):
        sql = "UPDATE jogador_projeto SET status = ? WHERE id_jogador = ? AND id_projeto = ?"
        parametros = (novo_status, id_jogador, id_projeto)
        try:
            self.__bd.executar(sql, parametros)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao atualizar status: {e}")

    def buscar(self, id_jogador: int, id_projeto: int):
        sql = "SELECT id_jogador, id_projeto, status FROM jogador_projeto WHERE id_jogador = ? AND id_projeto = ?"
        try:
            resultado = self.__bd.executar_query(sql, (id_jogador, id_projeto))
            return JogadorProjeto(*resultado[0]) if resultado else None
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar jogador-projeto específico: {e}")
            return None