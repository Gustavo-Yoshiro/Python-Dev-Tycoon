import pygame
from Intermediario.UI.Janela import Janela

class TelaChatCliente(Janela):
    def __init__(self, projeto, cliente, mensagens, callback_enviar, callback_finalizar):
        super().__init__(x=240, y=80, largura=800, altura=600, titulo=f"Chat com {cliente.get_nome()}")

        self.projeto = projeto
        self.cliente = cliente
        self.mensagens = mensagens
        self.callback_enviar = callback_enviar
        self.callback_finalizar = callback_finalizar

        self.fonte_msg = pygame.font.SysFont("Arial", 18)
        self.fonte_botao = pygame.font.SysFont("Arial", 20)
        self.COR_BALAO_CLIENTE = (255, 255, 255)
        self.COR_BALAO_JOGADOR = (210, 255, 210)
        self.COR_TEXTO = (0, 0, 0)

        self.opcoes_resposta = ["Entendido, vou começar!", "Preciso de mais detalhes.", "O projeto está finalizado."]
        self.botoes_resposta_rect = [pygame.Rect(20 + i * 260, self.rect.height - 70, 250, 45) for i, _ in enumerate(self.opcoes_resposta)]

    def desenhar_conteudo(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        y_offset = 50 # Posição Y relativa ao topo da janela
        
        # Área de Mensagens
        for msg in self.mensagens:
            linhas = [msg.get_mensagem()[i:i+60] for i in range(0, len(msg.get_mensagem()), 60)]
            
            for linha_texto in linhas:
                msg_surf = self.fonte_msg.render(linha_texto, True, self.COR_TEXTO)
                padding = 10
                
                if msg.get_enviado_por().lower() == 'jogador':
                    cor_balao = self.COR_BALAO_JOGADOR
                    x_pos = self.rect.width - msg_surf.get_width() - 2 * padding - 20
                else:
                    cor_balao = self.COR_BALAO_CLIENTE
                    x_pos = 20

                balao_rect = pygame.Rect(self.rect.x + x_pos, self.rect.y + y_offset, msg_surf.get_width() + 2 * padding, msg_surf.get_height() + 2 * padding)
                pygame.draw.rect(tela, cor_balao, balao_rect, border_radius=15)
                tela.blit(msg_surf, (balao_rect.x + padding, balao_rect.y + padding))
                y_offset += msg_surf.get_height() + 5
            y_offset += 15

        # Área de Resposta
        area_resp_rect = pygame.Rect(self.rect.x, self.rect.bottom - 90, self.rect.width, 90)
        pygame.draw.rect(tela, (220, 220, 220), area_resp_rect)

        for i, texto in enumerate(self.opcoes_resposta):
            rect_relativo = self.botoes_resposta_rect[i]
            rect_absoluto = rect_relativo.move(self.rect.topleft)
            cor_botao = (235, 235, 235) if rect_absoluto.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(tela, cor_botao, rect_absoluto, border_radius=10)
            pygame.draw.rect(tela, (180, 180, 180), rect_absoluto, 2, border_radius=10)
            resp_surf = self.fonte_botao.render(texto, True, self.COR_TEXTO)
            tela.blit(resp_surf, (rect_absoluto.centerx - resp_surf.get_width()//2, rect_absoluto.centery - resp_surf.get_height()//2))

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                for i, rect_relativo in enumerate(self.botoes_resposta_rect):
                    rect_absoluto = rect_relativo.move(self.rect.topleft)
                    if rect_absoluto.collidepoint(evento.pos):
                        texto_resposta = self.opcoes_resposta[i]
                        if texto_resposta == "O projeto está finalizado.":
                            self.callback_finalizar(self.projeto)
                            self.deve_fechar = True
                        else:
                            self.callback_enviar(self.projeto, texto_resposta)
                        return

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)