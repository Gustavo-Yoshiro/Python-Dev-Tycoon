import pygame

class TelaChatCliente:
    def __init__(self, largura, altura, projeto, cliente, mensagens, callback_enviar, callback_finalizar, callback_voltar):
        self.largura, self.altura = largura, altura
        self.projeto = projeto
        self.cliente = cliente
        self.mensagens = mensagens  # Lista de objetos ChatCliente
        self.callback_enviar = callback_enviar
        self.callback_finalizar = callback_finalizar
        self.callback_voltar = callback_voltar

        # --- Configurações Visuais ---
        self.fonte_titulo = pygame.font.SysFont("Arial", 32, bold=True)
        self.fonte_msg = pygame.font.SysFont("Arial", 20)
        self.fonte_botao = pygame.font.SysFont("Arial", 22)
        
        self.COR_FUNDO = (225, 225, 210)
        self.COR_BALAO_CLIENTE = (255, 255, 255)
        self.COR_BALAO_JOGADOR = (210, 255, 210)
        self.COR_TEXTO = (0, 0, 0)

        # --- Respostas Pré-definidas ---
        self.opcoes_resposta = [
            "Entendido, vou começar!",
            "Preciso de mais detalhes.",
            "O projeto está finalizado."
        ]
        self.botoes_resposta_rect = []
        base_y = self.altura - 120
        for i, _ in enumerate(self.opcoes_resposta):
            rect = pygame.Rect(50 + i * 270, base_y, 250, 50)
            self.botoes_resposta_rect.append(rect)
            
        # --- Botões de Ação ---
        self.botao_voltar_rect = pygame.Rect(self.largura - 170, 20, 150, 40)

    def desenhar(self, tela):
        tela.fill(self.COR_FUNDO)
        mouse_pos = pygame.mouse.get_pos()

        # --- Título ---
        nome_cliente = self.cliente.get_nome() if self.cliente else "Cliente"
        titulo_surf = self.fonte_titulo.render(f"Chat com {nome_cliente}", True, self.COR_TEXTO)
        tela.blit(titulo_surf, (50, 30))

        # --- Botão Voltar ---
        cor_voltar = (220, 60, 60) if self.botao_voltar_rect.collidepoint(mouse_pos) else (200, 40, 40)
        pygame.draw.rect(tela, cor_voltar, self.botao_voltar_rect, border_radius=8)
        voltar_surf = self.fonte_botao.render("Voltar", True, (255, 255, 255))
        tela.blit(voltar_surf, (self.botao_voltar_rect.centerx - voltar_surf.get_width()//2, self.botao_voltar_rect.centery - voltar_surf.get_height()//2))

        # --- Área de Mensagens ---
        y_offset = 100
        for msg in self.mensagens:
            # Quebra de linha simples (melhorias podem ser feitas aqui)
            linhas = [msg.get_mensagem()[i:i+80] for i in range(0, len(msg.get_mensagem()), 80)]
            
            for linha_texto in linhas:
                msg_surf = self.fonte_msg.render(linha_texto, True, self.COR_TEXTO)
                padding = 10
                
                if msg.get_enviado_por().lower() == 'jogador':
                    cor_balao = self.COR_BALAO_JOGADOR
                    x_pos = self.largura - msg_surf.get_width() - 2 * padding - 50
                else: # Enviado pelo cliente
                    cor_balao = self.COR_BALAO_CLIENTE
                    x_pos = 50

                balao_rect = pygame.Rect(x_pos, y_offset, msg_surf.get_width() + 2 * padding, msg_surf.get_height() + 2 * padding)
                pygame.draw.rect(tela, cor_balao, balao_rect, border_radius=15)
                tela.blit(msg_surf, (balao_rect.x + padding, balao_rect.y + padding))
                y_offset += msg_surf.get_height() + 5
            
            y_offset += 15 # Espaço entre mensagens

        # --- Área de Resposta ---
        pygame.draw.rect(tela, (240, 240, 240), (0, self.altura - 150, self.largura, 150))
        for i, texto in enumerate(self.opcoes_resposta):
            rect = self.botoes_resposta_rect[i]
            cor_botao = (220, 220, 220) if rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(tela, cor_botao, rect, border_radius=10)
            pygame.draw.rect(tela, (180, 180, 180), rect, 2, border_radius=10)
            
            resp_surf = self.fonte_botao.render(texto, True, self.COR_TEXTO)
            tela.blit(resp_surf, (rect.centerx - resp_surf.get_width()//2, rect.centery - resp_surf.get_height()//2))
            
    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                # Checa cliques nos botões de resposta
                for i, rect in enumerate(self.botoes_resposta_rect):
                    if rect.collidepoint(evento.pos):
                        texto_resposta = self.opcoes_resposta[i]
                        if texto_resposta == "O projeto está finalizado.":
                            self.callback_finalizar(self.projeto)
                        else:
                            self.callback_enviar(self.projeto, texto_resposta)
                        return # Sai após tratar um clique
                        
                # Checa clique no botão voltar
                if self.botao_voltar_rect.collidepoint(evento.pos):
                    self.callback_voltar()