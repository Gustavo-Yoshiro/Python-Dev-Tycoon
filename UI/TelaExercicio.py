import pygame
from Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
import random
import os

class TelaExercicio:
    def __init__(self, largura, altura, total_fases=1, fases_concluidas=0, callback_rever_introducao=None):
        self.largura = largura
        self.altura = altura
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Consolas', 24)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 18)
        self.exercicio_service = ExercicioServiceImpl()
        self.exercicios = []
        self.exercicio_selecionado = None
        self.input_ativo = False
        self.resposta_usuario = ""
        self.resultado = ""
        self.feedback_ativo = False
        self.indice_atual = 0
        self.acertos = 0
        self.erros = 0
        self.finalizado = False
        self.callback_rever_introducao = callback_rever_introducao

        # Livro de ajuda
        # Livro/ajuda no canto superior direito (fora do monitor)
        self.rect_livro = pygame.Rect(int(largura * 0.85), int(altura * 0.12), 48, 48)
        self.img_ajuda = pygame.image.load(os.path.join("Assets", "ajuda.png")).convert_alpha()
        self.img_ajuda = pygame.transform.smoothscale(self.img_ajuda, (self.rect_livro.width, self.rect_livro.height))

        # Imagem de fundo do monitor
        caminho_img = os.path.join("Assets", "intro_pc1.png")
        self.bg = pygame.image.load(caminho_img).convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        # Painel central do monitor (para enunciado e blocos)
        self.painel_x = int(largura * 0.286)
        self.painel_y = int(altura * 0.228)
        self.painel_w = int(largura * 0.425)
        self.painel_h = int(altura * 0.375)

        # Barra azul do topo (progresso dos tópicos e questões)
        self.barra_topo_x = self.painel_x
        self.barra_topo_y = self.painel_y - 82
        self.barra_topo_w = self.painel_w
        self.barra_topo_h = 16

        
        self.botao_w = 250        # Largura maior
        self.botao_h = 30         # Altura maior
        self.botao_x = self.painel_x + (self.painel_w - self.botao_w) // 2  # Centralizado
        self.botao_y = self.painel_y + self.painel_h + 42                   # Um pouco abaixo do painel
        self.rect_enviar = pygame.Rect(self.botao_x, self.botao_y, self.botao_w, self.botao_h)

        

        # Caixa de input para resposta dissertativa
        self.caixa_input = pygame.Rect(self.painel_x + 30, self.botao_y - 170, self.painel_w - 60, 90)
        self.rect_alternativas = []
        self.alternativa_selecionada = None

        # Progresso geral (tópicos)
        self.total_fases = total_fases
        self.fases_concluidas = fases_concluidas

        # Para drag and drop
        self.blocos_disponiveis = []
        self.blocos_resposta = []

    @staticmethod
    def quebrar_texto(texto, fonte, largura_max):
        palavras = texto.split(' ')
        linhas = []
        linha = ''
        for palavra in palavras:
            teste = linha + palavra + ' '
            if fonte.size(teste)[0] > largura_max:
                linhas.append(linha)
                linha = palavra + ' '
            else:
                linha = teste
        linhas.append(linha)
        return linhas

    def carregar_exercicios(self, id_fase):
        self.exercicios = self.exercicio_service.listar_exercicios_por_fase(id_fase)
        self.indice_atual = 0
        self.acertos = 0
        self.erros = 0
        self.finalizado = False
        self.exercicio_selecionado = self.exercicios[self.indice_atual] if self.exercicios else None
        self.resposta_usuario = ""
        self.resultado = ""
        self.alternativa_selecionada = None
        self.feedback_ativo = False
        self.blocos_disponiveis = []
        self.blocos_resposta = []

    def desenhar(self, tela):
        tela.blit(self.bg, (0, 0))

        # --- BARRA DE PROGRESSO GERAL (tópicos) ---
        if self.total_fases > 1:
            progresso = self.fases_concluidas / self.total_fases
            pygame.draw.rect(tela, (70, 120, 180), (self.barra_topo_x, self.barra_topo_y, self.barra_topo_w, 8), border_radius=3)
            pygame.draw.rect(tela, (0, 200, 255), (self.barra_topo_x, self.barra_topo_y, int(self.barra_topo_w * progresso), 8), border_radius=3)
            tela.blit(self.fonte_pequena.render(f"Tópicos: {self.fases_concluidas}/{self.total_fases}", True, (255,255,255)),
                      (self.barra_topo_x + self.barra_topo_w + 10, self.barra_topo_y - 2))

        # --- BARRA DE PROGRESSO DAS QUESTÕES ---
        if self.exercicios:
            total = len(self.exercicios)
            progresso = (self.indice_atual + 1) / total
            y_barra2 = self.barra_topo_y + 14
            pygame.draw.rect(tela, (80, 80, 80), (self.barra_topo_x, y_barra2, self.barra_topo_w, 12), border_radius=3)
            pygame.draw.rect(tela, (0, 200, 80), (self.barra_topo_x, y_barra2, int(self.barra_topo_w*progresso), 12), border_radius=3)
            tela.blit(self.fonte_pequena.render(f"Questão {self.indice_atual+1}/{total}", True, (255,255,255)),
                      (self.barra_topo_x + self.barra_topo_w + 10, y_barra2))

        # --- ÁREA CENTRAL DO EXERCÍCIO (painel escuro do monitor) ---
        if self.finalizado:
            msg = f"Quiz finalizado!"
            placar = f"Acertos: {self.acertos} | Erros: {self.erros} de {len(self.exercicios)}"
            tela.blit(self.fonte.render(msg, True, (0, 255, 255)), (self.painel_x + 30, self.painel_y + 70))
            tela.blit(self.fonte_pequena.render(placar, True, (255, 255, 255)), (self.painel_x + 30, self.painel_y + 120))
            return

        if self.exercicio_selecionado:
            y = self.painel_y + 48
            tela.blit(self.fonte.render("Enunciado:", True, (255, 255, 0)), (self.painel_x + 22, y))
            y += 34
            linhas_pergunta = self.quebrar_texto(self.exercicio_selecionado.get_pergunta(), self.fonte_pequena, self.painel_w - 60)
            for linha in linhas_pergunta:
                tela.blit(self.fonte_pequena.render(linha, True, (255, 255, 255)), (self.painel_x + 22, y))
                y += 25

            tela.blit(self.fonte_pequena.render(f"Dica: {self.exercicio_selecionado.get_dicas()}", True, (180, 180, 0)), (self.painel_x + 22, y))
            y += 32

            tipo = self.exercicio_selecionado.get_tipo().lower()

            # --------------- OBJETIVA -------------------
            if tipo == "objetiva":
                erradas = self.exercicio_selecionado.get_resposta_erradas()[:3] if self.exercicio_selecionado.get_resposta_erradas() else []
                alternativas = [self.exercicio_selecionado.get_resposta_certa()] + erradas
                random.seed(self.exercicio_selecionado.get_id_exercicio())
                random.shuffle(alternativas)
                letras = ['A', 'B', 'C', 'D'][:len(alternativas)]
                self.rect_alternativas = []
                for idx, alt in enumerate(alternativas):
                    rect = pygame.Rect(self.painel_x + 22, y, self.painel_w - 44, 30)
                    self.rect_alternativas.append((rect, alt, idx))
                    cor = (200, 200, 50)
                    pygame.draw.rect(tela, cor, rect, 0)
                    if self.alternativa_selecionada == idx:
                        pygame.draw.rect(tela, (0, 180, 255), rect, 4)
                    else:
                        pygame.draw.rect(tela, (80, 80, 80), rect, 2)
                    txt = f"{letras[idx]}) {alt}"
                    tela.blit(self.fonte_pequena.render(txt, True, (0, 0, 0)), (rect.x + 10, rect.y + 5))
                    y += 40

            # --------------- DISSERTATIVA -------------------
            elif tipo == "dissertativa":
                pygame.draw.rect(tela, (255, 255, 255), self.caixa_input, 2)
                linhas = self.resposta_usuario.split('\n')
                for idx2, linha in enumerate(linhas):
                    surface = self.fonte_pequena.render(linha, True, (255, 255, 255))
                    tela.blit(surface, (self.caixa_input.x + 5, self.caixa_input.y + 10 + idx2 * 25))
                # Cursor piscando ao final da última linha
                if self.input_ativo:
                    tempo = pygame.time.get_ticks()
                    if (tempo // 500) % 2 == 0:
                        cursor_x = self.caixa_input.x + 5 + self.fonte_pequena.size(linhas[-1])[0]
                        cursor_y = self.caixa_input.y + 10 + (len(linhas) - 1) * 25
                        pygame.draw.line(tela, (0, 255, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 20), 2)

            # --------------- DRAG & DROP (painel duplo) -------------------
            elif tipo == "dragdrop":
                if not self.blocos_disponiveis and not self.blocos_resposta:
                    resposta_certa = self.exercicio_selecionado.get_resposta_certa()
                    erradas = self.exercicio_selecionado.get_resposta_erradas()
                    blocos_certos = resposta_certa.split("|")
                    blocos_errados = erradas if erradas else []

                    blocos = blocos_certos + blocos_errados
                    random.shuffle(blocos)
                    self.blocos_disponiveis = [(bloco, None) for bloco in blocos]
                    self.blocos_resposta = []

                tela.blit(self.fonte_pequena.render("Blocos disponíveis:", True, (200,200,255)), (self.painel_x + 22, y))
                bloco_altura = 35
                for i, (bloco, _) in enumerate(self.blocos_disponiveis):
                    rect = pygame.Rect(self.painel_x + 22, y+30+i*bloco_altura, int(self.painel_w*0.48), bloco_altura-5)
                    pygame.draw.rect(tela, (40, 120, 255), rect)
                    pygame.draw.rect(tela, (30, 40, 90), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_disponiveis[i] = (bloco, rect)

                tela.blit(self.fonte_pequena.render("Sua resposta:", True, (120,255,120)), (self.painel_x + int(self.painel_w*0.55), y))
                for i, (bloco, _) in enumerate(self.blocos_resposta):
                    rect = pygame.Rect(self.painel_x + int(self.painel_w*0.55), y+30+i*bloco_altura, int(self.painel_w*0.43), bloco_altura-5)
                    pygame.draw.rect(tela, (80, 210, 80), rect)
                    pygame.draw.rect(tela, (30, 60, 30), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_resposta[i] = (bloco, rect)

            # --- Botão ENVIAR / CONTINUAR ---
            if not self.feedback_ativo:
                cor_btn = (0, 180, 80) if self.pode_enviar() else (80, 80, 80)
                label_btn = "ENVIAR"
            else:
                cor_btn = (0, 150, 200)
                label_btn = "CONTINUAR"
            pygame.draw.rect(tela, cor_btn, self.rect_enviar, border_radius=13)
            tela.blit(self.fonte_pequena.render(label_btn, True, (255, 255, 255)),
                      (self.rect_enviar.x + (self.rect_enviar.w-100)//2 + 12, self.rect_enviar.y + 9))

            # --- Feedback ---
            if self.resultado:
                cor = (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)
                tipo = self.exercicio_selecionado.get_tipo().lower()
                if tipo == "dissertativa":
                    tela.blit(self.fonte.render(self.resultado, True, cor),
                              (self.caixa_input.x, self.caixa_input.y + self.caixa_input.height + 15))
                elif tipo == "objetiva":
                    tela.blit(self.fonte.render(self.resultado, True, cor),
                              (self.painel_x + 22, y + 36))
                elif tipo == "dragdrop":
                    tela.blit(self.fonte.render(self.resultado, True, cor),
                              (self.painel_x + int(self.painel_w*0.55), y + 180))

        # --- Livro/ajuda ---
        tela.blit(self.img_ajuda, (self.rect_livro.x, self.rect_livro.y))


    def pode_enviar(self):
        if not self.exercicio_selecionado:
            return False
        tipo = self.exercicio_selecionado.get_tipo().lower()
        if tipo == "objetiva":
            return self.alternativa_selecionada is not None
        elif tipo == "dragdrop":
            resposta_certa = self.exercicio_selecionado.get_resposta_certa()
            blocos_certos = [b.strip() for b in resposta_certa.split("|")]
            return len(self.blocos_resposta) == len(blocos_certos)
        else:
            return len(self.resposta_usuario.strip()) > 0

    def tratar_eventos(self, eventos):
        for evento in eventos:
            # DRAG & DROP
            if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "dragdrop":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    for i, (bloco, rect) in enumerate(self.blocos_disponiveis):
                        if rect and rect.collidepoint(x, y) and not self.feedback_ativo:
                            self.blocos_resposta.append((bloco, None))
                            self.blocos_disponiveis.pop(i)
                            break
                    for i, (bloco, rect) in enumerate(self.blocos_resposta):
                        if rect and rect.collidepoint(x, y) and not self.feedback_ativo:
                            self.blocos_disponiveis.append((bloco, None))
                            self.blocos_resposta.pop(i)
                            break

            # RESTANTE DOS EVENTOS NORMAIS
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                if self.rect_livro.collidepoint(x, y):
                    if self.callback_rever_introducao:
                        self.callback_rever_introducao(self)
                    return

                # Selecionar alternativa
                if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "objetiva":
                    if hasattr(self, "rect_alternativas"):
                        for rect, alt, idx in self.rect_alternativas:
                            if rect.collidepoint(x, y) and not self.feedback_ativo:
                                self.alternativa_selecionada = idx
                # Input box
                if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "dissertativa":
                    if self.caixa_input.collidepoint(x, y) and not self.feedback_ativo:
                        self.input_ativo = True

                # Clique no botão ENVIAR / CONTINUAR
                if self.exercicio_selecionado and self.rect_enviar.collidepoint(x, y):
                    if not self.feedback_ativo and self.pode_enviar():
                        self.feedback_ativo = True
                        correta = self.verificar_resposta()
                        if correta:
                            self.acertos += 1
                        else:
                            self.erros += 1
                    elif self.feedback_ativo:
                        self.indice_atual += 1
                        if self.indice_atual < len(self.exercicios):
                            self.exercicio_selecionado = self.exercicios[self.indice_atual]
                            self.resposta_usuario = ""
                            self.resultado = ""
                            self.alternativa_selecionada = None
                            self.feedback_ativo = False
                            self.blocos_disponiveis = []
                            self.blocos_resposta = []
                        else:
                            self.finalizado = True

            if evento.type == pygame.KEYDOWN and self.input_ativo and not self.feedback_ativo:
                if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "dissertativa":
                    if evento.key == pygame.K_RETURN:
                        self.resposta_usuario += '\n'
                    elif evento.key == pygame.K_BACKSPACE:
                        self.resposta_usuario = self.resposta_usuario[:-1]
                    else:
                        if len(self.resposta_usuario) < 80 and evento.unicode.isprintable():
                            self.resposta_usuario += evento.unicode

    def verificar_resposta(self):
        if not self.exercicio_selecionado:
            return False
        tipo = self.exercicio_selecionado.get_tipo().lower()
        if tipo == "objetiva":
            alternativas = [self.exercicio_selecionado.get_resposta_certa()] + self.exercicio_selecionado.get_resposta_erradas()
            random.seed(self.exercicio_selecionado.get_id_exercicio())
            random.shuffle(alternativas)
            if self.alternativa_selecionada is not None:
                resposta = alternativas[self.alternativa_selecionada]
                correta = (resposta.strip().lower() == self.exercicio_selecionado.get_resposta_certa().strip().lower())
                self.resultado = "Resposta Correta!" if correta else "Resposta Incorreta!"
                return correta
        elif tipo == "dragdrop":
            resposta_user = "|".join([b[0] for b in self.blocos_resposta])
            resposta_certa = self.exercicio_selecionado.get_resposta_certa().replace("\r\n", "\n")
            correta = resposta_user.strip() == resposta_certa.strip()
            self.resultado = "Resposta Correta!" if correta else "Resposta Incorreta!"
            return correta
        else:
            correta = (self.resposta_usuario.strip().lower() == self.exercicio_selecionado.get_resposta_certa().strip().lower())
            self.resultado = "Resposta Correta!" if correta else "Resposta Incorreta!"
            return correta
        return False