import pygame
from Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
import random

class TelaExercicio:
    def __init__(self, largura, altura, total_fases=1, fases_concluidas=0,callback_rever_introducao=None):
        self.largura = largura
        self.altura = altura
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Consolas', 24)  # monoespaçada para código
        self.fonte_pequena = pygame.font.SysFont('Consolas', 18)
        self.exercicio_service = ExercicioServiceImpl()
        self.exercicios = []
        self.exercicio_selecionado = None
        self.input_ativo = False
        self.resposta_usuario = ""
        self.resultado = ""
        self.caixa_input = pygame.Rect(50, 400, 400, 80)
        self.rect_alternativas = []
        self.alternativa_selecionada = None
        self.rect_enviar = pygame.Rect(480, 400, 120, 40)
        self.feedback_ativo = False
        self.indice_atual = 0
        self.acertos = 0
        self.erros = 0
        self.finalizado = False
        self.rect_livro = pygame.Rect(self.largura - 60, 25, 40, 40)  # ajusta a posição conforme o layout
        self.callback_rever_introducao = callback_rever_introducao

        # Progresso geral (tópicos)
        self.total_fases = total_fases
        self.fases_concluidas = fases_concluidas

        # Para drag and drop
        self.blocos_disponiveis = []
        self.blocos_resposta = []
    #testando quebra de linha automatica
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
        tela.fill((30, 30, 30))

        # Barra de progresso geral (tópicos) - descendo para Y = 30
        if self.total_fases > 1:
            largura_total = 500
            progresso = self.fases_concluidas / self.total_fases
            pygame.draw.rect(tela, (120, 120, 120), (50, 15, largura_total, 8))
            pygame.draw.rect(tela, (0, 200, 255), (50, 15, int(largura_total * progresso), 8))
            tela.blit(self.fonte_pequena.render(f"Tópicos: {self.fases_concluidas}/{self.total_fases}", True, (255,255,255)), (560, 13))

        # Barra de progresso das questões - descendo para Y = 60
        if self.exercicios:
            total = len(self.exercicios)
            progresso = (self.indice_atual + 1) / total
            pygame.draw.rect(tela, (80, 80, 80), (50, 30, 500, 18))
            pygame.draw.rect(tela, (0, 200, 80), (50, 30, int(500*progresso), 18))
            tela.blit(self.fonte_pequena.render(f"Questão {self.indice_atual+1}/{total}", True, (255,255,255)), (560, 32))

        # Tela finalizada
        if self.finalizado:
            """
            msg = f"Quiz finalizado!"
            placar = f"Acertos: {self.acertos} | Erros: {self.erros} de {len(self.exercicios)}"
            tela.blit(self.fonte.render(msg, True, (0, 255, 255)), (50, 150))
            tela.blit(self.fonte_pequena.render(placar, True, (255, 255, 255)), (50, 200))
            """
            return

        

        if self.exercicio_selecionado:
            y = 60
            tela.blit(self.fonte.render("Enunciado:", True, (255, 255, 0)), (50, y))
            y += 30
            linhas_pergunta = self.quebrar_texto(self.exercicio_selecionado.get_pergunta(), self.fonte_pequena, 540)
            for linha in linhas_pergunta:
                tela.blit(self.fonte_pequena.render(linha, True, (255, 255, 255)), (50, y))
                y += 25  # ajuste o espaçamento se quiser

            tela.blit(self.fonte_pequena.render(f"Dica: {self.exercicio_selecionado.get_dicas()}", True, (180, 180, 0)), (50, y))
            y += 30

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
                    rect = pygame.Rect(60, y, 450, 30)
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
                # Inicializa blocos só na primeira vez desse exercício
                if not self.blocos_disponiveis and not self.blocos_resposta:
                    resposta_certa = self.exercicio_selecionado.get_resposta_certa()
                    erradas = self.exercicio_selecionado.get_resposta_erradas()
                    blocos_certos = resposta_certa.split("|")
                    blocos_errados = erradas if erradas else []

                    blocos = blocos_certos + blocos_errados
                    random.shuffle(blocos)
                    self.blocos_disponiveis = [(bloco, None) for bloco in blocos]
                    self.blocos_resposta = []

                # PAINEL ESQUERDA: blocos disponíveis
                tela.blit(self.fonte_pequena.render("Blocos disponíveis:", True, (200,200,255)), (60, y))
                bloco_altura = 35
                for i, (bloco, _) in enumerate(self.blocos_disponiveis):
                    rect = pygame.Rect(60, y+30+i*bloco_altura, 300, bloco_altura-5)
                    pygame.draw.rect(tela, (40, 120, 255), rect)
                    pygame.draw.rect(tela, (30, 40, 90), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_disponiveis[i] = (bloco, rect)

                # PAINEL DIREITA: montagem da resposta
                tela.blit(self.fonte_pequena.render("Sua resposta:", True, (120,255,120)), (400, y))
                for i, (bloco, _) in enumerate(self.blocos_resposta):
                    rect = pygame.Rect(400, y+30+i*bloco_altura, 300, bloco_altura-5)
                    pygame.draw.rect(tela, (80, 210, 80), rect)
                    pygame.draw.rect(tela, (30, 60, 30), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_resposta[i] = (bloco, rect)

            # ----------------- Botão ENVIAR / CONTINUAR -------------------
            if not self.feedback_ativo:
                cor_btn = (0, 180, 80) if self.pode_enviar() else (80, 80, 80)
                label_btn = "ENVIAR"
            else:
                cor_btn = (0, 150, 200)
                label_btn = "CONTINUAR"
            pygame.draw.rect(tela, cor_btn, self.rect_enviar)
            tela.blit(self.fonte_pequena.render(label_btn, True, (255, 255, 255)), (self.rect_enviar.x + 10, self.rect_enviar.y + 10))

            tipo = self.exercicio_selecionado.get_tipo().lower()
            # Feedback
            if self.resultado:
                cor = (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)
                tipo = self.exercicio_selecionado.get_tipo().lower()
                if tipo == "dissertativa":
                    # Abaixa mais o feedback para não ficar em cima do input
                    tela.blit(self.fonte.render(self.resultado, True, cor), (50, self.caixa_input.y + self.caixa_input.height + 15))
                elif tipo == "objetiva":
                    # Usa o y+220 como antes ou ajuste como preferir
                    tela.blit(self.fonte.render(self.resultado, True, cor), (50, y + 220))
                elif tipo == "dragdrop":
                    # Pode colocar bem embaixo dos blocos montados
                    tela.blit(self.fonte.render(self.resultado, True, cor), (400, y + 180))

        # No método desenhar (no final dele)
        pygame.draw.rect(tela, (220, 220, 180), self.rect_livro)
        # Pode desenhar um livro, ou apenas um texto:
        tela.blit(self.fonte_pequena.render("📖", True, (60, 60, 60)), (self.rect_livro.x + 8, self.rect_livro.y + 6))

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
            # ---------------- DRAG & DROP -------------------
            if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "dragdrop":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    # CLICOU EM BLOCO DISPONÍVEL? (esquerda)
                    for i, (bloco, rect) in enumerate(self.blocos_disponiveis):
                        if rect and rect.collidepoint(x, y) and not self.feedback_ativo:
                            self.blocos_resposta.append((bloco, None))
                            self.blocos_disponiveis.pop(i)
                            break
                    # CLICOU EM BLOCO DE RESPOSTA? (direita)
                    for i, (bloco, rect) in enumerate(self.blocos_resposta):
                        if rect and rect.collidepoint(x, y) and not self.feedback_ativo:
                            self.blocos_disponiveis.append((bloco, None))
                            self.blocos_resposta.pop(i)
                            break

            # ------------- RESTANTE DOS EVENTOS NORMAIS -------------
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                if self.rect_livro.collidepoint(x, y):
                    # Chame uma função de callback (ex: self.callback_rever_introducao())
                    if self.callback_rever_introducao:
                        self.callback_rever_introducao(self)  # passe a própria tela/exercicio
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
                    elif self.feedback_ativo:  # CONTINUAR
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
