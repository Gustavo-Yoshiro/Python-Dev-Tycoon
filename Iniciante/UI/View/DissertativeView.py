import pygame

class DissertativeView:
    """
    View responsável por renderizar e editar a resposta de exercícios do tipo 'dissertativa'.
    - Renderiza Pergunta, Dica e o Editor de Código
    - Lida com cursor, teclas, e rolagem via mouse
    - Visual de scroll vertical (track + thumb) igual ao da introdução
    - NÃO executa/valida o código: isso fica na TelaExercicio
    """

    def __init__(self, fonte, fonte_pequena, fonte_editor, linhas_visiveis=5):
        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.fonte_editor = fonte_editor
        self.editor_lh = self.fonte_editor.get_height()

        self.exercicio = None

        # Estado do editor
        self.input_text = [""]
        self.cursor_pos = [0, 0]        # [linha, coluna]
        self.scroll_offset_y = 0         # em linhas
        self.scroll_offset_x = 0         # em caracteres
        self.linhas_visiveis = max(1, int(linhas_visiveis))
        self.input_ativo = False

        # Último rect do editor (para clique/scroll)
        self._last_editor_rect = None

        # Scrollbar vertical (visual + drag)
        self._vtrack_rect = None         # trilho
        self._vthumb_rect = None         # "thumb"
        self._vdragging = False
        self._vdrag_offset = 0           # distância do mouse até o topo da thumb ao iniciar drag
        self._v_ctx = None               # contexto do scroll: dict com viewport_h, content_h, track_top, track_h, thumb_h

    # --------------------- API pública ---------------------
    def set_exercicio(self, exercicio):
        self.exercicio = exercicio
        self.reset()

    def reset(self):
        self.input_text = [""]
        self.cursor_pos = [0, 0]
        self.scroll_offset_y = 0
        self.scroll_offset_x = 0
        self.input_ativo = False
        self._last_editor_rect = None
        self._vtrack_rect = None
        self._vthumb_rect = None
        self._vdragging = False
        self._v_ctx = None

    def can_submit(self):
        return len(self.get_codigo_usuario().strip()) > 0

    def get_codigo_usuario(self):
        return "\n".join(self.input_text).rstrip()

    # --------------------- Utilitários ---------------------
    @staticmethod
    def clamp(val, mini, maxi):
        return max(mini, min(val, maxi))

    @staticmethod
    def quebrar_texto(texto, fonte, largura_max):
        palavras = (texto or "").split(' ')
        linhas = []
        linha = ''
        for palavra in palavras:
            teste = linha + palavra + ' '
            if fonte.size(teste)[0] > largura_max:
                linhas.append(linha.strip())
                linha = palavra + ' '
            else:
                linha = teste
        if linha.strip():
            linhas.append(linha.strip())
        return linhas

    @staticmethod
    def ajustar_fonte_para_caber(texto, fonte_base, largura_max, altura_max, min_font=13, espacamento=4):
        font_size = fonte_base.get_height()
        fonte = fonte_base
        while font_size >= min_font:
            linhas = DissertativeView.quebrar_texto(texto, fonte, largura_max)
            total_h = len(linhas) * (fonte.get_height() + espacamento)
            if total_h <= altura_max:
                return fonte, linhas
            font_size -= 1
            fonte = pygame.font.SysFont('Consolas', font_size)
        linhas = DissertativeView.quebrar_texto(texto, fonte, largura_max)
        max_linhas = max(1, altura_max // (fonte.get_height() + espacamento))
        if len(linhas) > max_linhas:
            linhas = linhas[:max_linhas-1] + ["..."]
        return fonte, linhas

    def ajustar_scroll_horizontal_para_cursor(self, largura_caixa):
        """Mantém o cursor visível horizontalmente dentro da caixa."""
        linha, coluna = self.cursor_pos
        texto = self.input_text[linha]
        texto_visivel = texto[self.scroll_offset_x:coluna]
        px_cursor = self.fonte_editor.size(texto_visivel)[0]
        while px_cursor > largura_caixa and self.scroll_offset_x < len(texto):
            self.scroll_offset_x += 1
            texto_visivel = texto[self.scroll_offset_x:coluna]
            px_cursor = self.fonte_editor.size(texto_visivel)[0]
        while px_cursor < 0 and self.scroll_offset_x > 0:
            self.scroll_offset_x -= 1
            texto_visivel = texto[self.scroll_offset_x:coluna]
            px_cursor = self.fonte_editor.size(texto_visivel)[0]

    # --------------------- Render ---------------------
    def draw(self, tela, content_rect, feedback_ativo=False):
        if not self.exercicio:
            return

        largura_max = content_rect.w
        yy = content_rect.y

        # Pergunta
        fonte_pergunta, linhas_pergunta = self.ajustar_fonte_para_caber(
            self.exercicio.get_pergunta(), self.fonte_pequena, largura_max, content_rect.h // 3
        )
        for linha in linhas_pergunta:
            tela.blit(fonte_pergunta.render(linha, True, (255, 255, 255)), (content_rect.x, yy))
            yy += fonte_pergunta.get_height() + 2

        # Dica
        fonte_dica, linhas_dica = self.ajustar_fonte_para_caber(
            f"Dica: {self.exercicio.get_dicas()}", self.fonte_pequena, largura_max, content_rect.h // 4
        )
        for linha in linhas_dica:
            tela.blit(fonte_dica.render(linha, True, (180, 180, 0)), (content_rect.x, yy))
            yy += fonte_dica.get_height() + 2

        # Editor (viewport)
        CAIXA_OFFSET = 40
        editor_h = self.linhas_visiveis * self.editor_lh + 16
        caixa = pygame.Rect(content_rect.x, yy + CAIXA_OFFSET, content_rect.w, editor_h)
        self._last_editor_rect = caixa

        # Fundo/borda
        pygame.draw.rect(tela, (52, 56, 64), caixa)
        pygame.draw.rect(tela, (70, 120, 200), caixa, 2)

        # Área útil de texto (para medir largura)
        largura_caixa_texto = caixa.w - 30

        # Linhas visíveis
        total_linhas = len(self.input_text)
        ini = self.scroll_offset_y
        fim = min(self.scroll_offset_y + self.linhas_visiveis, total_linhas)

        for idx in range(ini, fim):
            y_linha = caixa.y + (idx - self.scroll_offset_y) * self.editor_lh + 6

            # Numeração
            num_surface = self.fonte_editor.render(str(idx+1).rjust(2), True, (90, 160, 220))
            tela.blit(num_surface, (caixa.x-26, y_linha))

            # Destaque da linha do cursor
            if idx == self.cursor_pos[0]:
                pygame.draw.rect(tela, (38, 54, 92), (caixa.x+6, y_linha-2, largura_caixa_texto, self.editor_lh))

            # Texto respeitando scroll_x
            linha_texto = self.input_text[idx]
            texto_visivel = linha_texto[self.scroll_offset_x:]
            while self.fonte_editor.size(texto_visivel)[0] > largura_caixa_texto and len(texto_visivel) > 0:
                texto_visivel = texto_visivel[:-1]

            texto_surface = self.fonte_editor.render(texto_visivel, True, (255, 255, 255))
            tela.blit(texto_surface, (caixa.x+18, y_linha))

        # Cursor piscando
        if self.input_ativo and ini <= self.cursor_pos[0] < fim:
            tempo = pygame.time.get_ticks()
            if (tempo // 500) % 2 == 0:
                y_cursor = caixa.y + (self.cursor_pos[0] - self.scroll_offset_y) * self.editor_lh + 6
                linha_atual = self.input_text[self.cursor_pos[0]]
                texto_ate_cursor = linha_atual[self.scroll_offset_x:self.cursor_pos[1]]
                cursor_x = caixa.x + 18 + self.fonte_editor.size(texto_ate_cursor)[0]
                pygame.draw.line(tela, (0, 255, 0), (cursor_x, y_cursor+4), (cursor_x, y_cursor+self.editor_lh-6), 2)

        # ---------- SCROLLBAR VERTICAL (efeito visual tipo introdução) ----------
        self._vtrack_rect = None
        self._vthumb_rect = None
        self._v_ctx = None

        viewport_h = self.linhas_visiveis * self.editor_lh  # altura útil (sem padding)
        content_h = max(1, total_linhas) * self.editor_lh
        if content_h > viewport_h:
            track_x = caixa.right - 8
            track_w = 6
            track_top = caixa.y + 4
            track_h = editor_h - 8
            self._vtrack_rect = pygame.Rect(track_x, track_top, track_w, track_h)
            pygame.draw.rect(tela, (60, 70, 90), self._vtrack_rect, border_radius=4)

            # Tamanho da thumb (mesma ideia da introdução)
            ratio = viewport_h / content_h
            thumb_h = max(24, int(viewport_h * ratio))
            # Posição da thumb mapeando scroll em linhas -> pixels
            scroll_px = self.scroll_offset_y * self.editor_lh
            max_scroll_px = max(1, content_h - viewport_h)
            thumb_top = track_top + int((scroll_px * (track_h - thumb_h)) / max_scroll_px)
            self._vthumb_rect = pygame.Rect(track_x, thumb_top, track_w, thumb_h)
            pygame.draw.rect(tela, (120, 180, 255), self._vthumb_rect, border_radius=4)

            # Contexto para o drag
            self._v_ctx = {
                "viewport_h": viewport_h,
                "content_h": content_h,
                "track_top": track_top,
                "track_h": track_h,
                "thumb_h": thumb_h
            }

    # --------------------- Eventos ---------------------
    def handle_event(self, evento, feedback_ativo=False):
        if feedback_ativo:
            return

        # Clique dentro do editor: ativa e posiciona cursor
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self._last_editor_rect and self._last_editor_rect.collidepoint(evento.pos):
                self.input_ativo = True
                x, y = evento.pos
                linha_clicada = (y - self._last_editor_rect.y - 6) // self.editor_lh + self.scroll_offset_y
                linha_clicada = self.clamp(int(linha_clicada), 0, len(self.input_text)-1)

                texto = self.input_text[linha_clicada]
                x_rel = x - (self._last_editor_rect.x + 18)
                if x_rel <= 0:
                    col = self.scroll_offset_x
                else:
                    col = self.scroll_offset_x
                    while col <= len(texto):
                        width = self.fonte_editor.size(texto[self.scroll_offset_x:col])[0]
                        if width > x_rel:
                            break
                        col += 1
                    if col > 0:
                        col -= 1
                self.cursor_pos = [linha_clicada, self.clamp(col, 0, len(texto))]

            # Drag da thumb da barra vertical
            if evento.button == 1 and self._vthumb_rect and self._vthumb_rect.collidepoint(evento.pos):
                self._vdragging = True
                self._vdrag_offset = evento.pos[1] - self._vthumb_rect.y

        elif evento.type == pygame.MOUSEMOTION:
            # Arrastando a thumb vertical
            if self._vdragging and self._v_ctx and self._vtrack_rect and self._vthumb_rect:
                track_top = self._v_ctx["track_top"]
                track_h = self._v_ctx["track_h"]
                thumb_h = self._v_ctx["thumb_h"]
                viewport_h = self._v_ctx["viewport_h"]
                content_h = self._v_ctx["content_h"]

                new_thumb_y = evento.pos[1] - self._vdrag_offset
                new_thumb_y = self.clamp(new_thumb_y, track_top, track_top + track_h - thumb_h)
                self._vthumb_rect.y = new_thumb_y

                # Mapeia posição da thumb -> scroll em linhas
                perc = (new_thumb_y - track_top) / max(1, (track_h - thumb_h))
                max_scroll_px = max(1, content_h - viewport_h)
                scroll_px = int(perc * max_scroll_px)
                self.scroll_offset_y = self.clamp(scroll_px // self.editor_lh, 0, max(0, len(self.input_text) - self.linhas_visiveis))

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and self._vdragging:
                self._vdragging = False

        # Rodinha do mouse: vertical (efeito visual igual ao da introdução)
        elif evento.type == pygame.MOUSEWHEEL:
            mouse_sobre_editor = self._last_editor_rect and self._last_editor_rect.collidepoint(pygame.mouse.get_pos())
            if self.input_ativo or mouse_sobre_editor:
                # passo em "linhas" por notch (ajuste fino)
                step_lines = max(1, self.linhas_visiveis // 3)  # 1~3 linhas por notch
                if evento.y != 0:
                    max_y = max(0, len(self.input_text) - self.linhas_visiveis)
                    self.scroll_offset_y = self.clamp(self.scroll_offset_y - (evento.y * step_lines), 0, max_y)

                # Mantém o horizontal existente (se já estava funcionando pra você)
                # nativo pelo evento.x ou Shift + scroll vertical como fallback
                mods = pygame.key.get_mods()
                delta_h = 0
                if evento.x != 0:
                    delta_h = evento.x
                elif (mods & pygame.KMOD_SHIFT) and evento.y != 0:
                    delta_h = evento.y
                if delta_h != 0:
                    passo_cols = 4
                    self.scroll_offset_x = max(0, self.scroll_offset_x - int(delta_h * passo_cols))

        # Teclado
        elif evento.type == pygame.KEYDOWN and self.input_ativo:
            linha, coluna = self.cursor_pos

            if evento.key == pygame.K_RETURN:
                self.input_text.insert(linha + 1, self.input_text[linha][coluna:])
                self.input_text[linha] = self.input_text[linha][:coluna]
                linha += 1
                coluna = 0
                self.scroll_offset_x = 0

            elif evento.key == pygame.K_BACKSPACE:
                if coluna > 0:
                    self.input_text[linha] = self.input_text[linha][:coluna-1] + self.input_text[linha][coluna:]
                    coluna -= 1
                elif linha > 0:
                    prev_len = len(self.input_text[linha-1])
                    self.input_text[linha-1] += self.input_text[linha]
                    self.input_text.pop(linha)
                    linha -= 1
                    coluna = prev_len
                    self.scroll_offset_x = 0

            elif evento.key == pygame.K_TAB:
                self.input_text[linha] = self.input_text[linha][:coluna] + "    " + self.input_text[linha][coluna:]
                coluna += 4

            elif evento.key == pygame.K_LEFT:
                if coluna > 0:
                    coluna -= 1
                elif linha > 0:
                    linha -= 1
                    coluna = len(self.input_text[linha])

            elif evento.key == pygame.K_RIGHT:
                if coluna < len(self.input_text[linha]):
                    coluna += 1
                elif linha < len(self.input_text) - 1:
                    linha += 1
                    coluna = 0

            elif evento.key == pygame.K_UP:
                if linha > 0:
                    linha -= 1
                    coluna = min(coluna, len(self.input_text[linha]))
                    self.scroll_offset_x = 0

            elif evento.key == pygame.K_DOWN:
                if linha < len(self.input_text)-1:
                    linha += 1
                    coluna = min(coluna, len(self.input_text[linha]))
                    self.scroll_offset_x = 0

            else:
                if evento.unicode and evento.unicode.isprintable():
                    self.input_text[linha] = self.input_text[linha][:coluna] + evento.unicode + self.input_text[linha][coluna:]
                    coluna += 1

            # Normaliza e mantém visível
            linha = self.clamp(linha, 0, len(self.input_text)-1)
            coluna = self.clamp(coluna, 0, len(self.input_text[linha]))
            self.cursor_pos = [linha, coluna]

            # Scroll vertical para manter cursor visível
            if self.cursor_pos[0] < self.scroll_offset_y:
                self.scroll_offset_y = self.cursor_pos[0]
            elif self.cursor_pos[0] >= self.scroll_offset_y + self.linhas_visiveis:
                self.scroll_offset_y = self.cursor_pos[0] - self.linhas_visiveis + 1

            # Scroll horizontal para manter cursor visível
            if self._last_editor_rect:
                largura_caixa_texto = self._last_editor_rect.w - 30
                self.ajustar_scroll_horizontal_para_cursor(largura_caixa_texto)
