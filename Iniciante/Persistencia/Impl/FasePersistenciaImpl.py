from Iniciante.Persistencia.FasePersistencia import FasePersistencia
from Iniciante.Persistencia.Entidade.Fase import Fase
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class FasePersistenciaImpl(FasePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, fase: Fase):
        sql = """
            INSERT INTO fase (tipo_fase, topico, introdução)
            VALUES (?, ?, ?)
        """
        parametros = (
            fase.get_tipo_fase(),
            fase.get_topico(),
            fase.get_introducao()
        )
        return self.__bd.executar(sql, parametros)

    def buscar_por_id(self, id_fase: int) -> Fase:
        sql = "SELECT * FROM fase WHERE id_fase = ?"
        resultado = self.__bd.executar_query(sql, (id_fase,), fetchone=True)
        if resultado:
            return Fase(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM fase"
        resultados = self.__bd.executar_query(sql)
        return [Fase(*row) for row in resultados]

    def deletar(self, id_fase: int):
        sql = "DELETE FROM fase WHERE id_fase = ?"
        self.__bd.executar(sql, (id_fase,))

    def atualizar(self, fase: Fase):
        sql = """
            UPDATE fase
            SET tipo_fase = ?, topico = ?, introdução = ?
            WHERE id_fase = ?
        """
        parametros = (
            fase.get_tipo_fase(),
            fase.get_topico(),
            fase.get_introducao(),
            fase.get_id_fase()
        )
        self.__bd.executar(sql, parametros)
