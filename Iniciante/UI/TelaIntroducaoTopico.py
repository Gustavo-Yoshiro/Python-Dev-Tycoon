import pygame
import os
import re

class TelaIntroducaoTopico:
    def __init__(self, largura, altura, nome_topico, descricao, on_confirmar, jogador=None):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.descricao = descricao or ""
        self.on_confirmar = on_confirmar
        self.jogador = jogador
        self.nome_jogador = jogador.get_nome() if jogador else "Visitante"
        self.painel_visivel = True

        # Arrastar painel
        self.dragging = False
        self.drag_offset = (0, 0)

        pygame.font.init()
        self.font_size_titulo = 28
        self.font_size = 22
        self.font_size_pequena = 20
        self.fonte_titulo = pygame.font.SysFont('Consolas', self.font_size_titulo, bold=True)
        self.fonte = pygame.font.SysFont('Consolas', self.font_size)
        self.fonte_pequena = pygame.font.SysFont('Consolas', self.font_size_pequena)
        self.fonte_mono = pygame.font.SysFont('Consolas', 18)
        self.fonte_mono_small = pygame.font.SysFont('Consolas', 16)
        # ↓ fontes menores para os EXEMPLOS (cabe mais no card)
        self.fonte_mono_card = pygame.font.SysFont('Consolas', 14)
        self.fonte_legenda = pygame.font.SysFont('Consolas', 16, italic=True)
        self.fonte_legenda_small = pygame.font.SysFont('Consolas', 14, italic=True)

        # Painel central
        self.rect_painel = pygame.Rect(
            int(largura * 0.25),
            int(altura * 0.13),
            int(largura * 0.54),
            int(altura * 0.66)
        )

        btn_w, btn_h = 200, 52
        self.rect_btn = pygame.Rect(
            self.rect_painel.x + (self.rect_painel.w - btn_w) // 2,
            self.rect_painel.bottom - btn_h - 28,
            btn_w,
            btn_h
        )

        # Pré-processa a descrição em (intro, exemplos[])
        self._intro_text, self._example_blocks = self._parse_descricao(self.descricao)

        # Scroll dos exemplos
        self.ex_scroll = 0
        self._ex_content_h = 0
        self._area_ex_rect = None
        self._ex_thumb_rect = None
        self._ex_dragging = False
        self._ex_drag_offset = 0
        self._cached_layout = None  # cache de layout (rects dos cards)

    # ------------------------ PARSER / LAYOUT ------------------------

    def _parse_descricao(self, texto):
        """
        Divide a descrição em:
        - intro_text (antes de 'Exemplo:' / 'Exemplos:')
        - example_blocks: lista de blocos (cada bloco é uma lista de linhas)
          Agrupa por linhas em branco.
        """
        split_regex = re.compile(r'\n\s*exemplos?:\s*\n', flags=re.IGNORECASE)
        parts = split_regex.split(texto, maxsplit=1)
        intro = parts[0].strip()

        blocks = []
        if len(parts) == 2:
            examples_raw = parts[1].strip()
            lines = examples_raw.replace('\r\n', '\n').replace('\r', '\n').split('\n')
            cur = []
            for ln in lines:
                if ln.strip() == "":
                    if cur:
                        blocks.append(cur)
                        cur = []
                else:
                    cur.append(ln)
            if cur:
                blocks.append(cur)

        return intro, blocks

    # ------------------------ TEXTO: QUEBRA E AJUSTE (MANTIDOS) ------------------------

    def quebrar_linha(self, texto, fonte, largura_max):
        linhas = []
        paragrafos = texto.split('\n')
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            atual = ""
            for palavra in palavras:
                teste = f"{atual} {palavra}" if atual else palavra
                if fonte.size(teste)[0] <= largura_max:
                    atual = teste
                else:
                    if atual:
                        linhas.append(atual)
                    atual = palavra
            if atual:
                linhas.append(atual)
        return linhas

    def ajustar_fonte_para_caber(self, texto, fonte_base, largura_max, altura_max, min_font=14):
        # Tenta reduzir a fonte até caber no painel
        font_size = fonte_base.get_height()
        fonte = fonte_base
        while font_size >= min_font:
            linhas = self.quebrar_linha(texto, fonte, largura_max)
            total_h = len(linhas) * (fonte.get_height() + 4)
            if total_h <= altura_max:
                return fonte, linhas
            font_size -= 1
            fonte = pygame.font.SysFont('Consolas', font_size)
        # Se não couber de jeito nenhum, retorna no mínimo e corta linhas
        linhas = self.quebrar_linha(texto, fonte, largura_max)
        max_linhas = max(1, altura_max // (fonte.get_height() + 4))
        if len(linhas) > max_linhas:
            linhas = linhas[:max_linhas-1] + ["..."]
        return fonte, linhas

    # ------------------------ RENDER HELPERS ------------------------

    def _draw_tag(self, tela, text, x, y, pad_x=8, pad_y=4, bg=(38,58,94), fg=(200,230,255)):
        s_txt = self.fonte_pequena.render(text, True, fg)
        w = s_txt.get_width() + pad_x*2
        h = s_txt.get_height() + pad_y*2
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(tela, bg, rect, border_radius=8)
        pygame.draw.rect(tela, (90, 170, 255), rect, 2, border_radius=8)
        tela.blit(s_txt, (x + pad_x, y + pad_y))
        return rect

    def _draw_minitag(self, tela, text, x, y, pad_x=6, pad_y=2, bg=(36,70,36), fg=(200,255,200)):
        s_txt = self.fonte_legenda_small.render(text, True, fg)
        w = s_txt.get_width() + pad_x*2
        h = s_txt.get_height() + pad_y*2
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(tela, bg, rect, border_radius=6)
        pygame.draw.rect(tela, (120, 200, 120), rect, 2, border_radius=6)
        tela.blit(s_txt, (x + pad_x, y + pad_y))
        return rect

    def _color_for_token(self, token):
        kw = {"print()", "input()", "if", "else", "elif", "for", "while",
              "True", "False", "variáveis", "variável", "int", "float",
              "str", "bool", "and", "or", "not"}
        token_clean = token.strip(",.;:!?()[]{}")
        if token_clean in kw:
            return (160, 220, 255)
        if token_clean in {"dados", "entrada", "saída", "console"}:
            return (230, 230, 120)
        return (255, 255, 255)

    def _draw_colored_line(self, tela, text, x, y, fonte):
        cur_x = x
        space_w = fonte.size(" ")[0]
        for raw in text.split(" "):
            color = self._color_for_token(raw)
            r = fonte.render(raw, True, color)
            tela.blit(r, (cur_x, y))
            cur_x += r.get_width() + space_w

    def _draw_code_line(self, tela, text, x, y, fonte):
        keywords = {"if","else","elif","for","while","in","print","input","range","int","float",
                    "str","bool","True","False","and","or","not","def","return","None"}
        s = text
        i = 0
        cur_x = x

        def draw_chunk(chunk, color):
            nonlocal cur_x
            if not chunk:
                return
            img = fonte.render(chunk, True, color)
            tela.blit(img, (cur_x, y))
            cur_x += img.get_width()

        while i < len(s):
            ch = s[i]
            # strings
            if ch in ("'", '"'):
                quote = ch
                j = i + 1
                while j < len(s):
                    if s[j] == quote and s[j-1] != "\\":
                        j += 1
                        break
                    j += 1
                draw_chunk(s[i:j], (230,230,120))
                i = j
                continue
            # números
            if ch.isdigit():
                j = i+1
                while j < len(s) and (s[j].isdigit() or s[j] == "."):
                    j += 1
                draw_chunk(s[i:j], (150, 220, 255))
                i = j
                continue
            # palavras/identificadores
            if ch.isalpha() or ch == "_":
                j = i+1
                while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                    j += 1
                tok = s[i:j]
                color = (160,220,255) if tok in keywords else (230,230,230)
                draw_chunk(tok, color)
                i = j
                continue
            # espaço/pontuação
            draw_chunk(ch, (230,230,230))
            i += 1

    def _measure_card_height(self, lines, col_w):
        pad = 12
        h = pad  # top padding
        for ln in lines:
            ln_stripped = ln.strip()
            if ln_stripped.lower().startswith("saída:"):
                # tag + saída
                tag_h = self.fonte_legenda_small.get_height() + 2*2  # pad_y=2
                h += tag_h + 4
                out_txt = ln_stripped.split(":", 1)[1].strip()
                out_h = self.fonte_legenda_small.get_height()
                h += out_h + 6
            else:
                # diminuir fonte dos exemplos (14)
                font = self.fonte_mono_card
                text = ln.replace("\t", "    ")
                # encolhe um pouco se necessário (limite 12)
                max_w = col_w - 24
                fsz = font.get_height()
                tmp_font = font
                while tmp_font.size(text)[0] > max_w and fsz > 12:
                    fsz -= 1
                    tmp_font = pygame.font.SysFont('Consolas', fsz)
                h += tmp_font.get_height() + 6
        h += pad  # bottom padding
        return h

    def _draw_example_card(self, tela, rect, lines):
        pygame.draw.rect(tela, (28, 34, 48), rect, border_radius=12)
        pygame.draw.rect(tela, (80, 120, 200), rect, 2, border_radius=12)

        pad = 12
        x = rect.x + pad
        y = rect.y + pad
        max_w = rect.w - pad*2

        for ln in lines:
            ln_stripped = ln.strip()
            if ln_stripped.lower().startswith("saída:"):
                tag_rect = self._draw_minitag(tela, "Saída", x, y, bg=(36,70,36), fg=(200,255,200))
                y = tag_rect.bottom + 4
                out_txt = ln_stripped.split(":", 1)[1].strip()
                out_img = self.fonte_legenda_small.render(out_txt if out_txt else "—", True, (200,255,200))
                tela.blit(out_img, (x, y))
                y += out_img.get_height() + 6
            else:
                # código com fonte 14 (diminui até 12 se precisar)
                text = ln.replace("\t", "    ")
                tmp_font = self.fonte_mono_card
                fsz = tmp_font.get_height()
                while tmp_font.size(text)[0] > max_w and fsz > 12:
                    fsz -= 1
                    tmp_font = pygame.font.SysFont('Consolas', fsz)
                # se ainda não coube, corta e põe "…"
                while tmp_font.size(text)[0] > max_w and len(text) > 1:
                    text = text[:-1]
                if tmp_font.size(text)[0] > max_w and len(text) > 1:
                    text = text[:-1] + "…"
                self._draw_code_line(tela, text, x, y, tmp_font)
                y += tmp_font.get_height() + 6

    def _layout_examples(self, area_ex, cols, gap=12):
        """Calcula retângulos dos cards em colunas (com alturas reais), e a altura total para scroll."""
        if not self._example_blocks:
            self._cached_layout = ([], 0)
            return [], 0

        col_w = (area_ex.w - (gap * (cols - 1))) // cols
        col_xs = [area_ex.x + i * (col_w + gap) for i in range(cols)]
        col_ys = [area_ex.y for _ in range(cols)]

        rects = []
        for block in self._example_blocks:
            col = min(range(cols), key=lambda c: col_ys[c])
            h = self._measure_card_height(block, col_w)
            r = pygame.Rect(col_xs[col], col_ys[col], col_w, h)
            rects.append((r, block))
            col_ys[col] += h + gap

        content_h = max(col_ys) - area_ex.y if rects else 0
        self._cached_layout = (rects, content_h)
        return rects, content_h

    # ------------------------ DESENHO ------------------------

    def desenhar(self, tela):
        if not self.painel_visivel:
            return

        painel = self.rect_painel
        painel_surf = pygame.Surface((painel.w, painel.h), pygame.SRCALPHA)
        pygame.draw.rect(painel_surf, (18, 24, 32, 210), (0, 0, painel.w, painel.h), border_radius=16)
        tela.blit(painel_surf, (painel.x, painel.y))
        pygame.draw.rect(tela, (42, 103, 188), painel, 6, border_radius=16)

        # --- Barra azul do topo ---
        header_h = 50
        header_rect = pygame.Rect(painel.x, painel.y, painel.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header_rect, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255),
                         (painel.x, painel.y + header_h),
                         (painel.x + painel.w, painel.y + header_h), 2)

        # Botão X no header
        tam = 32
        espaco = 10
        self.rect_x = pygame.Rect(self.rect_painel.right - tam - espaco,
                                  self.rect_painel.y + espaco, tam, tam)
        pygame.draw.circle(tela, (255, 100, 100), self.rect_x.center, tam // 2)
        x_mark = self.fonte_pequena.render("x", True, (40, 0, 0))
        tela.blit(x_mark, (self.rect_x.x + (tam - x_mark.get_width()) // 2,
                           self.rect_x.y + (tam - x_mark.get_height()) // 2))

        # Título centralizado
        titulo = f"Tópico: {self.nome_topico}"
        titulo_surface = self.fonte_titulo.render(titulo, True, (130, 220, 255))
        titulo_rect = titulo_surface.get_rect(center=(painel.centerx, painel.y + header_h // 2 + 2))
        tela.blit(titulo_surface, titulo_rect)

        # Área do conteúdo
        margem_x = 44
        margem_y = 38
        x = painel.x + margem_x
        y = painel.y + header_h + margem_y

        # Usuário (tag)
        usuario_txt = f"Usuário: {self.nome_jogador}"
        tag_rect = self._draw_tag(tela, usuario_txt, x, y)
        y = tag_rect.bottom + 8

        # divisória
        pygame.draw.line(tela, (80, 120, 180), (x, y), (painel.x + painel.w - margem_x, y), 2)
        y += 12

        largura_max = painel.w - 2 * margem_x
        altura_max_total = self.rect_btn.y - y  # espaço total até o botão

        # espaço dividido: intro (58%) e exemplos (resto) quando houver exemplos
        tem_exemplos = len(self._example_blocks) > 0
        if tem_exemplos:
            altura_intro = int(altura_max_total * 0.58)
            altura_ex = altura_max_total - altura_intro - 8
        else:
            altura_intro = altura_max_total
            altura_ex = 0

        # --- INTRO: com cores em palavras-chave ---
        fonte_otimizada, linhas_intro = self.ajustar_fonte_para_caber(self._intro_text, self.fonte_pequena, largura_max, altura_intro)
        for linha in linhas_intro:
            self._draw_colored_line(tela, linha, x, y, fonte_otimizada)
            y += fonte_otimizada.get_height() + 4

        # --- EXEMPLOS: área com SCROLL ---
        self._area_ex_rect = None
        self._ex_thumb_rect = None

        if tem_exemplos and altura_ex > 60:
            y += 8
            label = self.fonte.render("Exemplos", True, (200, 220, 255))
            tela.blit(label, (x, y))
            y += label.get_height() + 8

            area_ex = pygame.Rect(x, y, largura_max, altura_ex - (label.get_height() + 8))
            self._area_ex_rect = area_ex

            cols = 2 if (len(self._example_blocks) >= 4 and area_ex.w >= 520) else 1
            rects, content_h = self._layout_examples(area_ex, cols)
            self._ex_content_h = content_h

            # superfície rolável
            surf_h = max(content_h, area_ex.h)
            ex_surf = pygame.Surface((area_ex.w, surf_h), pygame.SRCALPHA)

            # desenha os cards dentro da superfície (posições relativas)
            for r, block in rects:
                local_rect = pygame.Rect(r.x - area_ex.x, r.y - area_ex.y, r.w, r.h)
                self._draw_example_card(ex_surf, local_rect, block)

            # limita o scroll
            max_scroll = max(0, content_h - area_ex.h)
            if self.ex_scroll > max_scroll:
                self.ex_scroll = max_scroll
            if self.ex_scroll < 0:
                self.ex_scroll = 0

            # recorte e blit
            src_rect = pygame.Rect(0, self.ex_scroll, area_ex.w, area_ex.h)
            tela.blit(ex_surf, area_ex.topleft, src_rect)

            # scroll bar
            if content_h > area_ex.h:
                track_x = area_ex.right - 8
                track_w = 6
                pygame.draw.rect(tela, (60, 70, 90), (track_x, area_ex.y, track_w, area_ex.h), border_radius=4)

                ratio = area_ex.h / content_h
                thumb_h = max(24, int(area_ex.h * ratio))
                thumb_y = area_ex.y + int(self.ex_scroll * (area_ex.h - thumb_h) / (content_h - area_ex.h))
                thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
                pygame.draw.rect(tela, (120, 180, 255), thumb_rect, border_radius=4)
                self._ex_thumb_rect = thumb_rect

        # Botão "ENTENDIDO"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_hover = self.rect_btn.collidepoint(mouse_x, mouse_y)
        cor_texto = (255,255,255)
        fonte_botao = self.fonte
        cor_btn = (0, 180, 80) if botao_hover else (0, 150, 200)
        if botao_hover:
            cor_texto = (255, 230, 80)
            fonte_botao = pygame.font.SysFont('Consolas', 22, bold=True)
        pygame.draw.rect(tela, cor_btn, self.rect_btn, border_radius=24)
        botao_surface = fonte_botao.render("ENTENDIDO", True, cor_texto)
        tela.blit(
            botao_surface,
            (
                self.rect_btn.x + (self.rect_btn.w - botao_surface.get_width()) // 2,
                self.rect_btn.y + (self.rect_btn.h - botao_surface.get_height()) // 2
            )
        )

    # ------------------------ EVENTOS ------------------------

    def tratar_eventos(self, eventos):
        if not self.painel_visivel:
            return
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # fechar
                if hasattr(self, "rect_x") and self.rect_x.collidepoint(x, y):
                    self.painel_visivel = False
                    return
                # arrastar painel
                if evento.button == 1:
                    header_h = 50
                    header_rect = pygame.Rect(self.rect_painel.x, self.rect_painel.y, self.rect_painel.w, header_h)
                    if header_rect.collidepoint(evento.pos):
                        self.dragging = True
                        mx, my = evento.pos
                        self.drag_offset = (mx - self.rect_painel.x, my - self.rect_painel.y)
                # scroll bar drag
                if evento.button == 1 and self._ex_thumb_rect and self._ex_thumb_rect.collidepoint(x, y):
                    self._ex_dragging = True
                    self._ex_drag_offset = y - self._ex_thumb_rect.y

                # botão "ENTENDIDO"
                if self.rect_btn.collidepoint(x, y):
                    if self.on_confirmar:
                        self.on_confirmar()

            elif evento.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mx, my = evento.pos
                    dx, dy = self.drag_offset
                    self.rect_painel.x = mx - dx
                    self.rect_painel.y = my - dy
                    self.rect_btn.x = self.rect_painel.x + (self.rect_painel.w - self.rect_btn.w) // 2
                    self.rect_btn.y = self.rect_painel.bottom - self.rect_btn.h - 28

                # drag da barra de rolagem
                if self._ex_dragging and self._area_ex_rect and self._ex_thumb_rect:
                    ax, ay, aw, ah = self._area_ex_rect
                    content_h = max(self._ex_content_h, ah)
                    if self._ex_content_h > ah:
                        thumb_h = self._ex_thumb_rect.h
                        new_thumb_y = max(ay, min(ay + ah - thumb_h, evento.pos[1] - self._ex_drag_offset))
                        self._ex_thumb_rect.y = new_thumb_y
                        # mapeia thumb_y -> scroll
                        perc = (new_thumb_y - ay) / max(1, (ah - thumb_h))
                        self.ex_scroll = int(perc * (self._ex_content_h - ah))

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and self.dragging:
                    self.dragging = False
                if evento.button == 1 and self._ex_dragging:
                    self._ex_dragging = False

            # scroll do mouse (pygame 2)
            elif evento.type == pygame.MOUSEWHEEL:
                if self._area_ex_rect:
                    mx, my = pygame.mouse.get_pos()
                    if self._area_ex_rect.collidepoint(mx, my) and self._ex_content_h > self._area_ex_rect.h:
                        passo = 48
                        # evento.y > 0 = roda pra cima
                        self.ex_scroll -= evento.y * passo
                        self.ex_scroll = max(0, min(self.ex_scroll, self._ex_content_h - self._area_ex_rect.h))
