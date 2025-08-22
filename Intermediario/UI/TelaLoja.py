import pygame

class TelaLoja:
    def __init__(self, largura, altura, jogador, loja_service, callback_voltar):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.loja_service = loja_service
        self.callback_voltar = callback_voltar

        # botão voltar
        self.botao_voltar = pygame.Rect(largura // 2 - 100, altura - 100, 200, 50)

        # produtos fixos (mock inicial, mas podiam vir do BD futuramente)
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

        # agora guardo pares (rect, produto) só para botões clicáveis
        self.botoes_comprar = []

        # mensagem de feedback
        self.mensagem = ""
        self.cor_mensagem = (255, 255, 255)

    def tratar_eventos(self, eventos):
        for ev in eventos:
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                # voltar
                if self.botao_voltar.collidepoint(ev.pos):
                    self.callback_voltar()
                    return

                # comprar (usa a lista de botões já mapeados com produto)
                for (botao, produto) in self.botoes_comprar:
                    if botao.collidepoint(ev.pos):
                        try:
                            # passa o tempo base; redução será aplicada no service
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

    def desenhar(self, tela):
        tela.fill((30, 30, 30))

        fonte = pygame.font.SysFont('Arial', 42, bold=True)
        titulo = fonte.render("Loja", True, (255, 255, 255))
        tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 30))

        # colunas (sem "Produto")
        fonte_header = pygame.font.SysFont('Arial', 22, bold=True)
        cabecalho = ["Nome", "Tipo", "Preço", "Tempo", "Ação"]
        pos_x = [180, 360, 520, 650, 820]

        fonte_item = pygame.font.SysFont('Arial', 20)   # menor que antes
        fonte_secao = pygame.font.SysFont('Arial', 28, bold=True)

        y = 120
        self.botoes_comprar.clear()

        # status atual do jogador
        itens_jogador = self.loja_service.listar_itens_jogador(self.jogador.get_id_jogador())
        equip_comprados = {(i.get_nome().strip().lower(), i.get_categoria().strip().lower())
                           for i in itens_jogador if i.get_duracao_total() == 0}
        em_andamento = self.loja_service.listar_em_andamento(self.jogador.get_id_jogador())
        tem_curso_rodando = len(em_andamento) > 0

        # paleta por categoria
        cores_categorias = {
            "Curso": (60, 90, 140),
            "Treinamento": (60, 120, 90),
            "Equipamentos": (90, 60, 120)
        }

        categorias = {}
        for p in self.produtos:
            categorias.setdefault(p["produto"], []).append(p)

        for categoria, itens in categorias.items():
            # título da categoria
            pygame.draw.line(tela, (200, 200, 200), (60, y - 10), (self.largura - 60, y - 10), 2)
            titulo_cat = fonte_secao.render(categoria, True, (100, 200, 255))
            tela.blit(titulo_cat, (80, y))
            y += 35

            # cabeçalho
            for i, col in enumerate(cabecalho):
                tela.blit(fonte_header.render(col, True, (200, 200, 50)), (pos_x[i], y))
            y += 30

            cor_fundo = cores_categorias.get(categoria, (50, 50, 50))

            # itens
            for produto in itens:
                # fundo suave por categoria
                rect_bg = pygame.Rect(100, y, self.largura - 200, 28)
                pygame.draw.rect(tela, cor_fundo, rect_bg, border_radius=4)

                nome = produto["nome"]
                tipo = produto["tipo"]
                preco = produto["preco"]
                tempo_base = produto["tempo"]

                # tempo para exibir (já com redução, quando for curso/treinamento)
                if tempo_base > 0:
                    tempo_exibir = self.loja_service.calcular_tempo_com_reducao(self.jogador.get_id_jogador(), tempo_base)
                else:
                    tempo_exibir = 0

                # textos básicos
                tela.blit(fonte_item.render(nome, True, (255, 255, 255)), (pos_x[0], y+4))
                tela.blit(fonte_item.render(tipo, True, (255, 255, 255)), (pos_x[1], y+4))
                tela.blit(fonte_item.render(f"${preco}", True, (0, 255, 0)), (pos_x[2], y+4))
                tela.blit(fonte_item.render(f"{tempo_exibir}s", True, (255, 255, 255)), (pos_x[3], y+4))

                # lógica do botão/estado
                botao_area = pygame.Rect(pos_x[4], y, 140, 28)
                desenhou_botao = False

                if categoria == "Equipamentos":
                    # já comprado?
                    if (nome.strip().lower(), tipo.strip().lower()) in equip_comprados:
                        # label "Comprado"
                        pygame.draw.rect(tela, (100, 100, 100), botao_area, border_radius=6)
                        txt = fonte_item.render("Comprado", True, (230, 230, 230))
                        tela.blit(txt, (botao_area.centerx - txt.get_width() // 2,
                                        botao_area.centery - txt.get_height() // 2))
                    else:
                        # botão comprar
                        pygame.draw.rect(tela, (70, 200, 70), botao_area, border_radius=6)
                        txt = fonte_item.render("Comprar", True, (255, 255, 255))
                        tela.blit(txt, (botao_area.centerx - txt.get_width() // 2,
                                        botao_area.centery - txt.get_height() // 2))
                        self.botoes_comprar.append((botao_area, produto))
                        desenhou_botao = True
                else:
                    # curso/treinamento
                    if tem_curso_rodando:
                        pygame.draw.rect(tela, (120, 120, 120), botao_area, border_radius=6)
                        txt = fonte_item.render("Em andamento", True, (240, 240, 240))
                        tela.blit(txt, (botao_area.centerx - txt.get_width() // 2,
                                        botao_area.centery - txt.get_height() // 2))
                    else:
                        pygame.draw.rect(tela, (70, 200, 70), botao_area, border_radius=6)
                        txt = fonte_item.render("Comprar", True, (255, 255, 255))
                        tela.blit(txt, (botao_area.centerx - txt.get_width() // 2,
                                        botao_area.centery - txt.get_height() // 2))
                        self.botoes_comprar.append((botao_area, produto))
                        desenhou_botao = True

                y += 34   # espaçamento reduzido

            y += 25

        # botão voltar
        pygame.draw.rect(tela, (200, 50, 50), self.botao_voltar, border_radius=8)
        fonte_btn = pygame.font.SysFont('Arial', 26, bold=True)
        texto_btn = fonte_btn.render("Voltar", True, (255, 255, 255))
        tela.blit(texto_btn, (self.botao_voltar.centerx - texto_btn.get_width() // 2,
                              self.botao_voltar.centery - texto_btn.get_height() // 2))

        if self.mensagem:
            fonte_msg = pygame.font.SysFont('Arial', 22, bold=True)
            txt_msg = fonte_msg.render(self.mensagem, True, self.cor_mensagem)
            tela.blit(txt_msg, (self.largura // 2 - txt_msg.get_width() // 2, self.altura - 150))
