from Intermediario.Service.LojaService import LojaService
from Intermediario.Persistencia.Impl.LojaPersistenciaImpl import LojaPersistenciaImpl
from Intermediario.Persistencia.Entidade.Loja import Loja
from Iniciante.Persistencia.Impl.JogadorPersistenciaImpl import JogadorPersistenciaImpl
from Iniciante.Persistencia.Entidade.Jogador import Jogador
from datetime import datetime, timedelta


class LojaServiceImpl(LojaService):
    def __init__(self):
        self.loja_persistencia = LojaPersistenciaImpl()
        self.jogador_persistencia = JogadorPersistenciaImpl()

    # ---------- REDUÇÃO DE TEMPO (sem mexer no BD) ----------
    def _percentual_reducao_por_equipamentos(self, id_jogador: int) -> float:
        """
        Soma as reduções de tempo baseadas nos equipamentos já comprados.
        Teclado basico: -5%
        Teclado Pro:    -10%
        Monitor basico: -5%
        Monitor Pro:    -10%
        """
        itens = self.loja_persistencia.listar_por_jogador(id_jogador)
        p = 0.0
        for item in itens:
            # equipamento => duracao_total == 0
            if item.get_duracao_total() == 0:
                nome = (item.get_nome() or "").strip().lower()
                cat  = (item.get_categoria() or "").strip().lower()
                if nome == "teclado" and cat == "basico":
                    p += 0.05
                elif nome == "teclado" and cat == "pro":
                    p += 0.10
                elif nome == "monitor" and cat == "basico":
                    p += 0.05
                elif nome == "monitor" and cat == "pro":
                    p += 0.10
        # se quiser um limite máximo, descomente a linha abaixo
        # p = min(p, 0.50)
        return p

    def calcular_tempo_com_reducao(self, id_jogador: int, tempo_base: int) -> int:
        """Tempo final aplicado em cursos/treinamentos conforme equipamentos já comprados."""
        if tempo_base <= 0:
            return 0
        p = self._percentual_reducao_por_equipamentos(id_jogador)
        tempo = int(round(tempo_base * (1.0 - p)))
        return max(1, tempo)

    # --------------------------------------------------------

    def comprar_item(self, id_jogador: int, nome: str, categoria: str, preco: float, duracao_segundos: int):
        jogador = self.jogador_persistencia.buscar_por_id(id_jogador)
        if not jogador:
            raise Exception("Jogador não encontrado.")

        if jogador.get_dinheiro() < preco:
            raise Exception("Dinheiro insuficiente para a compra.")

        # cursos/treinamentos (tempo > 0) => apenas 1 por vez
        if duracao_segundos > 0:
            em_andamento = self.loja_persistencia.listar_em_andamento(id_jogador)
            if em_andamento:
                raise Exception("Você já possui um curso em andamento. Conclua antes de iniciar outro.")
        else:
            # equipamento (tempo == 0) => não pode comprar o mesmo equipamento duas vezes
            existentes = self.loja_persistencia.listar_por_jogador(id_jogador)
            for it in existentes:
                if (it.get_duracao_total() == 0 and
                    (it.get_nome() or "").strip().lower() == (nome or "").strip().lower() and
                    (it.get_categoria() or "").strip().lower() == (categoria or "").strip().lower()):
                    raise Exception(f"{nome} ({categoria}) já foi comprado.")

        # desconta dinheiro do jogador
        jogador.set_dinheiro(jogador.get_dinheiro() - preco)
        self.jogador_persistencia.atualizar(jogador)

        # aplica redução de tempo em cursos/treinamentos
        tempo_final = self.calcular_tempo_com_reducao(id_jogador, duracao_segundos) if duracao_segundos > 0 else 0

        novo_item = Loja(
            id_item=None,
            id_jogador=id_jogador,
            nome=nome,
            categoria=categoria,
            preco=preco,
            duracao_segundos=tempo_final,   # já com redução
            duracao_total=tempo_final,      # guarda o total já reduzido
            status="andamento" if tempo_final > 0 else "usado"
        )

        return self.loja_persistencia.salvar(novo_item)

    def buscar_item_por_id(self, id_item: int):
        return self.loja_persistencia.buscar_por_id(id_item)

    def listar_itens_jogador(self, id_jogador: int):
        return self.loja_persistencia.listar_por_jogador(id_jogador)

    def listar_em_andamento(self, id_jogador: int):
        return self.loja_persistencia.listar_em_andamento(id_jogador)

    def concluir_item(self, id_item: int):
        item = self.loja_persistencia.buscar_por_id(id_item)
        if not item:
            raise Exception("Item não encontrado.")

        # atualiza status
        self.loja_persistencia.concluir_item(id_item)

        # aplicar recompensas dependendo do item
        jogador = self.jogador_persistencia.buscar_por_id(item.get_id_jogador())
        if not jogador:
            raise Exception("Jogador não encontrado.")

        # Regras básicas de evolução (nomes iguais aos seus)
        if (item.get_nome() or "").lower() == "front-end":
            cat = (item.get_categoria() or "").lower()
            if cat == "iniciante":
                jogador.set_frontend(jogador.get_frontend() + 1)
            elif cat == "intermediario":
                jogador.set_frontend(jogador.get_frontend() + 2)
            elif cat == "avancado":
                jogador.set_frontend(jogador.get_frontend() + 3)

        elif (item.get_nome() or "").lower() == "social":
            cat = (item.get_categoria() or "").lower()
            if cat == "iniciante":
                jogador.set_social(jogador.get_social() + 1)
            elif cat == "intermediario":
                jogador.set_social(jogador.get_social() + 2)
            elif cat == "avancado":
                jogador.set_social(jogador.get_social() + 3)

        # salva evolução
        self.jogador_persistencia.atualizar(jogador)
        return jogador

    def deletar_item(self, id_item: int):
        return self.loja_persistencia.deletar(id_item)

    def atualizar_item(self, loja: Loja):
        return self.loja_persistencia.atualizar(loja)
