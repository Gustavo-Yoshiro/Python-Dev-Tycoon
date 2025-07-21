import pygame

class TelaIntroducaoTopico:
    def __init__(self, largura, altura, nome_topico, descricao, on_confirmar):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.descricao = descricao
        self.on_confirmar = on_confirmar

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 34, bold=True)
        self.fonte = pygame.font.SysFont('Arial', 24)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)
        self.rect_confirmar = pygame.Rect(largura // 2 - 70, altura - 110, 140, 50)

    def desenhar(self, tela):
        tela.fill((35, 35, 55))
        tela.blit(self.fonte_titulo.render(f"Tópico: {self.nome_topico}", True, (0, 210, 255)), (60, 40))
        # Quebrar a descrição em linhas de até 60 caracteres
        descricao = self.descricao
        linhas = []
        while len(descricao) > 0:
            if len(descricao) > 60:
                idx = descricao.rfind(' ', 0, 60)
                if idx == -1: idx = 60
                linhas.append(descricao[:idx])
                descricao = descricao[idx:].lstrip()
            else:
                linhas.append(descricao)
                break
        y = 110
        for linha in linhas:
            tela.blit(self.fonte_pequena.render(linha, True, (255,255,255)), (60, y))
            y += 32

        tela.blit(self.fonte_pequena.render("Leia com atenção a introdução acima.", True, (255,255,100)), (60, y+8))
        # Botão
        pygame.draw.rect(tela, (0, 170, 80), self.rect_confirmar)
        tela.blit(self.fonte_pequena.render("ENTENDI!", True, (255,255,255)), (self.rect_confirmar.x+22, self.rect_confirmar.y+14))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_confirmar.collidepoint(x, y):
                    if self.on_confirmar:
                        self.on_confirmar()
