# Intermediario/UI/TelaCobraCodigo.py
import pygame, random, math
from Intermediario.Content.CobraContent import get_cobra_content  # <- agora traz WHY nos distratores

class TelaCobraCodigo:
    """
    Cobrinha de Código — iniciante
    - Adapta a sequência e os distratores ao TÓPICO (print, input, variáveis, operadores, if/else, for, while, funções).
    - Tooltip on-hover no histórico com a EXPLICAÇÃO do erro (igual PyFoot).
    - Pause (ESPAÇO), invulnerabilidade inicial, spawn seguro e UI polida.
    """

    def __init__(self, largura, altura, jogador, id_fase, nome_topico, on_finish, sequencia_alvo=None, sfx=None):
        self.largura  = largura
        self.altura   = altura
        self.jogador  = jogador
        self.id_fase  = id_fase
        self.topico   = (nome_topico or "").lower()
        self.on_finish = on_finish
        self.sfx = sfx

        pygame.font.init()
        self.fonte      = pygame.font.SysFont("Consolas", 22)
        self.fonte_g    = pygame.font.SysFont("Consolas", 28, bold=True)
        self.fonte_t    = pygame.font.SysFont("Consolas", 18)
        self.fonte_mini = pygame.font.SysFont("Consolas", 16)

        # Painel/arena + sidebar
        self.prompt = pygame.Rect(int(largura*0.12), int(altura*0.10), int(largura*0.76), int(altura*0.80))
        self.sidebar_w = 260
        arena_w = self.prompt.w - 64 - self.sidebar_w - 12
        self.arena  = pygame.Rect(self.prompt.x+32, self.prompt.y+140, arena_w, self.prompt.h-210)
        self.sidebar = pygame.Rect(self.arena.right+12, self.arena.y, self.sidebar_w, self.arena.h)

        # Conteúdo (sequência e distratores com WHY)
        if sequencia_alvo:
            seq_raw = sequencia_alvo[:]
            _, pool_raw = get_cobra_content(self.topico)
        else:
            seq_raw, pool_raw = get_cobra_content(self.topico)

        self.seq = [self._tok_txt(t) for t in (seq_raw or [])]  # só strings aqui
        # distratores: guardamos só os textos para spawn, e mapeamos why por texto
        self._pool_distratores = [self._tok_txt(t) for t in (pool_raw or [])]
        self._why_by_txt = {}
        for d in (pool_raw or []):
            try:
                if isinstance(d, dict):
                    txt = self._tok_txt(d)
                    why = str(d.get("why","")).strip()
                else:
                    txt = self._tok_txt(d[0])
                    why = str(d[1])
                if txt:
                    self._why_by_txt[txt] = why
            except Exception:
                pass

        self.idx_alvo = 0
        self.montados = []

        # Snake (grid)
        self.cell  = 20
        self.snake = [(self.arena.centerx, self.arena.centery),
                      (self.arena.centerx - self.cell, self.arena.centery),
                      (self.arena.centerx - 2*self.cell, self.arena.centery)]
        self.dir   = (1, 0)
        self.pending_dir = self.dir
        self.move_interval = 120
        self._last_move    = pygame.time.get_ticks()

        # Vidas / tempo / score
        self.vidas = 3
        self.score = 0
        self.base_pts_certo = 120
        self.penalidade_errado = 60
        self.start_time = pygame.time.get_ticks()
        self.game_len_ms = 60_000
        self.finished = False

        # Invulnerabilidade inicial + spawn seguro
        self.spawn_safe_dist = 160
        self.invuln_ms = 2000
        self.invuln_until = self.start_time + self.invuln_ms

        # Pause
        self.paused = False
        self._pause_started = 0
        self._pause_total_ms = 0

        # Tokens
        self.tokens = []
        self.max_tokens = 7
        self._last_extra_spawn = pygame.time.get_ticks()
        self.extra_spawn_interval = 1400

        # Efeitos / histórico
        self.fx = []
        self.historico = []         # {"txt":str, "ok":bool, "why":str}
        self.acertos = 0
        self.erros   = 0

        # Hover + scroll do histórico
        self._hist_rows = []        # [(rect, item)]
        self._hist_area = pygame.Rect(0,0,0,0)
        self._hover_tooltip = ""
        self._scroll_hist = 0.0

        # Pós-jogo
        self._stars = 0
        self.btn_avancar_rect = None
        self._called_finish = False

        # Primeira leva
        self._spawn_wave(inicio=True)

    # ---------- helpers ----------
    def _tok_txt(self, token):
        try:
            if isinstance(token, dict):
                t = token.get("txt") or token.get("code") or token.get("text") or ""
                return str(t)
            if isinstance(token, (list, tuple)) and token:
                return str(token[0])
            return str(token)
        except Exception:
            return str(token)

    def _SFX(self, name, *a, **kw):
        s = getattr(self, "sfx", None)
        if not s:
            return
        fn = getattr(s, name, None)
        if callable(fn):
            try: fn(*a, **kw)
            except Exception: pass

    # ---------- util ----------
    def _rnd_pos_in_arena(self, w, h):
        x = random.randint(self.arena.x + 10, self.arena.right - w - 10)
        y = random.randint(self.arena.y + 10, self.arena.bottom - h - 10)
        return x, y

    def _rnd_pos_away_from_snake(self, w, h, min_dist):
        hx, hy = self.snake[0]
        for _ in range(60):
            x = random.randint(self.arena.x + 10, self.arena.right - w - 10)
            y = random.randint(self.arena.y + 10, self.arena.bottom - h - 10)
            cx, cy = x + w/2, y + h/2
            if math.hypot(cx - hx, cy - hy) >= min_dist:
                return x, y
        return self._rnd_pos_in_arena(w, h)

    def _add_fx(self, txt, x, y):
        self.fx.append({"txt": txt, "x": x, "y": y, "alpha": 255, "dy": -24})

    def _wrap_text(self, text, font, max_w):
        if not text:
            return [""]
        words = str(text).split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    def _wrap_fit(self, text, font, max_w, max_h, min_size=14):
        size = font.get_height()
        def wrap_lines(txt, f, w):
            words = txt.split()
            lines, cur = [], ""
            for wd in words:
                test = (cur + " " + wd).strip()
                if f.size(test)[0] <= w:
                    cur = test
                else:
                    if cur: lines.append(cur); cur = wd
            if cur: lines.append(cur)
            return lines

        f = font
        lines = wrap_lines(text, f, max_w)
        total_h = len(lines) * (f.get_height()+2)
        while total_h > max_h and size > min_size:
            size -= 1
            f = pygame.font.SysFont("Consolas", size)
            lines = wrap_lines(text, f, max_w)
            total_h = len(lines) * (f.get_height()+2)

        while total_h > max_h and lines:
            last = lines[-1]
            while last and f.size(last + "…")[0] > max_w:
                last = last[:-1]
            if last: lines[-1] = last + "…"
            else: lines.pop()
            total_h = len(lines) * (f.get_height()+2)
        return f, lines

    # ---------- tokens ----------
    def _spawn_token(self, token, correto=False, ordem=None):
        txt = self._tok_txt(token)
        f = self.fonte_mini
        w, h = f.size(txt)
        w = max(60, w + 14)
        h = max(26, h + 10)
        x, y = self._rnd_pos_away_from_snake(w, h, self.spawn_safe_dist)
        rect = pygame.Rect(x, y, w, h)
        ang = random.uniform(0, 2*math.pi)
        speed = random.uniform(60, 110)
        vx, vy = math.cos(ang)*speed, math.sin(ang)*speed
        self.tokens.append({
            "txt": txt, "rect": rect, "vx": vx, "vy": vy,
            "correto": bool(correto), "ordem": ordem
        })

    def _spawn_wave(self, inicio=False):
        self.tokens.clear()
        if not self.seq:
            return
        self._spawn_token(self.seq[self.idx_alvo], correto=True, ordem=self.idx_alvo)
        k = min(3, len(self._pool_distratores))
        for d in random.sample(self._pool_distratores, k=k):
            self._spawn_token(d, correto=False, ordem=None)

    def _maybe_spawn_extra_tokens(self):
        now = pygame.time.get_ticks()
        if now - self._last_extra_spawn >= self.extra_spawn_interval:
            self._last_extra_spawn = now
            if len(self.tokens) < self.max_tokens and self._pool_distratores and random.random() < 0.6:
                self._spawn_token(random.choice(self._pool_distratores), correto=False, ordem=None)

    # ---------- sequência nova ----------
    def _nova_sequencia(self):
        seq_raw, pool_raw = get_cobra_content(self.topico)
        self.seq = [self._tok_txt(t) for t in (seq_raw or [])]
        self._pool_distratores = [self._tok_txt(t) for t in (pool_raw or [])]
        self._why_by_txt = {}
        for d in (pool_raw or []):
            try:
                if isinstance(d, dict):
                    txt = self._tok_txt(d); why = str(d.get("why","")).strip()
                else:
                    txt = self._tok_txt(d[0]); why = str(d[1])
                if txt:
                    self._why_by_txt[txt] = why
            except Exception:
                pass
        self.idx_alvo = 0
        self.montados = []
        self._spawn_wave(inicio=True)

    # ---------- motivos/explicações ----------
    def _why_for_correct(self, step_index):
        total = len(self.seq)
        return f"Passo correto #{step_index+1} de {total}."

    def _why_for_wrong(self, eaten_txt):
        expected = self.seq[self.idx_alvo] if 0 <= self.idx_alvo < len(self.seq) else "—"
        # se não faz parte da sequência, tenta usar WHY específico do conteúdo
        if eaten_txt not in self.seq:
            why = self._why_by_txt.get(eaten_txt)
            return why if (why and why.strip()) else f"Não pertence à sequência deste tópico. Esperado agora: '{expected}'."
        # faz parte, mas fora de ordem/já coletado
        j = self.seq.index(eaten_txt)
        if j < self.idx_alvo:
            return f"Já coletado (passo #{j+1}). Agora o esperado é '{expected}' (#{self.idx_alvo+1})."
        elif j > self.idx_alvo:
            return f"Fora de ordem: isto é o passo #{j+1}, mas o esperado agora é '{expected}' (#{self.idx_alvo+1})."
        return "Token certo, mas não era o alvo atual."

    # ---------- loop / eventos ----------
    def tratar_eventos(self, eventos):
        # hover/scroll do histórico (mesmo após terminar)
        for ev in eventos:
            if ev.type == pygame.MOUSEMOTION:
                self._hover_tooltip = ""
                mx, my = ev.pos
                for r, item in self._hist_rows:
                    if r.collidepoint(mx, my):
                        tip = (item.get("why") or "").strip() or "Sem detalhes."
                        self._hover_tooltip = tip
                        break
            if ev.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                if self._hist_area.collidepoint(mx, my):
                    line_h = self.fonte_mini.get_height() + 6
                    content_h = max(0, len(self.historico) * line_h)
                    max_scroll = max(0, content_h - self._hist_area.h)
                    self._scroll_hist = max(0.0, min(self._scroll_hist - ev.y*40, float(max_scroll)))

        if self.finished:
            for ev in eventos:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self.btn_avancar_rect:
                    if self.btn_avancar_rect.collidepoint(ev.pos) and not self._called_finish:
                        self._called_finish = True
                        if self.on_finish:
                            self.on_finish(self.score, self._stars)
            return

        for ev in eventos:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    if self.paused:
                        self._pause_started = pygame.time.get_ticks()
                    else:
                        self._pause_total_ms += pygame.time.get_ticks() - self._pause_started
                        self._pause_started = 0
                    continue

                if self.paused:
                    continue

                if ev.key in (pygame.K_w, pygame.K_UP):
                    if self.dir != (0, 1): self.pending_dir = (0, -1)
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    if self.dir != (0, -1): self.pending_dir = (0, 1)
                elif ev.key in (pygame.K_a, pygame.K_LEFT):
                    if self.dir != (1, 0): self.pending_dir = (-1, 0)
                elif ev.key in (pygame.K_d, pygame.K_RIGHT):
                    if self.dir != (-1, 0): self.pending_dir = (1, 0)

    def _move_snake_if_time(self):
        now = pygame.time.get_ticks()
        if now - self._last_move < self.move_interval:
            return
        self._last_move = now
        self.dir = self.pending_dir

        hx, hy = self.snake[0]
        nx = hx + self.dir[0]*self.cell
        ny = hy + self.dir[1]*self.cell

        if nx < self.arena.x: nx = self.arena.right - self.cell
        if nx + self.cell > self.arena.right: nx = self.arena.x
        if ny < self.arena.y: ny = self.arena.bottom - self.cell
        if ny + self.cell > self.arena.bottom: ny = self.arena.y

        self._SFX("move_tick")

        if (nx, ny) in self.snake[:]:
            self.vidas -= 1
            self._add_fx("-1 vida", nx, ny)
            self._SFX("crash")
            self.snake = [(nx, ny),
                          (nx - self.dir[0]*self.cell, ny - self.dir[1]*self.cell),
                          (nx - 2*self.dir[0]*self.cell, ny - 2*self.dir[1]*self.cell)]
        else:
            self.snake.insert(0, (nx, ny))
            self.snake.pop()

    def _update_tokens(self, dt):
        for t in self.tokens:
            r = t["rect"]
            r.x += t["vx"] * dt
            r.y += t["vy"] * dt
            if r.left < self.arena.left or r.right > self.arena.right:
                t["vx"] *= -1
                r.x = max(self.arena.left, min(r.x, self.arena.right - r.w))
            if r.top < self.arena.top or r.bottom > self.arena.bottom:
                t["vy"] *= -1
                r.y = max(self.arena.top, min(r.y, self.arena.bottom - r.h))

        for f in self.fx[:]:
            f["y"] += f["dy"] * dt
            f["alpha"] -= 180 * dt
            if f["alpha"] <= 0:
                self.fx.remove(f)

        self._maybe_spawn_extra_tokens()

    def _check_eats(self):
        if pygame.time.get_ticks() < self.invuln_until:
            return

        hx, hy = self.snake[0]
        head_rect = pygame.Rect(hx, hy, self.cell, self.cell)
        eaten = None
        for t in self.tokens:
            if head_rect.colliderect(t["rect"]):
                eaten = t
                break
        if eaten is None:
            return

        if eaten["correto"] and eaten["ordem"] == self.idx_alvo:
            self.acertos += 1
            self.score += self.base_pts_certo
            why = self._why_for_correct(self.idx_alvo)
            self.historico.append({"txt": self.seq[self.idx_alvo], "ok": True, "why": why})
            self.montados.append(self.seq[self.idx_alvo])
            self.idx_alvo += 1
            self._add_fx("+OK", head_rect.centerx, head_rect.centery)
            self._SFX("eat")

            self.move_interval = max(80, self.move_interval - 4)
            self.snake.append(self.snake[-1])

            try: self.tokens.remove(eaten)
            except ValueError: pass

            if self.idx_alvo >= len(self.seq):
                self.score += 60
                self._SFX("bonus")
                self._nova_sequencia()
            else:
                self._spawn_wave()

        else:
            self.erros += 1
            self.vidas -= 1
            self.score = max(0, self.score - self.penalidade_errado)
            why = self._why_for_wrong(eaten["txt"])
            self._add_fx("ERR", head_rect.centerx, head_rect.centery)
            self._SFX("crash")
            self.historico.append({"txt": eaten["txt"], "ok": False, "why": why})
            if len(self.snake) > 3:
                self.snake.pop()
            try: self.tokens.remove(eaten)
            except ValueError: pass

    def _finish_now(self):
        if self.finished:
            return
        self.finished = True
        total = max(1, self.acertos + self.erros)
        acc = self.acertos / total
        if acc >= 0.85 and self.score >= 900:
            self._stars = 3
        elif acc >= 0.65 and self.score >= 600:
            self._stars = 2
        elif acc >= 0.45 and self.score >= 300:
            self._stars = 1
        else:
            self._stars = 0

    def _draw_hist_list(self, tela, start_y):
        y = start_y
        title = self.fonte_t.render("Comidos", True, (200,220,255))
        tela.blit(title, (self.sidebar.x+12, y))
        y += 26

        area_h = self.sidebar.bottom - y - 10
        area = pygame.Rect(self.sidebar.x+8, y, self.sidebar.w-16, max(60, area_h))
        self._hist_area = area

        pygame.draw.rect(tela, (28, 42, 64), area, border_radius=8)
        pygame.draw.rect(tela, (80, 140, 220), area, 1, border_radius=8)

        line_h = self.fonte_mini.get_height() + 6
        content_h = max(0, len(self.historico) * line_h)
        max_scroll = max(0, content_h - area.h)
        self._scroll_hist = max(0.0, min(self._scroll_hist, float(max_scroll)))

        old_clip = tela.get_clip()
        tela.set_clip(area)

        self._hist_rows = []
        if not self.historico:
            s = self.fonte_mini.render("— sem itens —", True, (210, 215, 225))
            tela.blit(s, (area.centerx - s.get_width()//2, area.centery - s.get_height()//2))
            tela.set_clip(old_clip)
            return y + area.h

        first_idx = int(self._scroll_hist // line_h)
        yy = area.y - int(self._scroll_hist - first_idx * line_h)

        i = first_idx
        inner_w = area.w - 12
        while i < len(self.historico) and yy < area.bottom:
            it = self.historico[i]
            row_rect = pygame.Rect(area.x+4, yy, inner_w, line_h-2)
            base_col = (40, 56, 84) if it.get("ok") else (48, 52, 80)
            pygame.draw.rect(tela, base_col, row_rect, border_radius=6)

            txt = (it.get("txt","") or "").replace("\n","  ")
            wrap = self._wrap_text(txt, self.fonte_mini, inner_w - 12)
            line = wrap[0] + (" ..." if len(wrap) > 1 else "")
            col = (220, 240, 230) if it.get("ok") else (235, 210, 210)
            surf = self.fonte_mini.render("• " + line, True, col)
            tela.blit(surf, (row_rect.x+6, row_rect.y + (row_rect.h - surf.get_height())//2))

            self._hist_rows.append((row_rect, it))
            yy += line_h
            i += 1

        tela.set_clip(old_clip)

        if content_h > area.h:
            track = pygame.Rect(area.right-10, area.y+2, 8, area.h-4)
            pygame.draw.rect(tela, (26, 36, 52), track, border_radius=4)
            thumb_h = max(24, int(area.h * area.h / content_h))
            thumb_y = track.y + int((track.h - thumb_h) * (self._scroll_hist / max_scroll)) if max_scroll > 0 else track.y
            thumb = pygame.Rect(track.x+1, thumb_y, track.w-2, thumb_h)
            pygame.draw.rect(tela, (90, 170, 255), thumb, border_radius=4)

        return y + area.h

    def desenhar(self, tela):
        now = pygame.time.get_ticks()
        extra_pause = (now - self._pause_started) if self.paused and self._pause_started else 0
        base_elapsed = now - self.start_time
        invuln_elapsed = min(base_elapsed, self.invuln_ms)
        elapsed = base_elapsed - invuln_elapsed - (self._pause_total_ms + extra_pause)

        dt = 0.0
        if not hasattr(self, "_last_tick_draw"):
            self._last_tick_draw = now
        else:
            raw_dt = (now - self._last_tick_draw) / 1000.0
            self._last_tick_draw = now
            dt = 0.0 if self.paused else raw_dt

        surf = pygame.Surface((self.prompt.w, self.prompt.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (18, 24, 32, 240), (0,0,self.prompt.w,self.prompt.h), border_radius=16)
        pygame.draw.rect(surf, (42, 103, 188), (0,0,self.prompt.w,self.prompt.h), 6, border_radius=16)
        tela.blit(surf, (self.prompt.x, self.prompt.y))

        header_h = 56
        header = pygame.Rect(self.prompt.x, self.prompt.y, self.prompt.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (self.prompt.x, self.prompt.y+header_h), (self.prompt.x+self.prompt.w, self.prompt.y+header_h), 2)
        titulo = self.fonte_g.render("Cobrinha de Código", True, (230,240,255))
        tela.blit(titulo, (self.prompt.x+24, self.prompt.y+10))

        enun_txt = f"Coma na ordem:  {'  →  '.join(self.seq)}"
        enun_rect = pygame.Rect(self.prompt.x+24, self.prompt.y+66, self.prompt.w-48, 60)
        f_fit, lines = self._wrap_fit(enun_txt, self.fonte, enun_rect.w, enun_rect.h, min_size=14)
        y_line = enun_rect.y
        for ln in lines:
            s = f_fit.render(ln, True, (230,230,90))
            tela.blit(s, (enun_rect.x, y_line))
            y_line += f_fit.get_height()+2
        after_enun_y = y_line

        remain = max(0, (self.game_len_ms - max(0, int(elapsed)))//1000)
        hud_y = max(self.prompt.y+100, after_enun_y + 6)
        hud = f"Tempo: {remain:02d}s | Vidas: {self.vidas} | Score: {self.score}"
        tela.blit(self.fonte_t.render(hud, True, (210,210,210)), (self.prompt.x+24, hud_y))

        pygame.draw.rect(tela, (22,32,44), self.arena, border_radius=10)
        pygame.draw.rect(tela, (60, 160, 255), self.arena, 2, border_radius=10)

        if not self.finished and not self.paused:
            self._move_snake_if_time()
            self._update_tokens(dt)
            self._check_eats()
            if elapsed >= self.game_len_ms or self.vidas <= 0:
                self._finish_now()

        for t in self.tokens:
            r = t["rect"]
            base_col = (190, 205, 230)
            pygame.draw.rect(tela, base_col, r, border_radius=8)
            pygame.draw.rect(tela, (20, 20, 20), r, 2, border_radius=8)
            txt = str(t.get("txt", ""))
            f = self.fonte_mini
            while f.size(txt)[0] > r.w - 10 and f.get_height() > 12:
                f = pygame.font.SysFont("Consolas", f.get_height()-1)
            ts = f.render(txt, True, (0,0,0))
            tela.blit(ts, (r.centerx - ts.get_width()//2, r.centery - ts.get_height()//2))

        for i, (x,y) in enumerate(self.snake):
            col = (90, 230, 120) if i==0 else (60, 160, 100)
            pygame.draw.rect(tela, col, pygame.Rect(x, y, self.cell, self.cell), border_radius=4)

        pygame.draw.rect(tela, (25, 28, 36), self.sidebar, border_radius=10)
        pygame.draw.rect(tela, (80, 120, 200), self.sidebar, 2, border_radius=10)

        y = self.sidebar.y + 10
        tela.blit(self.fonte_t.render("Progresso", True, (200,220,255)), (self.sidebar.x+12, y))
        y += 26
        for i, step in enumerate(self.seq):
            ok = (i < self.idx_alvo)
            col = (120, 220, 160) if ok else (220, 220, 220)
            bullet = "✔" if ok else "•"
            line = f"{bullet} {step}"
            s = self.fonte_mini.render(line, True, col)
            tela.blit(s, (self.sidebar.x+12, y))
            y += s.get_height() + 6

        y += 8
        y = self._draw_hist_list(tela, y)

        for f in self.fx:
            s = self.fonte.render(f["txt"], True, (255,255,255))
            s.set_alpha(max(0, int(f["alpha"])) )
            tela.blit(s, (int(f["x"] - s.get_width()//2), int(f["y"])) )

        if self.paused and not self.finished:
            overlay = pygame.Surface((self.prompt.w, self.prompt.h), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 120), overlay.get_rect(), border_radius=16)
            tela.blit(overlay, (self.prompt.x, self.prompt.y))
            msg1 = self.fonte_g.render("PAUSADO", True, (255,255,255))
            msg2 = self.fonte.render("Aperte ESPAÇO para continuar", True, (230,230,200))
            cx = self.prompt.centerx
            cy = self.prompt.centery
            tela.blit(msg1, (cx - msg1.get_width()//2, cy - 40))
            tela.blit(msg2, (cx - msg2.get_width()//2, cy + 4))

        if not self.finished and now < self.invuln_until:
            remaining = self.invuln_until - now
            n = max(1, math.ceil(remaining / 1000))
            overlay = pygame.Surface((self.prompt.w, self.prompt.h), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 140), overlay.get_rect(), border_radius=16)
            tela.blit(overlay, (self.prompt.x, self.prompt.y))
            msg1 = self.fonte_g.render("Prepare-se!", True, (255,255,255))
            msg2 = self.fonte.render(f"{n}", True, (230,230,90))
            cx = self.prompt.centerx
            cy = self.prompt.centery
            tela.blit(msg1, (cx - msg1.get_width()//2, cy - 46))
            tela.blit(msg2, (cx - msg2.get_width()//2, cy + 4))

        if self.finished:
            overlay = pygame.Surface((self.prompt.w, self.prompt.h), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 160), overlay.get_rect(), border_radius=16)
            tela.blit(overlay, (self.prompt.x, self.prompt.y))

            cx = self.prompt.centerx
            cy = self.prompt.centery - 40
            titulo = "Fim do Minigame"
            ss = self.fonte_g.render(titulo, True, (255,255,255))
            tela.blit(ss, (cx - ss.get_width()//2, cy - 80))

            acc_pct = int((self.acertos/max(1,self.acertos+self.erros))*100)
            resumo = f"Score: {self.score}  |  Acurácia: {acc_pct}%  |  Vidas: {self.vidas}"
            rs = self.fonte.render(resumo, True, (230,230,200))
            tela.blit(rs, (cx - rs.get_width()//2, cy - 30))

            btn_w, btn_h = 220, 56
            btn_rect = pygame.Rect(cx - btn_w//2, cy + 20, btn_w, btn_h)
            pygame.draw.rect(tela, (0, 170, 220), btn_rect, border_radius=18)
            lbl = self.fonte.render("AVANÇAR", True, (255,255,255))
            tela.blit(lbl, (btn_rect.centerx - lbl.get_width()//2, btn_rect.centery - lbl.get_height()//2))
            self.btn_avancar_rect = btn_rect

        if self._hover_tooltip:
            mx, my = pygame.mouse.get_pos()
            lines = self._wrap_text(self._hover_tooltip, self.fonte_mini, 320)
            w = max(self.fonte_mini.size(l)[0] for l in lines) + 16
            h = len(lines)*(self.fonte_mini.get_height()+2) + 12
            x = min(mx + 16, self.prompt.right - w - 8)
            y = min(my + 16, self.prompt.bottom - h - 8)
            tip = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(tip, (30, 44, 70, 240), tip.get_rect(), border_radius=8)
            pygame.draw.rect(tip, (120, 180, 255), tip.get_rect(), 1, border_radius=8)
            yy = 6
            for ln in lines:
                s = self.fonte_mini.render(ln, True, (230, 240, 255))
                tip.blit(s, (8, yy)); yy += self.fonte_mini.get_height()+2
            tela.blit(tip, (x, y))
