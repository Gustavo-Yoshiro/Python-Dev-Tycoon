import sqlite3
from Intermediario.Persistencia.JogadorProjetoPersistencia import JogadorProjetoPersistencia
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

class JogadorProjetoPersistenciaImpl(JogadorProjetoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDadosIntermediario()

    def _mapear_para_objeto(self, row):
        """Função auxiliar para criar um objeto a partir de uma linha do banco."""
        if not row:
            return None
        # A ordem das colunas no SELECT * deve corresponder a esta ordem
        return JogadorProjeto(
            id_jogador=row[0], 
            id_projeto=row[1], 
            status=row[2], 
            detalhes_descobertos=row[3]
        )

    def salvar(self, jogador_projeto):
        sql = "INSERT INTO jogador_projeto (id_jogador, id_projeto, status, detalhes_descobertos) VALUES (?, ?, ?, ?)"
        parametros = (
            jogador_projeto.get_id_jogador(),
            jogador_projeto.get_id_projeto(),
            jogador_projeto.get_status(),
            jogador_projeto.get_detalhes_descobertos()
        )
        con = None
        try:
            con = self.__bd.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao salvar relação jogador-projeto: {e}")
            raise e
        finally:
            if con:
                con.close()

    def buscar(self, id_jogador, id_projeto):
        """Busca uma relação específica entre jogador e projeto."""
        sql = "SELECT * FROM jogador_projeto WHERE id_jogador = ? AND id_projeto = ?"
        con = None
        try:
            con = self.__bd.conectar()
            cursor = con.cursor()
            resultado = cursor.execute(sql, (id_jogador, id_projeto)).fetchone()
            return self._mapear_para_objeto(resultado)
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar relação específica: {e}")
            return None
        finally:
            if con:
                con.close()

    def listar_por_jogador(self, id_jogador):
        sql = "SELECT * FROM jogador_projeto WHERE id_jogador = ?"
        con = None
        try:
            con = self.__bd.conectar()
            cursor = con.cursor()
            resultados = cursor.execute(sql, (id_jogador,)).fetchall()
            return [self._mapear_para_objeto(row) for row in resultados]
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar projetos do jogador: {e}")
            return []
        finally:
            if con:
                con.close()

    def atualizar_status(self, id_jogador, id_projeto, novo_status):
        sql = "UPDATE jogador_projeto SET status = ? WHERE id_jogador = ? AND id_projeto = ?"
        parametros = (novo_status, id_jogador, id_projeto)
        con = None
        try:
            con = self.__bd.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao atualizar status do projeto: {e}")
        finally:
            if con:
                con.close()

    def atualizar_detalhes(self, id_jogador, id_projeto, novos_detalhes):
        """Atualiza apenas os detalhes descobertos de uma relação."""
        sql = "UPDATE jogador_projeto SET detalhes_descobertos = ? WHERE id_jogador = ? AND id_projeto = ?"
        parametros = (novos_detalhes, id_jogador, id_projeto)
        con = None
        try:
            con = self.__bd.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao atualizar detalhes do projeto: {e}")
        finally:
            if con:
                con.close()
