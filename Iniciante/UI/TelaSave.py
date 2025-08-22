import pygame
from datetime import datetime

class TelaSave:
    def __init__(self, largura, altura, save_service, jogador_service, callback_selecionar_slot, callback_criar_jogador):
        self.largura = largura
        self.altura = altura
        self.save_service = save_service
        self.jogador_service = jogador_service
        self.callback_selecionar_slot = callback_selecionar_slot
        self.callback_criar_jogador = callback_criar_jogador

        self.fundo = pygame.image.load("Assets/TelaSave.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))

        self.fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_normal = pygame.font.SysFont("Arial", 32)
        self.fonte_pequena = pygame.font.SysFont("Arial", 24)

        self.slots = []
        self.criar_slots()

        self.botao_voltar = pygame.Rect(50, 50, 120, 50)

        self.saves = self.save_service.listar_saves()
        self.areas_lixeira = {}

        self.confirmacao_ativa = False
        self.indice_confirmacao = None
        self.botao_sim = pygame.Rect(0, 0, 100, 40)
        self.botao_nao = pygame.Rect(0, 0, 100, 40)

    def criar_slots(self):
        slot_width = self.largura * 0.7
        slot_height = 120
        start_y = 180

        self.slots = []

        for i in range(3):
            rect = pygame.Rect(
                (self.largura - slot_width) // 2,
                start_y + i * (slot_height + 20),
                slot_width,
                slot_height
            )
            self.slots.append(rect)

    def mouse_sobre_elemento_prioritario(self, pos_mouse):
        if self.confirmacao_ativa:
            if self.botao_sim.collidepoint(pos_mouse) or self.botao_nao.collidepoint(pos_mouse):
                return True

            largura_janela = 400
            altura_janela = 200
            x = (self.largura - largura_janela) // 2
            y = (self.altura - altura_janela) // 2
            area_janela = pygame.Rect(x, y, largura_janela, altura_janela)
            if area_janela.collidepoint(pos_mouse):
                return True

        for area in self.areas_lixeira.values():
            if area.collidepoint(pos_mouse):
                return True

        return False

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        titulo = self.fonte_titulo.render("Selecionar Save", True, (255, 255, 255))
        tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 80))

        pygame.draw.rect(tela, (70, 70, 70), self.botao_voltar, border_radius=5)
        texto_voltar = self.fonte_normal.render("Voltar", True, (255, 255, 255))
        tela.blit(texto_voltar, (
            self.botao_voltar.x + (self.botao_voltar.width - texto_voltar.get_width()) // 2,
            self.botao_voltar.y + (self.botao_voltar.height - texto_voltar.get_height()) // 2
        ))

        COR_SLOT_1 = (20, 30, 60, 120)
        COR_SLOT_HOVER_1 = (100, 140, 200, 220)
        COR_BORDA = (60, 90, 140)

        pos_mouse = pygame.mouse.get_pos()
        self.areas_lixeira.clear()

        for i, slot in enumerate(self.slots):
            slot_surface = pygame.Surface((slot.width, slot.height), pygame.SRCALPHA)
            mouse_em_cima = slot.collidepoint(pos_mouse) and not self.mouse_sobre_elemento_prioritario(pos_mouse)
            cor_slot = COR_SLOT_HOVER_1 if mouse_em_cima else COR_SLOT_1

            pygame.draw.rect(slot_surface, cor_slot, slot_surface.get_rect(), border_radius=10)
            tela.blit(slot_surface, (slot.x, slot.y))
            pygame.draw.rect(tela, COR_BORDA, slot, width=3, border_radius=10)

            if i < len(self.saves):
                self.desenhar_slot_preenchido(tela, slot, i)
            else:
                self.desenhar_slot_vazio(tela, slot, i)

        if self.confirmacao_ativa:
            self.desenhar_confirmacao(tela)

    def desenhar_slot_preenchido(self, tela, slot, indice):
        save = self.saves[indice]
        jogador = self.jogador_service.buscar_jogador_por_id(save.get_id_jogador())
        tipo_fase = self.jogador_service.buscar_tipo_fase_atual(jogador.get_id_jogador())

        if tipo_fase and tipo_fase.lower() == "iniciante":
            caminho_imagem = "assets/TelaJogoIniciante.png"
        else:
            caminho_imagem = "assets/TelaJogoIniciante.png"

        try:
            imagem_fase = pygame.image.load(caminho_imagem)
            imagem_fase = pygame.transform.scale(imagem_fase, (130, 100))
        except Exception as e:
            print("Erro ao carregar imagem da fase:", e)
            imagem_fase = pygame.Surface((120, 90))
            imagem_fase.fill((150, 0, 0))

        tela.blit(imagem_fase, (slot.x + 10, slot.y + 10))

        texto_nome = self.fonte_normal.render(f"{jogador.get_nome()}", True, (0, 0, 0))
        tela.blit(texto_nome, (slot.x + 145, slot.y + 20))

        texto_fase_str = f"Fase: {tipo_fase}" if tipo_fase else "Fase: N/A"
        texto_fase = self.fonte_normal.render(texto_fase_str, True, (255, 255, 255))
        tela.blit(texto_fase, (slot.x + 145, slot.y + 50))

        try:
            data_obj = datetime.strptime(save.get_data_save(), "%Y-%m-%d %H:%M:%S")
            data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            print("Erro ao formatar data:", e)
            data_formatada = save.get_data_save()

        texto_data = self.fonte_pequena.render(data_formatada, True, (100, 100, 100))
        tela.blit(texto_data, (slot.x + slot.width - 150, slot.y + 20))

        try:
            icone_lixeira = pygame.image.load("assets/lixeira.png")
            icone_lixeira = pygame.transform.scale(icone_lixeira, (30, 30))
        except Exception as e:
            print("Erro ao carregar ícone da lixeira:", e)
            icone_lixeira = pygame.Surface((30, 30))
            icone_lixeira.fill((200, 0, 0))

        pos_x = slot.x + slot.width - 40
        pos_y = slot.y + slot.height - 40
        tela.blit(icone_lixeira, (pos_x, pos_y))
        self.areas_lixeira[indice] = pygame.Rect(pos_x, pos_y, 30, 30)

    def desenhar_slot_vazio(self, tela, slot, indice):
        texto = self.fonte_normal.render("Novo Jogo", True, (255, 255, 255))
        tela.blit(texto, (slot.x + 110, slot.y + (slot.height - texto.get_height()) // 2))

    def desenhar_confirmacao(self, tela):
        largura_janela = 400
        altura_janela = 200
        x = (self.largura - largura_janela) // 2
        y = (self.altura - altura_janela) // 2

        # Fundo da janela de confirmação
        fundo = pygame.Surface((largura_janela, altura_janela))
        fundo.fill((30, 30, 30))
        pygame.draw.rect(fundo, (200, 200, 200), fundo.get_rect(), 3)

        # Texto da confirmação
        texto = self.fonte_normal.render("Apagar este save?", True, (255, 255, 255))
        fundo.blit(texto, ((largura_janela - texto.get_width()) // 2, 40))

        # Botões
        self.botao_sim = pygame.Rect(x + 60, y + 120, 100, 40)
        self.botao_nao = pygame.Rect(x + 240, y + 120, 100, 40)

        pos_mouse = pygame.mouse.get_pos()

        # Hover e estilo dos botões
        def desenhar_botao(botao, texto_str, cor_base, cor_hover):
            cor = cor_hover if botao.collidepoint(pos_mouse) else cor_base
            pygame.draw.rect(tela, cor, botao, border_radius=8)
            pygame.draw.rect(tela, (255, 255, 255), botao, width=2, border_radius=8)
            texto_render = self.fonte_pequena.render(texto_str, True, (255, 255, 255))
            tela.blit(texto_render, (
                botao.x + (botao.width - texto_render.get_width()) // 2,
                botao.y + (botao.height - texto_render.get_height()) // 2
            ))

        tela.blit(fundo, (x, y))
        desenhar_botao(self.botao_sim, "Sim", (0, 150, 0), (0, 200, 0))
        desenhar_botao(self.botao_nao, "Não", (150, 0, 0), (200, 0, 0))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos

                if self.confirmacao_ativa:
                    if self.botao_sim.collidepoint(pos):
                        save = self.saves[self.indice_confirmacao]
                        id_jogador = save.get_id_jogador()
                        self.jogador_service.apagar_jogador(id_jogador)
                        self.saves = self.save_service.listar_saves()
                        self.confirmacao_ativa = False
                        self.indice_confirmacao = None
                        return "apagado"

                    elif self.botao_nao.collidepoint(pos):
                        self.confirmacao_ativa = False
                        self.indice_confirmacao = None
                        return "cancelado"

                if self.botao_voltar.collidepoint(pos):
                    return "voltar"

                for i, area in self.areas_lixeira.items():
                    if area.collidepoint(pos):
                        self.confirmacao_ativa = True
                        self.indice_confirmacao = i
                        return "confirmar"

                for i, slot in enumerate(self.slots):
                    if slot.collidepoint(pos):
                        if i < len(self.saves):
                            self.callback_selecionar_slot(self.saves[i])
                            return "carregar"
                        else:
                            self.callback_criar_jogador()
                            return "novo_jogador"
        return None