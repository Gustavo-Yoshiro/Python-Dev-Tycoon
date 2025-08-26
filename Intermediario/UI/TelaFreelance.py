import pygame
from Intermediario.UI.Janela import Janela

class TelaFreelance(Janela):
    def __init__(self, largura_tela, altura_tela, projeto_ativo, projetos_disponiveis, jogador, cliente_service, callback_abrir_dev, callback_ver_detalhes):
        
        painel_w = int(largura_tela * 0.54)
        painel_h = int(altura_tela * 0.66)
        painel_x = int(largura_tela * 0.25)
        painel_y = int(altura_tela * 0.13)

        titulo_janela = "[ PROJETO ATIVO ]" if projeto_ativo else "[ F.L.N.C.R. ] - Rede de Contratos"
        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, titulo=titulo_janela)
        
        self.cor_fundo = (18, 24, 32)
        self.cor_borda = (255, 190, 0)
        self.cor_titulo_bg = (28, 34, 42)

        self.projeto_ativo = projeto_ativo
        self.projetos_disponiveis = projetos_disponiveis
        self.jogador = jogador
        self.cliente_service = cliente_service
        self.callback_abrir_dev = callback_abrir_dev
        self.callback_ver_detalhes = callback_ver_detalhes

        # Paleta e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (200, 200, 200)
        self.COR_TEXTO_BLOQUEADO = (120, 120, 120)
        self.COR_FUNDO_HOVER = (40, 50, 65)
        self.COR_FUNDO_BLOQUEADO = (40, 40, 40, 200)

        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_item = pygame.font.SysFont('Consolas', 16)
        
        # Lógica de Scroll
        self.scroll_offset = 0
        self.altura_linha = 45
        self.max_visiveis = (self.rect.height - 120) // self.altura_linha
        self.rects_projetos = {}
        self.cache_clientes = {}

    def _get_cliente(self, cliente_id):
        if cliente_id not in self.cache_clientes:
            self.cache_clientes[cliente_id] = self.cliente_service.buscar_cliente_por_id(cliente_id)
        return self.cache_clientes[cliente_id]

    def desenhar_conteudo(self, tela):
        if self.projeto_ativo:
            self._desenhar_painel_projeto_ativo(tela)
        else:
            self._desenhar_lista_projetos(tela)

    def _desenhar_painel_projeto_ativo(self, tela):
        cliente = self._get_cliente(self.projeto_ativo.get_id_cliente())
        
        titulo_surf = self.fonte_h2.render(f"Contrato: {self.projeto_ativo.get_titulo()}", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(titulo_surf, (self.rect.x + 30, self.rect.y + 50))
        
        cliente_surf = self.fonte_item.render(f"Cliente: {cliente.get_nome()}", True, self.COR_TEXTO_CORPO)
        tela.blit(cliente_surf, (self.rect.x + 30, self.rect.y + 80))

        recompensa_surf = self.fonte_item.render(f"Pagamento: R$ {self.projeto_ativo.get_recompensa():.2f}", True, (0, 220, 120))
        tela.blit(recompensa_surf, (self.rect.x + 30, self.rect.y + 110))
        
        self.botao_abrir_dev_rect = pygame.Rect(self.rect.centerx - 150, self.rect.bottom - 80, 300, 50)
        pygame.draw.rect(tela, self.COR_FUNDO_HOVER, self.botao_abrir_dev_rect, border_radius=8)
        texto_btn = self.fonte_h2.render("Abrir Ambiente de Dev", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(texto_btn, (self.botao_abrir_dev_rect.centerx - texto_btn.get_width()/2, self.botao_abrir_dev_rect.centery - texto_btn.get_height()/2))

    def _desenhar_lista_projetos(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        projetos_visiveis = self.projetos_disponiveis[self.scroll_offset : self.scroll_offset + self.max_visiveis]
        self.rects_projetos.clear()

        y_linha = self.rect.y + 80
        for projeto in projetos_visiveis:
            linha_rect = pygame.Rect(self.rect.x + 20, y_linha, self.rect.width - 40, self.altura_linha)
            self.rects_projetos[projeto.get_id_projeto()] = linha_rect
            
            tem_req = (self.jogador.get_nivel_backend() >= projeto.get_req_backend() and
                       self.jogador.get_nivel_frontend() >= projeto.get_req_frontend() and
                       self.jogador.get_nivel_social() >= projeto.get_req_social())

            cor_texto_titulo = self.COR_TEXTO_CORPO if tem_req else self.COR_TEXTO_BLOQUEADO
            
            if linha_rect.collidepoint(mouse_pos) and tem_req:
                pygame.draw.rect(tela, self.COR_FUNDO_HOVER, linha_rect)
                selector_surf = self.fonte_item.render("[>]", True, self.COR_TEXTO_PRIMARIO)
                tela.blit(selector_surf, (linha_rect.x + 10, linha_rect.y + 12))

            titulo_surf = self.fonte_item.render(projeto.get_titulo(), True, cor_texto_titulo)
            tela.blit(titulo_surf, (linha_rect.x + 50, linha_rect.y + 12))
            
            if not tem_req:
                req_str = f"Req: B{projeto.get_req_backend()}/F{projeto.get_req_frontend()}/S{projeto.get_req_social()}"
                req_surf = self.fonte_item.render(req_str, True, (180, 40, 40))
                tela.blit(req_surf, (linha_rect.right - req_surf.get_width() - 10, linha_rect.y + 12))
            
            y_linha += self.altura_linha

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.projeto_ativo:
                    if self.botao_abrir_dev_rect.collidepoint(evento.pos):
                        self.callback_abrir_dev(self.projeto_ativo)
                        self.deve_fechar = True
                else:
                    for proj_id, rect in self.rects_projetos.items():
                        if rect.collidepoint(evento.pos):
                            proj_clicado = next((p for p in self.projetos_disponiveis if p.get_id_projeto() == proj_id), None)
                            if proj_clicado:
                                tem_req = (self.jogador.get_nivel_backend() >= proj_clicado.get_req_backend()) # Simplificado
                                if tem_req:
                                    self.callback_ver_detalhes(proj_clicado)
                                    self.deve_fechar = True
                                else:
                                    print("Jogador não tem os requisitos!") # Adicionar som de "negado"
                                return

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)
