import pygame
from Intermediario.UI.Janela import Janela

class TelaFreelance(Janela):
    def __init__(self, projetos, cliente_service, callback_ver_detalhes):
        super().__init__(x=240, y=60, largura=800, altura=600, titulo="DevConnect - Encontre seu próximo desafio")

        self.projetos = sorted(projetos, key=lambda p: p.get_id_projeto(), reverse=True)
        self.cliente_service = cliente_service
        self.callback_ver_detalhes = callback_ver_detalhes

        # --- Paleta de Cores e Fontes (sem alterações) ---
        self.COR_FUNDO = (245, 245, 245)
        self.COR_CARD = (255, 255, 255)
        self.COR_BORDA_CARD = (220, 220, 220)
        self.COR_TEXTO_TITULO = (30, 30, 30)
        self.COR_TEXTO_CORPO = (80, 80, 80)
        self.COR_BOTAO = (0, 122, 255)
        self.COR_BOTAO_HOVER = (0, 100, 210)
        self.CORES_LOGO = [(60,80,120), (180,60,60), (60,120,80), (180,140,60)]

        self.fonte_h2 = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_corpo = pygame.font.SysFont("Arial", 16)
        self.fonte_logo = pygame.font.SysFont("Arial", 32, bold=True)
        
        # --- ATUALIZAÇÃO: Lógica de Rolagem (Scrollbar) ---
        self.scroll_offset = 0
        self.card_altura = 130
        self.max_visiveis = 4 # 4 cards de 130 cabem bem
        
        # Elementos do Scrollbar
        self.scrollbar_track_rect = pygame.Rect(self.rect.width - 25, 45, 15, self.rect.height - 100)
        self.scrollbar_handle_rect = pygame.Rect(self.scrollbar_track_rect.x, self.scrollbar_track_rect.y, 15, 50)
        self.botao_scroll_up = pygame.Rect(self.scrollbar_track_rect.x, 30, 15, 15)
        self.botao_scroll_down = pygame.Rect(self.scrollbar_track_rect.x, self.scrollbar_track_rect.bottom + 5, 15, 15)
        self.dragging_scrollbar = False
        self.drag_offset_y = 0

        self.botoes_detalhes = {}
        self.cache_clientes = {}
        self.atualizar_handle_scrollbar() # Calcula a posição/tamanho inicial do handle

    def _get_cliente(self, cliente_id):
        # ... (sem alterações)
        if cliente_id not in self.cache_clientes:
            self.cache_clientes[cliente_id] = self.cliente_service.buscar_cliente_por_id(cliente_id)
        return self.cache_clientes[cliente_id]

    # --- NOVOS MÉTODOS PARA O SCROLLBAR ---
    def atualizar_handle_scrollbar(self):
        """Calcula o tamanho e a posição do handle com base no scroll_offset."""
        if not self.projetos or len(self.projetos) <= self.max_visiveis:
            self.scrollbar_handle_rect.height = self.scrollbar_track_rect.height
            self.scrollbar_handle_rect.y = self.scrollbar_track_rect.y
            return

        # Calcula o tamanho do handle
        view_ratio = self.max_visiveis / len(self.projetos)
        handle_height = self.scrollbar_track_rect.height * view_ratio
        self.scrollbar_handle_rect.height = max(handle_height, 20) # Tamanho mínimo de 20px

        # Calcula a posição do handle
        max_scroll = len(self.projetos) - self.max_visiveis
        scroll_ratio = self.scroll_offset / max_scroll
        scrollable_space = self.scrollbar_track_rect.height - self.scrollbar_handle_rect.height
        self.scrollbar_handle_rect.y = self.scrollbar_track_rect.y + scrollable_space * scroll_ratio

    def _desenhar_scrollbar(self, tela):
        """Desenha todos os componentes do scrollbar."""
        if len(self.projetos) <= self.max_visiveis:
            return # Não desenha o scroll se não for necessário

        # Track
        pygame.draw.rect(tela, (220, 220, 220), self.scrollbar_track_rect.move(self.rect.topleft), border_radius=7)
        # Handle
        pygame.draw.rect(tela, (150, 150, 150), self.scrollbar_handle_rect.move(self.rect.topleft), border_radius=7)
        # Setas
        pygame.draw.rect(tela, (200, 200, 200), self.botao_scroll_up.move(self.rect.topleft), border_radius=3)
        pygame.draw.rect(tela, (200, 200, 200), self.botao_scroll_down.move(self.rect.topleft), border_radius=3)

    def desenhar_conteudo(self, tela):
        area_conteudo = pygame.Rect(self.rect.x, self.rect.y + 30, self.rect.width, self.rect.height - 30)
        pygame.draw.rect(tela, self.COR_FUNDO, area_conteudo)
        
        mouse_pos = pygame.mouse.get_pos()
        self.botoes_detalhes.clear()
        projetos_visiveis = self.projetos[self.scroll_offset : self.scroll_offset + self.max_visiveis]
        
        for i, projeto in enumerate(projetos_visiveis):
            card_y = area_conteudo.y + 20 + i * (self.card_altura + 10)
            # O card agora é um pouco mais estreito para dar espaço ao scrollbar
            card_rect = pygame.Rect(area_conteudo.x + 15, card_y, area_conteudo.width - 60, self.card_altura)
            
            # ... (todo o código de desenho do card permanece o mesmo)
            pygame.draw.rect(tela, self.COR_CARD, card_rect, border_radius=5)
            pygame.draw.rect(tela, self.COR_BORDA_CARD, card_rect, 1, border_radius=5)
            logo_rect = pygame.Rect(card_rect.x + 15, card_rect.y + 15, 64, 64)
            cliente = self._get_cliente(projeto.get_id_cliente())
            cliente_nome = cliente.get_nome() if cliente else "N/A"
            cor_logo_fundo = self.CORES_LOGO[projeto.get_id_cliente() % len(self.CORES_LOGO)]
            pygame.draw.rect(tela, cor_logo_fundo, logo_rect, border_radius=5)
            inicial = cliente_nome[0].upper() if cliente_nome != "N/A" else "?"
            inicial_surf = self.fonte_logo.render(inicial, True, (255, 255, 255))
            tela.blit(inicial_surf, (logo_rect.centerx - inicial_surf.get_width() / 2, logo_rect.centery - inicial_surf.get_height() / 2))
            info_x = logo_rect.right + 20
            titulo_surf = self.fonte_h2.render(projeto.get_titulo(), True, self.COR_TEXTO_TITULO)
            tela.blit(titulo_surf, (info_x, card_rect.y + 15))
            cliente_surf = self.fonte_corpo.render(cliente_nome, True, self.COR_TEXTO_CORPO)
            tela.blit(cliente_surf, (info_x, card_rect.y + 45))
            desc_breve = projeto.get_descricao()[:55] + "..." if len(projeto.get_descricao()) > 55 else projeto.get_descricao()
            desc_surf = self.fonte_corpo.render(desc_breve, True, self.COR_TEXTO_CORPO)
            tela.blit(desc_surf, (info_x, card_rect.y + 65))
            remuneracao_surf = self.fonte_corpo.render(f"💰 R$ {projeto.get_recompensa():.2f}", True, (0, 150, 80))
            tela.blit(remuneracao_surf, (card_rect.x + 15, card_rect.bottom - 35))
            botao_rect = pygame.Rect(card_rect.right - 170, card_rect.centery - 20, 150, 40)
            self.botoes_detalhes[projeto.get_id_projeto()] = botao_rect
            cor_botao_atual = self.COR_BOTAO_HOVER if botao_rect.collidepoint(mouse_pos) else self.COR_BOTAO
            pygame.draw.rect(tela, cor_botao_atual, botao_rect, border_radius=5)
            botao_surf = self.fonte_corpo.render("Ver Detalhes", True, (255, 255, 255))
            tela.blit(botao_surf, (botao_rect.centerx - botao_surf.get_width() / 2, botao_rect.centery - botao_surf.get_height() / 2))

        # Desenha o scrollbar por cima de tudo
        self._desenhar_scrollbar(tela)

    def tratar_eventos_conteudo(self, eventos):
        max_scroll = len(self.projetos) - self.max_visiveis if self.projetos else 0

        for evento in eventos:
            # --- NOVA LÓGICA DE EVENTOS DO SCROLLBAR ---
            if evento.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= evento.y
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                self.atualizar_handle_scrollbar()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                handle_abs = self.scrollbar_handle_rect.move(self.rect.topleft)
                if handle_abs.collidepoint(evento.pos):
                    self.dragging_scrollbar = True
                    self.drag_offset_y = evento.pos[1] - handle_abs.y
                elif self.botao_scroll_up.move(self.rect.topleft).collidepoint(evento.pos):
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    self.atualizar_handle_scrollbar()
                elif self.botao_scroll_down.move(self.rect.topleft).collidepoint(evento.pos):
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                    self.atualizar_handle_scrollbar()

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.dragging_scrollbar = False
                # Checa cliques nos botões de detalhes
                for proj_id, rect in self.botoes_detalhes.items():
                    if rect.collidepoint(evento.pos):
                        projeto_clicado = next((p for p in self.projetos if p.get_id_projeto() == proj_id), None)
                        if projeto_clicado:
                            self.callback_ver_detalhes(projeto_clicado)
                            self.deve_fechar = True
                        return

            elif evento.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
                track_abs = self.scrollbar_track_rect.move(self.rect.topleft)
                # Posição do mouse relativa ao track
                relative_y = evento.pos[1] - track_abs.y - self.drag_offset_y
                # Proporção da posição do mouse no track
                scroll_ratio = relative_y / (track_abs.height - self.scrollbar_handle_rect.height)
                # Define o scroll_offset com base na proporção
                self.scroll_offset = round(scroll_ratio * max_scroll)
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                self.atualizar_handle_scrollbar()
    
    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)