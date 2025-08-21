import pygame

class TelaIntermediario:
    def __init__(self, largura, altura, callback_exercicios, callback_freelancer, callback_loja):
        self.largura = largura
        self.altura = altura
        self.callback_exercicios = callback_exercicios
        self.callback_freelancer = callback_freelancer
        self.callback_loja = callback_loja

        # Fonte
        self.fonte = pygame.font.SysFont("arial", 28)

        # Definição dos botões
        self.botoes = {
            "Exercícios": pygame.Rect(largura // 2 - 100, altura // 2 - 80, 200, 50),
            "Freelance": pygame.Rect(largura // 2 - 100, altura // 2, 200, 50),
            "Loja": pygame.Rect(largura // 2 - 100, altura // 2 + 80, 200, 50),
        }

    def desenhar(self, tela):
        # Fundo invisível com leve escurecimento
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Preto com 150 de opacidade
        tela.blit(overlay, (0, 0))

        # Caixa central semi-transparente
        caixa = pygame.Surface((400, 300), pygame.SRCALPHA)
        caixa.fill((255, 255, 255, 200))  # Branco com transparência
        tela.blit(caixa, (self.largura // 2 - 200, self.altura // 2 - 150))

        # Desenhar os botões
        for texto, rect in self.botoes.items():
            pygame.draw.rect(tela, (50, 50, 200), rect, border_radius=12)
            pygame.draw.rect(tela, (255, 255, 255), rect, 3, border_radius=12)

            render = self.fonte.render(texto, True, (255, 255, 255))
            tela.blit(render, (rect.centerx - render.get_width() // 2, rect.centery - render.get_height() // 2))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = pygame.mouse.get_pos()

                if self.botoes["Exercícios"].collidepoint(pos):
                    self.callback_exercicios()

                elif self.botoes["Freelance"].collidepoint(pos):
                    self.callback_freelancer()

                elif self.botoes["Loja"].collidepoint(pos):
                    self.callback_loja()
