import pygame

class TelaFimIniciante:
    def __init__(self, largura, altura, on_continuar_intermediario, on_menu_principal):
        self.largura = largura
        self.altura = altura
        self.on_continuar_intermediario = on_continuar_intermediario
        self.on_menu_principal = on_menu_principal

        # Fontes
        self.fonte_titulo = pygame.font.SysFont('Consolas', 48, bold=True)
        self.fonte_texto = pygame.font.SysFont('Consolas', 24)
        self.fonte_botao = pygame.font.SysFont('Consolas', 28, bold=True)

        # Cores
        self.COR_FUNDO = (18, 24, 32)
        self.COR_TITULO = (0, 220, 120)
        self.COR_TEXTO = (200, 200, 200)
        self.COR_BOTAO_CONTINUAR = (0, 180, 80)
        self.COR_BOTAO_MENU = (100, 100, 100)

        # Botões
        self.botao_continuar_rect = pygame.Rect(self.largura / 2 - 200, self.altura / 2 + 50, 400, 60)
        self.botao_menu_rect = pygame.Rect(self.largura / 2 - 200, self.altura / 2 + 130, 400, 60)

    def desenhar(self, tela):
        tela.fill(self.COR_FUNDO)

        # Mensagem de Conclusão
        titulo_surf = self.fonte_titulo.render("Módulo Iniciante Concluído!", True, self.COR_TITULO)
        titulo_rect = titulo_surf.get_rect(center=(self.largura / 2, self.altura / 2 - 100))
        tela.blit(titulo_surf, titulo_rect)
        
        texto_surf = self.fonte_texto.render("Você dominou os fundamentos. O mundo do freelance o aguarda.", True, self.COR_TEXTO)
        texto_rect = texto_surf.get_rect(center=(self.largura / 2, self.altura / 2 - 50))
        tela.blit(texto_surf, texto_rect)

        # Botão "Ir para o Intermediário"
        pygame.draw.rect(tela, self.COR_BOTAO_CONTINUAR, self.botao_continuar_rect, border_radius=10)
        continuar_surf = self.fonte_botao.render("Iniciar Carreira Freelancer", True, (255, 255, 255))
        continuar_rect = continuar_surf.get_rect(center=self.botao_continuar_rect.center)
        tela.blit(continuar_surf, continuar_rect)

        # Botão "Menu Principal"
        pygame.draw.rect(tela, self.COR_BOTAO_MENU, self.botao_menu_rect, border_radius=10)
        menu_surf = self.fonte_botao.render("Menu Principal", True, (255, 255, 255))
        menu_rect = menu_surf.get_rect(center=self.botao_menu_rect.center)
        tela.blit(menu_surf, menu_rect)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_continuar_rect.collidepoint(evento.pos):
                    self.on_continuar_intermediario()
                elif self.botao_menu_rect.collidepoint(evento.pos):
                    self.on_menu_principal()
