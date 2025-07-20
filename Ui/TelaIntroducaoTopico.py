import pygame

class TelaIntroducaoTopico:
    def __init__(self, fase, largura=640, altura=600):
        self.fase = fase  # objeto Fase (com get_titulo, get_introducao etc)
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont('Arial', 28)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)
        self.entendido = False
        self.rect_botao = pygame.Rect(largura//2 - 80, altura - 90, 160, 50)

    def desenhar(self, tela):
        tela.fill((35, 38, 55))
        y = 40
        # Título do tópico
        titulo = self.fase.get_titulo() if hasattr(self.fase, 'get_titulo') else f"Tópico: {self.fase.get_topico()}"
        tela.blit(self.fonte.render(str(titulo), True, (0, 200, 255)), (50, y))
        y += 50

        # Introdução (quebra em várias linhas se necessário)
        intro = self.fase.get_introducao() if hasattr(self.fase, 'get_introducao') else str(self.fase)
        linhas = self._quebrar_linhas(intro, self.fonte_pequena, self.largura - 100)
        for linha in linhas:
            tela.blit(self.fonte_pequena.render(linha, True, (230, 230, 230)), (50, y))
            y += 30

        # Botão "Entendi"
        pygame.draw.rect(tela, (0, 200, 120), self.rect_botao, border_radius=18)
        tela.blit(self.fonte_pequena.render("Entendi!", True, (255,255,255)), (self.rect_botao.x+35, self.rect_botao.y+13))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_botao.collidepoint(evento.pos):
                    self.entendido = True

    def _quebrar_linhas(self, texto, fonte, largura_max):
        # Simples quebra de linhas para textos longos
        palavras = texto.split()
        linhas = []
        linha = ""
        for palavra in palavras:
            test = f"{linha} {palavra}".strip()
            if fonte.size(test)[0] < largura_max:
                linha = test
            else:
                linhas.append(linha)
                linha = palavra
        if linha:
            linhas.append(linha)
        return linhas
