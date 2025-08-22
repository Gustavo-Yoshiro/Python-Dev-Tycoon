from Intermediario.Persistencia.ProjetoFreelancePersistencia import ProjetoFreelancePersistencia
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Iniciante.Persistencia.Impl.Banco import BancoDeDados

class ProjetoFreelancePersistenciaImpl(ProjetoFreelancePersistencia):
    def __init__(self):
        self.__bd = BancoDeDados()

    def salvar(self, projeto: ProjetoFreelance):
        sql = """
            INSERT INTO projeto_freelance (
                id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
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
        projeto_id = self.__bd.executar(sql, parametros)  # já retorna o lastrowid no BancoDeDados
        projeto.set_id_projeto(projeto_id)
        return projeto

    def atualizar(self, projeto: ProjetoFreelance):
        sql = """
            UPDATE projeto_freelance
            SET id_cliente=?, titulo=?, descricao=?, dificuldade=?, recompensa=?, habilidade_requerida=?, status=?
            WHERE id_projeto=?
        """
        parametros = (
            projeto.get_id_cliente(),
            projeto.get_titulo(),
            projeto.get_descricao(),
            projeto.get_dificuldade(),
            projeto.get_recompensa(),
            projeto.get_habilidade_requerida(),
            projeto.get_status(),
            projeto.get_id_projeto()
        )
        self.__bd.executar(sql, parametros)

    def deletar(self, id_projeto: int):
        sql = "DELETE FROM projeto_freelance WHERE id_projeto = ?"
        self.__bd.executar(sql, (id_projeto,))

    def buscar_por_id(self, id_projeto: int):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance
            WHERE id_projeto = ?
        """
        resultado = self.__bd.executar_query(sql, (id_projeto,), fetchone=True)
        if resultado:
            return ProjetoFreelance(*resultado)
        return None

    def listar_disponiveis(self):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance
            WHERE status = 'disponivel'
        """
        resultados = self.__bd.executar_query(sql)
        return [ProjetoFreelance(*row) for row in resultados]

    def listar_por_cliente(self, id_cliente: int):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance
            WHERE id_cliente = ?
        """
        resultados = self.__bd.executar_query(sql, (id_cliente,))
        return [ProjetoFreelance(*row) for row in resultados]

    def listar_todos(self):
        sql = """
            SELECT id_projeto, id_cliente, titulo, descricao, dificuldade, recompensa, habilidade_requerida, status
            FROM projeto_freelance
        """
        resultados = self.__bd.executar_query(sql)
        return [ProjetoFreelance(*row) for row in resultados]