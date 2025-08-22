import pygame

class TelaResultado:
    def __init__(self, largura, altura, sucesso, recompensa, callback_continuar):
        self.largura, self.altura = largura, altura
        self.sucesso = sucesso
        self.recompensa = recompensa
        self.callback_continuar = callback_continuar

        # --- Configurações Visuais ---
        self.fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 28)
        self.fonte_botao = pygame.font.SysFont("Arial", 30)

        # --- Cores ---
        self.COR_SUCESSO = (30, 150, 30)
        self.COR_FALHA = (180, 30, 30)
        self.COR_BRANCO = (255, 255, 255)
        self.COR_PRETO = (0, 0, 0)

        # --- Layout ---
        self.caixa_rect = pygame.Rect(0, 0, 600, 300)
        self.caixa_rect.center = (self.largura // 2, self.altura // 2)
        self.botao_continuar_rect = pygame.Rect(0, 0, 200, 50)
        self.botao_continuar_rect.center = (self.largura // 2, self.caixa_rect.bottom - 60)

    def desenhar(self, tela):
        # Overlay para focar na caixa de resultado
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        # Caixa central
        pygame.draw.rect(tela, (245, 245, 245), self.caixa_rect, border_radius=15)

        # --- Conteúdo Dinâmico (Sucesso vs. Falha) ---
        if self.sucesso:
            cor_titulo = self.COR_SUCESSO
            texto_titulo = "Projeto Concluído!"
            texto_sub = f"Você recebeu: R$ {self.recompensa:.2f}"
        else:
            cor_titulo = self.COR_FALHA
            texto_titulo = "Falha no Projeto"
            texto_sub = "Você não recebeu nenhuma recompensa."

        # Renderizar Textos
        titulo_surf = self.fonte_titulo.render(texto_titulo, True, cor_titulo)
        tela.blit(titulo_surf, (self.caixa_rect.centerx - titulo_surf.get_width() // 2, self.caixa_rect.top + 40))
        
        sub_surf = self.fonte_subtitulo.render(texto_sub, True, self.COR_PRETO)
        tela.blit(sub_surf, (self.caixa_rect.centerx - sub_surf.get_width() // 2, self.caixa_rect.top + 130))

        # --- Botão Continuar ---
        mouse_pos = pygame.mouse.get_pos()
        cor_botao = (100, 100, 100) if self.botao_continuar_rect.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(tela, cor_botao, self.botao_continuar_rect, border_radius=10)
        
        cont_surf = self.fonte_botao.render("Continuar", True, self.COR_BRANCO)
        tela.blit(cont_surf, (self.botao_continuar_rect.centerx - cont_surf.get_width() // 2, self.botao_continuar_rect.centery - cont_surf.get_height() // 2))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_continuar_rect.collidepoint(evento.pos):
                    self.callback_continuar()