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

    def buscar_tipo_fase_atual(self, id_jogador):
        try:
            # Validação básica
            if not isinstance(id_jogador, int) or id_jogador <= 0:
                raise ValueError("O ID do jogador deve ser um número inteiro positivo.")

            sql = """
                SELECT f.tipo_fase
                FROM jogador AS j
                JOIN fase AS f ON j.id_fase = f.id_fase
                WHERE j.id_jogador = ?
            """

            resultado = self.__bd.executar_query(sql, (id_jogador,), fetchone=True)

            if resultado:
                tipo_fase = resultado[0]
                return tipo_fase
            else:
                print("⚠️ Fase não encontrada para o jogador.")
                return None

        except ValueError as ve:
            print("❌ Erro de validação:", ve)
            return None

        except Exception as e:
            print("❌ Erro inesperado ao buscar tipo da fase:", str(e))
            return None
    
    def avancar_fase_jogador(self, id_jogador: int):
        try:
            # Consulta a fase atual do jogador
            sql_fase_atual = "SELECT id_fase FROM jogador WHERE id_jogador = ?"
            fase_atual = self.__bd.executar_query(sql_fase_atual, (id_jogador,), fetchone=True)

            # Consulta a última fase disponível
            sql_ultima_fase = "SELECT MAX(id_fase) FROM fase"
            ultima_fase = self.__bd.executar_query(sql_ultima_fase, fetchone=True)

            if fase_atual and ultima_fase:
                id_fase_atual = fase_atual[0]
                id_ultima_fase = ultima_fase[0]

                if id_fase_atual is not None and id_fase_atual < id_ultima_fase:
                    # Atualiza o jogador para a próxima fase
                    sql_update = "UPDATE jogador SET id_fase = id_fase + 1 WHERE id_jogador = ?"
                    self.__bd.executar(sql_update, (id_jogador,))
                    print(f"Jogador {id_jogador} avançou para a fase {id_fase_atual + 1}.")
                else:
                    print("Jogador já está na última fase.")
            else:
                print("Não foi possível obter os dados de fase.")
        except Exception as e:
            print("Erro ao tentar avançar fase:", e)