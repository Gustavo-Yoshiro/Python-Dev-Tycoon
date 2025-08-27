import pygame

class TelaLoja:
    def __init__(self, largura, altura, jogador, loja_service, callback_voltar):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.loja_service = loja_service
        self.callback_voltar = callback_voltar

        # Produtos fixos (mantidos)
        self.produtos = [
            {"produto": "Curso",        "nome": "Front-end", "tipo": "iniciante",     "preco": 50,  "tempo": 60},
            {"produto": "Curso",        "nome": "Front-end", "tipo": "intermediario", "preco": 100, "tempo": 120},
            {"produto": "Curso",        "nome": "Front-end", "tipo": "avancado",      "preco": 200, "tempo": 180},
            {"produto": "Treinamento",  "nome": "Social",    "tipo": "iniciante",     "preco": 40,  "tempo": 45},
            {"produto": "Treinamento",  "nome": "Social",    "tipo": "intermediario", "preco": 80,  "tempo": 90},
            {"produto": "Treinamento",  "nome": "Social",    "tipo": "avancado",      "preco": 150, "tempo": 150},
            {"produto": "Equipamentos", "nome": "Teclado",   "tipo": "basico",        "preco": 40,  "tempo": 0},
            {"produto": "Equipamentos", "nome": "Teclado",   "tipo": "Pro",           "preco": 80,  "tempo": 0},
            {"produto": "Equipamentos", "nome": "Monitor",   "tipo": "basico",        "preco": 40,  "tempo": 0},
            {"produto": "Equipamentos", "nome": "Monitor",   "tipo": "Pro",           "preco": 80,  "tempo": 0},
        ]

        # Layout da janela (popup central)
        w = min(int(self.largura * 0.82), 1100)
        h = min(int(self.altura * 0.8), 660)
        self.janela_rect = pygame.Rect(
            (self.largura - w)//2,
            (self.altura - h)//2,
            w, h
        )
        self.header_h = 64
        self.footer_h = 70
        self.padding = 16

        # Área scrollável da tabela
        self.view_rect = pygame.Rect(
            self.janela_rect.x + self.padding,
            self.janela_rect.y + self.header_h + self.padding,
            self.janela_rect.w - self.padding*2,
            self.janela_rect.h - (self.header_h + self.footer_h + self.padding*2)
        )

        # Botões e estados
        self.botoes_comprar = []  # [(rect_tela, produto)]
        self.mensagem = ""
        self.cor_mensagem = (255, 255, 255)
        self.scroll = 0.0

        # Botão Voltar (dentro do popup)
        self.botao_voltar = pygame.Rect(0, 0, 180, 44)  # posicionado no desenhar()

        # Carrega um fundo “geral” para aparecer sob o overlay (opcional)
        self._bg_img = None
        try:
            img = pygame.image.load("assets/TelaJogoIniciante.png")
            self._bg_img = pygame.transform.scale(img, (self.largura, self.altura))
        except Exception:
            self._bg_img = None  # se não existir, só mostra overlay

        # Paleta por categoria (mantida)
        self.cores_categorias = {
            "Curso": (60, 90, 140),
            "Treinamento": (60, 120, 90),
            "Equipamentos": (90, 60, 120)
        }

        # Colunas relativas ao popup
        # [Ícone+Nome, Tipo, Preço, Tempo, Ação]
        left = self.view_rect.x + 58   # espaço para ícone
        right = self.view_rect.right
        self.col_x = [
            left,                     # Nome
            left + 220,               # Tipo
            left + 380,               # Preço
            left + 510,               # Tempo
            right - 160               # Ação
        ]

        # Fontes
        self.font_titulo = pygame.font.SysFont('Arial', 30, bold=True)
        self.font_header = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_item   = pygame.font.SysFont('Arial', 20)
        self.font_secao  = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_btn    = pygame.font.SysFont('Arial', 22, bold=True)
        self.font_msg    = pygame.font.SysFont('Arial', 20, bold=True)

    # ---------- Utils de desenho ----------
    def _rounded(self, surf, rect, color, radius=16, width=0):
        pygame.draw.rect(surf, color, rect, width=width, border_radius=radius)

    def _shadow(self, surf, rect, radius=22, y_offset=8, alpha=110):
        # sombra simples (sem blur): um retângulo maior e translúcido
        s = pygame.Surface((rect.w + 20, rect.h + 20), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, alpha), s.get_rect(), border_radius=radius+6)
        surf.blit(s, (rect.x - 10, rect.y - 10 + y_offset))

    def _linha_div(self, surf, x1, y, x2, color=(200, 200, 200), w=1):
        pygame.draw.line(surf, color, (x1, y), (x2, y), w)

    def _draw_icon(self, surf, cx, cy, categoria, nome):
        # Ícones vetoriais simples, usando as cores da categoria
        col = self.cores_categorias.get(categoria, (100, 100, 100))
        # circulo de base
        pygame.draw.circle(surf, (24, 24, 28), (cx, cy), 20)
        pygame.draw.circle(surf, col, (cx, cy), 20, 2)

        if categoria == "Curso":
            # livro
            book = pygame.Rect(cx - 14, cy - 12, 22, 24)
            pygame.draw.rect(surf, col, book, border_radius=3)
            pygame.draw.rect(surf, (230, 230, 230), book, 2, border_radius=3)
            # lombada
            pygame.draw.line(surf, (230,230,230), (book.left+5, book.top+4), (book.left+5, book.bottom-4), 2)

        elif categoria == "Treinamento":
            # haltere
            pygame.draw.rect(surf, col, (cx-10, cy-4, 20, 8), border_radius=4)
            pygame.draw.rect(surf, col, (cx-18, cy-8, 6, 16), border_radius=2)
            pygame.draw.rect(surf, col, (cx+12, cy-8, 6, 16), border_radius=2)

        elif categoria == "Equipamentos":
            nm = (nome or "").strip().lower()
            if "monitor" in nm:
                # monitor
                pygame.draw.rect(surf, col, (cx-16, cy-12, 32, 18), 2, border_radius=3)
                pygame.draw.rect(surf, col, (cx-6, cy+8, 12, 3))
                pygame.draw.rect(surf, col, (cx-10, cy+11, 20, 2))
            elif "teclado" in nm:
                # teclado
                pygame.draw.rect(surf, col, (cx-18, cy-10, 36, 16), 2, border_radius=2)
                for i in range(-12, 13, 8):
                    pygame.draw.line(surf, col, (cx+i, cy-6), (cx+i, cy+4), 1)
            else:
                # fallback genérico
                pygame.draw.circle(surf, col, (cx, cy), 6)

    # ---------- Eventos ----------
    def tratar_eventos(self, eventos):
        for ev in eventos:
            if ev.type == pygame.MOUSEWHEEL:
                # scroll somente quando mouse está sobre a área de lista
                mx, my = pygame.mouse.get_pos()
                if self.view_rect.collidepoint(mx, my):
                    self.scroll -= ev.y * 40  # direção natural
                    self.scroll = max(0.0, min(self.scroll, float(getattr(self, "_max_scroll", 0))))

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                mx, my = ev.pos

                # Fechar no botão voltar (ou no X)
                if self.botao_voltar.collidepoint(mx, my):
                    self.callback_voltar()
                    return
                if hasattr(self, "btn_fechar") and self.btn_fechar.collidepoint(mx, my):
                    self.callback_voltar()
                    return

                # Comprar (rects já estão em coordenadas de tela)
                for (bot, produto) in self.botoes_comprar:
                    if bot.collidepoint(mx, my):
                        try:
                            self.loja_service.comprar_item(
                                id_jogador=self.jogador.get_id_jogador(),
                                nome=produto["nome"],
                                categoria=produto["tipo"],
                                preco=produto["preco"],
                                duracao_segundos=produto["tempo"]
                            )
                            self.mensagem = f"✔ {produto['nome']} ({produto['tipo']}) comprado!"
                            self.cor_mensagem = (0, 200, 0)
                        except Exception as e:
                            self.mensagem = f"✖ {e}"
                            self.cor_mensagem = (200, 50, 50)
                        return

    # ---------- Desenho ----------
    def desenhar(self, tela):
        # Fundo “geral” + overlay
        if self._bg_img:
            tela.blit(self._bg_img, (0, 0))
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        tela.blit(overlay, (0, 0))

        # Popup + sombra
        self._shadow(tela, self.janela_rect, y_offset=10, alpha=120)
        self._rounded(tela, self.janela_rect, (30, 34, 44), radius=20)       # corpo
        self._rounded(tela, self.janela_rect, (90, 170, 255), radius=20, width=3)  # borda

        # Header
        header_rect = pygame.Rect(self.janela_rect.x, self.janela_rect.y, self.janela_rect.w, self.header_h)
        self._rounded(tela, header_rect, (26, 32, 46), radius=20)
        titulo = self.font_titulo.render("Loja", True, (255, 255, 255))
        tela.blit(titulo, (header_rect.x + 20, header_rect.y + (self.header_h - titulo.get_height())//2))

        # Botão fechar (X) no header
        self.btn_fechar = pygame.Rect(header_rect.right - 50, header_rect.y + 14, 36, 36)
        pygame.draw.rect(tela, (60, 80, 120), self.btn_fechar, border_radius=8)
        x_font = pygame.font.SysFont('Arial', 22, bold=True)
        x_txt = x_font.render("X", True, (255, 255, 255))
        tela.blit(x_txt, (self.btn_fechar.centerx - x_txt.get_width()//2,
                          self.btn_fechar.centery - x_txt.get_height()//2))

        # Conteúdo scrollável
        # Moldura da lista
        pygame.draw.rect(tela, (22, 28, 40), self.view_rect, border_radius=12)
        pygame.draw.rect(tela, (80, 140, 220), self.view_rect, 1, border_radius=12)

        # Cabeçalho das colunas (fixo)
        ch_y = self.view_rect.y + 10
        headers = ["Nome", "Tipo", "Preço", "Tempo", "Ação"]
        for i, h in enumerate(headers):
            col = (200, 200, 50)
            surf = self.font_header.render(h, True, col)
            tela.blit(surf, (self.col_x[i], ch_y))
        self._linha_div(tela, self.view_rect.x+10, ch_y+28, self.view_rect.right-10, (60, 160, 255), 2)

        # Coleta status
        itens_jogador = self.loja_service.listar_itens_jogador(self.jogador.get_id_jogador())
        equip_comprados = {(i.get_nome().strip().lower(), i.get_categoria().strip().lower())
                           for i in itens_jogador if i.get_duracao_total() == 0}
        em_andamento = self.loja_service.listar_em_andamento(self.jogador.get_id_jogador())
        tem_curso_rodando = len(em_andamento) > 0

        categorias = {}
        for p in self.produtos:
            categorias.setdefault(p["produto"], []).append(p)

        # Área de recorte p/ scroll
        old_clip = tela.get_clip()
        tela.set_clip(self.view_rect)

        y = self.view_rect.y + 44 - int(self.scroll)
        row_h = 36
        gap_secao = 22

        self.botoes_comprar.clear()

        for categoria, itens in categorias.items():
            # Título da seção
            titulo_cat = self.font_secao.render(categoria, True, (100, 200, 255))
            tela.blit(titulo_cat, (self.view_rect.x + 8, y))
            y += gap_secao

            # Linhas da seção
            bg_col = self.cores_categorias.get(categoria, (50, 50, 50))
            for produto in itens:
                row_rect = pygame.Rect(self.view_rect.x + 8, y, self.view_rect.w - 16, row_h)
                # Fundo alternado leve
                pygame.draw.rect(tela, (bg_col[0], bg_col[1], bg_col[2],), row_rect, border_radius=6)

                # Ícone
                icon_x = self.view_rect.x + 26
                icon_y = y + row_h//2
                self._draw_icon(tela, icon_x, icon_y, categoria, produto["nome"])

                # Textos (mantendo cores)
                nome = produto["nome"]
                tipo = produto["tipo"]
                preco = produto["preco"]
                tempo_base = produto["tempo"]

                # tempo exibido (redução)
                tempo_exibir = 0
                if tempo_base > 0:
                    tempo_exibir = self.loja_service.calcular_tempo_com_reducao(self.jogador.get_id_jogador(), tempo_base)

                tela.blit(self.font_item.render(nome, True, (255, 255, 255)), (self.col_x[0], y + 7))
                tela.blit(self.font_item.render(tipo, True, (255, 255, 255)), (self.col_x[1], y + 7))
                tela.blit(self.font_item.render(f"${preco}", True, (0, 255, 0)), (self.col_x[2], y + 7))
                tela.blit(self.font_item.render(f"{tempo_exibir}s", True, (255, 255, 255)), (self.col_x[3], y + 7))

                # Botão/Aviso
                bot = pygame.Rect(self.col_x[4], y + 4, 140, row_h - 8)
                if categoria == "Equipamentos":
                    if (nome.strip().lower(), tipo.strip().lower()) in equip_comprados:
                        pygame.draw.rect(tela, (100, 100, 100), bot, border_radius=8)
                        txt = self.font_item.render("Comprado", True, (230, 230, 230))
                    else:
                        pygame.draw.rect(tela, (70, 200, 70), bot, border_radius=8)
                        txt = self.font_item.render("Comprar", True, (255, 255, 255))
                        # regista rect em coordenada de TELA (sem clip/scroll)
                        self.botoes_comprar.append((bot.copy(), produto))
                else:
                    if tem_curso_rodando:
                        pygame.draw.rect(tela, (120, 120, 120), bot, border_radius=8)
                        txt = self.font_item.render("Em andamento", True, (240, 240, 240))
                    else:
                        pygame.draw.rect(tela, (70, 200, 70), bot, border_radius=8)
                        txt = self.font_item.render("Comprar", True, (255, 255, 255))
                        self.botoes_comprar.append((bot.copy(), produto))

                tela.blit(txt, (bot.centerx - txt.get_width()//2, bot.centery - txt.get_height()//2))

                y += row_h + 6
            y += 12  # espaçamento após categoria

        # Calcula scroll máximo
        content_bottom = y + int(self.scroll)
        content_h = content_bottom - (self.view_rect.y + 44)
        max_scroll = max(0, content_h - (self.view_rect.h - 44))
        self._max_scroll = max_scroll

        tela.set_clip(old_clip)

        # Barra de scroll (se necessário)
        if max_scroll > 0:
            track = pygame.Rect(self.view_rect.right + 6, self.view_rect.y, 6, self.view_rect.h)
            pygame.draw.rect(tela, (50, 60, 80), track, border_radius=10)
            thumb_h = max(40, int(self.view_rect.h * (self.view_rect.h / (self.view_rect.h + max_scroll))))
            frac = 0 if max_scroll == 0 else (self.scroll / max_scroll)
            thumb_y = track.y + int((track.h - thumb_h) * frac)
            thumb = pygame.Rect(track.x, thumb_y, track.w, thumb_h)
            pygame.draw.rect(tela, (90, 170, 255), thumb, border_radius=10)

        # Footer (mensagem + Voltar)
        footer_rect = pygame.Rect(self.janela_rect.x, self.janela_rect.bottom - self.footer_h, self.janela_rect.w, self.footer_h)
        self._rounded(tela, footer_rect, (26, 32, 46), radius=20)
        if self.mensagem:
            txt_msg = self.font_msg.render(self.mensagem, True, self.cor_mensagem)
            tela.blit(txt_msg, (footer_rect.x + 18, footer_rect.y + footer_rect.h//2 - txt_msg.get_height()//2))

        # Posiciona botão Voltar no footer
        self.botao_voltar.update(
            footer_rect.right - self.padding - self.botao_voltar.w,
            footer_rect.y + (footer_rect.h - self.botao_voltar.h)//2,
            self.botao_voltar.w,
            self.botao_voltar.h
        )
        pygame.draw.rect(tela, (200, 50, 50), self.botao_voltar, border_radius=10)
        t = self.font_btn.render("Voltar", True, (255, 255, 255))
        tela.blit(t, (self.botao_voltar.centerx - t.get_width()//2,
                      self.botao_voltar.centery - t.get_height()//2))
