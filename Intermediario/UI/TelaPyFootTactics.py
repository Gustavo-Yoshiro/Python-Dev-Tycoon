import pygame
import random
import time
from math import pi
from Intermediario.Content.PyFootContent import get_pyfoot_questions

# ============================================================
# PyFoot Tactics — Passe certo -> DUEL (carrinho) -> CHUTE
#   • PASSAR: clique A/B/C (ou A/B/C/1/2/3).
#       - Acerto: +120 (+combo), anima até o receptor e entra no DUEL.
#       - Erro:   −40, −1 vida; anima e volta para o "10"; próxima pergunta.
#   • DUEL: mini-desafio relâmpago (2 opções). Zagueiro dá carrinho animado.
#       - Acerto no tempo: libera CHUTE.
#       - Erro/tempo: −40, −1 vida; bola volta pro "10".
#   • CHUTAR: mire no gol e clique (ou Espaço).
#       - Goleiro largo (72px) se move lateralmente; se passar pelo alvo, defende.
#       - Gol: +250 (+30*combo) + FX “GOOOOL!” no campo.
#       - Defesa/fora: −40, −1 vida + FX “DEFENDEU!”.
#       - Depois do chute: bola volta pro "10" e volta à fase PASSE.
#   • Sidebar: score/combo/vidas/tempo + histórico (scroll + hover do "por quê").
#   • Painel: título + tópico + timer circular.
#   • Fim: congela campo e mostra CONTINUAR; então on_finish({...}).
# ============================================================

class TelaPyFootTactics:
    def __init__(
        self,
        largura: int,
        altura: int,
        topic_title: str,
        on_finish,
        pass_score: int = 360,
        total_seconds: int | None = None,
        rounds: int = 14,
        round_seconds: int | None = None,
        match_seconds: int | None = None,
        sfx=None,
    ):
        self.largura = largura
        self.altura = altura
        self.topic_title = topic_title or "print"
        self.on_finish = on_finish
        self.pass_score = int(pass_score)
        self.sfx = sfx

        # FX de chute pós-animação
        self._shot_fx = None  # {"kind": "goal"|"save", "pos": (x, y)}
        self._ambient_started = False

        # duração: round_seconds / match_seconds / total_seconds
        _dur = round_seconds if round_seconds is not None else (
            match_seconds if match_seconds is not None else (
                total_seconds if total_seconds is not None else 45
            )
        )
        self.total_seconds = max(10, int(_dur))

        # ===== fonts
        pygame.font.init()
        self.fonte_xl   = pygame.font.SysFont("Consolas", 26, bold=True)
        self.fonte_g    = pygame.font.SysFont("Consolas", 22, bold=True)
        self.fonte      = pygame.font.SysFont("Consolas", 18)
        self.fonte_s    = pygame.font.SysFont("Consolas", 16)

        # ===== layout geral
        self.prompt = pygame.Rect(int(largura*0.14), int(altura*0.08), int(largura*0.72), int(altura*0.80))
        pad = 28
        header_h = 56
        self._header_h = header_h
        body_y = self.prompt.y + header_h + pad
        body_h = self.prompt.h - header_h - pad*2 - 64
        body_w = self.prompt.w - pad*2

        # campo + sidebar
        self.sidebar_w    = int(body_w * 0.28)
        self.field_rect   = pygame.Rect(self.prompt.x + pad, body_y, body_w - self.sidebar_w - 16, body_h)
        self.sidebar_rect = pygame.Rect(self.field_rect.right + 16, body_y, self.sidebar_w, body_h)

        # botão continuar
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

        # fases: pass -> duel -> shot -> (anim) -> pass
        self.phase = "pass"
        self._pass_was_correct = False
        self._reset_after_shot = False

        # ===== conteúdo
        n_rounds = 14 if (rounds is None) else int(rounds)
        self.questions = get_pyfoot_questions(self.topic_title, rounds=max(8, n_rounds))
        self.q_idx = 0

        # ===== campo e jogadores
        self._setup_pitch()

        # ===== histórico lateral + SCROLL
        self.hits_ok_list  = []
        self.hits_bug_list = []
        self._hist_rects_ok = []
        self._hist_rects_bug = []
        self._hover_tooltip = ""
        self.scroll_ok = 0.0
        self.scroll_bug = 0.0
        self._area_ok = pygame.Rect(0,0,0,0)
        self._area_bug = pygame.Rect(0,0,0,0)

        # ===== bola / animações
        self.ball_pos = [0, 0]
        self.ball_anim = None
        self._set_ball_to_10()

        # mira (somente no modo CHUTE)
        self.aim_pos = None

        # ===== duel (carrinho + mini-desafio)
        self.duel = None          # {"opts":[txt1,txt2], "correct":idx, "deadline":t, "rects":[Rect, Rect], "rx":, "ry":}
        self.tackle = None        # {"lane":i, "start":t, "dur":s}

        # ===== FX de campo (mensagens/celebração)
        self.field_msgs = []      # [{"text", "color", "start", "dur", "pos":(x,y)}]
        self.goal_rings = []      # [{"start", "dur", "x", "y"}]

        # --- Torcida ambiente (baixa) ---
        
        if self.sfx:
            self.sfx.start_ambient(vol=0.45)
            self._ambient_started = True
            

    # ---------------------------------------------------------
    # utils de campo
    def _setup_pitch(self):
        r = self.field_rect
        self.goal_rect   = pygame.Rect(r.centerx - int(r.w*0.22), r.y + 14, int(r.w*0.44), 36)
        self.box_rect    = pygame.Rect(r.centerx - int(r.w*0.28), self.goal_rect.bottom + 8, int(r.w*0.56), 90)
        self.p10_pos     = (r.centerx, r.bottom - 42)  # “camisa 10”
        lane_dx          = int(r.w * 0.22)
        lanes_cx         = [r.centerx - lane_dx, r.centerx, r.centerx + lane_dx]
        cy_receivers     = r.y + int(r.h*0.55)
        self.receivers   = [(lanes_cx[0], cy_receivers),
                            (lanes_cx[1], cy_receivers-14),
                            (lanes_cx[2], cy_receivers)]

        # linha adversária (mesmas colunas dos receptores, mais à frente)
        cy_defenders = (cy_receivers + self.box_rect.y) // 2
        self.defenders = [(lanes_cx[0], cy_defenders),
                          (lanes_cx[1], cy_defenders),
                          (lanes_cx[2], cy_defenders)]

        # goleiro "largo" 3x + nome
        self.gk_half_w = 36   # total 72 px
        self.gk_x = self.goal_rect.centerx
        self.gk_v = 150
        self.gk_dir = 1
        self.gk_name = random.choice(["Java", "C++", "Rust", "Go", "TypeScript"])

        # áreas clicáveis das opções
        self.opt_bubbles = [pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)]

    def _set_ball_to_10(self):
        self.ball_pos = [self.p10_pos[0], self.p10_pos[1] - 14]

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
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    # ---------------------------------------------------------
    # pontuação / vida
    def _tick_combo(self):
        now = time.time()
        if now - self.last_hit_ts <= self.combo_window:
            self.combo += 1
        else:
            self.combo = 1
        self.last_hit_ts = now
        self.max_combo = max(self.max_combo, self.combo)

    def _register_pass_hit(self, answer_text, why):
        self._tick_combo()
        add = 120 + (self.combo - 1) * 20
        self.score += add
        self.hits_ok_list.append({"code": answer_text, "why": why or "Passe certo.", "is_bug": False})
        return add

    def _register_miss(self, answer_text, why):
        self.misses += 1
        self.lives -= 1
        self.combo = 0
        self.score = max(0, self.score - 40)
        self.hits_bug_list.append({"code": answer_text, "why": why or "Erro na jogada.", "is_bug": True})
        if self.lives <= 0:
            self.running = False
            self.finished = True

    def _register_goal(self):
        bonus = 250 + int(30 * self.combo)
        self.score += bonus
        self.hits_ok_list.append({"code": "GOL!", "why": "Finalização precisa, sem defesa.", "is_bug": False})
        return bonus

    # ---------------------------------------------------------
    # mini-conteúdo p/ DUEL (2 opções)
    def _make_duel(self):
            """
            Monta um mini-duelo com 2 opções.
            - A alternativa correta é posicionada aleatoriamente à esquerda(0) ou direita(1).
            - O 'why' de cada lado é preenchido para logs/feedback coerentes.
            """
            qlist = get_pyfoot_questions(self.topic_title, rounds=1)
            if not qlist:
                # fallback simples e simétrico
                side_correct = random.randint(0, 1)
                opts2 = ["OK", "ERRO"]
                if side_correct == 1:
                    opts2 = ["ERRO", "OK"]
                return {"opts": opts2, "correct": side_correct, "why": ["", ""]}

            q = qlist[0]
            correct_idx = int(q.get("correct", 0))

            # pega um errado entre os dois possíveis (não fixa no +1)
            all_idx = [0, 1, 2]
            wrong_candidates = [i for i in all_idx if i != correct_idx]
            wrong_idx = random.choice(wrong_candidates)

            # decide o lado (0=esq, 1=dir) da alternativa correta
            side_correct = random.randint(0, 1)

            # monta pares (texto/why) já ordenados para esquerda/direita
            q_opts = q.get("opts", ["", "", ""])
            q_why  = q.get("why",  ["", "", ""])

            left_text  = q_opts[correct_idx] if side_correct == 0 else q_opts[wrong_idx]
            right_text = q_opts[wrong_idx]   if side_correct == 0 else q_opts[correct_idx]

            left_why   = q_why[correct_idx]  if side_correct == 0 else (q_why[wrong_idx] if len(q_why) > wrong_idx else "")
            right_why  = (q_why[wrong_idx] if len(q_why) > wrong_idx else "") if side_correct == 0 else q_why[correct_idx]

            return {
                "opts": [left_text, right_text],
                "correct": side_correct,           # 0 = esquerda, 1 = direita
                "why": [left_why, right_why],
            }

    # ---------------------------------------------------------
    # perguntas / opções
    def _current_question(self):
        if not self.questions:
            return None
        i = min(self.q_idx, len(self.questions)-1)
        return self.questions[i]

    def _advance_question(self):
        self.q_idx += 1
        if self.q_idx >= len(self.questions):
            more = get_pyfoot_questions(self.topic_title, rounds=10)
            self.questions.extend(more)

    # ---------------------------------------------------------
    # FX helpers
    def _add_message(self, text, color, pos, dur=1.2):
        self.field_msgs.append({"text": text, "color": color, "start": time.time(), "dur": dur, "pos": pos})

    def _spawn_goal_rings(self, x, y):
        self.goal_rings.append({"start": time.time(), "dur": 1.0, "x": x, "y": y})

    # ---------------------------------------------------------
    # draw — painel / timer
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

        titulo = self.fonte_xl.render("PyFoot Tactics", True, (230, 240, 255))
        tela.blit(titulo, (p.x+24, p.y+10))

        badge_col = (80, 170, 110)
        topic_txt = f"Tópico: {self.topic_title}"
        badge_surf = self.fonte.render(topic_txt, True, (255,255,255))
        padx, pady = 12, 8
        bw = badge_surf.get_width() + padx*2
        bh = badge_surf.get_height() + pady*2
        bx = header.right - bw - 16
        by = header.y + (header.h - bh)//2
        pygame.draw.rect(tela, badge_col, (bx, by, bw, bh), border_radius=10)
        pygame.draw.rect(tela, (20, 20, 25), (bx, by, bw, bh), 2, border_radius=10)
        tela.blit(badge_surf, (bx + padx, by + pady))

        subt = self.fonte.render("Passe certo → DUEL (carrinho) → se vencer, MIRE e CHUTE no gol", True, (190, 210, 245))
        tela.blit(subt, (p.x+24, p.y+10+26))

        self._draw_round_timer(tela, header, badge_col)

    def _draw_round_timer(self, tela: pygame.Surface, header_rect: pygame.Rect, color_main):
        cx = header_rect.centerx
        lift = int(header_rect.h * 0.25)
        cy = header_rect.y + header_rect.h // 2 - lift
        outer_r = min(20, max(14, header_rect.h // 3))
        inner_r = max(8, int(outer_r * 0.7))
        ring_w  = max(2, outer_r - inner_r)
        cy = max(header_rect.y + outer_r + 2, cy)

        pygame.draw.circle(tela, (22, 30, 40), (cx, cy), outer_r)
        pygame.draw.circle(tela, (12, 18, 26), (cx, cy), inner_r)

        now = time.time()
        remain = max(0.0, self.start_ts + self.total_seconds - now) if self.running else 0.0
        frac = 0.0 if not self.running else max(0.0, min(1.0, remain / self.total_seconds))

        col_arc = (min(color_main[0]+30,255), min(color_main[1]+30,255), min(color_main[2]+30,255))
        rect = pygame.Rect(cx - outer_r, cy - outer_r, outer_r*2, outer_r*2)
        start_angle = -pi/2
        end_angle   = start_angle + 2*pi*frac
        if frac > 0:
            pygame.draw.arc(tela, col_arc, rect, start_angle, end_angle, ring_w)
        pygame.draw.circle(tela, (60, 160, 255), (cx, cy), outer_r, 1)

    # ---------------------------------------------------------
    # draw — campo / jogadores / opções / bola / FX
    def _draw_pitch(self, tela: pygame.Surface):
        r = self.field_rect
        pygame.draw.rect(tela, (24, 80, 44), r, border_radius=12)
        pygame.draw.rect(tela, (90, 170, 255), r, 2, border_radius=12)

        # linhas do campo
        pygame.draw.line(tela, (210, 255, 210), (r.x+16, r.centery), (r.right-16, r.centery), 2)
        pygame.draw.circle(tela, (210, 255, 210), (r.centerx, r.centery), 36, 2)

        # área e gol
        pygame.draw.rect(tela, (210, 255, 210), self.box_rect, 2, border_radius=6)
        pygame.draw.rect(tela, (220, 240, 255), self.goal_rect, 3, border_radius=4)

        # goleiro largo + nome
        gk_rect = pygame.Rect(int(self.gk_x - self.gk_half_w), self.goal_rect.centery-12, self.gk_half_w*2, 24)
        pygame.draw.rect(tela, (60, 120, 220), gk_rect, border_radius=6)
        name_surf = self.fonte_s.render(self.gk_name, True, (230,240,255))
        tela.blit(name_surf, (gk_rect.centerx - name_surf.get_width()//2, gk_rect.y - 18))

        # nosso “10”
        x10, y10 = self.p10_pos
        pygame.draw.circle(tela, (245, 245, 245), (x10, y10), 14)
        pygame.draw.circle(tela, (20, 20, 20), (x10, y10), 14, 2)

        # linha adversária
        for (dx, dy) in self.defenders:
            pygame.draw.circle(tela, (220, 80, 80), (dx, dy), 11)
            pygame.draw.circle(tela, (30, 20, 20), (dx, dy), 11, 2)

        labels = ["A", "B", "C"]
        q = self._current_question()
        opts = q["opts"] if q else ["", "", ""]
        show_options = (self.phase == "pass" and self.ball_anim is None)

        self.opt_bubbles = []
        placed_opt_bubbles = []
        for i, (cx, cy) in enumerate(self.receivers):
            # receptores
            pygame.draw.circle(tela, (240, 220, 120), (cx, cy), 12)
            pygame.draw.circle(tela, (20, 20, 20), (cx, cy), 12, 2)

            if show_options:
                # label acima
                tag = self.fonte_g.render(labels[i], True, (20,30,40))
                tag_rect = pygame.Rect(cx-14, cy-36, 28, 22)
                pygame.draw.rect(tela, (255, 235, 120), tag_rect, border_radius=8)
                pygame.draw.rect(tela, (40, 40, 50), tag_rect, 2, border_radius=8)
                tela.blit(tag, (tag_rect.centerx - tag.get_width()//2, tag_rect.centery - tag.get_height()//2))

                # bolha com a opção
                max_w = int(self.field_rect.w * 0.28)
                lines = self._wrap_text(opts[i], self.fonte_s, max_w)
                lines = lines[:3] + (["..."] if len(lines) > 3 else [])
                bb_w = max(self.fonte_s.size(l)[0] for l in lines) + 16
                bb_h = len(lines)*(self.fonte_s.get_height()+2) + 12

                bx = cx - bb_w//2
                by = cy - 72 - bb_h

                # FIX 1: clamp vertical INCONDICIONAL (evita a bolha sumir pra cima)
                by = max(self.field_rect.y+8, by)

                # clamp horizontal
                bx = max(self.field_rect.x+8, min(bx, self.field_rect.right-8-bb_w))

                bubble = pygame.Rect(bx, by, bb_w, bb_h)

                # anticolisão leve: empilha pra cima se colidir com alguma já colocada
                tries = 0
                while any(bubble.colliderect(pr) for pr in placed_opt_bubbles) and tries < 6:
                    bubble.y -= 12
                    # FIX 2: manter top sempre no campo mesmo ao empilhar
                    bubble.y = max(self.field_rect.y+8, bubble.y)
                    tries += 1

                # desenha
                pygame.draw.rect(tela, (36, 52, 92), bubble, border_radius=8)
                pygame.draw.rect(tela, (120, 180, 255), bubble, 1, border_radius=8)

                yy = bubble.y + 6
                for ln in lines:
                    img = self.fonte_s.render(ln, True, (235, 235, 245))
                    tela.blit(img, (bubble.x+8, yy))
                    yy += self.fonte_s.get_height()+2

                self.opt_bubbles.append(bubble)
                placed_opt_bubbles.append(bubble)

        # DUEL UI (se ativo)
        if self.phase == "duel" and self.duel and self.ball_anim is None:
            rx, ry = self.duel["rx"], self.duel["ry"]
            # mini timer barra
            tleft = max(0.0, self.duel["deadline"] - time.time())
            frac = tleft / self.duel["total"]
            bar_w = 160
            bar = pygame.Rect(rx - bar_w//2, ry - 70, bar_w, 10)
            pygame.draw.rect(tela, (30, 46, 72), bar, border_radius=6)
            if frac > 0:
                fill = pygame.Rect(bar.x, bar.y, int(bar_w*frac), bar.h)
                pygame.draw.rect(tela, (240, 200, 90), fill, border_radius=6)
            pygame.draw.rect(tela, (90, 170, 255), bar, 1, border_radius=6)

            # duas bolhas de opção
            self.duel["rects"] = []
            opts2 = self.duel["opts"]
            placed_duel = []

            for j in range(2):
                text = opts2[j]
                lines = self._wrap_text(text, self.fonte_s, 180)
                bb_w = max(self.fonte_s.size(l)[0] for l in lines) + 16
                bb_h = len(lines)*(self.fonte_s.get_height()+2) + 12

                # left (0) fica à esquerda do rx; right (1) à direita
                bx = rx - (bb_w + 12) if j == 0 else rx + 12
                by = ry - 52 - bb_h

                # FIX 3: clamp vertical INCONDICIONAL também no DUEL
                by = max(self.field_rect.y+8, by)

                # clamp horizontal dentro do campo
                bx = max(self.field_rect.x+8, min(bx, self.field_rect.right-8-bb_w))
                bubble = pygame.Rect(bx, by, bb_w, bb_h)

                # anticolisão simples entre as duas bolhas do DUEL
                tries = 0
                while any(bubble.colliderect(pr) for pr in placed_duel) and tries < 4:
                    bubble.y -= 12
                    bubble.y = max(self.field_rect.y+8, bubble.y)
                    tries += 1

                # desenha
                pygame.draw.rect(tela, (44, 60, 96), bubble, border_radius=8)
                pygame.draw.rect(tela, (120, 180, 255), bubble, 1, border_radius=8)
                yy = bubble.y + 6
                for ln in lines:
                    img = self.fonte_s.render(ln, True, (235, 235, 245))
                    tela.blit(img, (bubble.x+8, yy))
                    yy += self.fonte_s.get_height()+2

                self.duel["rects"].append(bubble)
                placed_duel.append(bubble)

            # animação do carrinho (zagueiro deslizando até o receptor)
            if self.tackle:
                lane = self.tackle["lane"]
                sx, sy = self.defenders[lane]
                dur = self.tackle["dur"]
                tt = max(0.0, min(1.0, (time.time()-self.tackle["start"]) / dur))
                ex, ey = rx, ry
                cx = int(sx + (ex - sx)*tt)
                cy = int(sy + (ey - sy)*tt)
                pygame.draw.circle(tela, (255, 120, 120), (cx, cy), 12)
                pygame.draw.circle(tela, (40, 20, 20), (cx, cy), 12, 2)

        # bola
        pygame.draw.circle(tela, (250,250,250), (int(self.ball_pos[0]), int(self.ball_pos[1])), 6)
        pygame.draw.circle(tela, (20,20,20), (int(self.ball_pos[0]), int(self.ball_pos[1])), 6, 1)

        # mira do chute
        if self.phase == "shot" and self.ball_anim is None:
            mx, my = pygame.mouse.get_pos()
            if self.goal_rect.collidepoint(mx, my):
                self.aim_pos = (mx, my)
                x0, y0 = self.ball_pos
                x1, y1 = mx, max(self.goal_rect.y+4, min(my, self.goal_rect.bottom-4))
                pygame.draw.line(tela, (240, 255, 240), (x0, y0), (x1, y1), 2)
                pygame.draw.circle(tela, (240,255,240), (x1, y1), 5, 2)
            else:
                self.aim_pos = None

        # FX: mensagens flutuantes
        now = time.time()
        alive = []
        for fx in self.field_msgs:
            t = (now - fx["start"]) / fx["dur"]
            if 0 <= t <= 1:
                alive.append(fx)
                alpha = int(255 * (1 - t))
                ty = fx["pos"][1] - int(22 * t)
                surf = self.fonte_xl.render(fx["text"], True, fx["color"])
                tmp = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                tmp.blit(surf, (0, 0))
                tmp.set_alpha(alpha)
                tela.blit(tmp, (fx["pos"][0] - surf.get_width()//2, ty))
        self.field_msgs = alive

        # FX: anéis de gol
        rings_alive = []
        for ring in self.goal_rings:
            t = (now - ring["start"]) / ring["dur"]
            if 0 <= t <= 1:
                rings_alive.append(ring)
                radius = int(10 + 80 * t)
                alpha = int(200 * (1 - t))
                ring_s = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
                pygame.draw.circle(ring_s, (240, 255, 200, alpha), (radius+2, radius+2), radius, 3)
                tela.blit(ring_s, (ring["x"] - radius - 2, ring["y"] - radius - 2))
        self.goal_rings = rings_alive

    # ---------------------------------------------------------
    # draw — sidebar
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
        row("MAX",   f"x{self.max_combo}", y); y += 30
        row("VIDAS", "♥"*self.lives, y); y += 30
        row("TEMPO", f"{secs:02d}s", y); y += 30
        fase_txt = {"pass":"PASSE", "duel":"DUEL", "shot":"CHUTE"}.get(self.phase, "ANIM")
        row("FASE",  fase_txt, y); y += 18

        y += 6
        pygame.draw.line(tela, (60, 160, 255), (r.x+12, y), (r.right-12, y), 2)
        y += 8

        title_h = self.fonte_g.get_height() + 2
        available_boxes = (r.bottom - 12) - (y + title_h + 6 + title_h + 6)
        box_h = max(60, available_boxes // 2)

        title = self.fonte_g.render(f"Acertos ({len(self.hits_ok_list)})", True, (130, 230, 160))
        tela.blit(title, (r.x+14, y)); y += title_h
        self._area_ok = pygame.Rect(r.x+10, y, r.w-20, box_h)
        self._draw_scroll_list(tela, self._area_ok, self.hits_ok_list, False, "scroll_ok")
        y = self._area_ok.bottom + 6

        title2 = self.fonte_g.render(f"Erros ({len(self.hits_bug_list)})", True, (255, 170, 160))
        tela.blit(title2, (r.x+14, y)); y += title_h
        self._area_bug = pygame.Rect(r.x+10, y, r.w-20, box_h)
        self._draw_scroll_list(tela, self._area_bug, self.hits_bug_list, True, "scroll_bug")

        if self._hover_tooltip:
            mx, my = pygame.mouse.get_pos()
            lines = self._wrap_text(self._hover_tooltip, self.fonte_s, 320)
            w = max(self.fonte_s.size(l)[0] for l in lines) + 16
            h = len(lines)*(self.fonte_s.get_height()+2) + 12
            x = min(mx + 16, self.prompt.right - w - 8)
            y2 = min(my + 16, self.prompt.bottom - h - 8)
            tip = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(tip, (30, 44, 70, 240), tip.get_rect(), border_radius=8)
            pygame.draw.rect(tip, (120, 180, 255), tip.get_rect(), 1, border_radius=8)
            yy = 6
            for ln in lines:
                s = self.fonte_s.render(ln, True, (230, 240, 255))
                tip.blit(s, (8, yy)); yy += self.fonte_s.get_height()+2
            tela.blit(tip, (x, y2))

    def _draw_scroll_list(self, tela, area: pygame.Rect, items, is_bug: bool, scroll_attr: str):
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

        if is_bug: self._hist_rects_bug = []
        else:      self._hist_rects_ok  = []

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
            if is_bug: self._hist_rects_bug.append(pair)
            else:      self._hist_rects_ok.append(pair)

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

    # ---------------------------------------------------------
    # draw — fim
    def _draw_finish_overlay(self, tela: pygame.Surface):
        overlay = pygame.Surface((self.field_rect.w, self.field_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0,0,0,140), overlay.get_rect(), border_radius=16)
        tela.blit(overlay, (self.field_rect.x, self.field_rect.y))

        title = self.fonte_xl.render("Fim do minigame!", True, (240, 250, 255))
        tela.blit(title, (self.field_rect.centerx - title.get_width()//2, self.field_rect.y + 40))

        info = [
            f"Score: {self.score}",
            f"Acertos (passes/gols): {len(self.hits_ok_list)}",
            f"Erros (passes/chutes): {len(self.hits_bug_list)}",
            f"Falhas: {self.misses}",
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
    # lógica de animações simples
    def _update_keeper(self, dt):
        left  = self.goal_rect.x + self.gk_half_w
        right = self.goal_rect.right - self.gk_half_w
        self.gk_x += self.gk_dir * self.gk_v * dt
        if self.gk_x < left:  self.gk_x, self.gk_dir = left, 1
        if self.gk_x > right: self.gk_x, self.gk_dir = right, -1

    def _animate_ball(self):
        if not self.ball_anim:
            return

        now = time.time()
        t = (now - self.ball_anim["start"]) / self.ball_anim["dur"]
        t = max(0.0, min(1.0, t))

        ax, ay = self.ball_anim["a"]
        bx, by = self.ball_anim["b"]

        # ease-in-out quad
        tt = 2*t*t if t < 0.5 else -1 + (4-2*t)*t
        self.ball_pos[0] = ax + (bx - ax) * tt
        self.ball_pos[1] = ay + (by - ay) * tt

        if t >= 1.0:
            end_type = self.ball_anim["type"]
            self.ball_anim = None

            if end_type == "pass_end":
                if not self._pass_was_correct:
                    self._set_ball_to_10()

            elif end_type == "shot_end":
                # disparar FX após a bola chegar
                if getattr(self, "_shot_fx", None):
                    fx = self._shot_fx
                    self._shot_fx = None
                    if fx["kind"] == "save":
                        if self.sfx: self.sfx.save()
                        self._add_message("DEFENDEU!", (255, 180, 180), fx["pos"], 1.1)
                    else:
                        if self.sfx: self.sfx.goal()
                        self._add_message("GOOOOL!", (255, 240, 120), fx["pos"], 1.2)
                        self._spawn_goal_rings(self.goal_rect.centerx, self.goal_rect.centery)

                if self._reset_after_shot:
                    self._set_ball_to_10()
                    self._reset_after_shot = False
                self.phase = "pass"

    # ---------------------------------------------------------
    # loop — desenhar
    def desenhar(self, tela: pygame.Surface):
        prev = getattr(self, "_prev_tick", time.time())
        now = time.time()
        dt = max(0.0, min(0.05, now - prev))
        self._prev_tick = now

        if self.running:
            elapsed_total = now - self.start_ts
            self.time_left = max(0.0, self.total_seconds - elapsed_total)
            if self.time_left <= 0:
                self.running = False
                self.finished = True

        self._update_keeper(dt)
        self._animate_ball()

        # tempo de DUEL expirado?
        if self.phase == "duel" and self.duel and self.ball_anim is None:
            if time.time() > self.duel["deadline"]:
                if self.sfx: self.sfx.tackle()
                self._register_miss("Duelo", "Perdeu a bola no carrinho (tempo esgotado).")
                self.duel = None
                self.tackle = None
                self.phase = "pass"
                self._set_ball_to_10()

        self._draw_panel(tela)
        self._draw_pitch(tela)
        self._draw_sidebar(tela)

        # parar torcida quando finalizar (uma vez)
        
        if self.finished and self._ambient_started and self.sfx:
            self.sfx.stop_ambient()
            self._ambient_started = False
        

        if self.finished:
            self._draw_finish_overlay(tela)

    # ---------------------------------------------------------
    # eventos
    def tratar_eventos(self, eventos):
        for ev in eventos:
            # hover do histórico
            if ev.type == pygame.MOUSEMOTION:
                self._hover_tooltip = ""
                mx, my = ev.pos
                for rect, it in (self._hist_rects_ok + self._hist_rects_bug):
                    if rect.collidepoint(mx, my):
                        self._hover_tooltip = (it.get("why") or "Sem detalhes.").strip()
                        break

            # scroll listas
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

            # fallback scroll
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
                    max_scroll_bug = max(0, content_h_bug - self._area_bug.h)  # FIX: usa content_h_bug
                    self.scroll_bug = max(0.0, min(self.scroll_bug - (delta/1), float(max_scroll_bug)))

            # clique primário
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
                            "rounds": int(self.q_idx),
                        }
                        self.on_finish(result)
                    return

                if not self.running or self.finished:
                    return

                # ignorar cliques durante animação
                if self.ball_anim is not None:
                    continue

                # DUEL: clique numa das duas opções
                if self.phase == "duel" and self.duel:
                    for j, rect in enumerate(self.duel["rects"]):
                        if rect.collidepoint(mx, my):
                            if j == self.duel["correct"]:
                                if self.sfx: self.sfx.dribble()
                                self._add_message("Drible!", (180,255,180), (self.duel["rx"], self.duel["ry"]-80), 0.9)
                                self.duel = None
                                self.tackle = None
                                self.phase = "shot"
                            else:
                                if self.sfx: self.sfx.tackle()
                                chosen_text = ""
                                try:
                                    chosen_text = self.duel.get("opts", [])[j]
                                except Exception:
                                    chosen_text = "Duelo (resposta errada)"
                                why_list = self.duel.get("why")
                                why_text = (why_list[j] if isinstance(why_list, list) and j < len(why_list)
                                            else "Resposta incorreta no DUEL (carrinho).")
                                self._register_miss(chosen_text or "Duelo (resposta errada)", why_text)
                                self.duel = None
                                self.tackle = None
                                self.phase = "pass"
                                self._set_ball_to_10()
                            break
                    continue

                # CHUTE
                if self.phase == "shot":
                    if self.goal_rect.collidepoint(mx, my):
                        self._do_shot((mx, my))
                    continue

                # PASSE
                if self.phase == "pass":
                    q = self._current_question()
                    if q:
                        for i, bubble in enumerate(self.opt_bubbles):
                            if bubble.collidepoint(mx, my):
                                is_correct = (i == q["correct"])
                                rx, ry = self.receivers[i]
                                self._do_pass((rx, ry), is_correct, q, i, lane=i)
                                break

            # teclado
            if ev.type == pygame.KEYDOWN and self.running and not self.finished:
                # Espaço = chute (se em modo CHUTE)
                if ev.key == pygame.K_SPACE and self.phase == "shot" and self.ball_anim is None:
                    mx, my = pygame.mouse.get_pos()
                    if self.goal_rect.collidepoint(mx, my):
                        self._do_shot((mx, my))

                # PASSE via A/B/C/1/2/3
                elif self.phase == "pass" and self.ball_anim is None:
                    key_to_idx = {
                        pygame.K_a: 0, pygame.K_1: 0, pygame.K_KP1: 0,
                        pygame.K_b: 1, pygame.K_2: 1, pygame.K_KP2: 1,
                        pygame.K_c: 2, pygame.K_3: 2, pygame.K_KP3: 2,
                    }
                    if ev.key in key_to_idx:
                        q = self._current_question()
                        if q:
                            i = key_to_idx[ev.key]
                            is_correct = (i == q["correct"])
                            rx, ry = self.receivers[i]
                            self._do_pass((rx, ry), is_correct, q, i, lane=i)

                # DUEL com setas esquerda/direita
                elif self.phase == "duel" and self.duel and self.ball_anim is None:
                    if ev.key in (pygame.K_LEFT, pygame.K_a):
                        j = 0
                    elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                        j = 1
                    else:
                        j = None

                    if j is not None:
                        if j == self.duel["correct"]:
                            if self.sfx: self.sfx.dribble()
                            self._add_message("Drible!", (180,255,180), (self.duel["rx"], self.duel["ry"]-80), 0.9)
                            self.duel = None
                            self.tackle = None
                            self.phase = "shot"
                        else:
                            if self.sfx: self.sfx.tackle()
                            chosen_text = ""
                            try:
                                chosen_text = self.duel.get("opts", [])[j]
                            except Exception:
                                chosen_text = "Duelo (resposta errada)"
                            why_list = self.duel.get("why")
                            why_text = (why_list[j] if isinstance(why_list, list) and j < len(why_list)
                                        else "Resposta incorreta no DUEL (carrinho).")
                            self._register_miss(chosen_text or "Duelo (resposta errada)", why_text)
                            self.duel = None
                            self.tackle = None
                            self.phase = "pass"
                            self._set_ball_to_10()

    # ---------------------------------------------------------
    # ações de jogo
    def _do_pass(self, target_xy, is_correct, q, chosen_idx, lane=1):
        if self.sfx: self.sfx.pass_kick()
        a = (self.ball_pos[0], self.ball_pos[1])
        b = (target_xy[0], target_xy[1] - 10)
        self._pass_was_correct = bool(is_correct)
        self.ball_anim = {"type": "pass_end", "start": time.time(), "dur": 0.35, "a": a, "b": b}

        if is_correct:
            self._register_pass_hit(q["opts"][chosen_idx], q["why"][chosen_idx])
            # prepara DUEL
            self.phase = "duel"
            self.duel = self._make_duel()
            self.duel["rx"], self.duel["ry"] = int(target_xy[0]), int(target_xy[1])
            self.duel["total"] = 4.0
            self.duel["deadline"] = time.time() + self.duel["total"]
            self.duel["rects"] = []
            self.tackle = {"lane": lane, "start": time.time(), "dur": 1.8}
        else:
            self._register_miss(q["opts"][chosen_idx], q["why"][chosen_idx])
            self.phase = "pass"

        self._advance_question()

    def _do_shot(self, aim_xy):
        x1, y1 = self.ball_pos
        x2 = max(self.goal_rect.x+6, min(aim_xy[0], self.goal_rect.right-6))
        y2 = max(self.goal_rect.y+6, min(aim_xy[1], self.goal_rect.bottom-6))

        flight = 0.50

        if self.sfx: self.sfx.shot()

        # goleiro segue a direção do chute
        self.gk_dir = 1 if (x2 > self.gk_x) else -1
        left  = self.goal_rect.x + self.gk_half_w
        right = self.goal_rect.right - self.gk_half_w
        pred_gk_x = self.gk_x + self.gk_dir * self.gk_v * flight
        pred_gk_x = max(left, min(pred_gk_x, right))

        reach = self.gk_half_w + 14
        is_save = abs(x2 - pred_gk_x) <= reach

        self.ball_anim = {"type": "shot_end", "start": time.time(), "dur": flight, "a": (x1, y1), "b": (x2, y2)}
        self._reset_after_shot = True
        self.phase = "anim"

        if is_save:
            self._register_miss("Chute", "Chute defendido pelo goleiro.")
            self._shot_fx = {"kind": "save", "pos": (x2, self.goal_rect.y + 8)}
        else:
            self._register_goal()
            self._shot_fx = {"kind": "goal", "pos": (self.goal_rect.centerx, self.goal_rect.y - 4)}

    # ---------------------------------------------------------
    def get_state(self):
        return {
            "score": self.score,
            "combo": self.combo,
            "max_combo": self.max_combo,
            "lives": self.lives,
            "time_left": self.time_left,
            "phase": self.phase,
        }
