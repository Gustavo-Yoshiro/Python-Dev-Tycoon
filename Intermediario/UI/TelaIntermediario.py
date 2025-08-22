import pygame
from Intermediario.UI.Janela import Janela

class TelaIntermediario(Janela):
    def __init__(self, callback_exercicios, callback_freelancer, callback_loja):
        super().__init__(x=440, y=210, largura=400, altura=300, titulo="Menu Principal")

        self.callbacks = {
            "Exercícios": callback_exercicios,
            "Freelance": callback_freelancer,
            "Loja": callback_loja
        }
        self.fonte_botao = pygame.font.SysFont("Arial", 28, bold=True)
        
        # Posições relativas ao interior da janela
        self.botoes_rect_relativos = {
            "Exercícios": pygame.Rect(50, 50, 300, 50),
            "Freelance": pygame.Rect(50, 120, 300, 50),
            "Loja": pygame.Rect(50, 190, 300, 50),
        }

    def desenhar_conteudo(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        for texto, rect_relativo in self.botoes_rect_relativos.items():
            rect_absoluto = rect_relativo.move(self.rect.topleft)
            
            cor = (0, 150, 255) if rect_absoluto.collidepoint(mouse_pos) else (0, 122, 200)
            pygame.draw.rect(tela, cor, rect_absoluto, border_radius=10)
            
            render_texto = self.fonte_botao.render(texto, True, (255, 255, 255))
            tela.blit(render_texto, (rect_absoluto.centerx - render_texto.get_width() // 2, rect_absoluto.centery - render_texto.get_height() // 2))

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                for texto, rect_relativo in self.botoes_rect_relativos.items():
                    rect_absoluto = rect_relativo.move(self.rect.topleft)
                    if rect_absoluto.collidepoint(evento.pos):
                        self.callbacks[texto]()
                        self.deve_fechar = True # Fecha o menu após a seleção
                        return

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)