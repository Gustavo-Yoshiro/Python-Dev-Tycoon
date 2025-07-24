import pygame

class TelaInicio:
    def __init__(self, largura, altura, callback_iniciar):
        self.largura = largura
        self.altura = altura
        self.callback_iniciar = callback_iniciar
        self.fonte = pygame.font.SysFont('Consolas', 32)
        self.fundo = pygame.image.load("assets/TelaInicio.png")
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        self.botao_iniciar = pygame.Rect(largura // 2 - 100, altura - 150, 200, 60)

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))
        pygame.draw.rect(tela, (0, 180, 80), self.botao_iniciar, border_radius=12)
        texto = self.fonte.render("INICIAR", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=self.botao_iniciar.center)
        tela.blit(texto, texto_rect)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_iniciar.collidepoint(evento.pos):
                    self.callback_iniciar()
