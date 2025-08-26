from typing import Optional, List
from Intermediario.Service.JogadorProjetoService import JogadorProjetoService
from Intermediario.Persistencia.Impl.JogadorProjetoPersistenciaImpl import JogadorProjetoPersistenciaImpl
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class JogadorProjetoServiceImpl(JogadorProjetoService):
    def __init__(self):
        self.persistencia = JogadorProjetoPersistenciaImpl()
        self.projeto_persistencia = ProjetoFreelancePersistenciaImpl()

    def aceitar_projeto(self, jogador_projeto: JogadorProjeto) -> None:
        """Registra que o jogador aceitou um projeto."""
        self.persistencia.salvar(jogador_projeto)

    def atualizar_status(self, jogador_projeto: JogadorProjeto) -> None:
        """Atualiza o status da relação jogador-projeto."""
        self.persistencia.atualizar_status(
            jogador_projeto.get_id_jogador(),
            jogador_projeto.get_id_projeto(),
            jogador_projeto.get_status()
        )

    def remover_relacao(self, id_jogador: int, id_projeto: int) -> None:
        """Remove a relação entre jogador e projeto."""
        self.persistencia.remover(id_jogador, id_projeto)

    def buscar_relacao(self, id_jogador: int, id_projeto: int) -> Optional[JogadorProjeto]:
        """Busca uma relação específica entre jogador e projeto."""
        return self.persistencia.buscar(id_jogador, id_projeto)

    def listar_projetos_do_jogador(self, id_jogador: int) -> List[JogadorProjeto]:
        """Lista todos os projetos associados ao jogador."""
        return self.persistencia.listar_por_jogador(id_jogador)

    def buscar_projeto_ativo(self, id_jogador: int) -> Optional[ProjetoFreelance]:
        """
        Verifica se o jogador tem um projeto 'em_andamento' e retorna o objeto ProjetoFreelance completo.
        Retorna None se nenhum projeto estiver ativo.
        """
        try:
            projetos_do_jogador = self.persistencia.listar_por_jogador(id_jogador)
            for relacao in projetos_do_jogador:
                if relacao.get_status() == "em_andamento":
                    return self.projeto_persistencia.buscar_por_id(relacao.get_id_projeto())
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao buscar projeto ativo: {e}")
            return None