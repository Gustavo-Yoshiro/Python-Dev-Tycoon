import sqlite3
# Certifique-se de que os caminhos de importação estão corretos
from Intermediario.Persistencia.Entidade.Dialogo import DialogoNo, DialogoOpcao
from Intermediario.Persistencia.DialogoPersistencia import DialogoNoPersistencia, DialogoOpcaoPersistencia
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class DialogoNoPersistenciaImpl(DialogoNoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, no):
        sql = "INSERT INTO dialogo_nos (id_projeto, texto_npc, is_inicio) VALUES (?, ?, ?)"
        parametros = (no.get_id_projeto(), no.get_texto_npc(), no.get_is_inicio())
        id_gerado = self.__bd.executar_e_retornar_id(sql, parametros)
        no.set_id_no(id_gerado)
        return no

    def buscar_no_inicial(self, id_projeto):
        """Encontra o primeiro nó de diálogo para um projeto específico."""
        sql = "SELECT * FROM dialogo_nos WHERE id_projeto = ? AND is_inicio = 1"
        resultado = self.__bd.executar_query(sql, (id_projeto,), fetchone=True)
        return DialogoNo(*resultado) if resultado else None

    def buscar_por_id(self, id_no):
        """Busca um nó de diálogo específico pelo seu ID."""
        sql = "SELECT * FROM dialogo_nos WHERE id_no = ?"
        resultado = self.__bd.executar_query(sql, (id_no,), fetchone=True)
        return DialogoNo(*resultado) if resultado else None


class DialogoOpcaoPersistenciaImpl(DialogoOpcaoPersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, opcao):
        sql = """
            INSERT INTO dialogo_opcoes (id_no_origem, id_no_destino, texto_opcao, req_social, efeito)
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            opcao.get_id_no_origem(),
            opcao.get_id_no_destino(),
            opcao.get_texto_opcao(),
            opcao.get_req_social(),
            opcao.get_efeito()
        )
        id_gerado = self.__bd.executar_e_retornar_id(sql, parametros)
        opcao.set_id_opcao(id_gerado)
        return opcao

    def buscar_opcoes_por_no_origem(self, id_no_origem):
        """Encontra todas as opções de diálogo que partem de um nó específico."""
        sql = "SELECT * FROM dialogo_opcoes WHERE id_no_origem = ?"
        resultados = self.__bd.executar_query(sql, (id_no_origem,))
        return [DialogoOpcao(*row) for row in resultados]
