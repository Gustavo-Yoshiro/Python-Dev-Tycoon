import pygame
from Intermediario.UI.Janela import Janela

class TelaProjeto(Janela):
    def __init__(self, projeto, cliente, callback_aceitar, callback_chat, callback_voltar):
        super().__init__(x=290, y=80, largura=700, altura=550, titulo=f"Oportunidade: {projeto.get_titulo()}")
        
        self.projeto = projeto
        self.cliente = cliente
        self.callback_aceitar = callback_aceitar
        self.callback_chat = callback_chat
        self.callback_voltar = callback_voltar

        # Paleta de Cores e Fontes consistentes com a tela anterior
        self.COR_FUNDO = (245, 245, 245)
        self.COR_TEXTO_TITULO = (10, 10, 10)
        self.COR_TEXTO_CORPO = (80, 80, 80)
        self.COR_BOTAO_PRIMARIO = (0, 130, 0) # Verde para Aceitar
        self.COR_BOTAO_PRIMARIO_HOVER = (0, 150, 0)
        self.COR_BOTAO_SECUNDARIO = (80, 80, 80)
        self.COR_BOTAO_SECUNDARIO_HOVER = (100, 100, 100)
        self.COR_ESTRELA = (255, 190, 0)
        
        self.fonte_h1 = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_h2 = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_corpo = pygame.font.SysFont("Arial", 16)
        self.fonte_tag = pygame.font.SysFont("Arial", 12, bold=True)

        # Retângulos dos botões
        self.botao_aceitar_rect = pygame.Rect(self.rect.width - 220, 40, 200, 45)
        self.botao_chat_rect = pygame.Rect(self.rect.width - 220, 95, 200, 45)
        self.botao_voltar_rect = pygame.Rect(20, self.rect.height - 60, 120, 40)

    def desenhar_conteudo(self, tela):
        area_conteudo = pygame.Rect(self.rect.x, self.rect.y + 30, self.rect.width, self.rect.height - 30)
        pygame.draw.rect(tela, self.COR_FUNDO, area_conteudo)
        mouse_pos = pygame.mouse.get_pos()
        
        # --- Header ---
        titulo_surf = self.fonte_h1.render(self.projeto.get_titulo(), True, self.COR_TEXTO_TITULO)
        tela.blit(titulo_surf, (area_conteudo.x + 20, area_conteudo.y + 20))
        cliente_surf = self.fonte_h2.render(self.cliente.get_nome(), True, self.COR_TEXTO_CORPO)
        tela.blit(cliente_surf, (area_conteudo.x + 20, area_conteudo.y + 55))
        
        # Reputação (Mock)
        mock_reputacao = 4.5 + (self.cliente.get_id_cliente() % 5) / 10.0 
        estrelas = "★" * int(mock_reputacao) + "☆" * (5 - int(mock_reputacao))
        reputacao_surf = self.fonte_corpo.render(f"{mock_reputacao:.1f} {estrelas}", True, self.COR_ESTRELA)
        tela.blit(reputacao_surf, (area_conteudo.x + 20, area_conteudo.y + 85))
        
        # --- Corpo ---
        pygame.draw.line(tela, (220,220,220), (area_conteudo.x + 20, area_conteudo.y + 120), (area_conteudo.right - 20, area_conteudo.y + 120))
        
        # Descrição Completa
        y_desc = area_conteudo.y + 140
        linhas = [self.projeto.get_descricao()[i:i+70] for i in range(0, len(self.projeto.get_descricao()), 70)]
        for linha in linhas:
             linha_surf = self.fonte_corpo.render(linha, True, self.COR_TEXTO_CORPO)
             tela.blit(linha_surf, (area_conteudo.x + 20, y_desc)); y_desc += 22

        # Habilidades (Mock)
        mock_tags = [["Python", "API REST", "Web"], ["SQL", "Database", "Otimização"], ["Automação", "Web Scraping"]]
        tags_do_projeto = mock_tags[self.projeto.get_id_projeto() % len(mock_tags)]
        y_desc += 20 # Espaço
        x_tag = area_conteudo.x + 20
        for tag in tags_do_projeto:
            tag_surf = self.fonte_tag.render(tag, True, (255,255,255))
            tag_rect = tag_surf.get_rect(topleft=(x_tag, y_desc))
            pygame.draw.rect(tela, (80,80,80), tag_rect.inflate(15, 8), border_radius=12)
            tela.blit(tag_surf, tag_rect.move(8, 4))
            x_tag += tag_rect.width + 25

        # --- Botões de Ação ---
        # Botão Aceitar
        aceitar_abs_rect = self.botao_aceitar_rect.move(self.rect.topleft)
        cor_aceitar = self.COR_BOTAO_PRIMARIO_HOVER if aceitar_abs_rect.collidepoint(mouse_pos) else self.COR_BOTAO_PRIMARIO
        pygame.draw.rect(tela, cor_aceitar, aceitar_abs_rect, border_radius=8)
        aceitar_surf = self.fonte_h2.render("Aceitar Contrato", True, (255,255,255))
        tela.blit(aceitar_surf, (aceitar_abs_rect.centerx - aceitar_surf.get_width()/2, aceitar_abs_rect.centery - aceitar_surf.get_height()/2))
        
        # Botão Chat
        chat_abs_rect = self.botao_chat_rect.move(self.rect.topleft)
        cor_chat = self.COR_BOTAO_SECUNDARIO_HOVER if chat_abs_rect.collidepoint(mouse_pos) else self.COR_BOTAO_SECUNDARIO
        pygame.draw.rect(tela, cor_chat, chat_abs_rect, border_radius=8)
        chat_surf = self.fonte_h2.render("Chat com Cliente", True, (255,255,255))
        tela.blit(chat_surf, (chat_abs_rect.centerx - chat_surf.get_width()/2, chat_abs_rect.centery - chat_surf.get_height()/2))

        # Botão Voltar
        voltar_abs_rect = self.botao_voltar_rect.move(self.rect.topleft)
        pygame.draw.rect(tela, (200,200,200), voltar_abs_rect, 1, border_radius=5)
        voltar_surf = self.fonte_corpo.render("Voltar", True, self.COR_TEXTO_CORPO)
        tela.blit(voltar_surf, (voltar_abs_rect.centerx - voltar_surf.get_width()/2, voltar_abs_rect.centery - voltar_surf.get_height()/2))

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_aceitar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_aceitar(self.projeto)
                    self.deve_fechar = True
                elif self.botao_chat_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_chat(self.projeto)
                    self.deve_fechar = True
                elif self.botao_voltar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_voltar()
                    self.deve_fechar = True

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)