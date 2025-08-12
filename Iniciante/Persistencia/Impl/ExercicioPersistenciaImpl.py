from Iniciante.Persistencia.ExercicioPersistencia import ExercicioPersistencia
from Iniciante.Persistencia.Entidade.Exercicio import Exercicio
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class ExercicioPersistenciaImpl(ExercicioPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, exercicio: Exercicio):
        sql = """
            INSERT INTO exercicio (id_fase, dicas, pergunta, tipo, resposta_certa, resposta_errada, entrada_teste)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        resposta_erradas = exercicio.get_resposta_erradas()
        if isinstance(resposta_erradas, list):
            resposta_erradas = "|".join(resposta_erradas)
        elif resposta_erradas is None:
            resposta_erradas = ""

        parametros = (
            exercicio.get_id_fase(),
            exercicio.get_dicas(),
            exercicio.get_pergunta(),
            exercicio.get_tipo(),
            exercicio.get_resposta_certa(),
            resposta_erradas,
            getattr(exercicio, 'entrada_teste', None) or getattr(exercicio, 'get_entrada_teste', lambda: None)()
        )
        return self.__bd.executar(sql, parametros)



    def buscar_por_id(self, id_exercicio: int) -> Exercicio:
        sql = "SELECT * FROM exercicio WHERE id_exercicio = ?"
        resultado = self.__bd.executar_query(sql, (id_exercicio,), fetchone=True)
        if resultado:
            return Exercicio(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM exercicio"
        resultados = self.__bd.executar_query(sql)
        return [Exercicio(*row) for row in resultados]

    def deletar(self, id_exercicio: int):
        sql = "DELETE FROM exercicio WHERE id_exercicio = ?"
        self.__bd.executar(sql, (id_exercicio,))

    def atualizar(self, exercicio: Exercicio):
        sql = """
            UPDATE exercicio
            SET id_fase = ?, dicas = ?, pergunta = ?, tipo = ?, resposta_certa = ?, resposta_errada = ?, entrada_teste = ?
            WHERE id_exercicio = ?
        """
        parametros = (
            exercicio.get_id_fase(),
            exercicio.get_dicas(),
            exercicio.get_pergunta(),
            exercicio.get_tipo(),
            exercicio.get_resposta_certa(),
            exercicio.get_resposta_erradas(),
            exercicio.get_entrada_teste(),
            exercicio.get_id_exercicio()
        )
        self.__bd.executar(sql, parametros)
