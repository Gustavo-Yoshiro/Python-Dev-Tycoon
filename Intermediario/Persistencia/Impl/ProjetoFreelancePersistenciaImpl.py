from Intermediario.Persistencia.ProjetoFreelancePersistencia import ProjetoFreelancePersistencia
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Impl.Banco import BancoDeDados  # substitui Conexao

class ProjetoFreelancePersistenciaImpl(ProjetoFreelancePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, projeto: ProjetoFreelance):
        sql = """
            INSERT INTO projeto_freelance (
                id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id_projeto
        """
        parametros = (
            projeto.get_id_cliente(),
            projeto.get_titulo(),
            projeto.get_descricao(),
            projeto.get_dificuldade(),
            projeto.get_recompensa(),
            projeto.get_habilidade_requerida(),
            projeto.get_status()
        )
        resultado = self.__bd.executar_query(sql, parametros, fetchone=True)
        projeto.set_id_projeto(resultado[0])

    def buscarPorId(self, id_projeto: int):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance WHERE id_projeto = ?
        """
        resultado = self.__bd.executar_query(sql, (id_projeto,), fetchone=True)
        if resultado:
            return ProjetoFreelance(*resultado)
        return None

    def listarTodos(self):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance
        """
        resultados = self.__bd.executar_query(sql)
        return [ProjetoFreelance(*row) for row in resultados]

    def deletar(self, id_projeto: int):
        sql = "DELETE FROM projeto_freelance WHERE id_projeto = ?"
        self.__bd.executar(sql, (id_projeto,))