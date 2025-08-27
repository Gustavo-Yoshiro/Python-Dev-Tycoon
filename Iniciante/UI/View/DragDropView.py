# Iniciante/UI/View/DragDropView.py
import pygame
import random

class DragDropView:
    """
    View para exercícios 'dragdrop' com layout:
      - Esquerda: blocos "bagunçados" (posições aleatórias, sem sobreposição)
      - Direita: sua resposta (empilhados em ordem)
    Interação: clique no bloco (esq -> dir) e clique no bloco na direita (dir -> esq).
    Envio: permitido quando houver pelo menos 2 blocos na resposta.
    """
    MIN_SUBMIT = 1  # quantidade mínima de blocos na resposta para liberar ENVIAR

    def __init__(self, fonte_base: pygame.font.Font, fonte_pequena: pygame.font.Font):
        self.fonte_base = fonte_base
        self.fonte_pequena = fonte_pequena

        self.exercicio = None
        self._exercicio_id = None

        # estado textual
        self.disponiveis = []      # lista de strings (ordem atual)
        self.resposta = []         # lista de strings (ordem atual)
        self._alvo_qtd = 0         # qtd de blocos corretos esperados

        # hit-test rects
        self._left_rects = []      # rects dos blocos à esquerda (ordem = self.disponiveis)
        self._right_rects = []     # rects dos blocos à direita (ordem = self.resposta)

        # cache/controle do layout bagunçado
        self._left_area_rect_last = None
        self._left_cached_rects = None
        self._left_layout_dirty = True

    # ----------------------------
    # Utilitários
    # ----------------------------
    @staticmethod
    def _quebrar_texto(texto, fonte, largura_max):
        palavras = (texto or "").split(' ')
        linhas, linha = [], ''
        for palavra in palavras:
            teste = linha + palavra + ' '
            if fonte.size(teste)[0] > largura_max:
                if linha.strip():
                    linhas.append(linha.strip())
                linha = palavra + ' '
            else:
                linha = teste
        if linha.strip():
            linhas.append(linha.strip())
        return linhas

    @staticmethod
    def _ajustar_fonte_para_caber(texto, fonte_base, largura_max, altura_max, min_font=13, espacamento=4):
        font_size = fonte_base.get_height()
        fonte = fonte_base
        while font_size >= min_font:
            linhas = DragDropView._quebrar_texto(texto, fonte, largura_max)
            total_h = len(linhas) * (fonte.get_height() + espacamento)
            if total_h <= altura_max:
                return fonte, linhas
            font_size -= 1
            fonte = pygame.font.SysFont('Consolas', font_size)
        linhas = DragDropView._quebrar_texto(texto, fonte, largura_max)
        max_linhas = max(1, altura_max // (fonte.get_height() + espacamento))
        if len(linhas) > max_linhas:
            linhas = linhas[:max_linhas-1] + ["..."]
        return fonte, linhas

    @staticmethod
    def _sanitize_bloco(txt: str) -> str:
        # preserva indentação (TAB -> 4 espaços) e remove quebras internas
        txt = (txt or "").replace("\t", "    ")
        return txt.replace("\r\n", " ").replace("\n", " ")

    @staticmethod
    def _rect_no_overlap(test_rect: pygame.Rect, rects, margin=6) -> bool:
        """Retorna True se test_rect NÃO colide com nenhum rect em 'rects', considerando margem bilateral."""
        a = test_rect.inflate(margin, margin)
        for r in rects:
            if a.colliderect(r.inflate(margin, margin)):
                return False
        return True

    @staticmethod
    def _first_fit_scan(area: pygame.Rect, bw: int, bh: int, placed_rects, margin=6, step=6) -> pygame.Rect | None:
        """
        Procura posição livre varrendo a área em “grade”.
        Garante não sobreposição (com margem). Retorna um Rect ou None.
        """
        # varreduras com passos diferentes (começa mais largo, afina se apertado)
        for st in (step, max(3, step - 2), 2):
            y = area.y
            while y <= area.bottom - bh:
                x = area.x
                while x <= area.right - bw:
                    cand = pygame.Rect(x, y, bw, bh)
                    if DragDropView._rect_no_overlap(cand, placed_rects, margin=margin):
                        return cand
                    x += st
                y += st
        return None

    @staticmethod
    def _relax_no_overlap(area: pygame.Rect, rects, margin=6, iters=16):
        """
        Pequeno pós-processamento: se algum par ainda encostar (considerando margem),
        empurra levemente para separar, sem sair da área.
        """
        if not rects:
            return
        for _ in range(iters):
            moved = False
            for i in range(len(rects)):
                for j in range(i+1, len(rects)):
                    a = rects[i]
                    b = rects[j]
                    ai = a.inflate(margin, margin)
                    bi = b.inflate(margin, margin)
                    if ai.colliderect(bi):
                        # vetor de empurrão simples (horizontal prior)
                        dx_left  = max(0, (ai.right - bi.left))
                        dx_right = max(0, (bi.right - ai.left))
                        dy_up    = max(0, (ai.bottom - bi.top))
                        dy_down  = max(0, (bi.bottom - ai.top))

                        # escolhe menor afastamento
                        options = [
                            ("left",  dx_left),
                            ("right", dx_right),
                            ("up",    dy_up),
                            ("down",  dy_down),
                        ]
                        direction, _ = min(options, key=lambda t: t[1])

                        if direction == "left":
                            b.x = min(b.x + max(1, margin//2), area.right - b.w)
                        elif direction == "right":
                            a.x = min(a.x + max(1, margin//2), area.right - a.w)
                        elif direction == "up":
                            b.y = min(b.y + max(1, margin//2), area.bottom - b.h)
                        else:  # down
                            a.y = min(a.y + max(1, margin//2), area.bottom - a.h)

                        # clampa para ficar dentro
                        a.x = max(area.x, min(a.x, area.right - a.w))
                        a.y = max(area.y, min(a.y, area.bottom - a.h))
                        b.x = max(area.x, min(b.x, area.right - b.w))
                        b.y = max(area.y, min(b.y, area.bottom - b.h))
                        moved = True
            if not moved:
                break

    # ----------------------------
    # Ciclo de vida
    # ----------------------------
    def reset(self):
        self.exercicio = None
        self._exercicio_id = None
        self.disponiveis = []
        self.resposta = []
        self._alvo_qtd = 0
        self._left_rects = []
        self._right_rects = []
        self._left_area_rect_last = None
        self._left_cached_rects = None
        self._left_layout_dirty = True

    def set_exercicio(self, exercicio):
        """Prepara blocos de acordo com o exercício atual."""
        self.reset()
        if not exercicio:
            return

        self.exercicio = exercicio
        self._exercicio_id = getattr(exercicio, "get_id_exercicio", lambda: None)()

        resp_certa = (exercicio.get_resposta_certa() or "")
        corretos = resp_certa.split("|") if resp_certa else []
        self._alvo_qtd = len(corretos)

        erradas = exercicio.get_resposta_erradas() or []
        # Monta a lista de blocos disponíveis (corretos + errados), embaralhando com seed do id
        blocos = list(corretos) + list(erradas)
        seed = self._exercicio_id if self._exercicio_id is not None else 0
        random.seed(seed)
        random.shuffle(blocos)
        self.disponiveis = blocos
        self.resposta = []
        self._left_layout_dirty = True

    # ----------------------------
    # API p/ container
    # ----------------------------
    def can_submit(self) -> bool:
        # Agora libera com qualquer quantidade >= MIN_SUBMIT
        return len(self.resposta) >= self.MIN_SUBMIT

    def get_user_answer(self) -> str:
        return "|".join(self.resposta)

    # ----------------------------
    # Layout “bagunçado” (esquerda)
    # ----------------------------
    def _compute_baguncado_layout(self, area_rect: pygame.Rect):
        """
        Gera posições aleatórias, sem sobreposição, para cada item de self.disponiveis.
        As posições ficam estáveis até mudar a lista ou a área.
        """
        rects = []
        if not self.disponiveis:
            return rects

        # Parâmetros visuais
        block_h = 34
        pad_x = 10
        min_w = max(80, int(area_rect.w * 0.28))
        max_w = max(min_w, int(area_rect.w * 0.9))

        attempts_per_block = 180
        margin = 8

        # seed base por exercício
        base_seed = str(self._exercicio_id if self._exercicio_id is not None else 0)

        # >>> Novo: contador por ocorrência de texto (evita RNG idêntico p/ textos repetidos)
        occ = {}

        for bloco in self.disponiveis:
            # largura baseada no texto (limitada)
            txt = self._sanitize_bloco(bloco)
            txt_w = self.fonte_pequena.size(txt)[0] + 2 * pad_x
            bw = max(min_w, min(max_w, txt_w))
            bh = block_h

            k = txt
            c = occ.get(k, 0)
            occ[k] = c + 1

            # RNG estável por bloco (id + texto + ocorrência)
            rng = random.Random(f"{base_seed}|{txt}|{c}")

            placed = False
            # 1) tentativa aleatória com rejeição
            for _ in range(attempts_per_block):
                x = rng.randint(area_rect.x, max(area_rect.x, area_rect.right - bw))
                y = rng.randint(area_rect.y, max(area_rect.y, area_rect.bottom - bh))
                candidate = pygame.Rect(x, y, bw, bh)
                if self._rect_no_overlap(candidate, rects, margin=margin):
                    rects.append(candidate)
                    placed = True
                    break

            # 2) fallback determinístico (grade first-fit)
            if not placed:
                ff = self._first_fit_scan(area_rect, bw, bh, rects, margin=margin, step=6)
                if ff is not None:
                    rects.append(ff)
                    placed = True

            # 3) fallback extra: tenta com margem reduzida e passo menor (ainda SEM sobrepor)
            if not placed:
                ff = self._first_fit_scan(area_rect, bw, bh, rects, margin=max(2, margin-4), step=3)
                if ff is not None:
                    rects.append(ff)
                    placed = True

            # 4) último recurso: varredura fina 100% segura (nunca “na marra”)
            if not placed:
                ff = self._first_fit_scan(area_rect, bw, bh, rects, margin=0, step=2)
                if ff is not None:
                    rects.append(ff)
                    placed = True
                else:
                    # Em áreas EXTREMAMENTE lotadas: força dentro e depois relaxa (ainda sem cruzar)
                    cand = pygame.Rect(area_rect.x, area_rect.y, bw, bh)
                    # encontra qualquer x,y que minimize interseção
                    best = None
                    best_hits = 10**9
                    y = area_rect.y
                    while y <= area_rect.bottom - bh:
                        x = area_rect.x
                        while x <= area_rect.right - bw:
                            cand.topleft = (x, y)
                            hits = sum(cand.colliderect(r) for r in rects)
                            if hits < best_hits:
                                best_hits = hits
                                best = cand.copy()
                                if best_hits == 0:
                                    break
                            x += 2
                        if best_hits == 0:
                            break
                        y += 2
                    rects.append(best if best is not None else cand)

        # Pós-processo: pequeno relax para afastar o que encostar pela margem
        self._relax_no_overlap(area_rect, rects, margin=margin, iters=18)

        return rects

    # ----------------------------
    # Render / Eventos
    # ----------------------------
    def draw(self, tela: pygame.Surface, content_rect: pygame.Rect, feedback_ativo: bool = False):
        """
        Desenha pergunta, dica e as duas colunas dentro de content_rect.
        Usa clipping na área esquerda para garantir que nada desenhe fora dela.
        """
        if not self.exercicio:
            return

        x = content_rect.x
        y = content_rect.y
        w = content_rect.w
        h_total = content_rect.h

        # ---- PERGUNTA (~1/4)
        fonte_pergunta, linhas_pergunta = self._ajustar_fonte_para_caber(
            self.exercicio.get_pergunta(), self.fonte_pequena, w, h_total // 4
        )
        for ln in linhas_pergunta:
            tela.blit(fonte_pergunta.render(ln, True, (255, 255, 255)), (x, y))
            y += fonte_pergunta.get_height() + 2

        # ---- DICA (~1/6)
        dica_txt = f"Dica: {self.exercicio.get_dicas() or ''}"
        fonte_dica, linhas_dica = self._ajustar_fonte_para_caber(
            dica_txt, self.fonte_pequena, w, h_total // 6
        )
        for ln in linhas_dica:
            tela.blit(fonte_dica.render(ln, True, (180, 180, 0)), (x, y))
            y += fonte_dica.get_height() + 2

        # ---- LAYOUT COLUNAS
        gap = 20
        left_w = int(w * 0.48)
        right_w = w - left_w - gap
        left_x = x
        right_x = x + left_w + gap

        # Títulos
        tela.blit(self.fonte_pequena.render("Blocos disponíveis (bagunça):", True, (200, 200, 255)), (left_x, y))
        tela.blit(self.fonte_pequena.render("Sua resposta:", True, (120, 255, 120)), (right_x, y))

        y_list = y + 30

        # Áreas de cada lado
        left_area = pygame.Rect(left_x, y_list, left_w, content_rect.bottom - y_list - 12)
        right_area = pygame.Rect(right_x, y_list, right_w, content_rect.bottom - y_list - 12)

        # Fundo leve e bordas
        pygame.draw.rect(tela, (26, 36, 56), left_area, border_radius=8)
        pygame.draw.rect(tela, (70, 110, 180), left_area, 2, border_radius=8)
        pygame.draw.rect(tela, (24, 44, 28), right_area, border_radius=8)
        pygame.draw.rect(tela, (70, 140, 90), right_area, 2, border_radius=8)

        # ----- LADO ESQUERDO (bagunçado) com CLIPPING -----
        area_changed = (self._left_area_rect_last is None) or (self._left_area_rect_last != left_area)
        if area_changed:
            self._left_area_rect_last = left_area.copy()
            self._left_layout_dirty = True

        if self._left_layout_dirty or self._left_cached_rects is None:
            self._left_cached_rects = self._compute_baguncado_layout(left_area)
            self._left_layout_dirty = False

        self._left_rects = []
        old_clip = tela.get_clip()
        tela.set_clip(left_area)  # nada desenha fora da área esquerda

        for i, bloco in enumerate(self.disponiveis):
            if i >= len(self._left_cached_rects):
                break
            rect = self._left_cached_rects[i]

            pygame.draw.rect(tela, (40, 120, 255), rect, border_radius=6)
            pygame.draw.rect(tela, (30, 40, 90), rect, 2, border_radius=6)

            texto = self._sanitize_bloco(bloco)
            fonte_b = self.fonte_pequena
            while fonte_b.size(texto)[0] > rect.w - 12 and fonte_b.get_height() > 12:
                fonte_b = pygame.font.SysFont('Consolas', fonte_b.get_height() - 1)
            txt_img = fonte_b.render(texto, True, (255, 255, 255))
            tela.blit(txt_img, (rect.x + 6, rect.y + (rect.h - txt_img.get_height()) // 2))

            self._left_rects.append(rect)

        tela.set_clip(old_clip)  # restaura clipping

        # ----- LADO DIREITO (empilhado) -----
        self._right_rects = []
        n_linhas = max(1, len(self.resposta))
        # altura adaptativa por quantidade de linhas
        bloco_altura = max(28, min(35, (right_area.h - 20) // n_linhas)) if n_linhas > 0 else 30

        for i, bloco in enumerate(self.resposta):
            rect = pygame.Rect(right_area.x, right_area.y + i * bloco_altura, right_area.w, bloco_altura - 5)
            pygame.draw.rect(tela, (80, 210, 80), rect, border_radius=6)
            pygame.draw.rect(tela, (30, 60, 30), rect, 2, border_radius=6)

            texto = self._sanitize_bloco(bloco)
            fonte_b = self.fonte_pequena
            while fonte_b.size(texto)[0] > rect.w - 12 and fonte_b.get_height() > 12:
                fonte_b = pygame.font.SysFont('Consolas', fonte_b.get_height() - 1)
            txt_img = fonte_b.render(texto, True, (255, 255, 255))
            tela.blit(txt_img, (rect.x + 6, rect.y + (rect.h - txt_img.get_height()) // 2))

            self._right_rects.append(rect)

    def handle_event(self, evento: pygame.event.Event, feedback_ativo: bool = False):
        """Move bloco entre colunas ao clicar (apenas quando não estiver no feedback)."""
        if feedback_ativo or not self.exercicio:
            return

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos

            # Clique em um bloco da ESQUERDA -> vai para a DIREITA (append)
            for i, rect in enumerate(self._left_rects):
                if i < len(self.disponiveis) and rect.collidepoint(mx, my):
                    bloco = self.disponiveis.pop(i)
                    self.resposta.append(bloco)
                    # layout precisa ser recalculado (restantes mudam)
                    self._left_layout_dirty = True
                    return

            # Clique em um bloco da DIREITA -> volta para a ESQUERDA (append no fim)
            for i, rect in enumerate(self._right_rects):
                if i < len(self.resposta) and rect.collidepoint(mx, my):
                    bloco = self.resposta.pop(i)
                    self.disponiveis.append(bloco)
                    self._left_layout_dirty = True
                    return
