import pygame

def _get(obj, names, default=0):
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            return v() if callable(v) else v
    return default

def _fmt_money(v):
    try:
        v = float(v)
    except:
        return str(v)
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.0f}K"
    return f"${int(v)}"

class HUDIntermediario:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura  = altura
        self.h = 92  # altura da faixa superior

        self.font_xs = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_sm = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_md = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_lg = pygame.font.SysFont("Arial", 22, bold=True)

    # ---------- helpers ----------
    def _top_bar(self, screen):
        band = pygame.Surface((self.largura, self.h), pygame.SRCALPHA)
        pygame.draw.rect(band, (0, 0, 0, 140), (0, 0, self.largura, self.h))
        pygame.draw.rect(band, (0, 0, 0, 60),  (0, self.h-28, self.largura, 28))
        screen.blit(band, (0, 0))
        pygame.draw.line(screen, (255, 255, 255, 40), (0, self.h), (self.largura, self.h), 1)

    def _pill(self, surface, x, y, w, h, color, text):
        rect = pygame.Rect(x, y, w, h)
        pill = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(pill, color, pill.get_rect(), border_radius=h//2)
        surface.blit(pill, (x, y))
        txt = self.font_md.render(text, True, (255, 255, 255))
        surface.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))

    def _rounded_panel(self, surface, x, y, w, h, alpha=120):
        pnl = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(pnl, (0, 0, 0, alpha), pnl.get_rect(), border_radius=14)
        surface.blit(pnl, (x, y))

    def _draw_bar(self, surface, x, y, w, h, frac):
        frac = max(0.0, min(1.0, float(frac)))
        pygame.draw.rect(surface, (80, 80, 80), (x, y, w, h), border_radius=h//2)
        pygame.draw.rect(surface, (70, 200, 70), (x, y, int(w * frac), h), border_radius=h//2)

    # ---------- HUD ----------
    # *args / **kwargs para ignorar parâmetros extras (ex.: titulo=...)
    def desenhar(self, screen, jogador, itens_andamento, *args, **kwargs):
        self._top_bar(screen)

        # valores
        dinheiro = _get(jogador, ["get_dinheiro", "dinheiro", "get_money", "money"], 0)
        backend  = int(_get(jogador, ["get_backend", "backend"], 0))
        frontend = int(_get(jogador, ["get_frontend", "frontend"], 0))
        social   = int(_get(jogador, ["get_social", "get_soft", "get_softskill", "get_softskills", "softskills", "soft"], 0))

        # cores
        cor_b = (255, 153, 51)   # laranja
        cor_f = (59, 142, 255)   # azul
        cor_s = (165, 94, 255)   # roxo
        cor_cash = (85, 200, 85)

        # -------- esquerda: 3 pills com nomes completos --------
        pill_w, pill_h, gap = 168, 36, 10
        x0 = 16
        y0 = 14
        self._pill(screen, x0 + 0*(pill_w+gap), y0, pill_w, pill_h, cor_b, f"Back-end {backend}")
        self._pill(screen, x0 + 1*(pill_w+gap), y0, pill_w, pill_h, cor_f, f"Front-end {frontend}")
        self._pill(screen, x0 + 2*(pill_w+gap), y0, pill_w, pill_h, cor_s, f"Social {social}")

        # -------- meio: painel com barra contínua do curso --------
        mid_w = int(self.largura * 0.36)
        mid_x = (self.largura - mid_w)//2 + int(self.largura * 0.05)

        mid_y = 10
        self._rounded_panel(screen, mid_x, mid_y, mid_w, self.h-20)

        nome   = "Sem curso em andamento"
        prog   = 0.0
        rest_s = None
        if itens_andamento:
            item   = itens_andamento[0]
            nome   = _get(item, ["get_nome", "nome"], "Curso")
            total  = float(_get(item, ["get_duracao_total", "duracao_total"], 0))
            rest   = float(_get(item, ["get_duracao_segundos", "duracao_segundos"], 0))
            prog   = (total - rest) / total if total > 0 else 0.0
            rest_s = int(rest)

        title = self.font_sm.render(nome[:38], True, (255,255,255))
        screen.blit(title, (mid_x + 16, mid_y + 12))
        self._draw_bar(screen, mid_x + 16, mid_y + 40, mid_w - 32, 18, prog)
        if rest_s is not None:
            under = self.font_xs.render(f"{rest_s}s restantes", True, (220,220,220))
            screen.blit(under, (mid_x + 16, mid_y + 64))

        # -------- direita: cash --------
        right_w = 150
        right_x = self.largura - right_w - 16
        right_y = 14
        self._pill(screen, right_x, right_y, right_w, 36, cor_cash, _fmt_money(dinheiro))
