import pygame
from Intermediario.UI.Janela import Janela

class TelaResultado(Janela):
    def __init__(self, sucesso, recompensa, callback_continuar):
        super().__init__(x=340, y=235, largura=600, altura=250, titulo="Resultado do Projeto")
        
        self.sucesso = sucesso
        self.recompensa = recompensa
        self.callback_continuar = callback_continuar
        
        self.fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 26)
        self.fonte_botao = pygame.font.SysFont("Arial", 28)
        self.COR_SUCESSO = (30, 150, 30)
        self.COR_FALHA = (180, 30, 30)
        self.COR_PRETO = (0, 0, 0)

        self.botao_continuar_rect = pygame.Rect(self.rect.width // 2 - 100, self.rect.height - 70, 200, 50)

    def desenhar_conteudo(self, tela):
        if self.sucesso:
            cor_titulo = self.COR_SUCESSO
            texto_titulo = "Projeto Concluído!"
            texto_sub = f"Você recebeu: R$ {self.recompensa:.2f}"
        else:
            cor_titulo = self.COR_FALHA
            texto_titulo = "Falha no Projeto"
            texto_sub = "Nenhuma recompensa recebida."

        titulo_surf = self.fonte_titulo.render(texto_titulo, True, cor_titulo)
        tela.blit(titulo_surf, (self.rect.centerx - titulo_surf.get_width() // 2, self.rect.y + 50))
        sub_surf = self.fonte_subtitulo.render(texto_sub, True, self.COR_PRETO)
        tela.blit(sub_surf, (self.rect.centerx - sub_surf.get_width() // 2, self.rect.y + 120))

        # Botão Continuar
        rect_absoluto = self.botao_continuar_rect.move(self.rect.topleft)
        mouse_pos = pygame.mouse.get_pos()
        cor_botao = (100, 100, 100) if rect_absoluto.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(tela, cor_botao, rect_absoluto, border_radius=10)
        cont_surf = self.fonte_botao.render("Continuar", True, (255, 255, 255))
        tela.blit(cont_surf, (rect_absoluto.centerx - cont_surf.get_width() // 2, rect_absoluto.centery - cont_surf.get_height() // 2))

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                rect_absoluto = self.botao_continuar_rect.move(self.rect.topleft)
                if rect_absoluto.collidepoint(evento.pos):
                    self.callback_continuar()
                    self.deve_fechar = True

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)