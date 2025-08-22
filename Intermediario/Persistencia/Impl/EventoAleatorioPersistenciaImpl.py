from Intermediario.Persistencia.EventoAleatorioPersistencia import EventoAleatorioPersistencia
from Intermediario.Persistencia.Entidade.EventoAleatorio import EventoAleatorio
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class EventoAleatorioPersistenciaImpl(EventoAleatorioPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, evento: EventoAleatorio):
        sql = """
            INSERT INTO evento (
                titulo, descricao, dificuldade, recompensa_dinheiro,
                resposta_certa, resposta_errada, entrada_teste,
                tempo_aparecer_min, tempo_aparecer_max, tempo_para_fazer, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parametros = (
            evento.get_titulo(),
            evento.get_descricao(),
            evento.get_dificuldade(),
            evento.get_recompensa_dinheiro(),
            evento.get_resposta_certa(),
            evento.get_resposta_errada(),
            evento.get_entrada_teste(),
            evento.get_tempo_aparecer_min(),
            evento.get_tempo_aparecer_max(),
            evento.get_tempo_para_fazer(),
            evento.get_status()
        )
        return self.__bd.executar(sql, parametros)

    def buscar_por_id(self, id_evento: int) -> EventoAleatorio:
        sql = "SELECT * FROM evento WHERE id_evento = ?"
        resultado = self.__bd.executar_query(sql, (id_evento,), fetchone=True)
        if resultado:
            return EventoAleatorio(*resultado)
        return None

    def listar_todos(self) -> list:
        sql = "SELECT * FROM evento"
        resultados = self.__bd.executar_query(sql)
        return [EventoAleatorio(*row) for row in resultados]

    def deletar(self, id_evento: int):
        sql = "DELETE FROM evento WHERE id_evento = ?"
        self.__bd.executar(sql, (id_evento,))

    def atualizar(self, evento: EventoAleatorio):
        sql = """
            UPDATE evento
            SET titulo = ?, descricao = ?, dificuldade = ?, recompensa_dinheiro = ?,
                resposta_certa = ?, resposta_errada = ?, entrada_teste = ?,
                tempo_aparecer_min = ?, tempo_aparecer_max = ?, tempo_para_fazer = ?, status = ?
            WHERE id_evento = ?
        """
        parametros = (
            evento.get_titulo(),
            evento.get_descricao(),
            evento.get_dificuldade(),
            evento.get_recompensa_dinheiro(),
            evento.get_resposta_certa(),
            evento.get_resposta_errada(),
            evento.get_entrada_teste(),
            evento.get_tempo_aparecer_min(),
            evento.get_tempo_aparecer_max(),
            evento.get_tempo_para_fazer(),
            evento.get_status(),
            evento.get_id_evento()
        )
        self.__bd.executar(sql, parametros)

    def listar_ativos(self) -> list:
        sql = "SELECT * FROM evento WHERE status = 'ativo'"
        resultados = self.__bd.executar_query(sql)
        return [EventoAleatorio(*row) for row in resultados]

    def marcar_como_usado(self, id_evento: int):
        sql = "UPDATE evento SET status = 'usado' WHERE id_evento = ?"
        self.__bd.executar(sql, (id_evento,))
