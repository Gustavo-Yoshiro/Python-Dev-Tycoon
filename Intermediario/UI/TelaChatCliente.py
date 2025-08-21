import pygame

class TelaChatCliente:
    def __init__(self, largura, altura, cliente, mensagens, callback_responder, callback_sair):
        self.largura = largura
        self.altura = altura
        self.cliente = cliente
        self.mensagens = mensagens  # lista de tuplas (remetente, texto)
        self.callback_responder = callback_responder
        self.callback_sair = callback_sair
        self.font = pygame.font.SysFont("Arial", 24)

    def desenhar(self, tela):
        tela.fill((255, 255, 240))
        y = 50
        for remetente, texto in self.mensagens:
            msg = self.font.render(f"{remetente}: {texto}", True, (0, 0, 0))
            tela.blit(msg, (50, y))
            y += 40

        instr = self.font.render("Digite sua resposta no console ou pressione ESC para sair", True, (150, 0, 0))
        tela.blit(instr, (50, self.altura - 50))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.callback_sair()
