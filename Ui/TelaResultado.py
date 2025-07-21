import pygame

class TelaResultado:
    def __init__(self, largura, altura, acertos, erros, total_questoes, callback_avancar, callback_reiniciar=None, acertou_minimo=True):
        self.largura = largura
        self.altura = altura
        self.acertos = acertos
        self.erros = erros
        self.total_questoes = total_questoes
        self.callback_avancar = callback_avancar
        self.callback_reiniciar = callback_reiniciar
        self.acertou_minimo = acertou_minimo

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 38, bold=True)
        self.fonte = pygame.font.SysFont('Arial', 26)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)

        # Botões
        self.rect_avancar = pygame.Rect(largura//2-120, 400, 110, 48)
        self.rect_reiniciar = pygame.Rect(largura//2+20, 400, 110, 48)

        # Feedback
        self.parabens = acertos >= total_questoes * 0.7

    def desenhar(self, tela):
        tela.fill((20, 30, 50))

        # Título
        if self.acertou_minimo:
            titulo = "Parabéns!"
            cor_titulo = (80, 255, 120)
        else:
            titulo = "Você concluiu o tópico!"
            cor_titulo = (255, 230, 70)
        tela.blit(self.fonte_titulo.render(titulo, True, cor_titulo), (self.largura//2 - 180, 80))

        # Placar
        placar = f"Acertos: {self.acertos} / {self.total_questoes}"
        tela.blit(self.fonte.render(placar, True, (255,255,255)), (self.largura//2 - 110, 170))

        erros = f"Erros: {self.erros}"
        tela.blit(self.fonte.render(erros, True, (255, 80, 80)), (self.largura//2 - 110, 210))

        # Mensagem de motivação
        if self.acertou_minimo:
            tela.blit(self.fonte_pequena.render("Ótimo desempenho! Você pode avançar para o próximo tópico.", True, (200,255,200)), (self.largura//2 - 170, 260))
        else:
            tela.blit(self.fonte_pequena.render("Não foi dessa vez. Tente novamente para avançar!", True, (255,180,80)), (self.largura//2 - 170, 260))

        # Botão AVANÇAR só se acertou_minimo
        cor_btn = (0, 180, 80) if self.acertou_minimo else (90, 90, 90)
        pygame.draw.rect(tela, cor_btn, self.rect_avancar)
        cor_text = (255,255,255) if self.acertou_minimo else (180,180,180)
        tela.blit(self.fonte_pequena.render("AVANÇAR", True, cor_text), (self.rect_avancar.x + 10, self.rect_avancar.y + 12))

        # Botão TENTAR DE NOVO sempre habilitado
        pygame.draw.rect(tela, (100, 100, 250), self.rect_reiniciar)
        tela.blit(self.fonte_pequena.render("TENTAR DE NOVO", True, (255,255,255)), (self.rect_reiniciar.x + 3, self.rect_reiniciar.y + 12))


    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Só permite avançar se acertou o mínimo
                if self.rect_avancar.collidepoint(x, y) and self.acertou_minimo:
                    if self.callback_avancar:
                        self.callback_avancar()
                if self.rect_reiniciar.collidepoint(x, y):
                    if self.callback_reiniciar:
                        self.callback_reiniciar()
