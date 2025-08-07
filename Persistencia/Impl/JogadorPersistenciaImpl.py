from Persistencia.JogadorPersistencia import JogadorPersistencia
from Persistencia.Entidade.Jogador import Jogador
from Persistencia.Impl.Banco import BancoDeDados

class JogadorPersistenciaImpl(JogadorPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, jogador: Jogador):
        sql = """
            INSERT INTO jogador (nome, id_fase, social, dinheiro, backend, frontend)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parametros = (
            jogador.get_nome(),
            jogador.get_id_fase(),
            jogador.get_social(),
            jogador.get_dinheiro(),
            jogador.get_backend(),
            jogador.get_frontend()
        )
        return self.__bd.executar(sql, parametros)

    def buscar_por_id(self, id_jogador: int) -> Jogador:
        sql = "SELECT * FROM jogador WHERE id_jogador = ?"
        resultado = self.__bd.executar_query(sql, (id_jogador,), fetchone=True)
        if resultado:
            return Jogador(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM jogador"
        resultados = self.__bd.executar_query(sql)
        return [Jogador(*row) for row in resultados]

    def deletar(self, id_jogador: int):
        sql = "DELETE FROM jogador WHERE id_jogador = ?"
        self.__bd.executar(sql, (id_jogador,))

    def atualizar(self, jogador: Jogador):
        sql = """
            UPDATE jogador
            SET nome = ?, id_fase = ?, social = ?, dinheiro = ?, backend = ?, frontend = ?
            WHERE id_jogador = ?
        """
        parametros = (
            jogador.get_nome(),
            jogador.get_id_fase(),
            jogador.get_social(),
            jogador.get_dinheiro(),
            jogador.get_backend(),
            jogador.get_frontend(),
            jogador.get_id_jogador()
        )
        self.__bd.executar(sql, parametros)

    def buscar_progresso(self, id_jogador):
        try:
            # Verifica se o ID é válido
            if not isinstance(id_jogador, int) or id_jogador <= 0:
                raise ValueError("O ID do jogador deve ser um número inteiro positivo.")

            sql = """
                SELECT p.*
                FROM jogador AS j
                JOIN progresso_fase AS p ON j.id_jogador = p.id_jogador
                WHERE j.id_jogador = ?
            """

            progresso = self.__bd.executar_query(sql, (id_jogador,), fetchone=True)

            if progresso:
                print("✅ Progresso encontrado:", progresso)
                return progresso
            else:
                print("⚠️ Nenhum progresso encontrado para o jogador com ID:", id_jogador)
                return None

        except ValueError as ve:
            print("❌ Erro de validação:", ve)
            return None

        except Exception as e:
            print("❌ Erro inesperado ao buscar progresso:", str(e))
            return None