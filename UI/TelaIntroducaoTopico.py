import pygame
import os

class TelaIntroducaoTopico:
    def __init__(self, largura, altura, nome_topico, descricao, on_confirmar, jogador=None):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.descricao = descricao
        self.on_confirmar = on_confirmar
        self.jogador = jogador
        self.nome_jogador = jogador.get_nome() if jogador else "Visitante"
        self.painel_visivel = True  # Para fechar a tela

        # Arrastar painel
        self.dragging = False
        self.drag_offset = (0, 0)

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Consolas', 28, bold=True)
        self.fonte = pygame.font.SysFont('Consolas', 22)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 20)

        #caminho_img = os.path.join("Assets", "TelaJogoIniciante.png")
        #self.bg = pygame.image.load(caminho_img).convert_alpha()
        #self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        # Painel central
        self.rect_painel = pygame.Rect(
            int(largura * 0.25),
            int(altura * 0.13),
            int(largura * 0.54),
            int(altura * 0.66)
        )

        btn_w, btn_h = 200, 52
        self.rect_btn = pygame.Rect(
            self.rect_painel.x + (self.rect_painel.w - btn_w) // 2,
            self.rect_painel.bottom - btn_h - 28,
            btn_w,
            btn_h
        )

    def quebrar_linha(self, texto, fonte, largura_max):
        linhas = []
        paragrafos = texto.split('\n')
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            atual = ""
            for palavra in palavras:
                teste = f"{atual} {palavra}" if atual else palavra
                if fonte.size(teste)[0] <= largura_max:
                    atual = teste
                else:
                    if atual:
                        linhas.append(atual)
                    atual = palavra
            if atual:
                linhas.append(atual)
        return linhas

    def desenhar(self, tela):
        #tela.blit(self.bg, (0, 0))
        if not self.painel_visivel:
            return

        painel = self.rect_painel
        painel_surf = pygame.Surface((painel.w, painel.h), pygame.SRCALPHA)
        pygame.draw.rect(painel_surf, (18, 24, 32, 210), (0, 0, painel.w, painel.h), border_radius=16)
        tela.blit(painel_surf, (painel.x, painel.y))
        pygame.draw.rect(tela, (42, 103, 188), painel, 6, border_radius=16)

        # --- DESENHE A BARRA AZUL PRIMEIRO ---
        header_h = 50
        header_rect = pygame.Rect(painel.x, painel.y, painel.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header_rect, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (painel.x, painel.y + header_h), (painel.x + painel.w, painel.y + header_h), 2)

        # Botão X POR CIMA do header
        tam = 32
        espaco = 10
        self.rect_x = pygame.Rect(
            self.rect_painel.right - tam - espaco,
            self.rect_painel.y + espaco,
            tam, tam
        )
        pygame.draw.circle(tela, (255, 100, 100), self.rect_x.center, tam // 2)
        x_mark = self.fonte_pequena.render("x", True, (40, 0, 0))
        tela.blit(
            x_mark,
            (
                self.rect_x.x + (tam - x_mark.get_width()) // 2,
                self.rect_x.y + (tam - x_mark.get_height()) // 2,
            )
        )

        # Título centralizado
        titulo = f"Tópico: {self.nome_topico}"
        titulo_surface = self.fonte_titulo.render(titulo, True, (130, 220, 255))
        titulo_rect = titulo_surface.get_rect(center=(painel.centerx, painel.y + header_h // 2 + 2))
        tela.blit(titulo_surface, titulo_rect)

        # Área do conteúdo
        margem_x = 44
        margem_y = 38
        x = painel.x + margem_x
        y = painel.y + header_h + margem_y

        usuario_txt = f"Usuário logado: {self.nome_jogador}"
        usuario_surface = self.fonte_pequena.render(usuario_txt, True, (230, 230, 90))
        tela.blit(usuario_surface, (x, y))
        y += usuario_surface.get_height() + 6

        divisoria_y = y + 4
        pygame.draw.line(
            tela,
            (80, 120, 180),
            (x, divisoria_y),
            (painel.x + painel.w - margem_x, divisoria_y),
            2
        )
        y = divisoria_y + 12

        largura_max = painel.w - 2 * margem_x
        linhas = self.quebrar_linha(self.descricao, self.fonte_pequena, largura_max)
        for linha in linhas:
            tela.blit(self.fonte_pequena.render(linha, True, (255,255,255)), (x, y))
            y += 32

        # Botão "ENTENDIDO"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_hover = self.rect_btn.collidepoint(mouse_x, mouse_y)
        cor_texto = (255,255,255)
        fonte_botao = self.fonte
        cor_btn = (0, 180, 80) if botao_hover else (0, 150, 200)
        if botao_hover:
            cor_texto = (255, 230, 80)
            fonte_botao = pygame.font.SysFont('Consolas', 22, bold=True)
        pygame.draw.rect(tela, cor_btn, self.rect_btn, border_radius=24)
        botao_surface = fonte_botao.render("ENTENDIDO", True, cor_texto)
        tela.blit(
            botao_surface,
            (
                self.rect_btn.x + (self.rect_btn.w - botao_surface.get_width()) // 2,
                self.rect_btn.y + (self.rect_btn.h - botao_surface.get_height()) // 2
            )
        )

    def tratar_eventos(self, eventos):
        if not self.painel_visivel:
            return
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Clique no X para fechar o painel
                if hasattr(self, "rect_x") and self.rect_x.collidepoint(x, y):
                    self.painel_visivel = False
                    return  # só fecha!
                # Arrastar painel
                if evento.button == 1:
                    header_h = 50
                    header_rect = pygame.Rect(self.rect_painel.x, self.rect_painel.y, self.rect_painel.w, header_h)
                    if header_rect.collidepoint(evento.pos):
                        self.dragging = True
                        mx, my = evento.pos
                        self.drag_offset = (mx - self.rect_painel.x, my - self.rect_painel.y)
            elif evento.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mx, my = evento.pos
                    dx, dy = self.drag_offset
                    self.rect_painel.x = mx - dx
                    self.rect_painel.y = my - dy
                    self.rect_btn.x = self.rect_painel.x + (self.rect_painel.w - self.rect_btn.w) // 2
                    self.rect_btn.y = self.rect_painel.bottom - self.rect_btn.h - 28
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and self.dragging:
                    self.dragging = False

            # Clique no botão "ENTENDIDO"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_btn.collidepoint(x, y):
                    if self.on_confirmar:
                        self.on_confirmar()
