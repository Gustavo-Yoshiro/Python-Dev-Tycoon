import pygame
from Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
import random
import os
import requests

class TelaExercicio:
    def __init__(self, largura, altura, nome_topico, total_fases=1, fases_concluidas=0, callback_rever_introducao=None):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Consolas', 24)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 18)
        self.fonte_editor = pygame.font.SysFont('Consolas', 20)
        self.exercicio_service = ExercicioServiceImpl()
        self.exercicios = []
        self.exercicio_selecionado = None
        self.input_ativo = False
        self.resultado = ""
        self.feedback_ativo = False
        self.indice_atual = 0
        self.acertos = 0
        self.erros = 0
        self.finalizado = False
        self.callback_rever_introducao = callback_rever_introducao

        # Input editor moderno
        self.input_text = [""]
        self.cursor_pos = [0, 0]  # linha, coluna
        self.scroll_offset = 0
        self.linhas_visiveis = 5  # Quantidade de linhas visíveis no editor

        # Livro de ajuda
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

        # Input box para editor moderno (posição similar à antiga)
        self.editor_x = self.painel_x + 30
        self.editor_y = self.painel_y + self.painel_h - 150  # ajustado p/ não sobrepor botão
        self.editor_w = self.painel_w - 60
        self.editor_lh = 28  # altura da linha
        self.editor_h = self.linhas_visiveis * self.editor_lh + 20

        # Barra azul do topo (progresso dos tópicos e questões)
        self.barra_topo_x = self.painel_x
        self.barra_topo_y = self.painel_y - 82
        self.barra_topo_w = self.painel_w
        self.barra_topo_h = 16

        self.botao_w = 300
        self.botao_h = 100
        self.botao_x = self.painel_x + (self.painel_w - self.botao_w) // 2
        self.botao_y = self.painel_y + self.painel_h + 8
        self.rect_enviar = pygame.Rect(self.botao_x, self.botao_y, self.botao_w, self.botao_h)

        self.img_botao_enviar = pygame.image.load(os.path.join("Assets", "botao1.png")).convert_alpha()
        self.img_botao_enviar = pygame.transform.smoothscale(
            self.img_botao_enviar, (self.rect_enviar.width, self.rect_enviar.height)
        )

        self.rect_alternativas = []
        self.alternativa_selecionada = None

        self.total_fases = total_fases
        self.fases_concluidas = fases_concluidas

        self.blocos_disponiveis = []
        self.blocos_resposta = []

    @staticmethod
    def clamp(val, mini, maxi):
        return max(mini, min(val, maxi))

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
        self.input_text = [""]
        self.cursor_pos = [0, 0]
        self.resposta_usuario = ""
        self.resultado = ""
        self.alternativa_selecionada = None
        self.feedback_ativo = False
        self.blocos_disponiveis = []
        self.blocos_resposta = []
        self.scroll_offset = 0

    def get_codigo_usuario(self):
        # Junta todas as linhas do editor
        return "\n".join(self.input_text).rstrip()

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
            y = self.painel_y 
            # --- NOME DO TÓPICO ---
            nome_surface = self.fonte.render(self.nome_topico, True, (130, 220, 255))
            nome_rect = nome_surface.get_rect(centerx=self.painel_x + self.painel_w // 2, y=y)
            tela.blit(nome_surface, nome_rect)
            y = nome_rect.bottom + 8

            #tela.blit(self.fonte.render("Enunciado:", True, (255, 255, 0)), (self.painel_x + 22, y))
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

            # --------------- DISSERTATIVA (editor MODERNO) -------------------
            elif tipo == "dissertativa":
                # Editor "moderno" com scroll e linhas numeradas
                caixa = pygame.Rect(self.editor_x-20, self.editor_y-10, self.editor_w, self.editor_h)
                pygame.draw.rect(tela, (52, 56, 64), caixa)
                pygame.draw.rect(tela, (70, 120, 200), caixa, 2)
                total_linhas = len(self.input_text)
                linha, coluna = self.cursor_pos

                # Mantém cursor visível apenas se sair do range do scroll!
                if linha < self.scroll_offset:
                    self.scroll_offset = linha
                elif linha >= self.scroll_offset + self.linhas_visiveis:
                    self.scroll_offset = linha - self.linhas_visiveis + 1
                self.scroll_offset = self.clamp(self.scroll_offset, 0, max(0, total_linhas - self.linhas_visiveis))

                # Renderiza as linhas visíveis
                for idx in range(self.scroll_offset, min(self.scroll_offset + self.linhas_visiveis, total_linhas)):
                    y_linha = self.editor_y + (idx - self.scroll_offset) * self.editor_lh
                    linha_num_surface = self.fonte_editor.render(str(idx+1).rjust(2), True, (90, 160, 220))
                    tela.blit(linha_num_surface, (self.editor_x-35, y_linha))
                    # Highlight linha do cursor
                    if idx == linha:
                        pygame.draw.rect(tela, (38, 54, 92), (self.editor_x-5, y_linha, self.editor_w-35, self.editor_lh))
                    texto = self.fonte_editor.render(self.input_text[idx], True, (255,255,255))
                    tela.blit(texto, (self.editor_x, y_linha))

                # Barra de rolagem visual
                if total_linhas > self.linhas_visiveis:
                    barra_h = int(caixa.height * (self.linhas_visiveis/total_linhas))
                    barra_y = self.editor_y-10 + int(caixa.height * (self.scroll_offset/total_linhas))
                    pygame.draw.rect(tela, (80, 120, 200), (caixa.right+6, barra_y, 8, barra_h), border_radius=5)

                # Cursor piscando
                if self.input_ativo and self.scroll_offset <= linha < self.scroll_offset+self.linhas_visiveis:
                    tempo = pygame.time.get_ticks()
                    if (tempo // 500) % 2 == 0:
                        y_cursor = self.editor_y + (linha - self.scroll_offset) * self.editor_lh
                        texto_ate_cursor = self.fonte_editor.render(self.input_text[linha][:coluna], True, (255,255,255))
                        cursor_x = self.editor_x + texto_ate_cursor.get_width()
                        pygame.draw.line(tela, (0,255,0), (cursor_x, y_cursor+4), (cursor_x, y_cursor+self.editor_lh-6), 2)


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
        tela.blit(self.img_botao_enviar, (self.rect_enviar.x, self.rect_enviar.y))
        label_surface = self.fonte_pequena.render(label_btn, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=self.rect_enviar.center)
        tela.blit(label_surface, label_rect)

        # --- Feedback padronizado abaixo do botão ENVIAR/CONTINUAR ---
        if self.resultado:
            cor = (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)
            feedback_x = self.rect_enviar.right + 30
            feedback_y = self.rect_enviar.y + self.rect_enviar.height // 2 - self.fonte.get_height() // 2 - 15
            tela.blit(self.fonte.render(self.resultado, True, cor), (feedback_x, feedback_y))

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
            return len(self.get_codigo_usuario().strip()) > 0

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

            # --- EVENTOS DO EDITOR MODERNO ---
            tipo = self.exercicio_selecionado.get_tipo().lower() if self.exercicio_selecionado else ""
            if tipo == "dissertativa":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    editor_rect = pygame.Rect(self.editor_x-20, self.editor_y-10, self.editor_w, self.editor_h)
                    if editor_rect.collidepoint(x, y) and not self.feedback_ativo:
                        self.input_ativo = True
                        # Descobre a linha clicada
                        linha_clicada = (y - self.editor_y) // self.editor_lh + self.scroll_offset
                        if 0 <= linha_clicada < len(self.input_text):
                            # Descobre coluna aproximada
                            texto = self.input_text[linha_clicada]
                            col = 0
                            for i in range(len(texto)+1):
                                largura = self.fonte_editor.size(texto[:i])[0]
                                if self.editor_x + largura > x:
                                    break
                                col = i
                            self.cursor_pos = [linha_clicada, col]
                if evento.type == pygame.MOUSEWHEEL and self.input_ativo:
                    self.scroll_offset -= evento.y
                    self.scroll_offset = self.clamp(self.scroll_offset, 0, max(0, len(self.input_text) - self.linhas_visiveis))

                if evento.type == pygame.KEYDOWN and self.input_ativo and not self.feedback_ativo:
                    linha, coluna = self.cursor_pos
                    if evento.key == pygame.K_RETURN:
                        self.input_text.insert(linha + 1, self.input_text[linha][coluna:])
                        self.input_text[linha] = self.input_text[linha][:coluna]
                        linha += 1
                        coluna = 0
                    elif evento.key == pygame.K_BACKSPACE:
                        if coluna > 0:
                            self.input_text[linha] = self.input_text[linha][:coluna-1] + self.input_text[linha][coluna:]
                            coluna -= 1
                        elif linha > 0:
                            coluna = len(self.input_text[linha-1])
                            self.input_text[linha-1] += self.input_text[linha]
                            self.input_text.pop(linha)
                            linha -= 1
                    elif evento.key == pygame.K_TAB:
                        self.input_text[linha] = self.input_text[linha][:coluna] + "    " + self.input_text[linha][coluna:]
                        coluna += 4
                    elif evento.key == pygame.K_LEFT:
                        if coluna > 0:
                            coluna -= 1
                        elif linha > 0:
                            linha -= 1
                            coluna = len(self.input_text[linha])
                    elif evento.key == pygame.K_RIGHT:
                        if coluna < len(self.input_text[linha]):
                            coluna += 1
                        elif linha < len(self.input_text) - 1:
                            linha += 1
                            coluna = 0
                    elif evento.key == pygame.K_UP:
                        if linha > 0:
                            linha -= 1
                            coluna = min(coluna, len(self.input_text[linha]))
                    elif evento.key == pygame.K_DOWN:
                        if linha < len(self.input_text)-1:
                            linha += 1
                            coluna = min(coluna, len(self.input_text[linha]))
                    else:
                        if evento.unicode.isprintable():
                            self.input_text[linha] = self.input_text[linha][:coluna] + evento.unicode + self.input_text[linha][coluna:]
                            coluna += 1
                    linha = self.clamp(linha, 0, len(self.input_text)-1)
                    coluna = self.clamp(coluna, 0, len(self.input_text[linha]))
                    self.cursor_pos = [linha, coluna]
                    # GARANTE QUE O CURSOR SEMPRE VISÍVEL APÓS TECLA
                    if self.cursor_pos[0] < self.scroll_offset:
                        self.scroll_offset = self.cursor_pos[0]
                    elif self.cursor_pos[0] >= self.scroll_offset + self.linhas_visiveis:
                        self.scroll_offset = self.cursor_pos[0] - self.linhas_visiveis + 1
                    self.scroll_offset = self.clamp(self.scroll_offset, 0, max(0, len(self.input_text) - self.linhas_visiveis))


            # RESTANTE DOS EVENTOS NORMAIS (objetiva, dragdrop, etc)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_livro.collidepoint(x, y):
                    if self.callback_rever_introducao:
                        self.callback_rever_introducao(self)
                    return
                if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "objetiva":
                    if hasattr(self, "rect_alternativas"):
                        for rect, alt, idx in self.rect_alternativas:
                            if rect.collidepoint(x, y) and not self.feedback_ativo:
                                self.alternativa_selecionada = idx
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
                            self.input_text = [""]
                            self.cursor_pos = [0, 0]
                            self.resultado = ""
                            self.alternativa_selecionada = None
                            self.feedback_ativo = False
                            self.blocos_disponiveis = []
                            self.blocos_resposta = []
                            self.scroll_offset = 0
                        else:
                            self.finalizado = True

    @staticmethod
    def executar_codigo_piston(codigo, versao="3.10.0"):
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {
            "language": "python",
            "version": versao,
            "files": [{"name": "main.py", "content": codigo}],
            "stdin": "",
            "args": [],
        }
        try:
            resp = requests.post(url, json=payload, timeout=8)
            resp.raise_for_status()
            saida = resp.json()
            if 'output' in saida:
                return saida['output'].strip()
            elif 'run' in saida and 'stdout' in saida['run']:
                return saida['run']['stdout'].strip()
            elif 'stdout' in saida:
                return saida['stdout'].strip()
            else:
                return "[SEM OUTPUT]"
        except Exception as e:
            return f"Erro: {e}"

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
        elif tipo == "dissertativa":
            codigo_usuario = self.get_codigo_usuario()
            saida_usuario = self.executar_codigo_piston(codigo_usuario)
            resposta_certa = self.exercicio_selecionado.get_resposta_certa().strip()
            if saida_usuario.strip() == resposta_certa:
                self.resultado = "Resposta Correta!"
                return True
            else:
                self.resultado = f"Resposta Incorreta!\nSaída: {saida_usuario}"
                return False
        return False
