import pygame

class TelaFreelance:
    def __init__(self, largura, altura, projetos, callback_selecionar, callback_voltar):
        self.largura = largura
        self.altura = altura
        self.projetos = projetos  # lista de objetos Projeto
        self.callback_selecionar = callback_selecionar
        self.callback_voltar = callback_voltar
        self.font = pygame.font.SysFont("Arial", 28)

    def desenhar(self, tela):
        tela.fill((240, 240, 240))
        titulo = self.font.render("Projetos Disponíveis", True, (0, 0, 0))
        tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 50))

        for i, projeto in enumerate(self.projetos):
            texto = self.font.render(f"{i+1}. {projeto.titulo} - ${projeto.recompensa}", True, (0, 0, 0))
            tela.blit(texto, (100, 150 + i * 50))

        voltar = self.font.render("0. Voltar", True, (100, 0, 0))
        tela.blit(voltar, (100, self.altura - 100))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_0:
                    self.callback_voltar()
                elif pygame.K_1 <= evento.key <= pygame.K_9:
                    idx = evento.key - pygame.K_1
                    if 0 <= idx < len(self.projetos):
                        self.callback_selecionar(self.projetos[idx])
