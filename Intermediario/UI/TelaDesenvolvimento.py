import pygame
import sys
from Intermediario.UI.Janela import Janela
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl

# -------------------------
# TelaDesenvolvimento
# -------------------------
class TelaDesenvolvimento(Janela):
    """
    Tela de desenvolvimento com:
      - Surface interna com alpha/transparência
      - Editor com scroll vertical/horizontal, gutter e cursor
      - Terminal com log e popup de saída
      - Briefing com detalhes técnicos carregados do service
      - Botões: Executar Testes, Entregar (bloqueado até passar), Desistir
      - Botão X no canto superior direito (fechar)
      - Move/drag da janela (se Janela.base não fizer; mantém compatibilidade)
    """

    def __init__(self, largura_tela, altura_tela, projeto, jogador, cliente,
                 callback_validar, callback_entregar, callback_desistir,
                 detalhes_revelados=None,
                 largura=None, altura=None):
        """
        largura_tela, altura_tela: tamanho da tela principal (para posicionamento inicial)
        projeto, jogador, cliente: objetos do seu domínio (usados para textos/calls)
        callbacks: funções externas para validação/entrega/desistir
        detalhes_revelados: opcionais (string) - inicial
        largura, altura: opcional para sobrescrever o tamanho (por padrão reduzido)
        """

        # Default: um pouco menor que antes
        painel_w = int((largura_tela * 0.72) if largura is None else largura)
        painel_h = int((altura_tela * 0.72) if altura is None else altura)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h,
                         titulo=f"[ AMBIENTE DE DESENVOLVIMENTO ]: {projeto.get_titulo() if hasattr(projeto, 'get_titulo') else str(projeto)}")

        # Transparência / cores (fundo com alpha)
        self.cor_fundo = (18, 24, 32, 210)            # RGBA (alpha para leve transparência)
        self.cor_borda = (42, 103, 188)
        self.cor_titulo_bg = (28, 44, 80)

        # Service
        self.service = JogadorProjetoServiceImpl()

        # Dados
        self.jogador = jogador
        self.projeto = projeto
        self.cliente = cliente
        self.callback_validar = callback_validar
        self.callback_entregar = callback_entregar
        self.callback_desistir = callback_desistir
        self.detalhes_revelados = (detalhes_revelados or "").strip()

        # Paleta & fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (220, 220, 220)
        self.COR_FUNDO_EDITOR = (10, 12, 15)
        self.COR_LINENUM_BG = (25, 30, 38)
        self.COR_SUCESSO = (0, 220, 120)
        self.COR_FALHA = (220, 50, 50)
        self.COR_BOTAO_EXECUTAR = (0, 150, 200)
        self.COR_BOTAO_ENTREGAR = (0, 180, 80)
        self.COR_BOTAO_DESISTIR = (180, 40, 40)
        self.COR_DETALHES = (180, 220, 255)

        pygame_font = pygame.font.get_default_font()
        # Consolas/Courier equivalentes podem não existir; usa padrão mas preserva tamanhos
        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_code = pygame.font.SysFont('Consolas', 16)
        self.fonte_terminal = pygame.font.SysFont('Consolas', 14)
        self.fonte_popup = pygame.font.SysFont('Consolas', 16)
        self.fonte_detalhes = pygame.font.SysFont('Consolas', 14)

        # Editor
        codigo_base = projeto.get_codigo_base() if hasattr(projeto, 'get_codigo_base') else ""
        self.linhas_codigo = codigo_base.split('\n') if codigo_base is not None else [""]
        self.linha_ativa = 0
        self.cursor_pos = len(self.linhas_codigo[0]) if self.linhas_codigo else 0
        self.input_ativo = True

        # Cursor blink
        self.cursor_visivel = True
        self.cursor_timer = 0
        self.cursor_intervalo = 500  # ms

        # Testes/Terminal
        self.resultados_testes = []
        self.feedback_resumido = "Terminal de Validação. Pressione 'Executar Testes'."
        self.testes_passaram = False

        # Popup
        self.popup_saida = False
        self._popup_btn_rect_local = None  # rect do botão dentro da surface (coords locais)
        self.rect_info_saida_local = None

        # Scroll
        self.editor_scroll_offset_y = 0
        self.editor_scroll_offset_x = 0
        self.altura_linha_code = self.fonte_code.get_height()
        self.dragging_scrollbar_v = False
        self.dragging_scrollbar_h = False

        # Drag da janela (se sua Janela não cuidar)
        self.arrastando = False
        self.arraste_offset = (0, 0)

        # Retângulos locais (recalculados)
        self._recalcular_layout_interno()

        # Controle de handles locais (são atualizados ao desenhar editor)
        self.scrollbar_v_handle_rect_local = None
        self.scrollbar_h_handle_rect_local = None

    # -------------------------
    # Layout interno (coord locais)
    # -------------------------
    def _recalcular_layout_interno(self):
        """Calcule rects em coordenadas LOCAIS (0..width, 0..height) da janela"""
        briefing_x, briefing_y = 15, 40
        briefing_w, briefing_h = 350, self.rect.height - 60
        self.briefing_rect_local = pygame.Rect(briefing_x, briefing_y, briefing_w, briefing_h)

        editor_x = briefing_x + briefing_w + 15
        editor_y = briefing_y
        editor_w = self.rect.width - briefing_w - 45
        editor_h = self.rect.height - 200
        self.editor_rect_local = pygame.Rect(editor_x, editor_y, editor_w, editor_h)

        self.terminal_rect_local = pygame.Rect(editor_x, editor_y + editor_h + 15, editor_w, 130)

        # Botões (coluna do briefing)
        self.botao_executar_rect_local = pygame.Rect(self.briefing_rect_local.left + 15,
                                                     self.briefing_rect_local.bottom - 180,
                                                     self.briefing_rect_local.width - 30, 50)
        self.botao_entregar_rect_local = pygame.Rect(self.briefing_rect_local.left + 15,
                                                     self.briefing_rect_local.bottom - 120,
                                                     self.briefing_rect_local.width - 30, 50)
        self.botao_desistir_rect_local = pygame.Rect(self.briefing_rect_local.left + 15,
                                                     self.briefing_rect_local.bottom - 60,
                                                     self.briefing_rect_local.width - 30, 50)

        # Botão fechar (X) - local coords
        size = 28
        self.botao_fechar_local = pygame.Rect(self.rect.width - size - 10, 10, size, size)

    # -------------------------
    # Conversão coordenadas
    # -------------------------
    def _to_local(self, pos_global):
        return (pos_global[0] - self.rect.x, pos_global[1] - self.rect.y)

    def _to_global_rect(self, rect_local):
        return rect_local.move(self.rect.topleft)

    # -------------------------
    # Update (cursor blink)
    # -------------------------
    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_intervalo:
            self.cursor_timer = 0
            self.cursor_visivel = not self.cursor_visivel

        # Recalcula layout caso a janela seja redimensionada/posicionada externamente
        self._recalcular_layout_interno()

    # -------------------------
    # Texto com quebra (usando surface local)
    # -------------------------
    def desenhar_texto_quebra_linha(self, surface, texto, rect, fonte, cor):
        y = rect.y
        paragrafos = texto.splitlines()
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            linha_atual = ''
            for palavra in palavras:
                teste_linha = f"{linha_atual} {palavra}".strip()
                if fonte.size(teste_linha)[0] <= rect.width:
                    linha_atual = teste_linha
                else:
                    if y + fonte.get_height() > rect.bottom:
                        return y
                    linha_surf = fonte.render(linha_atual, True, cor)
                    surface.blit(linha_surf, (rect.x, y))
                    y += fonte.get_height()
                    linha_atual = palavra
            if y + fonte.get_height() > rect.bottom:
                return y
            linha_surf = fonte.render(linha_atual, True, cor)
            surface.blit(linha_surf, (rect.x, y))
            y += fonte.get_height() + 4
        return y

    # -------------------------
    # Popup de saída (local)
    # -------------------------
    def _desenhar_popup_saida(self, surface):
        largura, altura = 600, 400
        popup_x = (self.rect.width // 2) - (largura // 2)
        popup_y = (self.rect.height // 2) - (altura // 2)

        # Sombra semi-transparente
        sombra = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 120))
        surface.blit(sombra, (0, 0))

        surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(surf, (30, 44, 70, 232), (0, 0, largura, altura), border_radius=20)
        pygame.draw.rect(surf, (120, 180, 255), (0, 0, largura, altura), 3, border_radius=20)

        surf.blit(self.fonte_h2.render("Log de Execução dos Testes:", True, (230,230,90)), (20, 20))

        y_popup = 65
        for linha in self.resultados_testes:
            if y_popup > altura - 50:
                surf.blit(self.fonte_popup.render("[...]", True, (220,180,180)), (20, y_popup))
                break
            cor = self.COR_SUCESSO if "✓" in linha else self.COR_FALHA if "✗" in linha else self.COR_TEXTO_CORPO
            area_linha_popup = pygame.Rect(20, y_popup, largura - 40, altura - y_popup - 20)
            y_popup = self.desenhar_texto_quebra_linha(surf, linha, area_linha_popup, self.fonte_popup, cor)

        btn_rect = pygame.Rect(largura-110, altura-50, 90, 38)
        pygame.draw.rect(surf, (255, 90, 90), btn_rect, border_radius=12)
        fechar_label = self.fonte_h2.render("FECHAR", True, (255,255,255))
        surf.blit(fechar_label, (btn_rect.centerx - fechar_label.get_width()/2, btn_rect.centery - fechar_label.get_height()/2))

        surface.blit(surf, (popup_x, popup_y))
        # salva em coords locais
        self._popup_btn_rect_local = pygame.Rect(popup_x + btn_rect.x, popup_y + btn_rect.y, btn_rect.w, btn_rect.h)

    # -------------------------
    # Desenhar editor (local)
    # -------------------------
    def _desenhar_editor(self, surface):
        pygame.draw.rect(surface, self.COR_FUNDO_EDITOR, self.editor_rect_local)

        gutter_width = 50
        gutter_rect = pygame.Rect(self.editor_rect_local.x, self.editor_rect_local.y, gutter_width, self.editor_rect_local.height - 15)
        pygame.draw.rect(surface, self.COR_LINENUM_BG, gutter_rect)

        editor_area = pygame.Rect(gutter_rect.right, self.editor_rect_local.y, self.editor_rect_local.width - gutter_width - 15, self.editor_rect_local.height - 15)

        max_linhas_visiveis = max(1, editor_area.height // self.altura_linha_code)
        max_scroll_y = max(0, len(self.linhas_codigo) - max_linhas_visiveis)
        self.editor_scroll_offset_y = max(0, min(self.editor_scroll_offset_y, max_scroll_y))

        max_largura_codigo = max((self.fonte_code.size(l)[0] for l in self.linhas_codigo), default=0)
        max_scroll_x = max(0, max_largura_codigo - editor_area.width + 20)
        self.editor_scroll_offset_x = max(0, min(self.editor_scroll_offset_x, max_scroll_x))

        # numeros de linha
        y_linha_num = editor_area.y + 5 - (self.editor_scroll_offset_y * self.altura_linha_code)
        for i in range(len(self.linhas_codigo)):
            if y_linha_num > editor_area.bottom:
                break
            if y_linha_num + self.altura_linha_code > editor_area.y:
                linha_num_surf = self.fonte_code.render(str(i+1), True, (140,140,140))
                surface.blit(linha_num_surf, (gutter_rect.right - linha_num_surf.get_width() - 10, y_linha_num))
            y_linha_num += self.altura_linha_code

        # clipping e codigo
        clip_original = surface.get_clip()
        surface.set_clip(editor_area)
        y_linha = editor_area.y + 5 - (self.editor_scroll_offset_y * self.altura_linha_code)
        for i, linha in enumerate(self.linhas_codigo):
            if y_linha > editor_area.bottom: break
            if y_linha + self.altura_linha_code > editor_area.y:
                linha_surf = self.fonte_code.render(linha, True, self.COR_TEXTO_CORPO)
                surface.blit(linha_surf, (editor_area.x + 10 - self.editor_scroll_offset_x, y_linha))

                if i == self.linha_ativa and self.input_ativo and self.cursor_visivel:
                    texto_ate_cursor = self.linhas_codigo[i][:self.cursor_pos]
                    cursor_x = editor_area.x + 10 - self.editor_scroll_offset_x + self.fonte_code.size(texto_ate_cursor)[0]
                    pygame.draw.line(surface, self.COR_TEXTO_PRIMARIO, (cursor_x, y_linha), (cursor_x, y_linha + self.altura_linha_code), 2)
            y_linha += self.altura_linha_code
        surface.set_clip(clip_original)

        # scrollbar vertical
        if max_scroll_y > 0:
            track_v = pygame.Rect(editor_area.right, editor_area.y, 10, editor_area.height)
            ratio_v = editor_area.height / max(1, len(self.linhas_codigo) * self.altura_linha_code)
            handle_h_v = max(20, track_v.height * ratio_v)
            ratio_pos_v = self.editor_scroll_offset_y / max_scroll_y if max_scroll_y > 0 else 0
            handle_y_v = track_v.y + (track_v.height - handle_h_v) * ratio_pos_v
            self.scrollbar_v_handle_rect_local = pygame.Rect(track_v.x, handle_y_v, 10, handle_h_v)
            pygame.draw.rect(surface, self.COR_LINENUM_BG, track_v)
            pygame.draw.rect(surface, (80,80,80), self.scrollbar_v_handle_rect_local)
        else:
            self.scrollbar_v_handle_rect_local = None

        # scrollbar horizontal
        if max_scroll_x > 0:
            track_h = pygame.Rect(editor_area.x, editor_area.bottom, editor_area.width, 10)
            ratio_h = editor_area.width / (max_largura_codigo + 20) if max_largura_codigo > 0 else 1
            handle_w_h = max(20, track_h.width * ratio_h)
            ratio_pos_h = self.editor_scroll_offset_x / max_scroll_x if max_scroll_x > 0 else 0
            handle_x_h = track_h.x + (track_h.width - handle_w_h) * ratio_pos_h
            self.scrollbar_h_handle_rect_local = pygame.Rect(handle_x_h, track_h.y, handle_w_h, 10)
            pygame.draw.rect(surface, self.COR_LINENUM_BG, track_h)
            pygame.draw.rect(surface, (80,80,80), self.scrollbar_h_handle_rect_local)

            dica_surf = self.fonte_terminal.render("Scroll Horizontal: Shift + Roda do Rato", True, (100,100,100))
            surface.blit(dica_surf, (track_h.x, track_h.bottom + 5))
        else:
            self.scrollbar_h_handle_rect_local = None

    # -------------------------
    # Desenhar todo conteúdo (global: recebe tela principal)
    # -------------------------
    def desenhar_conteudo(self, tela):
        # Surface local (com alpha)
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # fundo (rgba)
        pygame.draw.rect(surface, self.cor_fundo, (0,0,self.rect.width, self.rect.height), border_radius=8)

        # título e borda topo
        titulo_surf = self.fonte_h2.render(self.titulo, True, self.COR_TEXTO_PRIMARIO)
        surface.blit(titulo_surf, (15, 10))

        # desenha borda sutil
        pygame.draw.rect(surface, self.cor_borda, (0,0,self.rect.width, self.rect.height), 2, border_radius=8)

        # botão fechar (X)
        pygame.draw.rect(surface, (220,50,50), self.botao_fechar_local, border_radius=6)
        x_mark = self.fonte_h2.render("X", True, (255,255,255))
        surface.blit(x_mark, (self.botao_fechar_local.centerx - x_mark.get_width()/2, self.botao_fechar_local.centery - x_mark.get_height()/2))

        # ---------------- Briefing ----------------
        pygame.draw.rect(surface, self.cor_fundo, self.briefing_rect_local, border_radius=6)
        cliente_text = self.cliente.get_nome() if hasattr(self.cliente, 'get_nome') else str(self.cliente)
        cliente_surf = self.fonte_h2.render(f"Cliente: {cliente_text}", True, self.COR_TEXTO_SECUNDARIO)
        surface.blit(cliente_surf, (self.briefing_rect_local.x + 15, self.briefing_rect_local.y + 15))

        desc_label_surf = self.fonte_h2.render("Objetivo do Contrato:", True, self.COR_TEXTO_PRIMARIO)
        surface.blit(desc_label_surf, (self.briefing_rect_local.x + 15, self.briefing_rect_local.y + 50))

        desc_rect_area = pygame.Rect(self.briefing_rect_local.x + 15, self.briefing_rect_local.y + 80, self.briefing_rect_local.width - 30, 120)
        proj_desc = self.projeto.get_descricao() if hasattr(self.projeto, 'get_descricao') else str(self.projeto)
        y_apos_desc = self.desenhar_texto_quebra_linha(surface, proj_desc, desc_rect_area, self.fonte_code, self.COR_TEXTO_CORPO)

        # detalhes (carrega do service)
        try:
            detalhes_service = self.service.get_detalhes_descobertos(self.jogador.get_id_jogador(), self.projeto.get_id_projeto())
            if isinstance(detalhes_service, str):
                self.detalhes_revelados = detalhes_service.strip()
            elif isinstance(detalhes_service, list):
                self.detalhes_revelados = "\n".join(detalhes_service).strip()
        except Exception:
            pass

        detalhes_y = y_apos_desc + 20
        pygame.draw.line(surface, (80,100,120), (self.briefing_rect_local.x + 15, detalhes_y), (self.briefing_rect_local.right - 15, detalhes_y), 1)
        detalhes_label_surf = self.fonte_h2.render("Detalhes Técnicos:", True, self.COR_TEXTO_PRIMARIO)
        surface.blit(detalhes_label_surf, (self.briefing_rect_local.x + 15, detalhes_y + 10))

        detalhes_rect = pygame.Rect(self.briefing_rect_local.x + 15, detalhes_y + 40, self.briefing_rect_local.width - 30, 120)
        if self.detalhes_revelados:
            self.desenhar_texto_quebra_linha(surface, self.detalhes_revelados, detalhes_rect, self.fonte_detalhes, self.COR_DETALHES)
        else:
            nenhum_surf = self.fonte_detalhes.render("Nenhum detalhe técnico foi descoberto ainda.", True, (150,150,150))
            surface.blit(nenhum_surf, (detalhes_rect.x, detalhes_rect.y))

        # ---------------- Editor ----------------
        self._desenhar_editor(surface)

        # ---------------- Terminal ----------------
        pygame.draw.rect(surface, self.COR_FUNDO_EDITOR, self.terminal_rect_local)
        cor_feedback = self.COR_SUCESSO if self.testes_passaram else (self.COR_FALHA if self.resultados_testes else self.COR_TEXTO_CORPO)
        feedback_surf = self.fonte_terminal.render(self.feedback_resumido, True, cor_feedback)
        surface.blit(feedback_surf, (self.terminal_rect_local.x + 10, self.terminal_rect_local.y + 10))

        if self.resultados_testes:
            icon_x = self.terminal_rect_local.x + 15 + feedback_surf.get_width()
            icon_rect = pygame.Rect(icon_x, self.terminal_rect_local.y + 8, 24, 24)
            pygame.draw.circle(surface, (100, 180, 255), icon_rect.center, 12)
            i_mark = self.fonte_h2.render("i", True, (30,50,80))
            surface.blit(i_mark, (icon_rect.centerx - i_mark.get_width()/2, icon_rect.centery - i_mark.get_height()/2))
            self.rect_info_saida_local = icon_rect
        else:
            self.rect_info_saida_local = None

        # ---------------- Botões ----------------
        pygame.draw.rect(surface, self.COR_BOTAO_EXECUTAR, self.botao_executar_rect_local, border_radius=5)
        exec_surf = self.fonte_h2.render("Executar Testes", True, (255,255,255))
        surface.blit(exec_surf, (self.botao_executar_rect_local.centerx - exec_surf.get_width()/2, self.botao_executar_rect_local.centery - exec_surf.get_height()/2))

        if self.testes_passaram:
            pygame.draw.rect(surface, self.COR_BOTAO_ENTREGAR, self.botao_entregar_rect_local, border_radius=5)
            entregar_surf = self.fonte_h2.render("Entregar Projeto", True, (255,255,255))
        else:
            pygame.draw.rect(surface, (80,80,80), self.botao_entregar_rect_local, border_radius=5)
            entregar_surf = self.fonte_h2.render("Entregar Projeto (Bloqueado)", True, (150,150,150))
        surface.blit(entregar_surf, (self.botao_entregar_rect_local.centerx - entregar_surf.get_width()/2, self.botao_entregar_rect_local.centery - entregar_surf.get_height()/2))

        pygame.draw.rect(surface, self.COR_BOTAO_DESISTIR, self.botao_desistir_rect_local, border_radius=5)
        desistir_surf = self.fonte_h2.render("Desistir do Contrato", True, (255,255,255))
        surface.blit(desistir_surf, (self.botao_desistir_rect_local.centerx - desistir_surf.get_width()/2, self.botao_desistir_rect_local.centery - desistir_surf.get_height()/2))

        # popup de log
        if self.popup_saida:
            self._desenhar_popup_saida(surface)

        # por fim, blita a surface na tela principal na posição global da janela
        tela.blit(surface, (self.rect.x, self.rect.y))

    # -------------------------
    # Posição do cursor via mouse em coords locais
    # -------------------------
    def _get_posicao_cursor_pelo_mouse_local(self, pos_local):
        linha_texto = self.linhas_codigo[self.linha_ativa] if self.linhas_codigo else ""
        gutter_width = 50
        editor_text_x = self.editor_rect_local.x + gutter_width + 10
        pos_x_relativa = pos_local[0] - (editor_text_x - self.editor_scroll_offset_x)
        melhor_distancia, melhor_indice = float('inf'), 0
        for i in range(len(linha_texto) + 1):
            largura_sub = self.fonte_code.size(linha_texto[:i])[0]
            distancia = abs(pos_x_relativa - largura_sub)
            if distancia < melhor_distancia:
                melhor_distancia, melhor_indice = distancia, i
            else:
                break
        return melhor_indice

    # -------------------------
    # Tratamento de eventos (transforma eventos globais -> locais automaticamente)
    # -------------------------
    def tratar_eventos_conteudo(self, eventos):
        eventos_convertidos = []
        for ev in eventos:
            if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                pos_local = self._to_local(ev.pos)
                # cria nova dict baseando-se no ev.__dict__
                novo = pygame.event.Event(ev.type, {**ev.__dict__, "pos": pos_local})
                eventos_convertidos.append(novo)
            elif ev.type == pygame.MOUSEWHEEL:
                # mousewheel não tem pos; coloco atributo mouse_pos_local pra usar
                mouse_pos_global = pygame.mouse.get_pos()
                pos_local = self._to_local(mouse_pos_global)
                novo = pygame.event.Event(ev.type, {**ev.__dict__, "mouse_pos_local": pos_local})
                eventos_convertidos.append(novo)
            else:
                eventos_convertidos.append(ev)

        # Se popup está aberto, só tratar clique no botão de fechar do popup
        if self.popup_saida:
            for evento in eventos_convertidos:
                if self._popup_btn_rect_local and evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    if self._popup_btn_rect_local.collidepoint(evento.pos):
                        self.popup_saida = False
            return

        # Gerencia drag da janela (se Janela base não fizer)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # abrir arraste se clicar no header (região do título)
                mouse_global = evento.pos
                local = self._to_local(mouse_global)
                header_area = pygame.Rect(0, 0, self.rect.width, 36)
                if header_area.collidepoint(local):
                    self.arrastando = True
                    mx, my = mouse_global
                    self.arraste_offset = (self.rect.x - mx, self.rect.y - my)
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.arrastando = False
            elif evento.type == pygame.MOUSEMOTION and self.arrastando:
                mx, my = evento.pos
                self.rect.x = mx + self.arraste_offset[0]
                self.rect.y = my + self.arraste_offset[1]
                # ao mover, recalcule layouts locais
                self._recalcular_layout_interno()

        # Agora lida com eventos convertidos (coordenadas locais)
        for evento in eventos_convertidos:
            # Mouse wheel -> scroll editor se estiver sobre editor local
            if evento.type == pygame.MOUSEWHEEL:
                pos_local = evento.mouse_pos_local
                if self.editor_rect_local.collidepoint(pos_local):
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.editor_scroll_offset_x -= evento.y * 30
                    else:
                        self.editor_scroll_offset_y -= evento.y

            # Mouse down local
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # clique no X (fechar)
                if self.botao_fechar_local.collidepoint(evento.pos):
                    # fecha: se a classe Janela tiver lógica de fechar, use-a; senão marca visivel falso
                    try:
                        # se Janela tem atributo 'deve_fechar' ou método fechar
                        self.deve_fechar = True
                    except Exception:
                        self.visivel = False
                    continue

                # scrollbars drag
                if self.scrollbar_v_handle_rect_local and self.scrollbar_v_handle_rect_local.collidepoint(evento.pos):
                    self.dragging_scrollbar_v = True
                elif self.scrollbar_h_handle_rect_local and self.scrollbar_h_handle_rect_local.collidepoint(evento.pos):
                    self.dragging_scrollbar_h = True

                # botões
                elif self.botao_executar_rect_local.collidepoint(evento.pos):
                    codigo_final = "\n".join(self.linhas_codigo)
                    resultado_validacao = self.callback_validar(self.projeto, codigo_final)
                    # admite dict com "resultados" e "sucesso"
                    self.resultados_testes = resultado_validacao.get("resultados", []) if isinstance(resultado_validacao, dict) else []
                    self.testes_passaram = resultado_validacao.get("sucesso", False) if isinstance(resultado_validacao, dict) else False
                    self.feedback_resumido = "Sucesso: Todos os testes passaram!" if self.testes_passaram else "Falha: Verifique o log de testes."
                elif self.testes_passaram and self.botao_entregar_rect_local.collidepoint(evento.pos):
                    self.callback_entregar(self.projeto)
                    self.deve_fechar = True
                elif self.botao_desistir_rect_local.collidepoint(evento.pos):
                    self.callback_desistir(self.projeto)
                    self.deve_fechar = True
                elif self.rect_info_saida_local and self.rect_info_saida_local.collidepoint(evento.pos):
                    self.popup_saida = True
                # clique no editor: ativa input e posiciona cursor
                elif self.editor_rect_local.collidepoint(evento.pos):
                    self.input_ativo = True
                    clique_y_relativo = evento.pos[1] - (self.editor_rect_local.y + 5)
                    self.linha_ativa = min(len(self.linhas_codigo)-1, max(0, self.editor_scroll_offset_y + (clique_y_relativo // self.altura_linha_code)))
                    self.cursor_pos = self._get_posicao_cursor_pelo_mouse_local(evento.pos)

            # Mouse up local
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.dragging_scrollbar_v = False
                self.dragging_scrollbar_h = False

            # Mouse move local (drag scrollbar)
            if evento.type == pygame.MOUSEMOTION:
                if self.dragging_scrollbar_v and self.scrollbar_v_handle_rect_local:
                    gutter_w = 50
                    editor_area = pygame.Rect(self.editor_rect_local.x + gutter_w, self.editor_rect_local.y, self.editor_rect_local.width - gutter_w - 15, self.editor_rect_local.height - 15)
                    max_linhas_visiveis = max(1, editor_area.height // self.altura_linha_code)
                    max_scroll_y = max(0, len(self.linhas_codigo) - max_linhas_visiveis)
                    track_v = pygame.Rect(editor_area.right, editor_area.y, 10, editor_area.height)
                    relative_y = max(track_v.y, min(track_v.bottom, evento.pos[1])) - track_v.y
                    ratio_pos_v = relative_y / track_v.height if track_v.height > 0 else 0
                    self.editor_scroll_offset_y = round(ratio_pos_v * max_scroll_y)

                if self.dragging_scrollbar_h and self.scrollbar_h_handle_rect_local:
                    gutter_w = 50
                    editor_area = pygame.Rect(self.editor_rect_local.x + gutter_w, self.editor_rect_local.y, self.editor_rect_local.width - gutter_w - 15, self.editor_rect_local.height - 15)
                    max_largura_codigo = max((self.fonte_code.size(l)[0] for l in self.linhas_codigo), default=0)
                    max_scroll_x = max(0, max_largura_codigo - editor_area.width + 20)
                    track_h = pygame.Rect(editor_area.x, editor_area.bottom, editor_area.width, 10)
                    relative_x = max(track_h.x, min(track_h.right, evento.pos[0])) - track_h.x
                    ratio_pos_h = relative_x / track_h.width if track_h.width > 0 else 0
                    self.editor_scroll_offset_x = round(ratio_pos_h * max_scroll_x)

            # Teclado (local ou global - teclas não mudam posição)
            if evento.type == pygame.KEYDOWN and self.input_ativo and self.linhas_codigo:
                linha_atual = self.linhas_codigo[self.linha_ativa]
                if evento.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos-1] + linha_atual[self.cursor_pos:]
                        self.cursor_pos -= 1
                    elif self.linha_ativa > 0:
                        pos_ant = len(self.linhas_codigo[self.linha_ativa - 1])
                        self.linhas_codigo[self.linha_ativa - 1] += linha_atual
                        self.linhas_codigo.pop(self.linha_ativa)
                        self.linha_ativa -= 1
                        self.cursor_pos = pos_ant
                elif evento.key == pygame.K_RETURN:
                    parte_rest = linha_atual[self.cursor_pos:]
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos]
                    self.linhas_codigo.insert(self.linha_ativa + 1, parte_rest)
                    self.linha_ativa += 1
                    self.cursor_pos = 0
                elif evento.key == pygame.K_UP:
                    self.linha_ativa = max(0, self.linha_ativa - 1)
                    self.cursor_pos = min(self.cursor_pos, len(self.linhas_codigo[self.linha_ativa]))
                elif evento.key == pygame.K_DOWN:
                    self.linha_ativa = min(len(self.linhas_codigo)-1, self.linha_ativa + 1)
                    self.cursor_pos = min(self.cursor_pos, len(self.linhas_codigo[self.linha_ativa]))
                elif evento.key == pygame.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                elif evento.key == pygame.K_RIGHT:
                    self.cursor_pos = min(len(linha_atual), self.cursor_pos + 1)
                elif evento.key == pygame.K_TAB:
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos] + '    ' + linha_atual[self.cursor_pos:]
                    self.cursor_pos += 4
                else:
                    if evento.unicode:
                        self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos] + evento.unicode + linha_atual[self.cursor_pos:]
                        self.cursor_pos += len(evento.unicode)

    # -------------------------
    # Encaminhamento de eventos (public)
    # -------------------------
    def tratar_eventos(self, eventos):
        # se sua Janela base tem mover/fechar por padrão, pode chamar super().tratar_eventos(eventos) aqui
        try:
            super().tratar_eventos(eventos)
        except Exception:
            pass
        # trata conteúdo (converte coords)
        self.tratar_eventos_conteudo(eventos)

    # -------------------------
    # Adicionar detalhe (API)
    # -------------------------
    def adicionar_detalhe(self, detalhe):
        detalhe = str(detalhe).strip()
        if not detalhe:
            return
        if not self.detalhes_revelados:
            self.detalhes_revelados = detalhe
        else:
            linhas = [l.strip() for l in self.detalhes_revelados.splitlines() if l.strip()]
            if detalhe not in linhas:
                self.detalhes_revelados += "\n" + detalhe

# -------------------------
# Exemplo de uso mínimo (loop)
# -------------------------
if __name__ == "__main__":
    pygame.init()
    LARGURA, ALTURA = 1280, 720
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()

    # Fake projeto/jogador/cliente para demo - substitua pelos reais
    class Fake:
        def __init__(self, nome, titulo, descricao, codigo):
            self._nome = nome
            self._titulo = titulo
            self._descricao = descricao
            self._codigo = codigo
        def get_nome(self): return self._nome
        def get_titulo(self): return self._titulo
        def get_descricao(self): return self._descricao
        def get_codigo_base(self): return self._codigo
        def get_id_projeto(self): return 1

    class FakeJogador:
        def get_id_jogador(self): return 99

    projeto_demo = Fake("ClienteX", "Demo Projeto", "Criar feature X que faz Y.", "print('hello')\nfor i in range(10):\n    print(i)")
    jogador_demo = FakeJogador()
    cliente_demo = projeto_demo

    # Fake callbacks
    def validar_cb(proj, codigo):
        # exemplo: sempre retorne sucesso falso e 1 linha de log
        return {"sucesso": False, "resultados": ["✗ Erro: função foo não encontrada"]}

    def entregar_cb(proj):
        print("Entregue:", proj.get_titulo())

    def desistir_cb(proj):
        print("Desistiu:", proj.get_titulo())

    janela = TelaDesenvolvimento(LARGURA, ALTURA, projeto_demo, jogador_demo, cliente_demo, validar_cb, entregar_cb, desistir_cb)

    rodando = True
    while rodando:
        dt = clock.tick(60)
        eventos = pygame.event.get()
        for ev in eventos:
            if ev.type == pygame.QUIT:
                rodando = False

        # update
        janela.update(dt)

        # eventos
        janela.tratar_eventos(eventos)

        # render
        screen.fill((28,28,30))
        janela.desenhar_conteudo(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
