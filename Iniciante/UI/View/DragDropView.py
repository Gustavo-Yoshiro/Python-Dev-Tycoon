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
    def _rect_no_overlap(test_rect: pygame.Rect, rects, margin=4):
        # Verifica se test_rect (com "folga") colide com algum rect em rects
        inflated = test_rect.inflate(margin, margin)
        for r in rects:
            if inflated.colliderect(r):
                return False
        return True

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

        rng = random.Random()
        # usa seed do exercício para não "pular" toda vez
        seed = (self._exercicio_id if self._exercicio_id is not None else 0) + len(self.disponiveis) * 97
        rng.seed(seed)

        attempts_per_block = 200

        for bloco in self.disponiveis:
            # largura baseada no texto (limitada)
            txt = self._sanitize_bloco(bloco)
            txt_w = self.fonte_pequena.size(txt)[0] + 2 * pad_x
            bw = max(min_w, min(max_w, txt_w))
            bh = block_h

            placed = False
            for _ in range(attempts_per_block):
                x = rng.randint(area_rect.x, max(area_rect.x, area_rect.right - bw))
                y = rng.randint(area_rect.y, max(area_rect.y, area_rect.bottom - bh))
                candidate = pygame.Rect(x, y, bw, bh)
                if self._rect_no_overlap(candidate, rects, margin=6):
                    rects.append(candidate)
                    placed = True
                    break

            if not placed:
                # Fallback: empilha (quase não acontece)
                if rects:
                    last = rects[-1]
                    nx = area_rect.x
                    ny = last.bottom + 6
                else:
                    nx = area_rect.x
                    ny = area_rect.y
                rects.append(pygame.Rect(nx, ny, bw, bh))

        return rects

    # ----------------------------
    # Render / Eventos
    # ----------------------------
    def draw(self, tela: pygame.Surface, content_rect: pygame.Rect, feedback_ativo: bool = False):
        """
        Desenha pergunta, dica e as duas colunas dentro de content_rect.
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
        tela.blit(self.fonte_pequena.render("Blocos disponíveis (bagunça):", True, (200,200,255)), (left_x, y))
        tela.blit(self.fonte_pequena.render("Sua resposta:", True, (120,255,120)), (right_x, y))

        y_list = y + 30

        # Áreas de cada lado
        left_area = pygame.Rect(left_x, y_list, left_w, content_rect.bottom - y_list - 12)
        right_area_top = y_list

        # Fundo leve da área esquerda
        pygame.draw.rect(tela, (26, 36, 56), left_area, border_radius=8)
        pygame.draw.rect(tela, (70, 110, 180), left_area, 2, border_radius=8)

        # ----- LADO ESQUERDO (bagunçado)
        area_changed = (self._left_area_rect_last is None) or (self._left_area_rect_last != left_area)
        if area_changed:
            self._left_area_rect_last = left_area.copy()
            self._left_layout_dirty = True

        if self._left_layout_dirty or self._left_cached_rects is None:
            self._left_cached_rects = self._compute_baguncado_layout(left_area)
            self._left_layout_dirty = False

        self._left_rects = []
        for i, bloco in enumerate(self.disponiveis):
            if i >= len(self._left_cached_rects):
                break
            rect = self._left_cached_rects[i]

            # bloco visual
            pygame.draw.rect(tela, (40, 120, 255), rect, border_radius=6)
            pygame.draw.rect(tela, (30, 40, 90), rect, 2, border_radius=6)

            texto = self._sanitize_bloco(bloco)
            fonte_b = self.fonte_pequena
            # encolhe fonte se necessário
            while fonte_b.size(texto)[0] > rect.w - 12 and fonte_b.get_height() > 12:
                fonte_b = pygame.font.SysFont('Consolas', fonte_b.get_height() - 1)
            txt_img = fonte_b.render(texto, True, (255,255,255))
            tela.blit(txt_img, (rect.x + 6, rect.y + (rect.h - txt_img.get_height()) // 2))

            self._left_rects.append(rect)

        # ----- LADO DIREITO (empilhado)
        self._right_rects = []
        n_linhas = max(1, len(self.resposta))
        bloco_altura = max(28, min(35, (content_rect.bottom - right_area_top - 30)//n_linhas)) if n_linhas > 0 else 30
        for i, bloco in enumerate(self.resposta):
            rect = pygame.Rect(right_x, right_area_top + i*bloco_altura, right_w, bloco_altura-5)
            pygame.draw.rect(tela, (80, 210, 80), rect, border_radius=6)
            pygame.draw.rect(tela, (30, 60, 30), rect, 2, border_radius=6)

            texto = self._sanitize_bloco(bloco)
            fonte_b = self.fonte_pequena
            while fonte_b.size(texto)[0] > rect.w - 12 and fonte_b.get_height() > 12:
                fonte_b = pygame.font.SysFont('Consolas', fonte_b.get_height() - 1)
            txt_img = fonte_b.render(texto, True, (255,255,255))
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
