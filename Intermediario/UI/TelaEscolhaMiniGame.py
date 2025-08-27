# Intermediario/UI/TelaEscolhaMiniGame.py
import pygame
import os

class TelaEscolhaMiniGame:
    """
    Lobby de seleção de minigame (5ª questão)
    - Mostra regras claras (4/5) e o score mínimo para contar como acerto do minigame.
    - Cards empilhados com SCROLL do mouse quando há muitos minigames.
    - Anti-clique fantasma ao abrir (ignora 1º mouseup + cooldown curto).
    - Atalhos: 1 = Python Hero | 2 = Cobrinha de Código | 3 = Bug Squash Arcade | 4 = PyFoot Tactics | ESC no GameManager.
    """
    def __init__(self, largura, altura, on_choose, pass_score=360):
        self.largura = largura
        self.altura = altura
        self.on_choose = on_choose
        self.pass_score = pass_score  # Score necessário para contar como 5ª questão

        # ---- Fonts
        pygame.font.init()
        self.fonte_xl = pygame.font.SysFont("Consolas", 26, bold=True)
        self.fonte_g  = pygame.font.SysFont("Consolas", 22, bold=True)
        self.fonte    = pygame.font.SysFont("Consolas", 18)
        self.fonte_s  = pygame.font.SysFont("Consolas", 16)

        # ---- Painel
        self.prompt = pygame.Rect(int(largura*0.18), int(altura*0.10), int(largura*0.64), int(altura*0.76))

        # ---- Lista de cards
        self._cards = [
            {
                "key": "hero",
                "title": "1) Python Hero",
                "tag":   "Ritmo com A, S, D, F — acerte na linha azul.",
                "bullets": [
                    "Perguntas do tópico viram blocos que caem.",
                    f"Conta como ACERTO se Score ≥ {self.pass_score}."
                ],
                "badges": ["Duração ~35s", "Teclas: A S D F", "1 tentativa/rodada"],
                "shortcut": "1",
            },
            {
                "key": "cobra",
                "title": "2) Cobrinha de Código",
                "tag":   "Coma os trechos na ORDEM pedida.",
                "bullets": [
                    "WASD/Setas para mover • Espaço: PAUSE",
                    "Certo: +120  |  Errado: −60  |  3 vidas",
                    f"Conta como ACERTO se Score ≥ {self.pass_score}."
                ],
                "badges": ["Duração ~60s", "Sequências contínuas", "Histórico lateral"],
                "shortcut": "2",
            },
            {
                "key": "bug",
                "title": "3) Whack-a-Python (Bug Squash)",
                "tag":   "Rodadas de 5s: siga o ALVO do topo (BUG ou CORRETO) e clique nas cobras certas.",
                "bullets": [
                    "Só mouse. Feedback de marreta, anel de impacto e pop de pontos.",
                    "Histórico com hover + SCROLL para ver o porquê (durante e após o jogo).",
                    f"Conta como ACERTO se Score ≥ {self.pass_score}."
                ],
                "badges": ["Rodadas 5s", "Temporizador circular", "Combo ativo"],
                "shortcut": "3",
            },
            {
                "key": "pyfoot",
                "title": "4) PyFoot Tactics",
                "tag":   "Passe certo → POWER; com POWER cheio, mire e chute pro gol!",
                "bullets": [
                    "Clique no jogador com a opção CORRETA (A/B/C).",
                    "Cada acerto enche POWER; com POWER cheio, mire no gol e chute (clique ou Espaço).",
                    "Certo: +120 (+combo)  |  Gol: +250 (+30×combo)  |  Errado: −40  |  3 vidas",
                    f"Conta como ACERTO se Score ≥ {self.pass_score}."
                ],
                "badges": ["Duração ~45s", "Mouse + Espaço", "Mira e goleiro"],
                "shortcut": "4",
            },
        ]

        # ---- Imagens de fundo (opcionais)
        self._card_imgs = {
            "hero":  self._try_load_image(["assets/pythonhero.png", "assets/minigames/pythonhero.png", "pythonhero.png"]),
            "cobra": self._try_load_image(["assets/snakePython.png", "assets/minigames/snakePython.png", "snakePython.png"]),
            "bug":   self._try_load_image(["assets/BugHunter.png", "assets/minigames/BugHunter.png", "BugHunter.png"]),
            "pyfoot":self._try_load_image(["assets/Pyfoot.png", "assets/minigames/Pyfoot.png", "Pyfoot.png"]),
        }

        # ---- Layout da área scrollável (definido no draw, mas guardamos estado)
        self.scroll_y = 0
        self._max_scroll = 0
        self._card_rects_runtime = []  # [(key, rect), ...] recalculado a cada frame
        self._cards_view_rect = None   # viewport dos cards (clip)

        # ---- Anti-clique fantasma ao abrir
        self._opened_at_ms = pygame.time.get_ticks()
        self._click_guard_ms = 250
        self._ignore_first_mouseup = True

    # =============== UTILS: imagens ===============
    def _try_load_image(self, paths):
        for p in paths:
            try:
                if os.path.exists(p):
                    return pygame.image.load(p).convert_alpha()
            except Exception:
                pass
        return None

    # =============== UTILS: texto e quebra ===============
    @staticmethod
    def _wrap_text(text, fonte, max_w):
        """Quebra 'text' em linhas que caibam em max_w (palavra a palavra)."""
        if not text:
            return [""]
        words = str(text).split(" ")
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if fonte.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def _draw_wrapped_lines(self, tela, x, y, text, fonte, color, max_w, max_h=None, line_gap=4):
        """Desenha texto com wrap; retorna y final. Se max_h setado, corta com '…'."""
        lines = self._wrap_text(text, fonte, max_w)
        line_h = fonte.get_height() + line_gap
        if max_h is not None:
            max_lines = max(1, max_h // line_h)
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                if not lines[-1].endswith("…"):
                    while fonte.size(lines[-1] + "…")[0] > max_w and len(lines[-1]) > 1:
                        lines[-1] = lines[-1][:-1]
                    lines[-1] = (lines[-1] + "…").strip()
        for ln in lines:
            surf = fonte.render(ln, True, color)
            tela.blit(surf, (x, y))
            y += line_h
        return y

    # =============== INPUT ===============
    def tratar_eventos(self, eventos):
        now = pygame.time.get_ticks()

        for ev in eventos:
            # Guard contra clique fantasma
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if self._ignore_first_mouseup:
                    self._ignore_first_mouseup = False
                    continue
                if now - self._opened_at_ms < self._click_guard_ms:
                    continue

            # Scroll com rodinha, quando cursor em cima da área scrollável
            if ev.type == pygame.MOUSEWHEEL and self._cards_view_rect:
                mx, my = pygame.mouse.get_pos()
                if self._cards_view_rect.collidepoint(mx, my):
                    passo = 60  # px por notch (ajuste fino)
                    self.scroll_y = max(0, min(self.scroll_y - ev.y * passo, self._max_scroll))

            # Clique nos cards (após guard)
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                mx, my = ev.pos
                for key, rect in self._card_rects_runtime:
                    if rect.collidepoint(mx, my):
                        self.on_choose(key)
                        return

            # Atalhos por teclado
            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_1, pygame.K_KP1):
                    self.on_choose("hero")
                elif ev.key in (pygame.K_2, pygame.K_KP2):
                    self.on_choose("cobra")
                elif ev.key in (pygame.K_3, pygame.K_KP3):
                    self.on_choose("bug")
                elif ev.key in (pygame.K_4, pygame.K_KP4):
                    self.on_choose("pyfoot")

    # =============== DRAW HELPERS ===============
    def _draw_panel(self, tela):
        p = self.prompt
        surf = pygame.Surface((p.w, p.h), pygame.SRCALPHA)
        # fundo vidro escuro + molduras
        pygame.draw.rect(surf, (18, 24, 32, 235), surf.get_rect(), border_radius=16)
        pygame.draw.rect(surf, (42, 103, 188), surf.get_rect(), 6, border_radius=16)
        pygame.draw.rect(surf, (18, 24, 32), (8, 8, p.w-16, p.h-16), 4, border_radius=12)
        tela.blit(surf, (p.x, p.y))

        # header
        header_h = 56
        header = pygame.Rect(p.x, p.y, p.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (p.x, p.y+header_h), (p.x+p.w, p.y+header_h), 2)

        titulo = self.fonte_xl.render("Escolha o Minigame (5ª questão)", True, (230, 240, 255))
        tela.blit(titulo, (p.x+24, p.y+12))

        # banner de regras (com quebra automática)
        banner = pygame.Rect(p.x+24, p.y+header_h+12, p.w-48, 76)
        pygame.draw.rect(tela, (24, 34, 50), banner, border_radius=12)
        pygame.draw.rect(tela, (90, 170, 255), banner, 2, border_radius=12)

        x_txt = banner.x + 14
        y_txt = banner.y + 10
        maxw_banner = banner.w - 28
        self._draw_wrapped_lines(tela, x_txt, y_txt, "Regra do tópico: acerte 4 de 5.",
                                 self.fonte, (230,230,230), maxw_banner)
        _ = self._draw_wrapped_lines(
            tela, x_txt, y_txt + self.fonte.get_height() + 6,
            f"Este minigame vale como a 5ª questão se Score ≥ {self.pass_score}.",
            self.fonte, (180,210,255), maxw_banner
        )
        return banner.bottom + 16

    def _badge(self, tela, x, y, text):
        pad_x, pad_y = 10, 6
        s = self.fonte_s.render(text, True, (235, 235, 255))
        r = pygame.Rect(x, y, s.get_width()+pad_x*2, s.get_height()+pad_y*2)
        pygame.draw.rect(tela, (35, 55, 95), r, border_radius=10)
        pygame.draw.rect(tela, (90, 170, 255), r, 1, border_radius=10)
        tela.blit(s, (r.x+pad_x, r.y+pad_y))
        return r.right

    def _keypill(self, tela, cx, cy, label):
        pygame.draw.circle(tela, (110, 190, 255), (cx, cy), 18)
        ksurf = self.fonte.render(label, True, (28, 44, 80))
        tela.blit(ksurf, (cx - ksurf.get_width()//2, cy - ksurf.get_height()//2))

    def _blit_card_background(self, tela, rect, key, hovered):
        # base no estilo antigo
        base = (45, 70, 120) if not hovered else (60, 90, 150)
        card = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(card, base, card.get_rect(), border_radius=16)

        img = self._card_imgs.get(key)
        if img:
            iw, ih = img.get_width(), img.get_height()
            rw, rh = rect.w, rect.h
            scale = max(rw / iw, rh / ih)
            nw, nh = int(iw * scale), int(ih * scale)
            scaled = pygame.transform.smoothscale(img, (nw, nh))
            scaled.set_alpha(105)  # ~40% visível
            card.blit(scaled, ((rw - nw)//2, (rh - nh)//2))
            overlay = pygame.Surface((rw, rh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))
            card.blit(overlay, (0, 0))

        pygame.draw.rect(card, (90, 170, 255), card.get_rect(), 3, border_radius=16)
        tela.blit(card, rect.topleft)

    def _draw_card(self, tela, rect, key, title, tagline, bullets, badges, keylabel, hovered):
        self._blit_card_background(tela, rect, key, hovered)

        pad = 20
        tx = rect.x + pad
        ty = rect.y + 14
        maxw = rect.w - pad*2

        tela.blit(self.fonte_g.render(title, True, (255, 255, 255)), (tx, ty))
        ty += 24
        ty = self._draw_wrapped_lines(tela, tx, ty, tagline, self.fonte, (215,225,245), maxw, max_h=48)

        bottom_reserved = 44
        area_h = rect.bottom - bottom_reserved - ty
        for ln in bullets:
            if area_h <= 0:
                break
            bullet_prefix = "• "
            bp_w = self.fonte_s.size(bullet_prefix)[0]
            lines = self._wrap_text(ln, self.fonte_s, maxw - bp_w)
            line_h = self.fonte_s.get_height() + 3
            for j, l in enumerate(lines):
                if area_h < line_h:
                    surf_last = self.fonte_s.render("…", True, (230,230,230))
                    tela.blit(surf_last, (tx, ty))
                    ty += line_h
                    area_h -= line_h
                    break
                if j == 0:
                    bullet = self.fonte_s.render(bullet_prefix, True, (230,230,230))
                    tela.blit(bullet, (tx, ty))
                    surf = self.fonte_s.render(l, True, (230,230,230))
                    tela.blit(surf, (tx + bp_w, ty))
                else:
                    surf = self.fonte_s.render(l, True, (230,230,230))
                    tela.blit(surf, (tx, ty))
                ty += line_h
                area_h -= line_h

        by = rect.bottom - 32
        bx = tx
        for b in badges:
            bx = self._badge(tela, bx, by, b) + 8

        self._keypill(tela, rect.right-36, rect.y+24, keylabel)

    # =============== DRAW MAIN ===============
    def desenhar(self, tela):
        y_cards_top = self._draw_panel(tela)
        p = self.prompt

        hints_h = 52
        hints_rect = pygame.Rect(p.x + 40, p.bottom - 16 - hints_h, p.w - 80, hints_h)

        self._cards_view_rect = pygame.Rect(p.x + 40, y_cards_top, p.w - 80, hints_rect.top - 16 - y_cards_top)

        CARD_H = min(int(self.prompt.h * 0.25), 180)
        GAP    = 22
        total_content_h = len(self._cards) * CARD_H + (len(self._cards) - 1) * GAP
        self._max_scroll = max(0, total_content_h - self._cards_view_rect.h)
        self.scroll_y = max(0, min(self.scroll_y, self._max_scroll))

        old_clip = tela.get_clip()
        tela.set_clip(self._cards_view_rect)
        self._card_rects_runtime = []

        mx, my = pygame.mouse.get_pos()

        y = self._cards_view_rect.y - self.scroll_y
        for c in self._cards:
            rect = pygame.Rect(self._cards_view_rect.x, int(y), self._cards_view_rect.w, CARD_H)
            hovered = rect.collidepoint(mx, my)
            self._draw_card(
                tela, rect,
                c["key"], c["title"], c["tag"], c["bullets"], c["badges"], c["shortcut"], hovered
            )
            self._card_rects_runtime.append((c["key"], rect))
            y += CARD_H + GAP

        tela.set_clip(old_clip)

        if self._max_scroll > 0:
            track_w = 6
            track_x = self._cards_view_rect.right - track_w
            track_y = self._cards_view_rect.y
            track_h = self._cards_view_rect.h
            pygame.draw.rect(tela, (60, 70, 90), (track_x, track_y, track_w, track_h), border_radius=4)
            ratio = self._cards_view_rect.h / (total_content_h + 1e-5)
            thumb_h = max(24, int(track_h * ratio))
            thumb_y = track_y + int((track_h - thumb_h) * (self.scroll_y / self._max_scroll))
            pygame.draw.rect(tela, (120, 180, 255), (track_x, thumb_y, track_w, thumb_h), border_radius=4)

        surf = pygame.Surface((hints_rect.w, hints_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (25, 35, 52, 220), surf.get_rect(), border_radius=12)
        pygame.draw.rect(surf, (60, 160, 255), surf.get_rect(), 2, border_radius=12)
        txt = self.fonte_s.render("Clique em um card ou use 1 / 2 / 3 / 4  •  ESC para voltar", True, (220, 230, 245))
        surf.blit(txt, (16, hints_rect.h//2 - txt.get_height()//2))
        tela.blit(surf, (hints_rect.x, hints_rect.y))
