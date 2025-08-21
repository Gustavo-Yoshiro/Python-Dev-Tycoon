import pygame

class TelaProjeto:
    def __init__(self, largura, altura, projeto, cliente, callback_aceitar, callback_voltar):
        self.largura, self.altura = largura, altura
        self.projeto = projeto
        self.cliente = cliente
        self.callback_aceitar = callback_aceitar
        self.callback_voltar = callback_voltar
        self.fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
        self.fonte_texto = pygame.font.SysFont("Arial", 24)
        self.fonte_label = pygame.font.SysFont("Arial", 22, bold=True)
        self.botao_aceitar_rect = pygame.Rect(self.largura - 350, self.altura - 80, 150, 50)
        self.botao_voltar_rect = pygame.Rect(self.largura - 180, self.altura - 80, 150, 50)

    def desenhar(self, tela):
        tela.fill((230, 240, 255))
        titulo_surf = self.fonte_titulo.render(self.projeto.get_titulo(), True, (10, 10, 10))
        tela.blit(titulo_surf, (50, 50))
        
        # Bloco de Descrição
        desc_label = self.fonte_label.render("Descrição:", True, (50, 50, 50))
        tela.blit(desc_label, (50, 120))
        desc_surf = self.fonte_texto.render(self.projeto.get_descricao(), True, (30, 30, 30))
        tela.blit(desc_surf, (50, 150))

        # Detalhes
        recompensa_surf = self.fonte_texto.render(f"Recompensa: R$ {self.projeto.get_recompensa():.2f}", True, (0, 100, 0))
        tela.blit(recompensa_surf, (50, 220))
        dificuldade_surf = self.fonte_texto.render(f"Dificuldade: {self.projeto.get_dificuldade()}", True, (30, 30, 30))
        tela.blit(dificuldade_surf, (50, 260))

        # Cliente
        cliente_label = self.fonte_label.render("Cliente:", True, (50, 50, 50))
        tela.blit(cliente_label, (50, 330))
        cliente_nome = self.cliente.get_nome() if self.cliente else "Desconhecido"
        cliente_surf = self.fonte_texto.render(cliente_nome, True, (30, 30, 30))
        tela.blit(cliente_surf, (50, 360))

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        cor_aceitar = (0, 180, 100) if self.botao_aceitar_rect.collidepoint(mouse_pos) else (0, 150, 80)
        cor_voltar = (220, 60, 60) if self.botao_voltar_rect.collidepoint(mouse_pos) else (200, 40, 40)
        pygame.draw.rect(tela, cor_aceitar, self.botao_aceitar_rect, border_radius=8)
        pygame.draw.rect(tela, cor_voltar, self.botao_voltar_rect, border_radius=8)
        
        aceitar_surf = self.fonte_texto.render("Aceitar", True, (255, 255, 255))
        tela.blit(aceitar_surf, (self.botao_aceitar_rect.centerx - aceitar_surf.get_width()//2, self.botao_aceitar_rect.centery - aceitar_surf.get_height()//2))
        voltar_surf = self.fonte_texto.render("Voltar", True, (255, 255, 255))
        tela.blit(voltar_surf, (self.botao_voltar_rect.centerx - voltar_surf.get_width()//2, self.botao_voltar_rect.centery - voltar_surf.get_height()//2))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_aceitar_rect.collidepoint(evento.pos):
                    self.callback_aceitar(self.projeto)
                elif self.botao_voltar_rect.collidepoint(evento.pos):
                    self.callback_voltar()