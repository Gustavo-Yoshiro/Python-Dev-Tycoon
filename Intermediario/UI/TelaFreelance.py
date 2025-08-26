import pygame
from Intermediario.UI.Janela import Janela

class TelaFreelance(Janela):
    # O __init__ agora recebe 'projetos_info', uma lista de dicionários
    def __init__(self, largura_tela, altura_tela, projeto_ativo, projetos_info, cliente_service, callback_abrir_desenvolvimento):
        
        painel_w = int(largura_tela * 0.6)
        painel_h = int(altura_tela * 0.7)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        titulo_janela = "[ PAINEL DE CONTROLE ]" if projeto_ativo else "[ F.L.N.C.R. ] - Contratos Disponíveis"
        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, titulo=titulo_janela)
        
        # Re-estilização da Janela Base para o tema F.L.N.C.R.
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
        self.COR_TEXTO_SUCESSO = (0, 220, 120)
        self.COR_TEXTO_FALHA = (220, 50, 50)
        self.COR_FUNDO_HOVER = (40, 50, 65)

        self.fonte_h1 = pygame.font.SysFont('Consolas', 24, bold=True)
        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_item = pygame.font.SysFont('Consolas', 16)
        
        # Atributos para o scrollbar funcional
        self.scroll_offset = 0
        self.altura_linha = 50
        self.y_inicio_lista = 80
        self.max_visiveis = (self.rect.height - self.y_inicio_lista - 40) // self.altura_linha
        
        self.scrollbar_track_rect = pygame.Rect(self.rect.width - 25, self.y_inicio_lista, 15, self.rect.height - self.y_inicio_lista - 40)
        self.scrollbar_handle_rect = pygame.Rect(0,0,0,0)
        self.dragging_scrollbar = False

        self.rects_projetos = {}
        self.cache_clientes = {}
        self.atualizar_handle_scrollbar()

    def _get_cliente(self, cliente_id):
        if cliente_id not in self.cache_clientes:
            self.cache_clientes[cliente_id] = self.cliente_service.buscar_cliente_por_id(cliente_id)
        return self.cache_clientes[cliente_id]

    def atualizar_handle_scrollbar(self):
        """Calcula o tamanho e a posição do handle com base no scroll_offset."""
        num_projetos = len(self.projetos_info)
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
        """Desenha o scrollbar se for necessário."""
        if len(self.projetos_info) > self.max_visiveis:
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
        """Desenha a tela focada no projeto que o jogador já aceitou."""
        cliente = self._get_cliente(self.projeto_ativo.get_id_cliente())
        
        titulo_surf = self.fonte_h1.render(self.projeto_ativo.get_titulo(), True, self.COR_TEXTO_PRIMARIO)
        tela.blit(titulo_surf, (self.rect.x + 30, self.rect.y + 50))
        
        cliente_surf = self.fonte_h2.render(f"Cliente: {cliente.get_nome()}", True, self.COR_TEXTO_CORPO)
        tela.blit(cliente_surf, (self.rect.x + 30, self.rect.y + 90))

        recompensa_surf = self.fonte_h2.render(f"Pagamento: R$ {self.projeto_ativo.get_recompensa():.2f}", True, self.COR_TEXTO_SUCESSO)
        tela.blit(recompensa_surf, (self.rect.x + 30, self.rect.y + 120))
        
        status_surf = self.fonte_h2.render("Status: [ EM ANDAMENTO ]", True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(status_surf, (self.rect.x + 30, self.rect.y + 160))
        
        self.botao_abrir_dev_rect = pygame.Rect(self.rect.centerx - 150, self.rect.bottom - 80, 300, 50)
        cor_btn = self.COR_FUNDO_HOVER if self.botao_abrir_dev_rect.collidepoint(pygame.mouse.get_pos()) else (35, 45, 55)
        pygame.draw.rect(tela, cor_btn, self.botao_abrir_dev_rect, border_radius=8)
        texto_btn = self.fonte_h2.render("ABRIR AMBIENTE DE DEV", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(texto_btn, (self.botao_abrir_dev_rect.centerx - texto_btn.get_width()/2, self.botao_abrir_dev_rect.centery - texto_btn.get_height()/2))

    def _desenhar_lista_projetos(self, tela):
        """Desenha a lista de projetos disponíveis, usando a informação pré-processada do serviço."""
        mouse_pos = pygame.mouse.get_pos()
        infos_visiveis = self.projetos_info[self.scroll_offset : self.scroll_offset + self.max_visiveis]
        self.rects_projetos.clear()

        y_linha = self.rect.y + self.y_inicio_lista
        for info in infos_visiveis:
            projeto = info["projeto"]
            tem_req = info["pode_aceitar"]

            linha_rect = pygame.Rect(self.rect.x + 20, y_linha, self.rect.width - 70, self.altura_linha)
            self.rects_projetos[projeto.get_id_projeto()] = {"rect": linha_rect, "info": info}
            
            cor_texto_titulo = self.COR_TEXTO_CORPO if tem_req else self.COR_TEXTO_BLOQUEADO
            
            if linha_rect.collidepoint(mouse_pos) and tem_req:
                pygame.draw.rect(tela, self.COR_FUNDO_HOVER, linha_rect)
                selector_surf = self.fonte_item.render("[>]", True, self.COR_TEXTO_PRIMARIO)
                tela.blit(selector_surf, (linha_rect.x + 10, linha_rect.y + 15))

            titulo_surf = self.fonte_item.render(projeto.get_titulo(), True, cor_texto_titulo)
            tela.blit(titulo_surf, (linha_rect.x + 50, linha_rect.y + 8))
            
            cliente = self._get_cliente(projeto.get_id_cliente())
            cliente_surf = self.fonte_item.render(f"Cliente: {cliente.get_nome()}", True, self.COR_TEXTO_BLOQUEADO)
            tela.blit(cliente_surf, (linha_rect.x + 50, linha_rect.y + 28))

            req_str = f"Req: B{projeto.get_req_backend()}/F{projeto.get_req_frontend()}/S{projeto.get_req_social()}"
            cor_req = self.COR_TEXTO_SUCESSO if tem_req else self.COR_TEXTO_FALHA
            req_surf = self.fonte_item.render(req_str, True, cor_req)
            tela.blit(req_surf, (linha_rect.right - req_surf.get_width() - 10, linha_rect.y + 15))
            
            y_linha += self.altura_linha + 5

        self._desenhar_scrollbar(tela)

    def tratar_eventos(self, eventos):
        """Lida com todos os eventos, incluindo o scrollbar e os dois modos de visualização."""
        super().tratar_eventos(eventos)
        
        max_scroll = len(self.projetos_info) - self.max_visiveis if self.projetos_info else 0

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
                    for info_clique in self.rects_projetos.values():
                        if info_clique["rect"].collidepoint(evento.pos):
                            if info_clique["info"]["pode_aceitar"]:
                                self.callback_abrir_desenvolvimento(info_clique["info"]["projeto"])
                                self.deve_fechar = True
                            else:
                                print("Skills insuficientes!")
                            return
