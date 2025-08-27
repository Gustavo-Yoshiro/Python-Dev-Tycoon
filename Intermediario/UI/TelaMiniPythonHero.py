import pygame
import random
import re

# Tenta usar o conteúdo oficial do Python Hero (iniciante + intermediário).
# Se não encontrar, cai num fallback simples.
try:
    # caminho mais comum no teu projeto:
    from Intermediario.Content.PythonHeroContent import get_hero_pool as _content_get_hero_pool
except Exception:
    try:
        # alternativa se o pacote estiver no mesmo diretório
        from .PythonHeroContent import get_hero_pool as _content_get_hero_pool
    except Exception:
        _content_get_hero_pool = None


class TelaMiniPythonHero:
    """
    Minigame (35s). 4 trilhas (A,S,D,F). Uma pergunta por rodada.
    Uma rodada = até 4 blocos (1 correta + erradas). Próxima rodada só começa
    quando a atual termina. Blocos são NEUTROS; a cor aparece só ao apertar.

    Render dos cards:
    - NÃO faz word-wrap.
    - Quebra em '\\n' / ' | ' vindos do content.
    - **Auto-format**: também quebra em ';' e em blocos 'for/if/elif/else/while/def/try/except'
      no padrão "cabecalho: \\n    corpo".
    - Diminui a fonte até caber (mín. 12).
    - Se ainda assim não couber, põe '…' no fim e loga um aviso no console.

    >>> Mudança principal:
    Agora esta tela busca o pool via PythonHeroContent.get_hero_pool(topico),
    então o conteúdo respeita 100% o roteamento por TÍTULO EXATO normalizado,
    igual Cobrinha/BugSquash/PyFoot. Sem isso, ela caía num 'base' genérico.
    """

    def __init__(self, largura, altura, jogador, id_fase, nome_topico, on_finish, sfx=None):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.id_fase = id_fase

        # guardamos o título original (para roteador oficial) e a versão minúscula só para UI
        self.nome_topico_raw = nome_topico or ""
        self.nome_topico = (nome_topico or "").lower()

        self.on_finish = on_finish
        self.sfx = sfx

        # painel
        self.prompt = pygame.Rect(int(largura*0.18), int(altura*0.10), int(largura*0.64), int(altura*0.76))
        pygame.font.init()
        self.fonte    = pygame.font.SysFont("Consolas", 22)
        self.fonte_g  = pygame.font.SysFont("Consolas", 28, bold=True)
        self.fonte_t  = pygame.font.SysFont("Consolas", 18)
        self.fonte_fx = pygame.font.SysFont("Consolas", 26, bold=True)

        # Fonte/estilo dos cards
        self.note_font_base_size = 18
        self.note_font_min_size  = 12
        self.note_pad_x = 6
        self.note_pad_y = 6
        self.note_corner = 10
        self.note_line_gap = 2
        self.max_note_lines = 3

        # trilhas
        self.num_lanes = 4
        m = 36
        lane_w = (self.prompt.w - m*2) // self.num_lanes
        self.lanes = [pygame.Rect(self.prompt.x + m + i*lane_w, self.prompt.y+140, lane_w-10, self.prompt.h-200) for i in range(self.num_lanes)]
        self.hit_y = self.lanes[0].bottom - 48
        self.hit_window = 100
        self.early_window = 220

        # notas
        self.notes = []
        self.last_spawn = 0

        # ritmo/velocidade
        self.base_speed = 100
        self.base_beat  = 1200
        self.speed = self.base_speed
        self.beat_ms = self.base_beat

        # tempo
        now = pygame.time.get_ticks()
        self.start_time = now
        self.game_len_ms = 35_000

        # placar
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.best_combo = 0
        self.total_correct_notes = 0
        self.finished = False

        # teclas e feedback
        self.key_to_lane = {pygame.K_a:0, pygame.K_s:1, pygame.K_d:2, pygame.K_f:3}
        self.pressed = set()
        self.lane_flash = {0: None, 1: None, 2: None, 3: None}  # {lane: (color, until_ms)}

        # 1 tentativa por rodada
        self.wave_answered = False

        # perguntas por tópico (agora via conteúdo oficial)
        self.pool = self._criar_pool_por_topico(self.nome_topico_raw)
        self.current_prompt = None
        self._prepare_next_prompt()  # primeira rodada
        self._last_tick = now
        self.fx = []

        # solta a primeira rodada
        self._spawn_notes()
        self.last_spawn = now

    def _SFX(self, name, *a, **kw):
        s = getattr(self, "sfx", None)
        if not s:
            return
        fn = getattr(s, name, None)
        if callable(fn):
            try:
                fn(*a, **kw)
            except Exception:
                pass

    # ---------- CONTEÚDO ----------
    def _fallback_pool(self):
        """Pool mínimo caso o import do conteúdo não esteja disponível."""
        def p(prompt, ok, *wrong):
            alts = [{"txt": ok, "ok": True}] + [{"txt": w, "ok": False} for w in wrong]
            return {"prompt": prompt, "alternativas": alts}

        return [
            p("Qual imprime 7?", "print(3+4)", "print(3*4)", "print('7'+1)", "print(7,)"),
            p("Qual concatena 'py' e 'thon'?", "print('py'+'thon')", "print('py','thon')", "print( py + thon )", "print('py'.join('thon'))"),
            p("Qual imprime de 0 a 2 (um por linha)?",
              "for i in range(3): print(i)",
              "for i in range(1,3): print(i)", "for i in [3]: print(i)", "print(range(3))"),
        ]

    def _criar_pool_por_topico(self, topico_titulo):
        """
        Busca o pool do módulo oficial de conteúdo.
        Se falhar, usa o fallback mínimo acima.
        """
        if callable(_content_get_hero_pool):
            try:
                pool = _content_get_hero_pool(topico_titulo)
                # validação leve
                if isinstance(pool, list) and pool and isinstance(pool[0], dict) and "alternativas" in pool[0]:
                    return pool
            except Exception:
                # se der qualquer erro no conteúdo, seguimos no fallback
                pass
        return self._fallback_pool()

    # ---------- RODADA ----------
    def _prepare_next_prompt(self):
        self.current = random.choice(self.pool)
        self.current_prompt = self.current["prompt"]
        alts = self.current["alternativas"][:]
        random.shuffle(alts)

        corrects = [a for a in alts if a.get("ok")]
        wrongs  = [a for a in alts if not a.get("ok")]
        correct = random.choice(corrects) if corrects else {"txt":"...", "ok": True}
        k = min(3, len(wrongs))
        sampled_wrongs = random.sample(wrongs, k) if k > 0 else []

        alts_sel = [correct] + sampled_wrongs
        random.shuffle(alts_sel)

        self._lane_alternativas = []
        for i in range(self.num_lanes):
            if i < len(alts_sel):
                self._lane_alternativas.append(alts_sel[i])
            else:
                self._lane_alternativas.append({"txt": "...", "ok": False})

        self.total_correct_notes += 1
        self.wave_answered = False

        # --- SFX: nova rodada/pergunta
        self._SFX("wave_start", self.current_prompt)

    # ---------- CONTROLES ----------
    def tratar_eventos(self, eventos):
        if self.finished:
            return
        for ev in eventos:
            if ev.type == pygame.KEYDOWN and ev.key in self.key_to_lane:
                if self.wave_answered:
                    continue
                self.wave_answered = True
                self.pressed.add(ev.key)
                lane = self.key_to_lane[ev.key]
                self._try_hit(lane)
            elif ev.type == pygame.KEYUP and ev.key in self.pressed:
                self.pressed.discard(ev.key)

    # ---------- ACERTO ----------
    def _try_hit(self, lane):
        candidates = [n for n in self.notes if n["lane"] == lane]
        if not candidates:
            self._flash_lane(lane, (200,60,60))
            self._register_miss()
            return

        n = min(candidates, key=lambda x: abs(x["y"] - self.hit_y))
        signed = n["y"] - self.hit_y
        dist   = abs(signed)

        if dist <= self.hit_window:
            if n["correct"]:
                self.hits += 1
                self.combo += 1
                self.best_combo = max(self.best_combo, self.combo)

                precision = 1.0 - (dist / self.hit_window)
                base_pts = 100
                self.score += int(base_pts * (1 + 0.25*precision) * (1 + 0.02*self.combo))

                if   precision >= 0.8: tag = "PERFECT!"
                elif precision >= 0.5: tag = "GOOD"
                else:                  tag = "LATE"
                self._add_fx(tag, self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (70,200,70))

                # --- SFX: acerto + (opcional) combo
                t = tag.replace("!", "").lower()  # "perfect"|"good"|"late"
                self._SFX("hit", t)
                if self.combo > 1:
                    self._SFX("combo_up", int(self.combo))
            else:
                self.misses += 1
                self.combo = 0
                self.score = max(0, self.score - 40)
                self._add_fx("WRONG", self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (200,60,60))
                self._SFX("wrong")

            self.notes.remove(n)
            return

        if signed < -self.hit_window and dist <= self.hit_window + self.early_window:
            if n["correct"]:
                early_offset = (-signed) - self.hit_window
                early_ratio  = 1.0 - (early_offset / self.early_window)

                self.hits += 1
                self.combo += 1
                self.best_combo = max(self.best_combo, self.combo)

                base_early = 60
                self.score += int(base_early * (0.6 + 0.4*early_ratio) * (1 + 0.01*self.combo))

                tag = "GOOD" if early_ratio >= 0.5 else "BAD"
                self._add_fx(tag, self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (70,200,70))

                self._SFX("hit", "good" if early_ratio >= 0.5 else "bad")
                if self.combo > 1:
                    self._SFX("combo_up", int(self.combo))
            else:
                self.misses += 1
                self.combo = 0
                self.score = max(0, self.score - 40)
                self._add_fx("WRONG", self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (200,60,60))
                self._SFX("wrong")

            self.notes.remove(n)
            return

        self._flash_lane(lane, (200,60,60))
        self._register_miss()

    def _flash_lane(self, lane, color, dur_ms=150):
        self.lane_flash[lane] = (color, pygame.time.get_ticks() + dur_ms)

    def _register_miss(self):
        self.misses += 1
        self.combo = 0
        self.score = max(0, self.score - 30)
        self._add_fx("MISS", (self.lanes[0].x + self.lanes[-1].right)//2, self.hit_y-10)
        self._SFX("miss")

    # ---------- SPAWN / UPDATE ----------
    def _spawn_notes(self):
        for lane_idx, alt in enumerate(self._lane_alternativas):
            self.notes.append({
                "lane": lane_idx,
                "y": self.lanes[lane_idx].y - 30,  # centro do card
                "text": alt["txt"],
                "correct": bool(alt["ok"])
            })
            self._SFX("spawn_note", int(lane_idx), bool(alt["ok"]))

    def _add_fx(self, txt, x, y):
        self.fx.append({"txt": txt, "x": x, "y": y, "alpha": 255, "dy": -28})

    def _update_fx(self, dt):
        for f in self.fx[:]:
            f["y"] += f["dy"] * dt
            f["alpha"] -= 180 * dt
            if f["alpha"] <= 0:
                self.fx.remove(f)

    def _update_physics(self):
        if self.finished:
            return

        now = pygame.time.get_ticks()
        dt = (now - self._last_tick) / 1000.0
        self._last_tick = now

        self.speed = self.base_speed + self.combo * 2
        self.beat_ms = max(900, self.base_beat - self.combo * 5)

        for n in self.notes[:]:
            n["y"] += self.speed * dt
            if n["y"] > self.lanes[n["lane"]].bottom + 40:
                if n["correct"]:
                    self._register_miss()
                self.notes.remove(n)

        # terminou a onda atual; espera o "beat" pra começar a próxima
        if not self.notes and (now - self.last_spawn >= self.beat_ms):
            self._SFX("wave_end")
            self._prepare_next_prompt()
            self._spawn_notes()
            self.last_spawn = now

        if now - self.start_time >= self.game_len_ms:
            self.finished = True
            self._finish()
            return

        self._update_fx(dt)

    def _finish(self):
        total_events = max(1, self.hits + self.misses)
        acc = self.hits / total_events
        if acc >= 0.90: stars = 3
        elif acc >= 0.70: stars = 2
        elif acc >= 0.50: stars = 1
        else: stars = 0

        self._SFX("finish", bool(stars >= 1), int(self.score))

        if self.on_finish:
            self.on_finish(self.score, stars)

    # ---------- NOTAS: QUEBRA CONTROLADA + AUTO-FORMAT ----------
    def _prettify_note_text(self, text: str) -> str:
        t = (text or "").replace(" | ", "\n")
        t = re.sub(r"\s*;\s*", "\n", t)
        t = re.sub(
            r"(\b(for|if|elif|else|while|def|try|except)\b[^:\n]*:\s*)(\S)",
            r"\1\n    \3",
            t
        )
        return t

    def _manual_lines(self, text: str):
        t = self._prettify_note_text(text)
        lines = t.split("\n")
        if len(lines) > self.max_note_lines:
            lines = lines[:self.max_note_lines]
        return lines

    def _fit_block_font(self, lines, max_w):
        size = self.note_font_base_size
        while size >= self.note_font_min_size:
            font = pygame.font.SysFont("Consolas", size)
            if all(font.size(ln)[0] <= max_w for ln in lines):
                return font, lines, False
            size -= 1
        font = pygame.font.SysFont("Consolas", self.note_font_min_size)
        overflow = False
        new_lines = []
        for i, ln in enumerate(lines):
            s = ln
            if font.size(s)[0] > max_w:
                overflow = True
                while s and font.size(s + "…")[0] > max_w:
                    s = s[:-1]
                s = s + "…" if s else "…"
            new_lines.append(s)
        return font, new_lines, overflow

    def _draw_note_card(self, tela, lane_rect, center_y, text, is_correct):
        card_w = lane_rect.w - 12
        max_text_w = card_w - self.note_pad_x*2

        lines = self._manual_lines(text)
        font, lines, overflow = self._fit_block_font(lines, max_text_w)
        if overflow:
            try:
                pass
                # print(f"[PythonHero] Texto longo no card: {text!r}")
            except Exception:
                pass

        txt_h = sum(font.get_height() for _ in lines) + self.note_line_gap*(len(lines)-1 if lines else 0)
        card_h = self.note_pad_y*2 + txt_h
        card_rect = pygame.Rect(lane_rect.x+6, int(center_y) - card_h//2, card_w, card_h)

        pygame.draw.rect(tela, (190, 205, 230), card_rect, border_radius=self.note_corner)
        pygame.draw.rect(tela, (20, 20, 20), card_rect, 2, border_radius=self.note_corner)

        y = card_rect.y + self.note_pad_y
        for i, ln in enumerate(lines):
            ts = font.render(ln, True, (0,0,0))
            x = card_rect.centerx - ts.get_width()//2
            tela.blit(ts, (x, y))
            y += font.get_height()
            if i < len(lines)-1:
                y += self.note_line_gap

    # ---------- DESENHO ----------
    @staticmethod
    def _wrap(text, fonte, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if fonte.size(test)[0] <= max_w:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    def _draw_panel(self, tela):
        p = self.prompt
        surf = pygame.Surface((p.w, p.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (18, 24, 32, 240), (0,0,p.w,p.h), border_radius=16)
        pygame.draw.rect(surf, (42, 103, 188), (0,0,p.w,p.h), 6, border_radius=16)
        tela.blit(surf, (p.x, p.y))

        header_h = 56
        header = pygame.Rect(p.x, p.y, p.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (p.x, p.y+header_h), (p.x+p.w, p.y+header_h), 2)
        titulo = self.fonte_g.render("Python Hero", True, (230,240,255))
        tela.blit(titulo, (p.x+24, p.y+10))

    def desenhar(self, tela):
        if self.finished:
            return

        self._draw_panel(tela)
        p = self.prompt

        # update
        self._update_physics()
        now = pygame.time.get_ticks()

        # enunciado
        prompt_area = pygame.Rect(p.x+24, p.y+62, p.w-48, 72)
        lines = self._wrap(self.current_prompt, self.fonte, prompt_area.w)
        y = prompt_area.y
        for ln in lines[:3]:
            tela.blit(self.fonte.render(ln, True, (230,230,90)), (prompt_area.x, y))
            y += 24

        # trilhas + flash
        key_order = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
        for i, lane in enumerate(self.lanes):
            flash = self.lane_flash[i]
            if flash and now < flash[1]:
                color = flash[0]
            else:
                color = (40, 60, 100) if key_order[i] not in self.pressed else (55, 75, 125)
                if flash and now >= flash[1]:
                    self.lane_flash[i] = None
            pygame.draw.rect(tela, color, lane, border_radius=8)
            key_label = ["A","S","D","F"][i]
            ksurf = self.fonte.render(key_label, True, (160, 200, 255))
            tela.blit(ksurf, (lane.centerx - ksurf.get_width()//2, lane.y - 24))

        # hit line
        pygame.draw.line(tela, (110,190,255), (self.lanes[0].x, self.hit_y), (self.lanes[-1].right, self.hit_y), 4)

        # notas
        for n in self.notes:
            lane = self.lanes[n["lane"]]
            self._draw_note_card(tela, lane, n["y"], n["text"], n["correct"])

        # FX
        for f in self.fx:
            s = self.fonte_fx.render(f["txt"], True, (255,255,255))
            s.set_alpha(max(0, int(f["alpha"])))
            tela.blit(s, (int(f["x"] - s.get_width()//2), int(f["y"])))

        # HUD
        elapsed = pygame.time.get_ticks() - self.start_time
        remain = max(0, (self.game_len_ms - elapsed)//1000)
        hud1 = "A,S,D,F ► Colunas  |  Acerte na linha azul  |  Verde=acertou / Vermelho=errou"
        hud2 = f"Tempo: {remain:02d}s  |  Score: {self.score}  |  Combo: {self.combo}  |  Best: {self.best_combo}"
        tela.blit(self.fonte_t.render(hud1, True, (210,210,210)), (p.x+24, p.bottom-58))
        tela.blit(self.fonte_t.render(hud2, True, (210,210,210)), (p.x+24, p.bottom-34))
