from Intermediario.Persistencia.ProjetoFreelancePersistencia import ProjetoFreelancePersistencia
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class ProjetoFreelancePersistenciaImpl(ProjetoFreelancePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def _mapear_resultado_para_objeto(self, row):
        if not row:
            return None
        return ProjetoFreelance(
            id_projeto=row[0], id_cliente=row[1], titulo=row[2], descricao=row[3],
            dificuldade=row[4], recompensa=row[5], status=row[6],
            req_backend=row[7], req_frontend=row[8], req_social=row[9], tags=row[10],
            data_postagem=row[11], prazo_dias=row[12], tipo_desafio=row[13],
            codigo_base=row[14], testes=row[15]
        )

    def salvar(self, projeto: ProjetoFreelance) -> ProjetoFreelance:
        sql = """
            INSERT INTO projeto_freelance (
                id_cliente, titulo, descricao, dificuldade, recompensa, status,
                req_backend, req_frontend, req_social, tags, prazo_dias,
                tipo_desafio, codigo_base, testes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parametros = (
            projeto.get_id_cliente(), projeto.get_titulo(), projeto.get_descricao(),
            projeto.get_dificuldade(), projeto.get_recompensa(), projeto.get_status(),
            projeto.get_req_backend(), projeto.get_req_frontend(), projeto.get_req_social(),
            projeto.get_tags(), projeto.get_prazo_dias(), projeto.get_tipo_desafio(),
            projeto.get_codigo_base(), projeto.get_testes()
        )
        id_gerado = self.__bd.executar_e_retornar_id(sql, parametros)
        projeto.set_id_projeto(id_gerado)
        return projeto

    def atualizar(self, projeto: ProjetoFreelance):
        sql = """
            UPDATE projeto_freelance SET
            id_cliente=?, titulo=?, descricao=?, dificuldade=?, recompensa=?, status=?,
            req_backend=?, req_frontend=?, req_social=?, tags=?, prazo_dias=?,
            tipo_desafio=?, codigo_base=?, testes=?
            WHERE id_projeto=?
        """
        parametros = (
            projeto.get_id_cliente(), projeto.get_titulo(), projeto.get_descricao(),
            projeto.get_dificuldade(), projeto.get_recompensa(), projeto.get_status(),
            projeto.get_req_backend(), projeto.get_req_frontend(), projeto.get_req_social(),
            projeto.get_tags(), projeto.get_prazo_dias(), projeto.get_tipo_desafio(),
            projeto.get_codigo_base(), projeto.get_testes(), projeto.get_id_projeto()
        )
        self.__bd.executar(sql, parametros)

    def deletar(self, id_projeto: int):
        sql = "DELETE FROM projeto_freelance WHERE id_projeto = ?"
        self.__bd.executar(sql, (id_projeto,))

    def buscar_por_id(self, id_projeto: int) -> ProjetoFreelance:
        sql = "SELECT * FROM projeto_freelance WHERE id_projeto = ?"
        resultado = self.__bd.executar_query(sql, (id_projeto,), fetchone=True)
        return self._mapear_resultado_para_objeto(resultado)

    def listar_disponiveis(self) -> list:
        sql = "SELECT * FROM projeto_freelance WHERE status = 'disponivel' ORDER BY dificuldade, recompensa"
        resultados = self.__bd.executar_query(sql)
        return [self._mapear_resultado_para_objeto(row) for row in resultados]

    def deletar_todos(self):
        sql = "DELETE FROM projeto_freelance"
        self.__bd.executar(sql)
        print("Todos os projetos foram deletados.")