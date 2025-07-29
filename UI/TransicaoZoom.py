import pygame

class TransicaoZoom:
    def __init__(self, largura, altura, imagem_origem, callback_fim_zoom):
        self.largura = largura
        self.altura = altura
        self.imagem_origem = imagem_origem
        self.callback_fim_zoom = callback_fim_zoom
        self.progresso = 0
        self.velocidade_zoom = 0.02  # velocidade do zoom
        self.zoom_concluido = False

        # Definindo o retângulo da área do monitor (ajustável)
        self.monitor_rect = pygame.Rect(420, 200, 1080, 610)  # estimado com base na imagem

    def desenhar(self, tela):
        if self.zoom_concluido:
            return

        self.progresso += self.velocidade_zoom
        if self.progresso >= 1.0:
            self.progresso = 1.0
            self.zoom_concluido = True
            self.callback_fim_zoom()
            return

        # Interpolação para efeito de zoom
        zoom_rect = self.monitor_rect.inflate(
            self.monitor_rect.width * self.progresso,
            self.monitor_rect.height * self.progresso
        )

        # Ajustar posição para manter centralizado
        zoom_rect.center = self.monitor_rect.center

        # Recortar e aplicar o zoom na tela
        subimagem = self.imagem_origem.subsurface(self.monitor_rect).copy()
        imagem_zoom = pygame.transform.smoothscale(subimagem, (zoom_rect.width, zoom_rect.height))

        # Preencher fundo de preto e desenhar zoom centralizado
        tela.fill((0, 0, 0))
        tela.blit(imagem_zoom, imagem_zoom.get_rect(center=(self.largura // 2, self.altura // 2)))

