import pygame
import random

class TelaMiniPythonHero:
    """
    Minigame (45s). 4 trilhas (A,S,D,F). Uma pergunta por rodada.
    Uma rodada = até 4 blocos (1 correta + erradas). Próxima rodada só começa
    quando a atual termina. Blocos são NEUTROS; a cor aparece só ao apertar.
    """

    def __init__(self, largura, altura, jogador, id_fase, nome_topico, on_finish):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.id_fase = id_fase
        self.nome_topico = (nome_topico or "").lower()
        self.on_finish = on_finish

        # painel
        self.prompt = pygame.Rect(int(largura*0.18), int(altura*0.10), int(largura*0.64), int(altura*0.76))
        pygame.font.init()
        self.fonte    = pygame.font.SysFont("Consolas", 22)
        self.fonte_g  = pygame.font.SysFont("Consolas", 28, bold=True)
        self.fonte_t  = pygame.font.SysFont("Consolas", 18)
        self.fonte_fx = pygame.font.SysFont("Consolas", 26, bold=True)

        # trilhas
        self.num_lanes = 4
        m = 36
        lane_w = (self.prompt.w - m*2) // self.num_lanes
        self.lanes = [pygame.Rect(self.prompt.x + m + i*lane_w, self.prompt.y+140, lane_w-10, self.prompt.h-200) for i in range(self.num_lanes)]
        self.hit_y = self.lanes[0].bottom - 48
        self.hit_window = 100  # janela generosa

        # notas
        self.notes = []
        self.last_spawn = 0
        ###
        self.hit_window = 100  # janela generosa
        self.early_window = 220  # NOVO: janela de adiantado (px) acima da hitline

        # ritmo/velocidade (calmo)
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

        # perguntas (somente do tópico atual; fallback p/ base)
        self.pool = self._criar_pool_por_topico(self.nome_topico)
        self.current_prompt = None
        self._prepare_next_prompt()  # prepara primeira rodada
        self._last_tick = now
        self.fx = []

        # solta a primeira rodada de cara
        self._spawn_notes()
        self.last_spawn = now

    # ---------- CONTEÚDO ----------
    def _criar_pool_por_topico(self, topico):
        def p(prompt, ok, *wrong):
            alts = [{"txt": ok, "ok": True}] + [{"txt": w, "ok": False} for w in wrong]
            return {"prompt": prompt, "alternativas": alts}

        base = [
            p("Qual imprime 7?", "print(3+4)", "print(3*4)", "print('7'+1)", "print(7,)"),
            p("Qual concatena 'py' e 'thon'?", "print('py'+'thon')", "print('py','thon')", "print( py + thon )", "print('py'.join('thon'))"),
            p("Qual imprime de 0 a 2 (um por linha)?", "for i in range(3): print(i)", "for i in range(1,3): print(i)", "for i in [3]: print(i)", "print(range(3))"),
        ]

        # listas específicas por tópico
        topic_only = []
        if "print" in topico:
            topic_only = [
                # 1) iguais à sua referência
                p("Imprimir exatamente: Hello",
                "print('Hello')",
                "print(Hello)", "print(\"Hello)", "print('Hello'"),

                # 2) número puro
                p("Imprimir exatamente: 7",
                "print(7)",
                "print('7'+1)", "print(3*4)", "print(7.0)"),

                # 4) apóstrofo dentro do texto
                p("Imprimir exatamente: I'm ok",
                "print(\"I'm ok\")",
                "print('Im ok')", "print(\"I'm ok)", "print(I'm ok)"),

                # 5) aspas duplas dentro do texto
                p("Imprimir exatamente: He said \"hi\"",
                "print('He said \"hi\"')",
                "print(\"He said 'hi'\")", "print(He said \"hi\")", "print('He said \"hi')"),

                # 6) clássico
                p("Imprimir exatamente: Hello, World!",
                "print('Hello, World!')",
                "print(\"Hello, World!)", "print(Hello, World!)", "print('Hello,' 'World')"),
            ]
        elif "input" in topico:
            topic_only = [
                p("Ler uma linha do usuário em s", "s = input()", "s = input", "s = input(str)", "input() = s"),
                p("Ler número inteiro", "n = int(input())", "n = input(int())", "n = int(input)", "int = input()"),
                p("Ler e depois imprimir", "s=input(); print(s)", "print(input)", "s=print(input())", "input(print(s))"),
                p("Ler dois inputs separados", "a = input(); b = input()", "a, b = input()", "input(); input() = a, b", "a = b = input()"),
                p("Ler e imprimir direto", "print(input())", "input(print())", "print = input()", "input(); print()"),
                p("Ler nome e cumprimentar", "nome = input(); print('Olá', nome)", "input(print('Olá'))", "nome = print(input())", "print('Olá', input())")
            ]
        elif "for" in topico:
            topic_only = [
                p("Imprimir 0..4", "for i in range(5): print(i)", "for i in range(1,5): print(i)", "for i in 5: print(i)", "print(range(5))"),
                p("Somar 0..2 em s", "s=0\nfor i in range(3): s+=i\nprint(s)", "s=0\nfor i in range(3): s=s+i\nprint(i)", "for i in range(3): s+=i; print(s)", "s=0; for i in range(3): s+=i"),
                p("Loop sobre lista a", "a=[1,2];\nfor x in a: print(x)", "a=(1,2);\nfor x in a: print(a)", "for x in [a]: print(x)", "for x in a: print(a[x])"),
            ]
        elif "if" in topico:
            topic_only = [
                p("Imprimir 'ok' se x>0", "x=1\nif x>0:\n    print('ok')", "x=1\nif (x>0)\n    print('ok')", "x=1\nif x>0: print('ok'", "if x>0: print ok"),
                p("if/else válido", "if True:\n    print(1)\nelse:\n    print(2)", "if True:\nprint(1)\nelse:\nprint(2)", "if True:\n    print(1)\nelse print(2)", "if True: print(1)\nelse:"),
            ]

        return topic_only if topic_only else base

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
        sampled_wrongs = random.sample(wrongs, k) if k>0 else []

        alts_sel = [correct] + sampled_wrongs
        random.shuffle(alts_sel)

        self._lane_alternativas = []
        for i in range(self.num_lanes):
            if i < len(alts_sel):
                self._lane_alternativas.append(alts_sel[i])
            else:
                self._lane_alternativas.append({"txt":"...", "ok": False})

        self.total_correct_notes += 1
        self.wave_answered = False  # libera tentativa para a nova rodada

    # ---------- CONTROLES ----------
    def tratar_eventos(self, eventos):
        if self.finished:
            return
        for ev in eventos:
            if ev.type == pygame.KEYDOWN and ev.key in self.key_to_lane:
                if self.wave_answered:
                    # já tentou nessa rodada → ignora
                    continue
                self.wave_answered = True  # trava a rodada ao primeiro input
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

        # nota mais perto da linha de acerto
        n = min(candidates, key=lambda x: abs(x["y"] - self.hit_y))
        signed = n["y"] - self.hit_y   # <0 = acima (adiantado), >0 = abaixo (atrasado)
        dist   = abs(signed)

        # ---------- DENTRO DA JANELA (acerto normal) ----------
        if dist <= self.hit_window:
            if n["correct"]:
                self.hits += 1
                self.combo += 1
                self.best_combo = max(self.best_combo, self.combo)

                precision = 1.0 - (dist / self.hit_window)  # 1.0 perfeito → 0 na borda
                base_pts = 100
                self.score += int(base_pts * (1 + 0.25*precision) * (1 + 0.02*self.combo))

                if   precision >= 0.8: tag = "PERFECT!"
                elif precision >= 0.5: tag = "GOOD"
                else:                  tag = "LATE"
                self._add_fx(tag, self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (70,200,70))   # verde
            else:
                self.misses += 1
                self.combo = 0
                self.score = max(0, self.score - 40)
                self._add_fx("WRONG", self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (200,60,60))   # vermelho

            self.notes.remove(n)
            return

        # ---------- FORA DA JANELA, MAS ADIANTADO (EARLY) ----------
        # permite clicar ANTES da linha dentro de um "early window" mais largo
        if signed < -self.hit_window and dist <= self.hit_window + self.early_window:
            if n["correct"]:
                # quão perto da borda da janela (quanto mais perto, melhor)
                early_offset = (-signed) - self.hit_window  # 0 na borda; cresce p/ cima
                early_ratio  = 1.0 - (early_offset / self.early_window)  # 1.0 (quase bom) → 0 (bem cedo)

                self.hits += 1
                self.combo += 1
                self.best_combo = max(self.best_combo, self.combo)

                # pontuação menor que o acerto normal
                # (base ~60, com bônus leve por proximidade e combo)
                base_early = 60
                self.score += int(base_early * (0.6 + 0.4*early_ratio) * (1 + 0.01*self.combo))

                tag = "GOOD" if early_ratio >= 0.5 else "BAD"
                self._add_fx(tag, self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (70,200,70))   # verde (acertou)
            else:
                # apertou cedo mas na errada -> erro normal
                self.misses += 1
                self.combo = 0
                self.score = max(0, self.score - 40)
                self._add_fx("WRONG", self.lanes[lane].centerx, self.hit_y-10)
                self._flash_lane(lane, (200,60,60))   # vermelho

            self.notes.remove(n)
            return

        # ---------- MUITO CEDO (fora do early window) OU TARDIO FORA DA JANELA ----------
        self._flash_lane(lane, (200,60,60))
        self._register_miss()

    def _flash_lane(self, lane, color, dur_ms=150):
        self.lane_flash[lane] = (color, pygame.time.get_ticks() + dur_ms)

    def _register_miss(self):
        self.misses += 1
        self.combo = 0
        self.score = max(0, self.score - 30)
        self._add_fx("MISS", (self.lanes[0].x + self.lanes[-1].right)//2, self.hit_y-10)

    # ---------- SPAWN / UPDATE ----------
    def _spawn_notes(self):
        # cria blocos da rodada atual (não troca a pergunta aqui!)
        for lane_idx, alt in enumerate(self._lane_alternativas):
            self.notes.append({
                "lane": lane_idx,
                "y": self.lanes[lane_idx].y - 30,
                "text": alt["txt"],
                "correct": bool(alt["ok"])
            })

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

        # aceleração leve
        self.speed = self.base_speed + self.combo * 2
        self.beat_ms = max(900, self.base_beat - self.combo * 5)

        # mover notas
        for n in self.notes[:]:
            n["y"] += self.speed * dt
            if n["y"] > self.lanes[n["lane"]].bottom + 24:
                if n["correct"]:
                    self._register_miss()
                self.notes.remove(n)

        # se a rodada acabou (sem notas) e bateu intervalo, prepara a PRÓXIMA pergunta e spawna
        if not self.notes and (now - self.last_spawn >= self.beat_ms):
            self._prepare_next_prompt()   # agora sim troca a pergunta
            self._spawn_notes()
            self.last_spawn = now

        # fim do jogo (encerra assim que o tempo acabar)
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
        if self.on_finish:
            self.on_finish(self.score, stars)

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

        # trilhas + flash verde/vermelho
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

        # linha de acerto
        pygame.draw.line(tela, (110,190,255), (self.lanes[0].x, self.hit_y), (self.lanes[-1].right, self.hit_y), 4)

        # notas (NEUTRAS)
        for n in self.notes:
            lane = self.lanes[n["lane"]]
            rect = pygame.Rect(lane.x+6, int(n["y"])-18, lane.w-12, 36)
            base_col = (190, 205, 230)
            pygame.draw.rect(tela, base_col, rect, border_radius=10)
            pygame.draw.rect(tela, (20, 20, 20), rect, 2, border_radius=10)
            txt = n["text"].replace("\n", " ")
            f = self.fonte
            while f.size(txt)[0] > rect.w - 12 and f.get_height() > 12:
                f = pygame.font.SysFont("Consolas", f.get_height()-1)
            ts = f.render(txt, True, (0,0,0))
            tela.blit(ts, (rect.centerx - ts.get_width()//2, rect.centery - ts.get_height()//2))

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
