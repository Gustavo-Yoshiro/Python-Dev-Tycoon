# UI/View/ObjectiveView.py
import pygame
import random

class ObjectiveView:
    """
    View responsável apenas pelo MIÔLO do exercício do tipo 'objetiva':
    - monta/guarda alternativas (com seed do id_exercicio)
    - desenha pergunta, dica e alternativas dentro de um content_rect
    - trata clique para selecionar alternativa
    - expõe can_submit() e get_user_answer()
    """
    def __init__(self, fonte_base: pygame.font.Font, fonte_pequena: pygame.font.Font):
        self.fonte_base = fonte_base
        self.fonte_pequena = fonte_pequena

        self.exercicio = None
        self.alternativas = []   # lista de strings
        self.letras = []         # ['A', 'B', ...]
        self.rects = []          # [(pygame.Rect, idx)]
        self.selecionada = None  # índice da alternativa
        self._exercicio_id = None

    # ----------------------------
    # Utilitários de texto (copiados para ficar independente do container)
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
            linhas = ObjectiveView._quebrar_texto(texto, fonte, largura_max)
            total_h = len(linhas) * (fonte.get_height() + espacamento)
            if total_h <= altura_max:
                return fonte, linhas
            font_size -= 1
            fonte = pygame.font.SysFont('Consolas', font_size)
        linhas = ObjectiveView._quebrar_texto(texto, fonte, largura_max)
        max_linhas = max(1, altura_max // (fonte.get_height() + espacamento))
        if len(linhas) > max_linhas:
            linhas = linhas[:max_linhas-1] + ["..."]
        return fonte, linhas

    # ----------------------------
    # Ciclo de vida
    # ----------------------------
    def reset(self):
        self.exercicio = None
        self.alternativas = []
        self.letras = []
        self.rects = []
        self.selecionada = None
        self._exercicio_id = None

    def set_exercicio(self, exercicio):
        """Prepara alternativas com base no exercício atual."""
        self.reset()
        if not exercicio:
            return

        self.exercicio = exercicio
        self._exercicio_id = getattr(exercicio, "get_id_exercicio", lambda: None)()

        # monta alternativas: correta + até 3 erradas
        correta = exercicio.get_resposta_certa() or ""
        erradas = exercicio.get_resposta_erradas() or []
        erradas = erradas[:3]  # garante no máx 3

        alts = [correta] + erradas
        # Embaralha de forma estável usando a seed do id_exercicio (igual ao comportamento antigo)
        seed = self._exercicio_id if self._exercicio_id is not None else 0
        random.seed(seed)
        random.shuffle(alts)
        self.alternativas = alts
        self.letras = ['A', 'B', 'C', 'D'][:len(self.alternativas)]
        self.selecionada = None
        self.rects = []

    # ----------------------------
    # API consultada pelo container
    # ----------------------------
    def can_submit(self) -> bool:
        return self.selecionada is not None

    def get_user_answer(self):
        if self.selecionada is None or not self.alternativas:
            return None
        return self.alternativas[self.selecionada]

    # ----------------------------
    # Render / Eventos
    # ----------------------------
    def draw(self, tela: pygame.Surface, content_rect: pygame.Rect, feedback_ativo: bool = False):
        """
        Desenha pergunta, dica e alternativas dentro do content_rect.
        Mantém o estilo e a responsividade do código anterior.
        """
        if not self.exercicio:
            return

        x = content_rect.x
        y = content_rect.y
        w = content_rect.w
        h_total = content_rect.h

        # ---- PERGUNTA (até ~1/3 da altura disponível)
        fonte_pergunta, linhas_pergunta = self._ajustar_fonte_para_caber(
            self.exercicio.get_pergunta(), self.fonte_pequena, w, h_total // 3
        )
        for ln in linhas_pergunta:
            tela.blit(fonte_pergunta.render(ln, True, (255, 255, 255)), (x, y))
            y += fonte_pergunta.get_height() + 2

        # ---- DICA (até ~1/4 da altura disponível)
        dica_txt = f"Dica: {self.exercicio.get_dicas() or ''}"
        fonte_dica, linhas_dica = self._ajustar_fonte_para_caber(
            dica_txt, self.fonte_pequena, w, h_total // 4
        )
        for ln in linhas_dica:
            tela.blit(fonte_dica.render(ln, True, (180, 180, 0)), (x, y))
            y += fonte_dica.get_height() + 2

        # ---- ALTERNATIVAS (ocupa o restante até o botão)
        altura_restante = content_rect.bottom - y - 14
        n = max(1, len(self.alternativas))
        alt_h = max(30, min(42, altura_restante // n))
        self.rects = []

        for idx, alt in enumerate(self.alternativas):
            rect = pygame.Rect(x, y, w, alt_h)
            self.rects.append((rect, idx))

            # fundo e borda (mantendo o visual atual)
            pygame.draw.rect(tela, (200, 200, 50), rect, 0)
            if self.selecionada == idx:
                pygame.draw.rect(tela, (0, 180, 255), rect, 4)
            else:
                pygame.draw.rect(tela, (80, 80, 80), rect, 2)

            label = f"{self.letras[idx]}) {alt}"
            fonte_alt, linhas_alt = self._ajustar_fonte_para_caber(label, self.fonte_pequena, rect.w - 18, alt_h - 6)
            y_alt = rect.y + 4
            for l in linhas_alt:
                tela.blit(fonte_alt.render(l, True, (0, 0, 0)), (rect.x + 10, y_alt))
                y_alt += fonte_alt.get_height()

            y += alt_h + 5

    def handle_event(self, evento: pygame.event.Event, feedback_ativo: bool = False):
        """Clique em alternativa (apenas quando não estiver no feedback)."""
        if feedback_ativo:
            return

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos
            for rect, idx in self.rects:
                if rect.collidepoint(mx, my):
                    self.selecionada = idx
                    break
