import pygame
from Intermediario.UI.Janela import Janela

class TelaProjeto(Janela):
    def __init__(self, largura_tela, altura_tela, projeto, cliente, jogador, 
                 callback_aceitar, callback_voltar):
        
        painel_w = int(largura_tela * 0.65)
        painel_h = int(altura_tela * 0.75)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, 
                         titulo=f"[ Análise de Contrato ]: {projeto.get_titulo()}")
        
        self.cor_fundo = (28, 34, 42)
        self.cor_borda = (255, 190, 0)
        self.cor_titulo_bg = (18, 24, 32)

        self.projeto = projeto
        self.cliente = cliente
        self.jogador = jogador # Precisamos do jogador para comparar as skills
        self.callback_aceitar = callback_aceitar
        self.callback_voltar = callback_voltar

        # Paleta de Cores e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0) # Dourado
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255) # Ciano
        self.COR_TEXTO_CORPO = (200, 200, 200)
        self.COR_BOTAO_ACEITAR = (0, 180, 80)
        self.COR_BOTAO_ACEITAR_HOVER = (0, 210, 100)
        self.COR_BOTAO_VOLTAR = (100, 100, 100)
        self.COR_BOTAO_VOLTAR_HOVER = (120, 120, 120)
        self.COR_SKILL_JOGADOR = (0, 150, 200)
        self.COR_SKILL_REQUISITO = (80, 80, 80)
        
        self.fonte_h1 = pygame.font.SysFont('Consolas', 24, bold=True)
        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_corpo = pygame.font.SysFont('Consolas', 16)
        self.fonte_tag = pygame.font.SysFont('Consolas', 14, bold=True)
        self.fonte_logo = pygame.font.SysFont('Consolas', 36, bold=True)

        self.botao_aceitar_rect = pygame.Rect(self.rect.width - 220, self.rect.height - 70, 200, 50)
        self.botao_voltar_rect = pygame.Rect(20, self.rect.height - 70, 150, 50)

    def desenhar_texto_quebra_linha(self, tela, texto, rect, fonte, cor):
        # ... (código da função de quebra de linha)
        palavras = texto.split(' '); linhas = []; linha_atual = ''
        for palavra in palavras:
            if fonte.size(linha_atual + ' ' + palavra)[0] < rect.width: linha_atual += ' ' + palavra
            else: linhas.append(linha_atual.strip()); linha_atual = palavra
        linhas.append(linha_atual.strip())
        y = rect.y
        for linha in linhas:
            if y + fonte.get_height() > rect.bottom: break
            linha_surf = fonte.render(linha, True, cor); tela.blit(linha_surf, (rect.x, y)); y += fonte.get_height()

    def _desenhar_barra_skill(self, tela, x, y, largura, label, nivel_jogador, nivel_req):
        """Desenha uma barra de comparação de skills."""
        label_surf = self.fonte_corpo.render(label, True, self.COR_TEXTO_CORPO)
        tela.blit(label_surf, (x, y))
        
        barra_bg_rect = pygame.Rect(x, y + 25, largura, 20)
        pygame.draw.rect(tela, (10, 12, 15), barra_bg_rect, border_radius=5)
        
        # Barra de requisito (fundo)
        largura_req = (nivel_req / 10) * largura # Supondo que o nível máximo é 10
        req_rect = pygame.Rect(x, y + 25, min(largura_req, largura), 20)
        pygame.draw.rect(tela, self.COR_SKILL_REQUISITO, req_rect, border_radius=5)

        # Barra do jogador (frente)
        largura_jogador = (nivel_jogador / 10) * largura
        jogador_rect = pygame.Rect(x, y + 25, min(largura_jogador, largura), 20)
        cor_jogador = self.COR_SKILL_JOGADOR if nivel_jogador >= nivel_req else (180, 40, 40)
        pygame.draw.rect(tela, cor_jogador, jogador_rect, border_radius=5)
        
        nivel_surf = self.fonte_tag.render(f"{nivel_jogador}/{nivel_req}", True, (255,255,255))
        tela.blit(nivel_surf, (x + 5, y + 27))

    def desenhar_conteudo(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        
        # --- Painel Esquerdo: Cliente e Descrição ---
        painel_esquerdo_w = int(self.rect.width * 0.55)
        
        # Cliente
        cliente_surf = self.fonte_h1.render(f"// Cliente: {self.cliente.get_nome()}", True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(cliente_surf, (self.rect.x + 20, self.rect.y + 40))
        
        # Descrição
        desc_label_surf = self.fonte_h2.render("Briefing do Contrato:", True, self.COR_TEXTO_CORPO)
        tela.blit(desc_label_surf, (self.rect.x + 20, self.rect.y + 90))
        desc_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 120, painel_esquerdo_w - 40, self.rect.height - 220)
        self.desenhar_texto_quebra_linha(tela, self.projeto.get_descricao(), desc_rect, self.fonte_corpo, self.COR_TEXTO_CORPO)

        # --- Painel Direito: Dados e Requisitos ---
        painel_direito_x = self.rect.x + painel_esquerdo_w + 20
        pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (painel_direito_x - 10, self.rect.y + 40), (painel_direito_x - 10, self.rect.bottom - 90))

        # Recompensa e Prazo
        recompensa_label = self.fonte_h2.render("Pagamento:", True, self.COR_TEXTO_CORPO)
        tela.blit(recompensa_label, (painel_direito_x, self.rect.y + 40))
        recompensa_valor = self.fonte_h1.render(f"R$ {self.projeto.get_recompensa():.2f}", True, (0, 220, 120))
        tela.blit(recompensa_valor, (painel_direito_x, self.rect.y + 65))

        prazo_label = self.fonte_h2.render("Prazo:", True, self.COR_TEXTO_CORPO)
        tela.blit(prazo_label, (painel_direito_x, self.rect.y + 120))
        prazo_valor = self.fonte_h1.render(f"{self.projeto.get_prazo_dias()} dias", True, self.COR_TEXTO_CORPO)
        tela.blit(prazo_valor, (painel_direito_x, self.rect.y + 145))
        
        # Requisitos de Skill
        req_label = self.fonte_h2.render("Requisitos de Skill:", True, self.COR_TEXTO_CORPO)
        tela.blit(req_label, (painel_direito_x, self.rect.y + 210))
        
        barra_w = self.rect.width - painel_esquerdo_w - 60
        self._desenhar_barra_skill(tela, painel_direito_x, self.rect.y + 240, barra_w, "Backend:", self.jogador.get_backend(), self.projeto.get_req_backend())
        self._desenhar_barra_skill(tela, painel_direito_x, self.rect.y + 300, barra_w, "Frontend:", self.jogador.get_frontend(), self.projeto.get_req_frontend())
        self._desenhar_barra_skill(tela, painel_direito_x, self.rect.y + 360, barra_w, "Social:", self.jogador.get_social(), self.projeto.get_req_social())

        # --- Rodapé de Ações ---
        rodape_y = self.rect.bottom - 90
        pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (self.rect.x + 20, rodape_y), (self.rect.right - 20, rodape_y), 1)
        
        voltar_abs = self.botao_voltar_rect.move(self.rect.topleft)
        aceitar_abs = self.botao_aceitar_rect.move(self.rect.topleft)
        
        cor_voltar = self.COR_BOTAO_VOLTAR_HOVER if voltar_abs.collidepoint(mouse_pos) else self.COR_BOTAO_VOLTAR
        pygame.draw.rect(tela, cor_voltar, voltar_abs, border_radius=8)
        voltar_surf = self.fonte_h2.render("Voltar", True, (255,255,255))
        tela.blit(voltar_surf, (voltar_abs.centerx - voltar_surf.get_width()/2, voltar_abs.centery - voltar_surf.get_height()/2))

        cor_aceitar = self.COR_BOTAO_ACEITAR_HOVER if aceitar_abs.collidepoint(mouse_pos) else self.COR_BOTAO_ACEITAR
        pygame.draw.rect(tela, cor_aceitar, aceitar_abs, border_radius=8)
        aceitar_surf = self.fonte_h2.render("Aceitar Contrato", True, (255,255,255))
        tela.blit(aceitar_surf, (aceitar_abs.centerx - aceitar_surf.get_width()/2, aceitar_abs.centery - aceitar_surf.get_height()/2))

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_aceitar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    # A lógica de checagem de skills agora está no GameManager
                    self.callback_aceitar(self.projeto)
                    self.deve_fechar = True
                elif self.botao_voltar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_voltar()
                    self.deve_fechar = True

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)
