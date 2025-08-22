import pygame

class Janela:
    def __init__(self, x, y, largura, altura, titulo="Janela"):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.titulo = titulo
        self.visivel = True
        self.deve_fechar = False

        # --- Lógica para arrastar ---
        self.arrastando = False
        self.offset_arrasto = (0, 0)
        self.rect_titulo = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 30)
        
        # --- Botão de fechar ---
        self.rect_fechar = pygame.Rect(self.rect.right - 28, self.rect.top + 2, 26, 26)

        # --- Fontes e Cores ---
        self.fonte_titulo = pygame.font.SysFont("Arial", 18, bold=True)
        self.cor_fundo = (240, 240, 240)
        self.cor_borda = (100, 100, 100)
        self.cor_titulo_bg = (210, 210, 210)
        self.cor_fechar = (200, 40, 40)
        self.cor_fechar_hover = (230, 60, 60)

    def desenhar_base(self, tela):
        """Desenha o frame da janela (fundo, borda, título)."""
        # Fundo principal
        pygame.draw.rect(tela, self.cor_fundo, self.rect)
        # Borda
        pygame.draw.rect(tela, self.cor_borda, self.rect, 2)
        # Barra de título
        pygame.draw.rect(tela, self.cor_titulo_bg, self.rect_titulo)
        pygame.draw.line(tela, self.cor_borda, (self.rect.left, self.rect.top + 30), (self.rect.right, self.rect.top + 30), 2)
        
        # Texto do título
        titulo_surf = self.fonte_titulo.render(self.titulo, True, (20, 20, 20))
        tela.blit(titulo_surf, (self.rect.x + 10, self.rect.y + 5))
        
        # Botão de fechar
        cor_botao = self.cor_fechar_hover if self.rect_fechar.collidepoint(pygame.mouse.get_pos()) else self.cor_fechar
        pygame.draw.rect(tela, cor_botao, self.rect_fechar, border_radius=4)
        pygame.draw.line(tela, (255, 255, 255), (self.rect_fechar.left + 7, self.rect_fechar.top + 7), (self.rect_fechar.right - 7, self.rect_fechar.bottom - 7), 2)
        pygame.draw.line(tela, (255, 255, 255), (self.rect_fechar.left + 7, self.rect_fechar.bottom - 7), (self.rect_fechar.right - 7, self.rect_fechar.top + 7), 2)

    def desenhar_conteudo(self, tela):
        """Este método será sobrescrito pelas classes filhas."""
        pass

    def desenhar(self, tela):
        """Método principal de desenho, chamado pelo loop do jogo."""
        if not self.visivel:
            return
        self.desenhar_base(tela)
        self.desenhar_conteudo(tela)

    def tratar_eventos(self, eventos):
        """Trata eventos de arrastar e fechar."""
        if not self.visivel:
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_fechar.collidepoint(evento.pos):
                    self.deve_fechar = True
                elif self.rect_titulo.collidepoint(evento.pos):
                    self.arrastando = True
                    self.offset_arrasto = (evento.pos[0] - self.rect.x, evento.pos[1] - self.rect.y)
            
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.arrastando = False

            if evento.type == pygame.MOUSEMOTION and self.arrastando:
                self.rect.x = evento.pos[0] - self.offset_arrasto[0]
                self.rect.y = evento.pos[1] - self.offset_arrasto[1]
                # Atualiza a posição dos componentes internos
                self.rect_titulo.topleft = self.rect.topleft
                self.rect_fechar.topleft = (self.rect.right - 28, self.rect.top + 2)