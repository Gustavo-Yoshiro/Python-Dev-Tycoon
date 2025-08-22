import pygame

class TelaIntermediario:
    def __init__(self, largura, altura, callback_exercicios, callback_freelancer, callback_loja):
        self.largura = largura
        self.altura = altura
        self.callbacks = {
            "Exercícios": callback_exercicios,
            "Freelance": callback_freelancer,
            "Loja": callback_loja
        }
        self.fonte = pygame.font.SysFont("Arial", 32, bold=True)
        self.botoes_rect = {
            "Exercícios": pygame.Rect(largura // 2 - 150, altura // 2 - 100, 300, 60),
            "Freelance": pygame.Rect(largura // 2 - 150, altura // 2, 300, 60),
            "Loja": pygame.Rect(largura // 2 - 150, altura // 2 + 100, 300, 60),
        }

    def desenhar(self, tela):
        # Fundo do jogo (quarto) deve ser desenhado antes desta tela
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        for texto, rect in self.botoes_rect.items():
            cor = (0, 150, 255) if rect.collidepoint(mouse_pos) else (0, 122, 200)
            pygame.draw.rect(tela, cor, rect, border_radius=12)
            pygame.draw.rect(tela, (255, 255, 255), rect, 3, border_radius=12)
            
            render_texto = self.fonte.render(texto, True, (255, 255, 255))
            tela.blit(render_texto, (rect.centerx - render_texto.get_width() // 2, rect.centery - render_texto.get_height() // 2))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                for texto, rect in self.botoes_rect.items():
                    if rect.collidepoint(evento.pos):
                        self.callbacks[texto]() # Chama o callback correspondente
                        break