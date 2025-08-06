from Persistencia.SavePersistencia import SavePersistencia
from Persistencia.Entidade.Save import Save
from Persistencia.Impl.Banco import BancoDeDados

class SavePersistenciaImpl(SavePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, id_jogador, data_save,tempo_jogo):
        sql = """
            INSERT INTO save (id_jogador, data_save, tempo_jogo)
            VALUES (?, ?, ?)
        """
        parametros = (
            id_jogador,
            data_save,
            tempo_jogo
        )
        return self.__bd.executar(sql, parametros)

    def buscar_por_id(self, id_save: int) -> Save:
        sql = "SELECT * FROM save WHERE id_save = ?"
        resultado = self.__bd.executar_query(sql, (id_save,), fetchone=True)
        if resultado:
            return Save(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM save"
        resultados = self.__bd.executar_query(sql)
        return [Save(*row) for row in resultados]

    def deletar(self, id_save: int):
        sql = "DELETE FROM save WHERE id_save = ?"
        self.__bd.executar(sql, (id_save,))

    def atualizar(self, save: Save):
        sql = """
            UPDATE save
            SET id_jogador = ?, data_save = ?, tempo_jogo = ?
            WHERE id_save = ?
        """
        parametros = (
            save.get_id_jogador(),
            save.get_data_save(),
            save.get_tempo_jogo(),
            save.get_id_save()
        )
        self.__bd.executar(sql, parametros)

    def pode_salvar(self,id_jogador):
        sql = "SELECT COUNT(*) FROM save WHERE id_jogador = ?"
        total = self.__bd.executar_query(sql, (id_jogador,), fetchone=True)[0]
        return total < 3