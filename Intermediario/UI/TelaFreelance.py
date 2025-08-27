import pygame
from Intermediario.UI.Janela import Janela

class TelaFreelance(Janela):
    def __init__(self, largura_tela, altura_tela, projeto_ativo, projetos_info, cliente_service, callback_abrir_desenvolvimento):
        
        painel_w = int(largura_tela * 0.6)
        painel_h = int(altura_tela * 0.7)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        titulo_janela = "[ PAINEL DE CONTROLE ]" if projeto_ativo else "[ F.L.N.C.R. ] - Contratos Disponíveis"
        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, titulo=titulo_janela)
        
        self.cor_fundo = (18, 24, 32)
        self.cor_borda = (255, 190, 0)
        self.cor_titulo_bg = (28, 34, 42)

        self.projeto_ativo = projeto_ativo
        self.projetos_info = projetos_info
        self.cliente_service = cliente_service
        self.callback_abrir_desenvolvimento = callback_abrir_desenvolvimento

        # Paleta de Cores e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (200, 200, 200)
        self.COR_TEXTO_BLOQUEADO = (120, 100, 100)
        self.COR_FUNDO_HOVER = (40, 50, 65)
        self.CORES_LOGO = [(60,80,120), (180,60,60), (60,120,80), (180,140,60)]
        
        self.CORES_DIFICULDADE = {
            'Iniciante': (0, 180, 100),
            'Intermediario': (255, 180, 0),
            'Difícil': (220, 50, 50)
        }

        self.fonte_h1 = pygame.font.SysFont('Consolas', 24, bold=True)
        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_item = pygame.font.SysFont('Consolas', 16)
        self.fonte_logo = pygame.font.SysFont('Consolas', 32, bold=True)
        self.fonte_tag = pygame.font.SysFont('Consolas', 14, bold=True)
        
        # --- NOVO: Lógica de Filtro ---
        self.filtro_ativo = "Todos"
        self.projetos_filtrados = []
        self.botoes_filtro_rects = {}
        
        # Atributos para o scrollbar funcional
        self.scroll_offset = 0
        self.altura_linha = 80
        self.y_inicio_lista = 120 # Desce a lista para dar espaço aos filtros
        self.max_visiveis = (self.rect.height - self.y_inicio_lista - 40) // self.altura_linha
        
        self.scrollbar_track_rect = pygame.Rect(self.rect.width - 25, self.y_inicio_lista, 15, self.rect.height - self.y_inicio_lista - 40)
        self.scrollbar_handle_rect = pygame.Rect(0,0,0,0)
        self.dragging_scrollbar = False

        self.rects_projetos = {}
        self.cache_clientes = {}
        self._aplicar_filtro() # Aplica o filtro inicial
        self.atualizar_handle_scrollbar()

    def _aplicar_filtro(self):
        """Filtra a lista de projetos com base no filtro ativo."""
        if self.filtro_ativo == "Todos":
            self.projetos_filtrados = self.projetos_info
        else:
            self.projetos_filtrados = [
                info for info in self.projetos_info 
                if info["projeto"].get_dificuldade() == self.filtro_ativo
            ]
        self.scroll_offset = 0 # Reseta o scroll ao mudar de filtro
        self.atualizar_handle_scrollbar()

    def _get_cliente(self, cliente_id):
        if cliente_id not in self.cache_clientes:
            self.cache_clientes[cliente_id] = self.cliente_service.buscar_cliente_por_id(cliente_id)
        return self.cache_clientes[cliente_id]

    def atualizar_handle_scrollbar(self):
        num_projetos = len(self.projetos_filtrados) # Usa a lista filtrada
        if not num_projetos or num_projetos <= self.max_visiveis:
            self.scrollbar_handle_rect.height = 0; return

        view_ratio = self.max_visiveis / num_projetos
        handle_height = self.scrollbar_track_rect.height * view_ratio
        self.scrollbar_handle_rect.height = max(handle_height, 20)

        max_scroll = num_projetos - self.max_visiveis
        scroll_ratio = self.scroll_offset / max_scroll if max_scroll > 0 else 0
        scrollable_space = self.scrollbar_track_rect.height - self.scrollbar_handle_rect.height
        
        self.scrollbar_handle_rect.x = self.scrollbar_track_rect.x
        self.scrollbar_handle_rect.y = self.scrollbar_track_rect.y + scrollable_space * scroll_ratio
        
    def _desenhar_scrollbar(self, tela):
        if len(self.projetos_filtrados) > self.max_visiveis: # Usa a lista filtrada
            track_abs = self.scrollbar_track_rect.move(self.rect.topleft)
            handle_abs = self.scrollbar_handle_rect.move(self.rect.topleft)
            pygame.draw.rect(tela, (28, 34, 42), track_abs, border_radius=7)
            pygame.draw.rect(tela, self.COR_TEXTO_PRIMARIO, handle_abs, border_radius=7)

    def desenhar(self, tela):
        if not self.visivel: return
        self.desenhar_base(tela)
        if self.projeto_ativo:
            self._desenhar_painel_projeto_ativo(tela)
        else:
            self._desenhar_lista_projetos(tela)

    def _desenhar_painel_projeto_ativo(self, tela):
        cliente = self._get_cliente(self.projeto_ativo.get_id_cliente())
        
        titulo_surf = self.fonte_h1.render(self.projeto_ativo.get_titulo(), True, self.COR_TEXTO_PRIMARIO)
        tela.blit(titulo_surf, (self.rect.x + 30, self.rect.y + 50))
        
        cliente_surf = self.fonte_h2.render(f"Cliente: {cliente.get_nome()}", True, self.COR_TEXTO_CORPO)
        tela.blit(cliente_surf, (self.rect.x + 30, self.rect.y + 90))

        recompensa_surf = self.fonte_h2.render(f"Pagamento: R$ {self.projeto_ativo.get_recompensa():.2f}", True, (0, 220, 120))
        tela.blit(recompensa_surf, (self.rect.x + 30, self.rect.y + 120))
        
        status_surf = self.fonte_h2.render("Status: [ EM ANDAMENTO ]", True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(status_surf, (self.rect.x + 30, self.rect.y + 160))
        
        self.botao_abrir_dev_rect = pygame.Rect(self.rect.centerx - 150, self.rect.bottom - 80, 300, 50)
        cor_btn = self.COR_FUNDO_HOVER if self.botao_abrir_dev_rect.collidepoint(pygame.mouse.get_pos()) else (35, 45, 55)
        pygame.draw.rect(tela, cor_btn, self.botao_abrir_dev_rect, border_radius=8)
        texto_btn = self.fonte_h2.render("ABRIR AMBIENTE DE DEV", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(texto_btn, (self.botao_abrir_dev_rect.centerx - texto_btn.get_width()/2, self.botao_abrir_dev_rect.centery - texto_btn.get_height()/2))

    def _desenhar_lista_projetos(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        
        titulo_pagina_surf = self.fonte_h1.render("Feed de Contratos", True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(titulo_pagina_surf, (self.rect.x + 20, self.rect.y + 45))

        # --- NOVO: Desenha os botões de filtro ---
        filtros = ["Todos", "Iniciante", "Intermediario", "Difícil"]
        x_filtro = self.rect.x + 20
        y_filtro = self.rect.y + 80
        self.botoes_filtro_rects.clear()
        for filtro in filtros:
            texto_surf = self.fonte_item.render(filtro, True, self.COR_TEXTO_CORPO)
            padding = 20
            rect = pygame.Rect(x_filtro, y_filtro, texto_surf.get_width() + padding, 30)
            self.botoes_filtro_rects[filtro] = rect
            
            is_active = self.filtro_ativo == filtro
            cor_fundo = self.COR_TEXTO_PRIMARIO if is_active else self.COR_FUNDO_HOVER if rect.collidepoint(mouse_pos) else (28, 34, 42)
            cor_texto = (18, 24, 32) if is_active else self.COR_TEXTO_CORPO
            
            pygame.draw.rect(tela, cor_fundo, rect, border_radius=15)
            texto_renderizado = self.fonte_item.render(filtro, True, cor_texto)
            tela.blit(texto_renderizado, (rect.centerx - texto_renderizado.get_width()/2, rect.centery - texto_renderizado.get_height()/2))
            x_filtro += rect.width + 10

        infos_visiveis = self.projetos_filtrados[self.scroll_offset : self.scroll_offset + self.max_visiveis]
        self.rects_projetos.clear()

        y_linha = self.rect.y + self.y_inicio_lista
        for info in infos_visiveis:
            projeto = info["projeto"]
            tem_req = info["pode_aceitar"]

            card_rect = pygame.Rect(self.rect.x + 20, y_linha, self.rect.width - 70, self.altura_linha)
            self.rects_projetos[projeto.get_id_projeto()] = {"rect": card_rect, "info": info}
            
            cor_fundo_card = self.COR_FUNDO_HOVER if card_rect.collidepoint(mouse_pos) and tem_req else (28, 34, 42)
            pygame.draw.rect(tela, cor_fundo_card, card_rect, border_radius=5)
            
            logo_rect = pygame.Rect(card_rect.x + 10, card_rect.y + 10, 60, 60)
            cliente = self._get_cliente(projeto.get_id_cliente())
            cliente_nome = cliente.get_nome() if cliente else "N/A"
            cor_logo_fundo = self.CORES_LOGO[projeto.get_id_cliente() % len(self.CORES_LOGO)]
            pygame.draw.rect(tela, cor_logo_fundo, logo_rect, border_radius=5)
            inicial = cliente_nome[0].upper() if cliente_nome != "N/A" else "?"
            inicial_surf = self.fonte_logo.render(inicial, True, (255, 255, 255))
            tela.blit(inicial_surf, (logo_rect.centerx - inicial_surf.get_width() / 2, logo_rect.centery - inicial_surf.get_height() / 2))

            info_x = logo_rect.right + 15
            
            cor_texto_titulo = self.COR_TEXTO_CORPO if tem_req else self.COR_TEXTO_BLOQUEADO
            
            titulo_surf = self.fonte_item.render(projeto.get_titulo(), True, cor_texto_titulo)
            tela.blit(titulo_surf, (info_x, card_rect.y + 15))
            
            cliente_surf = self.fonte_item.render(f"Cliente: {cliente_nome}", True, self.COR_TEXTO_BLOQUEADO)
            tela.blit(cliente_surf, (info_x, card_rect.y + 35))

            dificuldade_texto = projeto.get_dificuldade()
            cor_dificuldade = self.CORES_DIFICULDADE.get(dificuldade_texto, (150, 150, 150))
            
            tag_rect = pygame.Rect(card_rect.right - 120, card_rect.y + 25, 100, 30)
            pygame.draw.rect(tela, cor_dificuldade, tag_rect, border_radius=15)
            
            dificuldade_surf = self.fonte_tag.render(dificuldade_texto, True, (255,255,255))
            tela.blit(dificuldade_surf, (tag_rect.centerx - dificuldade_surf.get_width()/2, tag_rect.centery - dificuldade_surf.get_height()/2))
            
            y_linha += self.altura_linha + 10

        self._desenhar_scrollbar(tela)

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        
        max_scroll = len(self.projetos_filtrados) - self.max_visiveis if self.projetos_filtrados else 0

        for evento in eventos:
            if evento.type == pygame.MOUSEWHEEL:
                if not self.projeto_ativo:
                    self.scroll_offset -= evento.y
                    self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                    self.atualizar_handle_scrollbar()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                handle_abs = self.scrollbar_handle_rect.move(self.rect.topleft)
                if handle_abs.collidepoint(evento.pos):
                    self.dragging_scrollbar = True

            elif evento.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
                track_abs = self.scrollbar_track_rect.move(self.rect.topleft)
                relative_y = evento.pos[1] - track_abs.y
                scrollable_space = track_abs.height - self.scrollbar_handle_rect.height
                scroll_ratio = relative_y / scrollable_space if scrollable_space > 0 else 0
                self.scroll_offset = round(scroll_ratio * max_scroll)
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                self.atualizar_handle_scrollbar()
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.dragging_scrollbar = False
                if self.projeto_ativo:
                    if hasattr(self, 'botao_abrir_dev_rect') and self.botao_abrir_dev_rect.collidepoint(evento.pos):
                        self.callback_abrir_desenvolvimento(self.projeto_ativo)
                        self.deve_fechar = True
                else: # Modo lista
                    # --- NOVO: Checa cliques nos filtros ---
                    for filtro, rect in self.botoes_filtro_rects.items():
                        if rect.collidepoint(evento.pos):
                            self.filtro_ativo = filtro
                            self._aplicar_filtro()
                            return # Consome o clique

                    for info_clique in self.rects_projetos.values():
                        if info_clique["rect"].collidepoint(evento.pos):
                            if info_clique["info"]["pode_aceitar"]:
                                self.callback_abrir_desenvolvimento(info_clique["info"]["projeto"])
                                self.deve_fechar = True
                            else:
                                print("Skills insuficientes!")
                            return
