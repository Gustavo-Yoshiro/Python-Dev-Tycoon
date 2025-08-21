import pygame

class TelaProjeto:
    def __init__(self, largura, altura, projeto, callback_aceitar, callback_voltar):
        self.largura = largura
        self.altura = altura
        self.projeto = projeto
        self.callback_aceitar = callback_aceitar
        self.callback_voltar = callback_voltar
        self.font = pygame.font.SysFont("Arial", 28)

    def desenhar(self, tela):
        tela.fill((220, 250, 220))
        titulo = self.font.render(f"Projeto: {self.projeto.titulo}", True, (0, 0, 0))
        tela.blit(titulo, (50, 50))

        desc = self.font.render(self.projeto.descricao, True, (50, 50, 50))
        tela.blit(desc, (50, 120))

        recompensa = self.font.render(f"Recompensa: ${self.projeto.recompensa}", True, (0, 100, 0))
        tela.blit(recompensa, (50, 200))

        aceitar = self.font.render("1. Aceitar Projeto", True, (0, 0, 150))
        voltar = self.font.render("0. Voltar", True, (150, 0, 0))
        tela.blit(aceitar, (50, 300))
        tela.blit(voltar, (50, 360))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    self.callback_aceitar(self.projeto)
                elif evento.key == pygame.K_0:
                    self.callback_voltar()
