from Service.ExercicioService import ExercicioService
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl
from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
class ExercicioServiceImpl(ExercicioService):
    def __init__(self):
        self.__persistencia = ExercicioPersistenciaImpl()

    def listar_exercicios_por_fase(self, id_fase: int) -> list:
        todos = self.__persistencia.listar_todos()
        return [e for e in todos if e.get_id_fase() == id_fase]

    def verificar_resposta(self, id_exercicio: int, resposta_usuario: str) -> bool:
        exercicio = self.__persistencia.buscar_por_id(id_exercicio)
        if not exercicio:
            print(" Exercício não encontrado.")
            return False
        return resposta_usuario.strip().lower() == exercicio.get_resposta_certa().strip().lower()

    def obter_dicas(self, id_exercicio: int) -> str:
        exercicio = self.__persistencia.buscar_por_id(id_exercicio)
        return exercicio.get_dicas() if exercicio else " Dica não disponível."
    
    def carregar_exercicios(self, id_fase, jogador):
        progresso_service = ProgressoFaseServiceImpl()
        progresso = progresso_service.buscar_progresso_por_jogador_fase(jogador.get_id_jogador(), id_fase)
        exercicios = self.listar_exercicios_por_fase(id_fase)
        if progresso:
            indice_atual = progresso.get_indice_exercicio()
            acertos = progresso.get_acertos()
            erros = progresso.get_erros()
            # Retorna tudo para usar na tela!
            return exercicios, progresso
        else:
            return exercicios, None


