import pygame

class TelaResultado:
    def __init__(self, largura, altura, sucesso, recompensa, callback_continuar):
        self.largura = largura
        self.altura = altura
        self.sucesso = sucesso
        self.recompensa = recompensa
        self.callback_continuar = callback_continuar
        self.font = pygame.font.SysFont("Arial", 32)

    def desenhar(self, tela):
        tela.fill((230, 230, 250))
        if self.sucesso:
            msg = self.font.render(f"Projeto concluído com sucesso! +${self.recompensa}", True, (0, 150, 0))
        else:
            msg = self.font.render("Falha no projeto! Nenhuma recompensa.", True, (200, 0, 0))

        tela.blit(msg, (self.largura // 2 - msg.get_width() // 2, self.altura // 2 - msg.get_height() // 2))

        cont = self.font.render("Pressione qualquer tecla para continuar", True, (0, 0, 0))
        tela.blit(cont, (self.largura // 2 - cont.get_width() // 2, self.altura // 2 + 60))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.callback_continuar()
