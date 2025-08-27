# Certifique-se de que os caminhos de importação correspondem à sua estrutura de pastas
from Intermediario.Service.JogadorProjetoService import JogadorProjetoService
from Intermediario.Persistencia.Impl.JogadorProjetoPersistenciaImpl import JogadorProjetoPersistenciaImpl
from Intermediario.Persistencia.Impl.ProjetoFreelancePersistenciaImpl import ProjetoFreelancePersistenciaImpl
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Iniciante.Service.Impl.JogadorServiceImpl import JogadorServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl

class JogadorProjetoServiceImpl(JogadorProjetoService):
    def __init__(self):
        self.persistencia = JogadorProjetoPersistenciaImpl()
        self.projeto_persistencia = ProjetoFreelancePersistenciaImpl() 
        self.jogador = JogadorServiceImpl()
        self.cliente_service = ClienteServiceImpl()

    def aceitar_projeto(self, jogador, projeto):
        """
        Contém a lógica de negócio para aceitar um projeto.
        Retorna True se o projeto foi aceito com sucesso, False caso contrário.
        """
        if self.buscar_projeto_ativo(jogador.get_id_jogador()):
            print("[SERVICE LOGIC] Falha: Jogador já possui um projeto ativo.")
            return False

        tem_req = (jogador.get_backend() >= projeto.get_req_backend() and
                   jogador.get_frontend() >= projeto.get_req_frontend() and
                   jogador.get_social() >= projeto.get_req_social())

        if not tem_req:
            print("[SERVICE LOGIC] Falha: Skills insuficientes.")
            return False
            
        nova_relacao = JogadorProjeto(
            id_jogador=jogador.get_id_jogador(),
            id_projeto=projeto.get_id_projeto(),
            status="em_andamento"
        )
        self.persistencia.salvar(nova_relacao)
        print(f"[SERVICE LOGIC] Sucesso: Contrato '{projeto.get_titulo()}' aceito.")
        return True

    def buscar_projeto_ativo(self, id_jogador):
        """
        Verifica se o jogador tem um projeto 'em_andamento' e retorna o objeto ProjetoFreelance completo.
        """
        projetos_do_jogador = self.persistencia.listar_por_jogador(id_jogador)
        for relacao in projetos_do_jogador:
            if relacao.get_status() == "em_andamento":
                return self.projeto_persistencia.buscar_por_id(relacao.get_id_projeto())
        return None

    def finalizar_projeto(self, jogador, projeto):
        """
        Finaliza um projeto, atualiza o status e adiciona a recompensa.
        """
        print(f"O projeto '{projeto.get_titulo()}' foi entregue com sucesso!")
        # 1. Atualiza o status do projeto no banco para 'concluido'
        self.persistencia.atualizar_status(jogador.get_id_jogador(), projeto.get_id_projeto(), 'concluido')
        
        # 2. Adiciona a recompensa ao dinheiro do jogador
        novo_dinheiro = jogador.get_dinheiro() + projeto.get_recompensa()
        jogador.set_dinheiro(novo_dinheiro)
        self.jogador.atualizar_jogador(jogador)
        print(f"Recompensa de R$ {projeto.get_recompensa():.2f} adicionada. Saldo atual: R$ {novo_dinheiro:.2f}")

    def desistir_projeto(self, jogador, projeto):
        """
        Desiste de um projeto, atualiza o status e aplica uma penalidade de reputação.
        """
        print(f"O jogador desistiu do projeto '{projeto.get_titulo()}'.")
        # 1. Atualiza o status do projeto no banco para 'desistiu'
        self.persistencia.atualizar_status(jogador.get_id_jogador(), projeto.get_id_projeto(), 'desistiu')
        
        # 2. Aplica a penalidade de reputação com o cliente
        cliente = self.cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        if cliente:
            # Penalidade: diminui a reputação em 0.5, com um mínimo de 0.0
            nova_reputacao = max(0.0, cliente.get_reputacao() - 0.5)
            cliente.set_reputacao(nova_reputacao)
            self.cliente_service.atualizar_cliente(cliente)
            print(f"Penalidade aplicada. Nova reputação com {cliente.get_nome()}: {nova_reputacao:.1f}")

