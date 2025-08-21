import pygame

class TelaFreelance:
    def __init__(self, largura, altura, projetos, callback_selecionar, callback_voltar):
        self.largura, self.altura = largura, altura
        self.projetos = projetos
        self.callback_selecionar = callback_selecionar
        self.callback_voltar = callback_voltar
        self.fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        self.fonte_item = pygame.font.SysFont("Arial", 24)
        self.fonte_botao = pygame.font.SysFont("Arial", 28)
        self.retangulos_projetos = [pygame.Rect(100, 150 + i * 60, self.largura - 200, 50) for i, _ in enumerate(self.projetos)]
        self.botao_voltar_rect = pygame.Rect(50, self.altura - 80, 150, 50)

    def desenhar(self, tela):
        tela.fill((240, 240, 240))
        titulo_surf = self.fonte_titulo.render("Projetos Disponíveis", True, (20, 20, 20))
        tela.blit(titulo_surf, (self.largura // 2 - titulo_surf.get_width() // 2, 50))
        mouse_pos = pygame.mouse.get_pos()
        for i, projeto in enumerate(self.projetos):
            rect = self.retangulos_projetos[i]
            cor_fundo = (220, 235, 255) if rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(tela, cor_fundo, rect, border_radius=8)
            pygame.draw.rect(tela, (180, 180, 180), rect, 2, border_radius=8)
            texto = f"{projeto.get_titulo()} | Recompensa: R$ {projeto.get_recompensa():.2f}"
            item_surf = self.fonte_item.render(texto, True, (20, 20, 20))
            tela.blit(item_surf, (rect.x + 15, rect.y + 12))
        pygame.draw.rect(tela, (210, 50, 50), self.botao_voltar_rect, border_radius=8)
        voltar_surf = self.fonte_botao.render("Voltar", True, (255, 255, 255))
        tela.blit(voltar_surf, (self.botao_voltar_rect.centerx - voltar_surf.get_width() // 2, self.botao_voltar_rect.centery - voltar_surf.get_height() // 2))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                for i, rect in enumerate(self.retangulos_projetos):
                    if rect.collidepoint(evento.pos):
                        self.callback_selecionar(self.projetos[i])
                        return
                if self.botao_voltar_rect.collidepoint(evento.pos):
                    self.callback_voltar()