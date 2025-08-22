from Iniciante.Service.ProgressoFaseService import ProgressoFaseService
from Iniciante.Persistencia.Impl.ProgressoFasePersistenciaImpl import ProgressoFasePersistenciaImpl
from Iniciante.Persistencia.Entidade.ProgressoFase import ProgressoFase

class ProgressoFaseServiceImpl(ProgressoFaseService):
    def __init__(self):
        self.progresso_persistencia = ProgressoFasePersistenciaImpl()

    def criar_progresso(self, id_jogador, id_fase, indice_exercicio=0, acertos=0, erros=0, resposta_parcial=""):
        novo_progresso = ProgressoFase(
            id_progresso=None,
            id_jogador=id_jogador,
            id_fase=id_fase,
            indice_exercicio=indice_exercicio,
            acertos=acertos,
            erros=erros,
            resposta_parcial=resposta_parcial,
            atualizado_em=None
        )
        return self.progresso_persistencia.salvar(novo_progresso)

    def buscar_progresso_por_id(self, id_progresso):
        return self.progresso_persistencia.buscar_por_id(id_progresso)

    def buscar_progresso_por_jogador_fase(self, id_jogador, id_fase):
        return self.progresso_persistencia.buscar_por_jogador_fase(id_jogador, id_fase)

    def listar_todos_progresso(self):
        return self.progresso_persistencia.listar_todos()

    def deletar_progresso(self, id_progresso):
        self.progresso_persistencia.deletar(id_progresso)

    def deletar_progresso_por_jogador_fase(self, id_jogador, id_fase):
        self.progresso_persistencia.deletar_por_jogador_fase(id_jogador, id_fase)



    def atualizar_progresso(self, progresso):
        self.progresso_persistencia.atualizar(progresso)

    def salvar_ou_atualizar_progresso(self, jogador, id_fase, indice_exercicio, acertos, erros, resposta_parcial):
        # Verifica se já existe progresso para esse jogador/fase
        progresso = self.progresso_persistencia.buscar_por_jogador_fase(jogador.get_id_jogador(), id_fase)

        if progresso:
            progresso.set_indice_exercicio(indice_exercicio)
            progresso.set_acertos(acertos)
            progresso.set_erros(erros)
            progresso.set_resposta_parcial(resposta_parcial)
            self.progresso_persistencia.atualizar(progresso)
        else:
            novo = ProgressoFase(
                id_progresso=None,
                id_jogador=jogador.get_id_jogador(),
                id_fase=id_fase,
                indice_exercicio=indice_exercicio,
                acertos=acertos,
                erros=erros,
                resposta_parcial=resposta_parcial,
                atualizado_em=None
            )
            self.progresso_persistencia.salvar(novo)

    

    def fase_ja_concluida(self, id_jogador, id_fase, total_exercicios):
        """Retorna True se todos os exercícios da fase foram concluídos."""
        progresso = self.progresso_persistencia.buscar_por_jogador_fase(id_jogador, id_fase)
        if not progresso:
            return False
        return progresso.get_indice_exercicio() >= total_exercicios
