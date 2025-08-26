import pygame
import random
import time
from math import pi
from Intermediario.Content.BugSquashContent import get_bug_squash_content

# ============================================================
# Whack-a-Python (Intermediário) — por rodadas
#   • Rodadas de 5s (configuráveis): várias cobras simultâneas.
#   • Alvo alterna por rodada: BUG ↔ CORRETO (badge colorido).
#   • Temporizador circular por rodada (topo, centro).
#   • Histórico lateral com hover + SCROLL (durante e após o jogo).
#   • Feedback de clique: marreta animada + anel de impacto + pop de pontos.
#   • Balões de código com ANTICOLISÃO (posicionamento inteligente + leader line).
#   • Fim: congela campo, botão CONTINUAR; então on_finish({...}).
# ============================================================

class TelaBugSquashArcade:
    def __init__(
        self,
        largura: int,
        altura: int,
        topic_title: str,
        on_finish,
        pass_score: int = 360,
        round_seconds: int = 35,   # duração total do minigame
        lanes: int = 7,
        sfx=None,
    ):
        self.sfx = sfx 
        self.largura = largura
        self.altura = altura
        self.topic_title = topic_title or "print"
        self.on_finish = on_finish
        self.pass_score = int(pass_score)
        self.total_seconds = max(10, int(round_seconds))

        

        # ===== fonts
        pygame.font.init()
        self.fonte_xl   = pygame.font.SysFont("Consolas", 26, bold=True)
        self.fonte_g    = pygame.font.SysFont("Consolas", 22, bold=True)
        self.fonte      = pygame.font.SysFont("Consolas", 18)
        self.fonte_s    = pygame.font.SysFont("Consolas", 16)
        self.fonte_mono = pygame.font.SysFont("Consolas", 18)

        # ===== layout geral
        self.prompt = pygame.Rect(int(largura*0.14), int(altura*0.08), int(largura*0.72), int(altura*0.80))
        pad = 28
        header_h = 56
        self._header_h = header_h  # guarda para o timer
        body_y = self.prompt.y + header_h + pad
        body_h = self.prompt.h - header_h - pad*2 - 64
        body_w = self.prompt.w - pad*2

        # campo + sidebar
        self.sidebar_w = int(body_w * 0.28)
        self.field_rect   = pygame.Rect(self.prompt.x + pad, body_y, body_w - self.sidebar_w - 16, body_h)
        self.sidebar_rect = pygame.Rect(self.field_rect.right + 16, body_y, self.sidebar_w, body_h)

        # botão continuar (só aparece no fim)
        btn_w, btn_h = 220, 52
        self.btn_continue = pygame.Rect(self.prompt.centerx - btn_w//2, self.prompt.bottom - pad - btn_h, btn_w, btn_h)

        # ===== estado base
        self.running = True
        self.finished = False
        self.start_ts = time.time()
        self.time_left = float(self.total_seconds)

        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.last_hit_ts = 0.0
        self.combo_window = 1.25
        self.lives = 3
        self.misses = 0

        # ===== conteúdo
        rows, _hint = get_bug_squash_content(self.topic_title, lanes=lanes, min_bugs=2)
        self.pool_bug = [r for r in rows if str(r.get("bug","0")) == "1"]
        self.pool_ok  = [r for r in rows if str(r.get("bug","0")) != "1"]
        if not self.pool_ok:  # fallback
            self.pool_ok = [{"code": r.get("fix") or r.get("code",""), "bug":"0", "why": r.get("why","")} for r in rows]

        # ===== grade de buracos
        self.grid_rows = 3
        self.grid_cols = 5
        self.holes = []      # lista de rects
        self._build_holes()

        # ===== por rodada
        self.round_len = 5.0                   # 5 segundos por rodada (ajustável)
        self.num_rounds = max(1, int(self.total_seconds // self.round_len))
        self.round_idx = 0                     # 0-based
        self.target_mode = "BUG"               # BUG ou CORRECT (alterna por rodada)
        self.round_start_ts = self.start_ts
        self.round_end_ts = self.round_start_ts + self.round_len

        # cobras ativas nesta rodada:
        # dict {hole_idx, code, is_bug, why, hit}
        self.spawns = []
        self._compose_round()                  # gera a 1ª rodada

        # ===== histórico lateral + SCROLL
        # cada item: {"code":str, "why":str, "is_bug":bool}
        self.hits_ok_list  = []
        self.hits_bug_list = []
        # rects visíveis (para hover)
        self._hist_rects_ok = []
        self._hist_rects_bug = []
        self._hover_tooltip = ""               # texto atual do tooltip (porquê)
        # scroll state
        self.scroll_ok = 0.0
        self.scroll_bug = 0.0
        self._area_ok = pygame.Rect(0,0,0,0)   # preenchido no draw
        self._area_bug = pygame.Rect(0,0,0,0)

        # ===== efeitos de clique
        # cada efeito: {"x","y","start","dur_mallet","dur_ring","dur_pop","success", "pop"}
        self.hit_fx = []

    def _SFX(self, name, *a, **kw):
        s = getattr(self, "sfx", None)
        if not s: return
        fn = getattr(s, name, None)
        if callable(fn):
            try: fn(*a, **kw)
            except Exception: pass
    
    # ---------------------------------------------------------
    # utils
    def _wrap_text(self, text: str, font: pygame.font.Font, max_w: int):
        if not text:
            return [""]
        words = str(text).split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # ====== ANTICOLISÃO DE BALÕES ======
    def _clamp_to_field(self, x, y, w, h):
        x = max(self.field_rect.x + 6, min(x, self.field_rect.right - 6 - w))
        y = max(self.field_rect.y + 6, min(y, self.field_rect.bottom - 6 - h))
        return x, y

    def _bubble_candidates(self, hole_rect: pygame.Rect, bb_w: int, bb_h: int):
        """
        Gera posições candidatas para o balão deste hole.
        Retorna lista de tuplas (x, y, ((ax,ay),(bx,by))) onde o último par
        é a 'leader line' ligando o hole ao balão.
        """
        cx = hole_rect.centerx
        anchor = (cx, hole_rect.y - 6)  # ponto de origem da leader line

        cand = []
        # A) acima-centro
        x = cx - bb_w // 2; y = hole_rect.y - bb_h - 28
        x, y = self._clamp_to_field(x, y, bb_w, bb_h)
        cand.append((x, y, (anchor, (x + bb_w // 2, y + bb_h))))
        # B) acima-esq
        x = hole_rect.x - bb_w - 12; y = hole_rect.y - bb_h + 4
        x, y = self._clamp_to_field(x, y, bb_w, bb_h)
        cand.append((x, y, (anchor, (x + bb_w, y + bb_h // 2))))
        # C) acima-dir
        x = hole_rect.right + 12; y = hole_rect.y - bb_h + 4
        x, y = self._clamp_to_field(x, y, bb_w, bb_h)
        cand.append((x, y, (anchor, (x, y + bb_h // 2))))
        # D) acima-centro deslocado
        x = cx - bb_w // 2 - 30; y = hole_rect.y - bb_h - 12
        x, y = self._clamp_to_field(x, y, bb_w, bb_h)
        cand.append((x, y, (anchor, (x + bb_w // 2, y + bb_h))))
        # E) fallback: abaixo-centro
        x = cx - bb_w // 2; y = hole_rect.bottom + 6
        x, y = self._clamp_to_field(x, y, bb_w, bb_h)
        cand.append((x, y, (anchor, (x + bb_w // 2, y))))
        return cand

    def _place_non_overlapping(self, candidates, placed_rects, bb_w, bb_h, pad=6):
        """Escolhe a 1ª posição candidata que não colide com balões já colocados."""
        for x, y, leader in candidates:
            r = pygame.Rect(x, y, bb_w, bb_h)
            ok = True
            for pr in placed_rects:
                if r.inflate(pad, pad).colliderect(pr.inflate(pad, pad)):
                    ok = False
                    break
            if ok:
                return r, leader
        # se todas colidem, usa a 1ª mesmo
        x, y, leader = candidates[0]
        return pygame.Rect(x, y, bb_w, bb_h), leader

    # ---------------------------------------------------------
    # campo / buracos
    def _build_holes(self):
        r = self.field_rect
        pad_x, pad_y = 18, 18
        inner = pygame.Rect(r.x + pad_x, r.y + pad_y, r.w - pad_x*2, r.h - pad_y*2)

        cell_w = inner.w // self.grid_cols
        cell_h = inner.h // self.grid_rows

        diameter = min(int(cell_w*0.6), int(cell_h*0.5))
        self.hole_radius = max(24, diameter//2)
        self.holes = []

        for gy in range(self.grid_rows):
            for gx in range(self.grid_cols):
                cx = inner.x + gx*cell_w + cell_w//2
                cy = inner.y + gy*cell_h + int(cell_h*0.65)
                rect = pygame.Rect(cx - self.hole_radius, cy - self.hole_radius,
                                   self.hole_radius*2, self.hole_radius*2)
                self.holes.append(rect)

    # ---------------------------------------------------------
    # rodada
    def _compose_round(self):
        """Gera as cobras da rodada atual (todas ficam o tempo da rodada)."""
        self.spawns = []

        # alterna alvo a cada rodada (BUG -> CORRECT -> BUG -> ...)
        self.target_mode = "BUG" if (self.round_idx % 2 == 0) else "CORRECT"

        # quantas cobras simultâneas? subset aleatório dos buracos
        total_holes = len(self.holes)
        min_snakes = max(4, total_holes // 3)
        max_snakes = max(min_snakes, total_holes - 3)
        k = random.randint(min_snakes, max_snakes)

        hole_indices = random.sample(range(total_holes), k=k)

        # alvos da rodada: ~60% do tipo alvo e pelo menos 1
        num_target = max(1, int(0.6 * k))
        target_first = random.sample(hole_indices, k=num_target)
        distractors = [h for h in hole_indices if h not in target_first]

        def pick_from(pool):
            row = random.choice(pool)
            code = (row.get("code") or "").replace("\t", "    ").replace("\r\n", "\n").replace("\r", "\n").strip()
            why  = (row.get("why") or "")
            return code, why

        if self.target_mode == "BUG":
            for hi in target_first:
                code, why = pick_from(self.pool_bug if self.pool_bug else self.pool_ok)
                self.spawns.append({"hole_idx": hi, "code": code, "is_bug": True,  "why": why, "hit": False})
            for hi in distractors:
                code, why = pick_from(self.pool_ok  if self.pool_ok  else self.pool_bug)
                self.spawns.append({"hole_idx": hi, "code": code, "is_bug": False, "why": why, "hit": False})
        else:  # CORRECT
            for hi in target_first:
                code, why = pick_from(self.pool_ok  if self.pool_ok  else self.pool_bug)
                self.spawns.append({"hole_idx": hi, "code": code, "is_bug": False, "why": why, "hit": False})
            for hi in distractors:
                code, why = pick_from(self.pool_bug if self.pool_bug else self.pool_ok)
                self.spawns.append({"hole_idx": hi, "code": code, "is_bug": True,  "why": why, "hit": False})

        # --- sons de spawn (agora que self.spawns está preenchida) ---
        for sp in self.spawns:
            if sp["is_bug"]:
                self._SFX("spawn_bug")
            else:
                self._SFX("spawn_ok")


    def _next_round_or_finish(self):
        # acabou a rodada atual
        self._SFX("round_end", self.target_mode, int(self.round_idx+1))

        self.round_idx += 1
        if self.round_idx >= self.num_rounds:
            self.running = False
            self.finished = True
            # fim por tempo -> som de finish (aprovado se bateu score)
            self._SFX("finish", bool(self.score >= self.pass_score), int(self.score))
            return
        now = time.time()
        self.round_start_ts = now
        self.round_end_ts = now + self.round_len
        self._compose_round()


    # ---------------------------------------------------------
    # pontuação / vida
    def _register_hit(self, spawn):
        now = time.time()
        if now - self.last_hit_ts <= self.combo_window:
            self.combo += 1
        else:
            self.combo = 1
        self.last_hit_ts = now
        self.max_combo = max(self.max_combo, self.combo)

        add = 120 + (self.combo - 1) * 20
        self.score += add

        # --- SONS ---
        self._SFX("squash")                 # acerto
        if self.combo > 1:
            self._SFX("combo_up", self.combo)  # qualquer aumento de combo

        # histórico (com fallback de why)
        why = (spawn.get("why") or "").strip()
        item = {"code": spawn["code"],
                "why": why if why else ("Sintaxe/saída válida." if not spawn["is_bug"] else "Bug de sintaxe/semântica."),
                "is_bug": spawn["is_bug"]}
        if self.target_mode == "BUG":
            self.hits_bug_list.append(item)
        else:
            self.hits_ok_list.append(item)
        return add

    def _register_miss(self):
        self._SFX("miss")     # erro
        self.misses += 1
        self.lives -= 1
        self.combo = 0
        self.score = max(0, self.score - 40)
        if self.lives <= 0:
            self.running = False
            self.finished = True
            # fim por vidas -> som de finish (reprovado)
            self._SFX("finish", False, int(self.score))
        return -40


    # ---------------------------------------------------------
    # efeitos
    def _spawn_hit_fx(self, x, y, success: bool, pop_text: str):
        self.hit_fx.append({
            "x": int(x),
            "y": int(y),
            "start": time.time(),
            "dur_mallet": 0.22,
            "dur_ring": 0.35,
            "dur_pop": 0.60,
            "success": bool(success),
            "pop": str(pop_text)
        })

    def _ease_out_cubic(self, t):
        t = max(0.0, min(1.0, t))
        return 1 - (1 - t) ** 3

    def _blit_rotate(self, surf, img, pivot_pos, origin_pos, angle_deg):
        """
        Gira 'img' em torno do ponto 'origin_pos' (coordenada local da imagem),
        posicionando o pivot em 'pivot_pos' na tela.
        """
        image_rect = img.get_rect(topleft=(pivot_pos[0] - origin_pos[0], pivot_pos[1] - origin_pos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pivot_pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle_deg)
        rotated_image_center = (pivot_pos[0] - rotated_offset.x, pivot_pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(img, angle_deg)
        rotated_rect = rotated_image.get_rect(center=rotated_image_center)
        surf.blit(rotated_image, rotated_rect)

    def _draw_hit_fx(self, tela: pygame.Surface):
        now = time.time()
        alive = []
        for fx in self.hit_fx:
            t = now - fx["start"]
            total_dur = max(fx["dur_pop"], fx["dur_ring"], fx["dur_mallet"])
            if t <= total_dur:
                alive.append(fx)

                # --- mallet ---
                if t <= fx["dur_mallet"]:
                    tn = t / fx["dur_mallet"]
                    tn = self._ease_out_cubic(tn)
                    angle = -70 + 90 * tn  # de levantada (-70) até quase 20°
                    # sprite da marreta
                    mallet = pygame.Surface((90, 90), pygame.SRCALPHA)
                    # cabo
                    pygame.draw.rect(mallet, (140, 100, 60), (44, 8, 8, 66), border_radius=4)
                    # cabeça
                    head_col = (200, 70, 70) if fx["success"] else (200, 60, 60)
                    pygame.draw.rect(mallet, (30, 20, 20), (26, 48, 42, 18), border_radius=5)
                    pygame.draw.rect(mallet, head_col, (28, 50, 38, 14), border_radius=4)
                    # pivot: ponta inferior da cabeça
                    pivot_local = (47, 62)
                    self._blit_rotate(tela, mallet, (fx["x"], fx["y"]), pivot_local, angle)

                # --- anel de impacto ---
                if t <= fx["dur_ring"]:
                    rn = t / fx["dur_ring"]
                    radius = int(8 + rn * 36)
                    alpha = int(180 * (1 - rn))
                    col = (120, 220, 160, alpha) if fx["success"] else (240, 120, 120, alpha)
                    ring = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
                    pygame.draw.circle(ring, col, (radius+2, radius+2), radius, 3)
                    tela.blit(ring, (fx["x"] - radius - 2, fx["y"] - radius - 2))

                # --- pop de pontos ---
                if t <= fx["dur_pop"] and fx["pop"]:
                    pn = t / fx["dur_pop"]
                    up = int(18 * pn)
                    alpha = int(255 * (1 - pn))
                    col = (180, 255, 200) if fx["success"] else (255, 180, 180)
                    pop_surf = self.fonte.render(fx["pop"], True, col)
                    tmp = pygame.Surface(pop_surf.get_size(), pygame.SRCALPHA)
                    tmp.blit(pop_surf, (0, 0))
                    tmp.set_alpha(alpha)
                    tela.blit(tmp, (fx["x"] - pop_surf.get_width()//2, fx["y"] - 30 - up))
        self.hit_fx = alive

    # ---------------------------------------------------------
    # draw
    def _draw_panel(self, tela: pygame.Surface):
        p = self.prompt
        surf = pygame.Surface((p.w, p.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (18, 24, 32, 235), surf.get_rect(), border_radius=16)
        pygame.draw.rect(surf, (42, 103, 188), surf.get_rect(), 6, border_radius=16)
        pygame.draw.rect(surf, (18, 24, 32), (8, 8, p.w-16, p.h-16), 4, border_radius=12)
        tela.blit(surf, (p.x, p.y))

        header = pygame.Rect(p.x, p.y, p.w, self._header_h)
        pygame.draw.rect(tela, (28, 44, 80), header, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (p.x, p.y+self._header_h), (p.x+p.w, p.y+self._header_h), 2)

        # título (esquerda)
        titulo = self.fonte_xl.render("Whack-a-Python", True, (230, 240, 255))
        tela.blit(titulo, (p.x+24, p.y+10))

        # badge (direita)
        alvo_bug = (self.target_mode == "BUG")
        badge_col = (210, 80, 80) if alvo_bug else (80, 170, 110)
        text_col  = (255,255,255)
        round_txt = f"Rodada {min(self.round_idx+1, self.num_rounds)}/{self.num_rounds}"
        alvo_txt  = "Alvo: COBRAS COM BUG" if alvo_bug else "Alvo: COBRAS CORRETAS"
        badge_str = f"{round_txt}  •  {alvo_txt}"
        badge_surf = self.fonte.render(badge_str, True, text_col)
        padx, pady = 12, 8
        bw = badge_surf.get_width() + padx*2
        bh = badge_surf.get_height() + pady*2
        bx = header.right - bw - 16
        by = header.y + (header.h - bh)//2
        pygame.draw.rect(tela, badge_col, (bx, by, bw, bh), border_radius=10)
        pygame.draw.rect(tela, (20, 20, 25), (bx, by, bw, bh), 2, border_radius=10)
        tela.blit(badge_surf, (bx + padx, by + pady))

        # subtítulo (tópico)
        subt = self.fonte.render(f"Tópico: {self.topic_title}", True, (190, 210, 245))
        tela.blit(subt, (p.x+24, p.y+10+26))

        # --- temporizador circular (centro do header) ---
        self._draw_round_timer(tela, header, badge_col)

    def _draw_round_timer(self, tela: pygame.Surface, header_rect: pygame.Rect, color_main):
        """Desenha um anel indicando a fração restante da RODADA."""
        cx = header_rect.centerx
        cy = header_rect.y + header_rect.h // 2
        outer_r = 20
        inner_r = 14
        ring_w  = outer_r - inner_r

        pygame.draw.circle(tela, (22, 30, 40), (cx, cy), outer_r)
        pygame.draw.circle(tela, (12, 18, 26), (cx, cy), inner_r)

        now = time.time()
        remain = max(0.0, self.round_end_ts - now) if self.running else 0.0
        frac = 0.0 if not self.running else max(0.0, min(1.0, remain / self.round_len))

        col_arc = (min(color_main[0]+30,255), min(color_main[1]+30,255), min(color_main[2]+30,255))
        rect = pygame.Rect(cx-outer_r, cy-outer_r, outer_r*2, outer_r*2)
        start_angle = -pi/2
        end_angle   = start_angle + 2*pi*frac
        if frac > 0:
            pygame.draw.arc(tela, col_arc, rect, start_angle, end_angle, ring_w)
        pygame.draw.circle(tela, (60, 160, 255), (cx, cy), outer_r, 1)

    def _draw_field(self, tela: pygame.Surface):
        pygame.draw.rect(tela, (24, 30, 44), self.field_rect, border_radius=12)
        pygame.draw.rect(tela, (90, 170, 255), self.field_rect, 2, border_radius=12)

        # buracos
        for rect in self.holes:
            pygame.draw.ellipse(tela, (20, 20, 28), rect)
            pygame.draw.ellipse(tela, (50, 80, 110), rect, 2)

        # ===== balões sem sobreposição =====
        placed_bubbles = []

        # cobras (ordena por y do hole para estabilidade visual)
        active_spawns = [s for s in self.spawns if not s["hit"]]
        active_spawns.sort(key=lambda s: self.holes[s["hole_idx"]].y)

        for s in active_spawns:
            rect = self.holes[s["hole_idx"]]
            # “cobra” emergindo (desenha primeiro)
            head = pygame.Rect(rect.centerx-18, rect.y-22, 36, 36)
            body = pygame.Rect(rect.centerx-12, rect.y-2, 24, 22)
            pygame.draw.ellipse(tela, (80, 200, 120), head)
            pygame.draw.ellipse(tela, (30, 80, 50), head, 2)
            pygame.draw.ellipse(tela, (80, 200, 120), body)
            pygame.draw.ellipse(tela, (30, 80, 50), body, 2)
            pygame.draw.circle(tela, (255,255,255), (head.centerx-6, head.centery-4), 3)
            pygame.draw.circle(tela, (255,255,255), (head.centerx+6, head.centery-4), 3)
            pygame.draw.circle(tela, (20,20,20), (head.centerx-6, head.centery-4), 1)
            pygame.draw.circle(tela, (20,20,20), (head.centerx+6, head.centery-4), 1)

            # balão com código (wrap) — agora com anticolisão
            max_w = int(self.field_rect.w * 0.35)
            lines = self._wrap_text(s["code"], self.fonte_s, max_w)
            lines = lines[:3] + (["..."] if len(lines) > 3 else [])
            bb_w = max(self.fonte_s.size(l)[0] for l in lines) + 16
            bb_h = len(lines) * (self.fonte_s.get_height() + 2) + 12

            # gera candidatos e escolhe sem sobreposição
            candidates = self._bubble_candidates(rect, bb_w, bb_h)
            bubble, leader = self._place_non_overlapping(candidates, placed_bubbles, bb_w, bb_h, pad=6)

            # desenha balão
            pygame.draw.rect(tela, (36, 52, 92), bubble, border_radius=8)
            pygame.draw.rect(tela, (120, 180, 255), bubble, 1, border_radius=8)

            # texto
            yy = bubble.y + 6
            for ln in lines:
                img = self.fonte_s.render(ln, True, (235, 235, 245))
                tela.blit(img, (bubble.x + 8, yy))
                yy += self.fonte_s.get_height() + 2

            # leader line (linha que liga o hole ao balão)
            if leader:
                (ax, ay), (bx, by) = leader
                pygame.draw.aaline(tela, (120, 180, 255), (ax, ay), (bx, by))

            # registra para evitar colisões nas próximas cobras
            placed_bubbles.append(bubble)

        # efeitos por cima do campo
        self._draw_hit_fx(tela)

    def _draw_sidebar(self, tela: pygame.Surface):
        r = self.sidebar_rect
        pygame.draw.rect(tela, (25, 36, 52), r, border_radius=12)
        pygame.draw.rect(tela, (90, 170, 255), r, 2, border_radius=12)

        def row(label, value, y):
            s1 = self.fonte_g.render(label, True, (230, 240, 255))
            s2 = self.fonte_g.render(value, True, (255, 235, 120))
            tela.blit(s1, (r.x + 14, y))
            tela.blit(s2, (r.right - 14 - s2.get_width(), y))

        y = r.y + 14
        secs = int(self.time_left)
        row("SCORE", str(self.score), y); y += 30
        row("COMBO", f"x{self.combo}", y); y += 30
        row("MAX", f"x{self.max_combo}", y); y += 30
        row("VIDAS", "♥"*self.lives, y); y += 30
        row("TEMPO", f"{secs:02d}s", y); y += 36

        alvo = "BUG" if self.target_mode=="BUG" else "CORRETO"
        alvo_s = self.fonte.render(f"Alvo desta rodada: {alvo}", True, (200, 220, 255))
        tela.blit(alvo_s, (r.x+14, y)); y += 28

        pygame.draw.line(tela, (60, 160, 255), (r.x+12, y), (r.right-12, y), 2)
        y += 8

        # ===== títulos + cálculo de áreas com altura dividida =====
        title_h = self.fonte_g.get_height() + 2
        available_boxes = (r.bottom - 12) - (y + title_h + 6 + title_h + 6)
        box_h = max(60, available_boxes // 2)

        # --- CORRETOS ---
        title = self.fonte_g.render(f"Corretos ({len(self.hits_ok_list)})", True, (130, 230, 160))
        tela.blit(title, (r.x+14, y)); y += title_h
        self._area_ok = pygame.Rect(r.x+10, y, r.w-20, box_h)
        self._draw_scroll_list(
            tela, self._area_ok, self.hits_ok_list,
            is_bug=False,
            scroll_attr="scroll_ok"
        )
        y = self._area_ok.bottom + 6

        # --- BUGS ---
        title2 = self.fonte_g.render(f"Bugs ({len(self.hits_bug_list)})", True, (255, 170, 160))
        tela.blit(title2, (r.x+14, y)); y += title_h
        self._area_bug = pygame.Rect(r.x+10, y, r.w-20, box_h)
        self._draw_scroll_list(
            tela, self._area_bug, self.hits_bug_list,
            is_bug=True,
            scroll_attr="scroll_bug"
        )

        # tooltip (se houver)
        if self._hover_tooltip:
            mx, my = pygame.mouse.get_pos()
            lines = self._wrap_text(self._hover_tooltip, self.fonte_s, 320)
            w = max(self.fonte_s.size(l)[0] for l in lines) + 16
            h = len(lines)*(self.fonte_s.get_height()+2) + 12
            x = min(mx + 16, self.prompt.right - w - 8)
            y = min(my + 16, self.prompt.bottom - h - 8)
            tip = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(tip, (30, 44, 70, 240), tip.get_rect(), border_radius=8)
            pygame.draw.rect(tip, (120, 180, 255), tip.get_rect(), 1, border_radius=8)
            yy = 6
            for ln in lines:
                s = self.fonte_s.render(ln, True, (230, 240, 255))
                tip.blit(s, (8, yy)); yy += self.fonte_s.get_height()+2
            tela.blit(tip, (x, y))

    def _draw_scroll_list(self, tela, area: pygame.Rect, items, is_bug: bool, scroll_attr: str):
        """Lista com SCROLL (roda do mouse) + barra."""
        pygame.draw.rect(tela, (28, 42, 64), area, border_radius=8)
        pygame.draw.rect(tela, (80, 140, 220), area, 1, border_radius=8)

        line_h = self.fonte_s.get_height() + 6
        content_h = max(0, len(items) * line_h)
        max_scroll = max(0, content_h - area.h)

        scroll_val = getattr(self, scroll_attr)
        scroll_val = max(0.0, min(scroll_val, float(max_scroll)))
        setattr(self, scroll_attr, scroll_val)

        old_clip = tela.get_clip()
        tela.set_clip(area)

        if not items:
            s = self.fonte_s.render("— sem itens —", True, (210, 215, 225))
            tela.blit(s, (area.centerx - s.get_width()//2, area.centery - s.get_height()//2))
            tela.set_clip(old_clip)
            return

        first_idx = int(scroll_val // line_h)
        y = area.y - int(scroll_val - first_idx * line_h)

        if is_bug:
            self._hist_rects_bug = []
        else:
            self._hist_rects_ok = []

        inner_w = area.w - 12
        i = first_idx
        while i < len(items) and y < area.bottom:
            it = items[i]
            row_rect = pygame.Rect(area.x+2, y, inner_w-2, line_h-1)
            base_col = (40, 56, 84) if not is_bug else (48, 52, 80)
            pygame.draw.rect(tela, base_col, row_rect, border_radius=6)

            txt = (it.get("code","") or "").replace("\n","  ")
            wrap = self._wrap_text(txt, self.fonte_s, inner_w - 14)
            line = wrap[0] + (" ..." if len(wrap) > 1 else "")
            surf = self.fonte_s.render("• " + line, True, (220, 235, 240) if not is_bug else (235, 225, 225))
            tela.blit(surf, (row_rect.x+6, row_rect.y + (row_rect.h - surf.get_height())//2))

            pair = (row_rect, it)
            if is_bug:
                self._hist_rects_bug.append(pair)
            else:
                self._hist_rects_ok.append(pair)

            y += line_h
            i += 1

        tela.set_clip(old_clip)

        if content_h > area.h:
            track = pygame.Rect(area.right-10, area.y+2, 8, area.h-4)
            pygame.draw.rect(tela, (26, 36, 52), track, border_radius=4)
            thumb_h = max(24, int(area.h * area.h / content_h))
            thumb_y = track.y + int((track.h - thumb_h) * (scroll_val / max_scroll)) if max_scroll > 0 else track.y
            thumb = pygame.Rect(track.x+1, thumb_y, track.w-2, thumb_h)
            pygame.draw.rect(tela, (90, 170, 255), thumb, border_radius=4)

    def _draw_finish_overlay(self, tela: pygame.Surface):
        overlay = pygame.Surface((self.field_rect.w, self.field_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0,0,0,140), overlay.get_rect(), border_radius=16)
        tela.blit(overlay, (self.field_rect.x, self.field_rect.y))

        title = self.fonte_xl.render("Fim do minigame!", True, (240, 250, 255))
        tela.blit(title, (self.field_rect.centerx - title.get_width()//2, self.field_rect.y + 40))

        info = [
            f"Score: {self.score}",
            f"Acertos CORRETOS: {len(self.hits_ok_list)}",
            f"Acertos BUGS: {len(self.hits_bug_list)}",
            f"Erros: {self.misses}",
        ]
        yy = self.field_rect.y + 90
        for t in info:
            s = self.fonte_g.render(t, True, (220, 230, 245))
            tela.blit(s, (self.field_rect.centerx - s.get_width()//2, yy))
            yy += 28

        mx, my = pygame.mouse.get_pos()
        hovered = self.btn_continue.collidepoint(mx, my)
        base = (0, 150, 200) if hovered else (0, 120, 170)
        pygame.draw.rect(tela, base, self.btn_continue, border_radius=16)
        pygame.draw.rect(tela, (20, 46, 68), self.btn_continue, 3, border_radius=16)
        s = self.fonte_g.render("CONTINUAR", True, (255,255,255))
        tela.blit(s, (self.btn_continue.centerx - s.get_width()//2,
                      self.btn_continue.centery - s.get_height()//2))

    # ---------------------------------------------------------
    # loop
    def desenhar(self, tela: pygame.Surface):
        prev = getattr(self, "_prev_tick", time.time())
        now = time.time()
        dt = max(0.0, min(0.05, now - prev))
        self._prev_tick = now

        if self.running:
            elapsed_total = now - self.start_ts
            self.time_left = max(0.0, self.total_seconds - elapsed_total)
            if now >= self.round_end_ts:
                self._next_round_or_finish()

        self._draw_panel(tela)
        self._draw_field(tela)
        self._draw_sidebar(tela)

        if self.finished:
            self._draw_finish_overlay(tela)

    def tratar_eventos(self, eventos):
        for ev in eventos:
            # hover do histórico (tooltip) — funciona durante e no fim
            if ev.type == pygame.MOUSEMOTION:
                self._hover_tooltip = ""
                mx, my = ev.pos
                for rect, it in (self._hist_rects_ok + self._hist_rects_bug):
                    if rect.collidepoint(mx, my):
                        self._hover_tooltip = (it.get("why") or "").strip()
                        if not self._hover_tooltip:
                            self._hover_tooltip = "Sintaxe/saída válida."
                        break

            # scroll com roda do mouse
            if ev.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                line_h = self.fonte_s.get_height() + 6
                if self._area_ok.collidepoint(mx, my):
                    content_h_ok = max(0, len(self.hits_ok_list)*line_h)
                    max_scroll_ok = max(0, content_h_ok - self._area_ok.h)
                    self.scroll_ok = max(0.0, min(self.scroll_ok - ev.y*40, float(max_scroll_ok)))
                if self._area_bug.collidepoint(mx, my):
                    content_h_bug = max(0, len(self.hits_bug_list)*line_h)
                    max_scroll_bug = max(0, content_h_bug - self._area_bug.h)
                    self.scroll_bug = max(0.0, min(self.scroll_bug - ev.y*40, float(max_scroll_bug)))

            # fallback: botões 4/5
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (4, 5):
                mx, my = ev.pos
                delta = 40 if ev.button == 4 else -40
                line_h = self.fonte_s.get_height() + 6
                if self._area_ok.collidepoint(mx, my):
                    content_h_ok = max(0, len(self.hits_ok_list)*line_h)
                    max_scroll_ok = max(0, content_h_ok - self._area_ok.h)
                    self.scroll_ok = max(0.0, min(self.scroll_ok - (delta/1), float(max_scroll_ok)))
                if self._area_bug.collidepoint(mx, my):
                    content_h_bug = max(0, len(self.hits_bug_list)*line_h)
                    max_scroll_bug = max(0, content_h_bug - self._area_bug.h)
                    self.scroll_bug = max(0.0, min(self.scroll_bug - (delta/1), float(max_scroll_bug)))

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos

                # fim: botão CONTINUAR
                if self.finished and self.btn_continue.collidepoint(mx, my):
                    if callable(self.on_finish):
                        result = {
                            "score": int(self.score),
                            "passed": self.score >= self.pass_score,
                            "hits_ok": len(self.hits_ok_list),
                            "hits_bug": len(self.hits_bug_list),
                            "misses": int(self.misses),
                            "time_spent": float(self.total_seconds - self.time_left),
                            "rounds": int(self.num_rounds),
                        }
                        self.on_finish(result)
                    return

                # durante o jogo: clique em uma cobra?
                if self.running and not self.finished:
                    clicked_spawn = None
                    clicked_rect = None
                    for s in self.spawns:
                        if s["hit"]:
                            continue
                        rect = self.holes[s["hole_idx"]]
                        head = pygame.Rect(rect.centerx-18, rect.y-22, 36, 36)
                        body = pygame.Rect(rect.centerx-12, rect.y-2, 24, 22)
                        if rect.collidepoint(mx, my) or head.collidepoint(mx, my) or body.collidepoint(mx, my):
                            clicked_spawn = s
                            clicked_rect = rect
                            break

                    if clicked_spawn:
                        wanted_bug = (self.target_mode == "BUG")
                        is_target = (clicked_spawn["is_bug"] == wanted_bug)
                        impact_x = clicked_rect.centerx if clicked_rect else mx
                        impact_y = (clicked_rect.y) if clicked_rect else my
                        if is_target:
                            clicked_spawn["hit"] = True
                            gained = self._register_hit(clicked_spawn)
                            self._spawn_hit_fx(impact_x, impact_y, True, f"+{gained}")
                        else:
                            penalty = self._register_miss()
                            self._spawn_hit_fx(impact_x, impact_y, False, f"{penalty}")
                    else:
                        # clique vazio dentro do campo = erro (feedback também)
                        if self.field_rect.collidepoint(mx, my):
                            penalty = self._register_miss()
                            self._spawn_hit_fx(mx, my, False, f"{penalty}")
