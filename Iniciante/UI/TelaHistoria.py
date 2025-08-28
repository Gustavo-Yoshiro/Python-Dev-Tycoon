# Iniciante/UI/TelaHistoria.py
import pygame
import random
import string
import math


class TelaHistoria:
    """
    Tela de história com:
      - Fundo animado "code rain"
      - Painéis translúcidos p/ legibilidade + sombra no texto
      - Título com glow sutil
      - Typewriter + cursor
      - Dots de páginas clicáveis e setas (← →)
      - Botão pulsante
      - Interação na pág. 2: escolher estilo (backend/frontend/full-stack)
      - Pular com tecla S
    """
    def __init__(self, largura, altura, on_confirmar):
        self.largura = largura
        self.altura = altura
        self.on_confirmar = on_confirmar

        # --- Fontes
        self.fonte_titulo = pygame.font.SysFont('Arial', 56, bold=True)
        self.fonte_texto  = pygame.font.SysFont('Arial', 27)
        self.fonte_ui     = pygame.font.SysFont('Arial', 20, bold=True)
        self.fonte_code   = pygame.font.SysFont('Consolas', 18, bold=True)

        # --- Cores / estilos
        self.col_txt      = (235, 240, 248)
        self.col_txt_dim  = (210, 218, 230)
        self.col_panel    = (16, 22, 34, 200)     # atrás do texto
        self.col_panel_t  = (18, 26, 40, 160)     # atrás do título
        self.col_panel_bd = (90, 150, 255, 130)   # borda do painel
        self.col_dot_on   = (120, 190, 255)
        self.col_dot_off  = (80, 105, 140)

        # --- Fundo gradiente + code rain
        self.bg_surface = pygame.Surface((largura, altura))
        self._fill_vertical_gradient(self.bg_surface, (8, 14, 26), (14, 22, 38))
        self.rain_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self._init_code_rain()

        # --- Botão continuar
        self.botao_rect = pygame.Rect(self.largura // 2 - 160, self.altura - 110, 320, 58)
        self.cor_btn = (0, 122, 200)
        self.cor_btn_hover = (0, 150, 255)

        # --- Setas (navegação)
        self.arrow_prev = pygame.Rect(32, self.altura//2 - 36, 64, 72)
        self.arrow_next = pygame.Rect(self.largura - 96, self.altura//2 - 36, 64, 72)

        # --- Páginas
        self.paginas = [
            {
                "titulo": "O Início da Jornada",
                "texto": (
                    "Você começa pequeno: um computador, uma ideia e vontade de aprender. "
                    "Aqui, prática vira progresso. A cada tópico, você entende um recurso, "
                    "resolve desafios e desbloqueia minigames."
                )
            },
            {
                "titulo": "Escolha seu Estilo",
                "texto": (
                    "Você vai escrever código, depurar bugs e transformar lógica em experiência. "
                    "Cada acerto soma pontos; cada erro ensina. Escolha um estilo que combina com você:"
                )
            },
            {
                "titulo": "Como Avançar",
                "texto": (
                    "Complete 4 desafios + 1 minigame por fase para avançar. "
                    "Dicas aparecem quando precisar. Respire, tente, acerte. "
                    "Pronto para começar?"
                )
            },
        ]
        self.idx_pagina = 0

        # --- Geometria do conteúdo (DEFINIR ANTES do wrap-cache!)
        self.max_w = int(self.largura * 0.70)
        self.content_x = self.largura // 2 - self.max_w // 2
        self.content_y = 180
        self.content_h = 260  # altura da área de texto

        # --- Interação pág. 2 (opcional)
        self.escolha_estilo = None
        self._opt_backend_rect   = pygame.Rect(0, 0, 210, 50)
        self._opt_frontend_rect  = pygame.Rect(0, 0, 210, 50)
        self._opt_fullstack_rect = pygame.Rect(0, 0, 210, 50)

        # --- Typewriter
        self._type_speed_cps = 52.0  # chars/s
        self._shown_chars = 0.0
        self._cursor_timer = 0.0

        # Cache de quebra de linha
        self._wrap_cache = {}
        self._rebuild_wrap_cache()  # agora max_w já existe

        # Tempo/efeitos
        self._last_ms = pygame.time.get_ticks()
        self._fade_alpha = 255        # primeira página inicia com fade
        self._fade_in_speed = 600.0
        self._pulse_phase = 0.0

        # Dots clicáveis
        self._dot_rects = []

    # ============================= Utils visuais =============================
    def _fill_vertical_gradient(self, surf, color_top, color_bottom):
        w, h = surf.get_size()
        for y in range(h):
            t = y / max(h-1, 1)
            r = int(color_top[0]*(1-t) + color_bottom[0]*t)
            g = int(color_top[1]*(1-t) + color_bottom[1]*t)
            b = int(color_top[2]*(1-t) + color_bottom[2]*t)
            pygame.draw.line(surf, (r, g, b), (0, y), (w, y))

    def _draw_panel(self, tela, rect, fill_rgba, border_rgba, radius=16, border_w=2):
        surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, fill_rgba, surf.get_rect(), border_radius=radius)
        pygame.draw.rect(surf, border_rgba, surf.get_rect(), width=border_w, border_radius=radius)
        tela.blit(surf, rect.topleft)

    def _blit_text_with_shadow(self, tela, fonte, texto, cor, pos, shadow_offset=(2, 2)):
        shadow = fonte.render(texto, True, (0, 0, 0))
        tela.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
        surf = fonte.render(texto, True, cor)
        tela.blit(surf, pos)

    def _draw_title_glow(self, tela, texto, y):
        base = self.fonte_titulo.render(texto, True, (255, 255, 255))
        x = self.largura // 2 - base.get_width() // 2
        for r, a in ((2, 90), (4, 50), (6, 32)):
            gsurf = self.fonte_titulo.render(texto, True, (120, 200, 255))
            gsurf.set_alpha(a)
            tela.blit(gsurf, (x - r, y)); tela.blit(gsurf, (x + r, y))
            tela.blit(gsurf, (x, y - r)); tela.blit(gsurf, (x, y + r))
        self._blit_text_with_shadow(tela, self.fonte_titulo, texto, (255, 255, 255), (x, y))

    def _draw_vignette(self, tela):
        vign = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        pygame.draw.rect(vign, (0, 0, 0, 0), vign.get_rect(), 0)
        pygame.draw.rect(vign, (0, 0, 0, 120), vign.get_rect(), width=24, border_radius=16)
        tela.blit(vign, (0, 0), special_flags=pygame.BLEND_PREMULTIPLIED)

    # ============================== Code rain ================================
    def _init_code_rain(self):
        self.code_chars = list("01{}[]()<>=+-*/%#@$&" + string.ascii_letters)
        self._glyph_cache = {ch: self.fonte_code.render(ch, True, (120, 255, 140)) for ch in set(self.code_chars)}
        self._head_cache  = {ch: self.fonte_code.render(ch, True, (235, 255, 235)) for ch in set(self.code_chars)}
        self.gw, self.gh = self.fonte_code.size("A")
        self.cols = max(1, self.largura // max(1, self.gw))
        self.drops = []
        for c in range(self.cols):
            x = c * self.gw + (self.gw // 8)
            y = random.randint(-self.altura, 0)
            speed = random.uniform(70, 180)
            self.drops.append({"x": x, "y": y, "speed": speed, "char": random.choice(self.code_chars)})

    def _update_code_rain(self, dt):
        self.rain_surface.fill((0, 0, 0, 35), special_flags=pygame.BLEND_RGBA_SUB)
        for d in self.drops:
            d["y"] += d["speed"] * dt
            if d["y"] > self.altura + self.gh * 2:
                d["y"] = random.uniform(-self.altura * 0.3, 0)
                d["speed"] = random.uniform(70, 180)
            if random.random() < 0.08:
                d["char"] = random.choice(self.code_chars)
            ch = d["char"]
            self.rain_surface.blit(self._glyph_cache[ch], (d["x"], d["y"] - self.gh))
            self.rain_surface.blit(self._head_cache[ch],  (d["x"], d["y"]))

    # =========================== Texto / páginas ============================
    def _rebuild_wrap_cache(self):
        self._wrap_cache.clear()
        for i, pag in enumerate(self.paginas):
            linhas = self._wrap(pag["texto"], self.fonte_texto, self.max_w)
            self._wrap_cache[i] = linhas

    def _wrap(self, texto, fonte, largura_max):
        palavras = texto.split()
        linhas, linha = [], ""
        for p in palavras:
            teste = (linha + " " + p).strip()
            if fonte.size(teste)[0] <= largura_max:
                linha = teste
            else:
                if linha: linhas.append(linha)
                linha = p
        if linha:
            linhas.append(linha)
        return linhas

    def _page_text_len(self, idx):
        return len(" ".join(self._wrap_cache.get(idx, [])))

    def _draw_page_text_typewriter(self, tela, idx, dt):
        linhas_full = self._wrap_cache.get(idx, [])
        texto_full = " ".join(linhas_full)
        parcial = texto_full[:int(self._shown_chars)]

        # painel para legibilidade
        text_panel = pygame.Rect(self.content_x - 16, self.content_y - 14, self.max_w + 32, self.content_h + 28)
        self._draw_panel(tela, text_panel, self.col_panel, self.col_panel_bd, radius=16, border_w=2)

        # render parcial com wrap
        y = self.content_y
        linhas_parciais = self._wrap(parcial, self.fonte_texto, self.max_w)
        for linha in linhas_parciais:
            self._blit_text_with_shadow(tela, self.fonte_texto, linha, self.col_txt, (self.content_x, y))
            y += self.fonte_texto.get_height() + 8

        # cursor piscante
        total_chars = self._page_text_len(idx)
        self._cursor_timer += dt
        if int(self._cursor_timer * 2) % 2 == 0 and self._shown_chars < total_chars:
            cur = self.fonte_texto.render("▌", True, (255, 255, 255))
            tela.blit(cur, (self.content_x + self.fonte_texto.size(linhas_parciais[-1] if linhas_parciais else "")[0] + 4,
                            y - (self.fonte_texto.get_height() + 8)))

        # opções interativas na página 2
        if self.idx_pagina == 1:
            self._draw_style_options(tela)

    def _is_page_fully_shown(self):
        return self._shown_chars >= self._page_text_len(self.idx_pagina)

    def _reset_typewriter(self):
        self._shown_chars = 0.0
        self._cursor_timer = 0.0

    # =============== Interação (página 2: estilo visual) ====================
    def _style_btn(self, tela, rect, label, selected=False, hover=False):
        base_fill = (30, 42, 60, 220) if not selected else (50, 90, 140, 230)
        base_bd   = (110, 170, 255, 180) if (hover or selected) else (90, 120, 160, 160)
        self._draw_panel(tela, rect, base_fill, base_bd, radius=12, border_w=2)
        color = (255, 255, 255) if (hover or selected) else self.col_txt_dim
        txt = self.fonte_ui.render(label, True, color)
        tela.blit(txt, txt.get_rect(center=rect.center))

    def _draw_style_options(self, tela):
        gap = 16
        total_w = self._opt_backend_rect.w * 3 + gap * 2
        start_x = self.largura//2 - total_w//2
        y = self.content_y + self.content_h + 20

        self._opt_backend_rect.topleft   = (start_x, y)
        self._opt_frontend_rect.topleft  = (start_x + self._opt_backend_rect.w + gap, y)
        self._opt_fullstack_rect.topleft = (start_x + (self._opt_backend_rect.w + gap)*2, y)

        mx, my = pygame.mouse.get_pos()
        self._style_btn(tela, self._opt_backend_rect,  "Backend",
                        selected=(self.escolha_estilo=="backend"),
                        hover=self._opt_backend_rect.collidepoint(mx, my))
        self._style_btn(tela, self._opt_frontend_rect, "Frontend",
                        selected=(self.escolha_estilo=="frontend"),
                        hover=self._opt_frontend_rect.collidepoint(mx, my))
        self._style_btn(tela, self._opt_fullstack_rect,"Full-stack",
                        selected=(self.escolha_estilo=="fullstack"),
                        hover=self._opt_fullstack_rect.collidepoint(mx, my))

        tip = self.fonte_ui.render("Escolha opcional (visual): isso não altera o jogo agora.", True, (200, 200, 200))
        tela.blit(tip, (self.largura//2 - tip.get_width()//2, y + 58 + 10))

    # =============================== Flow ===================================
    def _next(self):
        if self.idx_pagina < len(self.paginas) - 1:
            self.idx_pagina += 1
            self._reset_typewriter()
            self._fade_alpha = 255
        else:
            self.on_confirmar()

    def _prev(self):
        if self.idx_pagina > 0:
            self.idx_pagina -= 1
            self._reset_typewriter()
            self._fade_alpha = 255

    # =============================== Eventos =================================
    def tratar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                # botão
                if self.botao_rect.collidepoint(e.pos):
                    if self._is_page_fully_shown(): self._next()
                    else: self._shown_chars = self._page_text_len(self.idx_pagina)
                # setas
                elif self.arrow_next.collidepoint(e.pos):
                    if self._is_page_fully_shown(): self._next()
                    else: self._shown_chars = self._page_text_len(self.idx_pagina)
                elif self.arrow_prev.collidepoint(e.pos):
                    self._prev()
                else:
                    # dots
                    for i, r in enumerate(self._dot_rects):
                        if r.collidepoint(e.pos):
                            if i != self.idx_pagina:
                                self.idx_pagina = i
                                self._reset_typewriter()
                                self._fade_alpha = 255
                            break
                    # clique no texto
                    text_panel = pygame.Rect(self.content_x - 16, self.content_y - 14, self.max_w + 32, self.content_h + 28)
                    if text_panel.collidepoint(e.pos):
                        if self._is_page_fully_shown(): self._next()
                        else: self._shown_chars = self._page_text_len(self.idx_pagina)
                    # escolhas pág. 2
                    if self.idx_pagina == 1:
                        if self._opt_backend_rect.collidepoint(e.pos):   self.escolha_estilo = "backend"
                        elif self._opt_frontend_rect.collidepoint(e.pos): self.escolha_estilo = "frontend"
                        elif self._opt_fullstack_rect.collidepoint(e.pos):self.escolha_estilo = "fullstack"

            elif e.type == pygame.KEYUP:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_RIGHT):
                    if self._is_page_fully_shown(): self._next()
                    else: self._shown_chars = self._page_text_len(self.idx_pagina)
                elif e.key in (pygame.K_LEFT, pygame.K_BACKSPACE):
                    self._prev()
                elif e.key == pygame.K_s:
                    self.on_confirmar()

    # ============================= Update + Draw =============================
    def _tick(self):
        now = pygame.time.get_ticks()
        dt = (now - self._last_ms) / 1000.0
        self._last_ms = now
        return max(0.0, min(dt, 0.1))

    def update(self, dt=None):
        if dt is None:
            dt = self._tick()
        self._update_code_rain(dt)

        total_chars = self._page_text_len(self.idx_pagina)
        self._shown_chars = min(self._shown_chars + self._type_speed_cps * dt, total_chars + 1)

        if self._fade_alpha > 0:
            self._fade_alpha = max(0, self._fade_alpha - (255 * dt * (1000.0 / self._fade_in_speed)))

        self._pulse_phase = (self._pulse_phase + dt) % 1000.0

    def desenhar(self, tela):
        self.update()

        # BG
        tela.blit(self.bg_surface, (0, 0))
        tela.blit(self.rain_surface, (0, 0))

        # Painel do título + glow
        title_rect = pygame.Rect(self.largura//2 - 520//2, 88 - 14, 520, 74)
        self._draw_panel(tela, title_rect, self.col_panel_t, self.col_panel_bd, radius=16, border_w=2)
        self._draw_title_glow(tela, self.paginas[self.idx_pagina]["titulo"], 88)

        # Texto com typewriter
        self._draw_page_text_typewriter(tela, self.idx_pagina, 0.0)

        # Dots + setas
        self._draw_page_dots(tela)
        self._draw_arrows(tela)

        # Botão pulsante
        hover = self.botao_rect.collidepoint(pygame.mouse.get_pos())
        base = self.cor_btn_hover if hover else self.cor_btn
        pulse = 1 + 0.05 * (1 + math.sin(self._pulse_phase * 3.0))  # 1.0 .. 1.1

        r = max(0, min(255, int(base[0] * pulse)))
        g = max(0, min(255, int(base[1] * pulse)))
        b = max(0, min(255, int(base[2] * pulse)))
        btn_color = (r, g, b)

        pygame.draw.rect(tela, btn_color, self.botao_rect, border_radius=14)

        label = "Começar (Enter)" if (self.idx_pagina == len(self.paginas) - 1 and self._is_page_fully_shown()) else "Continuar (Enter)"
        self._blit_text_with_shadow(tela, self.fonte_texto, label, (255, 255, 255),
                                    (self.botao_rect.centerx - self.fonte_texto.size(label)[0]//2,
                                     self.botao_rect.centery - self.fonte_texto.get_height()//2))

        # Dica de pulo
        self._blit_text_with_shadow(tela, self.fonte_ui, "Pressione S para pular",
                                    (200, 200, 200), (20, self.altura - 40))

        # Vignette
        self._draw_vignette(tela)

        # Fade
        if self._fade_alpha > 0:
            fade = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            fade.fill((0, 0, 0, int(self._fade_alpha)))
            tela.blit(fade, (0, 0))

    def _draw_arrows(self, tela):
        mx, my = pygame.mouse.get_pos()
        # prev
        prev_hover = self.arrow_prev.collidepoint((mx, my))
        self._draw_panel(tela, self.arrow_prev, (20, 28, 42, 160 if prev_hover else 110),
                         (110, 170, 255, 150 if prev_hover else 110), radius=12, border_w=2)
        self._draw_arrow_icon(tela, self.arrow_prev, left=True)
        # next
        next_hover = self.arrow_next.collidepoint((mx, my))
        self._draw_panel(tela, self.arrow_next, (20, 28, 42, 160 if next_hover else 110),
                         (110, 170, 255, 150 if next_hover else 110), radius=12, border_w=2)
        self._draw_arrow_icon(tela, self.arrow_next, left=False)

    def _draw_arrow_icon(self, tela, rect, left=False):
        cx, cy = rect.center
        size = 16
        if left:
            pts = [(cx + size//2, cy - size), (cx - size//2, cy), (cx + size//2, cy + size)]
        else:
            pts = [(cx - size//2, cy - size), (cx + size//2, cy), (cx - size//2, cy + size)]
        pygame.draw.polygon(tela, (230, 240, 255), pts)

    def _draw_page_dots(self, tela):
        total = len(self.paginas)
        cx = self.largura // 2
        y = 160
        spacing = 22
        r = 6
        self._dot_rects = []
        for i in range(total):
            x = cx + (i - (total - 1) / 2) * spacing
            col = self.col_dot_on if i == self.idx_pagina else self.col_dot_off
            pygame.draw.circle(tela, col, (int(x), y), r)
            self._dot_rects.append(pygame.Rect(int(x - r*2), int(y - r*2), r*4, r*4))
