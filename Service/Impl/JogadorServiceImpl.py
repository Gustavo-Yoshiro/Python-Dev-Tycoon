from Service.JogadorService import JogadorService
from Persistencia.Impl.JogadorPersistenciaImpl import JogadorPersistenciaImpl
from Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl
from Persistencia.Entidade.Jogador import Jogador

class JogadorServiceImpl(JogadorService):
    def __init__(self):
        self.jogador_persistencia = JogadorPersistenciaImpl()
        self.fase_persistencia = FasePersistenciaImpl()

    def criar_jogador(self, nome):
        if not nome or not nome.strip():
            raise ValueError("Nome do jogador não pode ser vazio!")

        # Busca fase "Iniciante" (por tipo), assume que sempre existe pelo menos uma!

        id_fase = 1

        # Atributos iniciais fixos
        social = 0
        dinheiro = 0.0
        backend = 0
        frontend = 0

        novo_jogador = Jogador(
            id_jogador=None,
            nome=nome.strip(),
            id_fase=id_fase,
            social=social,
            dinheiro=dinheiro,
            backend=backend,
            frontend=frontend
        )
        return self.jogador_persistencia.salvar(novo_jogador)



    def buscar_jogador_por_id(self, id_jogador):
        return self.jogador_persistencia.buscar_por_id(id_jogador)

    def listar_todos_jogadores(self):
        return self.jogador_persistencia.listar_todos()

    def deletar_jogador(self, id_jogador):
        return self.jogador_persistencia.deletar(id_jogador)

    def atualizar_jogador(self, jogador):
        # Aqui você pode aplicar regras antes de atualizar, se quiser
        return self.jogador_persistencia.atualizar(jogador)

    def premiar_jogador(self, id_jogador, valor):
        jogador = self.jogador_persistencia.buscar_por_id(id_jogador)
        if not jogador:
            raise Exception("Jogador não existe!")
        if valor < 0:
            raise ValueError("Valor do prêmio não pode ser negativo!")
        jogador.set_dinheiro(jogador.get_dinheiro() + valor)
        self.jogador_persistencia.atualizar(jogador)
        return jogador.get_dinheiro()

    def punir_jogador(self, id_jogador, valor):
        jogador = self.jogador_persistencia.buscar_por_id(id_jogador)
        if not jogador:
            raise Exception("Jogador não existe!")
        if valor < 0:
            raise ValueError("Valor da punição não pode ser negativo!")
        jogador.set_dinheiro(max(0.0, jogador.get_dinheiro() - valor))
        self.jogador_persistencia.atualizar(jogador)
        return jogador.get_dinheiro()

    def evoluir_atributo(self, id_jogador, atributo, valor):
        jogador = self.jogador_persistencia.buscar_por_id(id_jogador)
        if not jogador:
            raise Exception("Jogador não existe!")
        if atributo not in ["social", "backend", "frontend"]:
            raise ValueError("Atributo inválido para evolução.")
        if valor < 0:
            raise ValueError("Valor para evolução não pode ser negativo!")
        # Atualiza o atributo desejado
        if atributo == "social":
            jogador.set_social(jogador.get_social() + valor)
        elif atributo == "backend":
            jogador.set_backend(jogador.get_backend() + valor)
        elif atributo == "frontend":
            jogador.set_frontend(jogador.get_frontend() + valor)
        self.jogador_persistencia.atualizar(jogador)

    def mudar_fase(self, id_jogador, nova_fase):
        jogador = self.jogador_persistencia.buscar_por_id(id_jogador)
        if not jogador:
            raise Exception("Jogador não existe!")
        fase = self.fase_persistencia.buscar_por_id(nova_fase)
        if not fase:
            raise Exception("Nova fase não existe!")
        jogador.set_id_fase(nova_fase)
        self.jogador_persistencia.atualizar(jogador)
