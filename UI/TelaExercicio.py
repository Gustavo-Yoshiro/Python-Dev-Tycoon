import pygame
from Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
import random
import os
import requests

class TelaExercicio:
    def __init__(self, largura, altura, nome_topico, total_fases=1, fases_concluidas=0, callback_rever_introducao=None, jogador=None, id_fase=None):
        # Básicos
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.total_fases = total_fases
        self.fases_concluidas = fases_concluidas
        self.callback_rever_introducao = callback_rever_introducao
        self.jogador = jogador
        self.id_fase = id_fase
        self.nome_jogador = jogador.get_nome() if jogador else ""

        self.dragging = False
        self.drag_offset = (0, 0)

        #self.centralizar_prompt()
        
        # Serviços
        self.exercicio_service = ExercicioServiceImpl()
        self.progresso_service = ProgressoFaseServiceImpl()

        # Carrega exercícios e progresso do jogador nesta fase
        self.exercicios, progresso = self.exercicio_service.carregar_exercicios(self.id_fase, self.jogador)


        # Recupera progresso salvo ou inicia do zero
        if progresso:
            self.indice_atual = progresso.get_indice_exercicio()
            self.acertos = progresso.get_acertos()
            self.erros = progresso.get_erros()
        else:
            self.indice_atual = 0
            self.acertos = 0
            self.erros = 0

        # FINALIZADO se já respondeu todos!
        if self.exercicios and self.indice_atual >= len(self.exercicios):
            self.finalizado = True
            self.exercicio_selecionado = None
        else:
            self.finalizado = False
            self.exercicio_selecionado = self.exercicios[self.indice_atual] if self.exercicios else None
        
        # Estado da interface/editor
        self.scroll_offset_x = 0
        self.input_ativo = False
        self.input_text = [""]
        self.cursor_pos = [0, 0]
        self.scroll_offset = 0
        self.linhas_visiveis = 5
        self.resultado = ""
        self.feedback_ativo = False
        self.resposta_usuario = ""
        self.alternativa_selecionada = None
        self.blocos_disponiveis = []
        self.blocos_resposta = []
        
        # Gráficos/UI
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Consolas', 24)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 18)
        self.fonte_editor = pygame.font.SysFont('Consolas', 20)
        self.editor_lh = self.fonte_editor.get_height()  # <-- Só aqui!
        
        
        self.rect_livro = pygame.Rect(int(largura * 0.85), int(altura * 0.12), 48, 48)
        self.img_ajuda = pygame.image.load(os.path.join("Assets", "ajuda.png")).convert_alpha()
        self.img_ajuda = pygame.transform.smoothscale(self.img_ajuda, (self.rect_livro.width, self.rect_livro.height))
        
        caminho_img = os.path.join("Assets", "TelaJogoIniciante.png")
        self.bg = pygame.image.load(caminho_img).convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        # Prompt
        self.prompt_visivel = True
        self.prompt_msg = ""
        # Centralizado e responsivo
        self.rect_prompt = pygame.Rect(
            int(largura * 0.25),
            int(altura * 0.13),
            int(largura * 0.54),
            int(altura * 0.66)
        )
        self.rect_q = None
        self.rect_x = None
        self.rect_btn = None
        self.rect_alternativas = []

        self.mouse_down_ao_entrar = pygame.mouse.get_pressed()[0]

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

    def centralizar_prompt(self):
        self.rect_prompt.x = int(self.largura * 0.25)
        self.rect_prompt.y = int(self.altura * 0.13)

    def get_codigo_usuario(self):
        return "\n".join(self.input_text).rstrip()

    def desenhar(self, tela):
        #print("ANTES DE DESENHAR:", self.rect_prompt.x, self.rect_prompt.y)
        tela.blit(self.bg, (0, 0))
        #tela.blit(self.fonte_pequena.render(f"Usuário: {self.nome_jogador}", True, (255, 220, 120)), (20, 20))

        if not self.prompt_visivel:
            # Exemplo: Prompt fechado, pode exibir outra coisa ou só o fundo
            #tela.blit(self.fonte.render("Prompt fechado!", True, (220,80,80)), (self.largura//2-160, self.altura//2))
            return

        prompt = self.rect_prompt
        prompt_surf = pygame.Surface((prompt.w, prompt.h), pygame.SRCALPHA)
        pygame.draw.rect(prompt_surf, (18, 24, 32, 210), (0, 0, prompt.w, prompt.h), border_radius=16)
        tela.blit(prompt_surf, (prompt.x, prompt.y))
        pygame.draw.rect(tela, (42, 103, 188), prompt, 6, border_radius=16)

        # HEADER
        header_h = 50
        header_rect = pygame.Rect(prompt.x, prompt.y, prompt.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header_rect, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (prompt.x, prompt.y+header_h), (prompt.x+prompt.w, prompt.y+header_h), 2)
        # Título
        txt = self.fonte.render(self.nome_topico, True, (230, 240, 255))
        tela.blit(txt, (prompt.x+24, prompt.y+10))
        # ? e X
        self.rect_q = pygame.Rect(prompt.right-90, prompt.y+10, 30, 30)
        self.rect_x = pygame.Rect(prompt.right-45, prompt.y+10, 30, 30)
        pygame.draw.circle(tela, (110, 190, 255), self.rect_q.center, 15)
        q_mark = self.fonte_pequena.render("?", True, (28, 44, 80))
        tela.blit(q_mark, (self.rect_q.x+8, self.rect_q.y+3))
        pygame.draw.circle(tela, (255, 100, 100), self.rect_x.center, 15)
        x_mark = self.fonte_pequena.render("x", True, (40, 0, 0))
        tela.blit(x_mark, (self.rect_x.x+9, self.rect_x.y+4))
        # Tooltip
        mx, my = pygame.mouse.get_pos()
        if self.rect_q.collidepoint(mx, my):
            texto_ajuda = "Clique para ver a introdução do tópico novamente."
            largura_balao = self.fonte_pequena.size(texto_ajuda)[0] + 32
            altura_balao = 40
            surf = pygame.Surface((largura_balao, altura_balao), pygame.SRCALPHA)
            pygame.draw.rect(surf, (40,60,110, 220), (0,0,largura_balao,altura_balao), border_radius=12)
            pygame.draw.rect(surf, (110,190,255), (0,0,largura_balao,altura_balao), 2, border_radius=12)
            tip = self.fonte_pequena.render(texto_ajuda, True, (255,255,255))
            surf.blit(tip, (16,10))
            tela.blit(surf, (mx-largura_balao//2, my-altura_balao-8))
        elif self.rect_x.collidepoint(mx, my):
            texto_ajuda = "Não se preocupe, seu progresso é salvo automaticamente."
            largura_balao = self.fonte_pequena.size(texto_ajuda)[0] + 32
            altura_balao = 40
            surf = pygame.Surface((largura_balao, altura_balao), pygame.SRCALPHA)
            pygame.draw.rect(surf, (40,60,110, 220), (0,0,largura_balao,altura_balao), border_radius=12)
            pygame.draw.rect(surf, (110,190,255), (0,0,largura_balao,altura_balao), 2, border_radius=12)
            tip = self.fonte_pequena.render(texto_ajuda, True, (255,255,255))
            surf.blit(tip, (16,10))
            tela.blit(surf, (mx-largura_balao//2, my-altura_balao-8))


        # -------- Barras de Progresso --------
        BAR_HEIGHT = 28
        bar1_rect = pygame.Rect(prompt.x+40, prompt.y+header_h+18, prompt.w-80, BAR_HEIGHT)
        bar2_rect = pygame.Rect(prompt.x+40, prompt.y+header_h+60, prompt.w-80, BAR_HEIGHT)
        barra1_perc = self.fases_concluidas / self.total_fases if self.total_fases > 0 else 0
        barra2_perc = (self.indice_atual+1)/len(self.exercicios) if self.exercicios else 0

        # Fundo das barras
        pygame.draw.rect(tela, (46, 48, 80), bar1_rect, border_radius=12)
        pygame.draw.rect(tela, (46, 48, 80), bar2_rect, border_radius=12)
        # Barras coloridas: laranja/amarelo + ciano/verde-água
        pygame.draw.rect(tela, (255, 204, 72), (bar1_rect.x, bar1_rect.y, int(bar1_rect.w*barra1_perc), bar1_rect.h), border_radius=12)
        pygame.draw.rect(tela, (84, 240, 200), (bar2_rect.x, bar2_rect.y, int(bar2_rect.w*barra2_perc), bar2_rect.h), border_radius=12)

        # Textos centralizados nas barras
        t1 = self.fonte_pequena.render(f"Tópicos: {self.fases_concluidas}/{self.total_fases}", True, (60, 60, 90))
        t2 = self.fonte_pequena.render(f"Questão {self.indice_atual+1}/{len(self.exercicios) if self.exercicios else 1}", True, (40, 130, 110))
        t1_y = bar1_rect.y + (BAR_HEIGHT - t1.get_height()) // 2
        t2_y = bar2_rect.y + (BAR_HEIGHT - t2.get_height()) // 2
        tela.blit(t1, (bar1_rect.x+8, t1_y))
        tela.blit(t2, (bar2_rect.x+8, t2_y))


        # --- Pergunta
        y = bar2_rect.bottom + 24
        if self.finalizado:
            msg = f"Quiz finalizado!"
            placar = f"Acertos: {self.acertos} | Erros: {self.erros} de {len(self.exercicios)}"
            tela.blit(self.fonte.render(msg, True, (0, 255, 255)), (prompt.x + 30, y+40))
            tela.blit(self.fonte_pequena.render(placar, True, (255, 255, 255)), (prompt.x + 30, y+100))
            return

        if self.exercicio_selecionado:
            # Pergunta/enunciado
            linhas_pergunta = self.quebrar_texto(self.exercicio_selecionado.get_pergunta(), self.fonte_pequena, prompt.w - 80)
            for linha in linhas_pergunta:
                tela.blit(self.fonte_pequena.render(linha, True, (255, 255, 255)), (prompt.x + 40, y))
                y += 27
            # Dica
            tela.blit(self.fonte_pequena.render(f"Dica: {self.exercicio_selecionado.get_dicas()}", True, (180, 180, 0)), (prompt.x + 40, y))
            y += 34

            tipo = self.exercicio_selecionado.get_tipo().lower()
            # ---------- OBJETIVA ----------
            if tipo == "objetiva":
                erradas = self.exercicio_selecionado.get_resposta_erradas()[:3] if self.exercicio_selecionado.get_resposta_erradas() else []
                alternativas = [self.exercicio_selecionado.get_resposta_certa()] + erradas
                random.seed(self.exercicio_selecionado.get_id_exercicio())
                random.shuffle(alternativas)
                letras = ['A', 'B', 'C', 'D'][:len(alternativas)]
                self.rect_alternativas = []
                for idx, alt in enumerate(alternativas):
                    rect = pygame.Rect(prompt.x + 40, y, prompt.w - 80, 34)
                    self.rect_alternativas.append((rect, alt, idx))
                    cor = (200, 200, 50)
                    pygame.draw.rect(tela, cor, rect, 0)
                    if self.alternativa_selecionada == idx:
                        pygame.draw.rect(tela, (0, 180, 255), rect, 4)
                    else:
                        pygame.draw.rect(tela, (80, 80, 80), rect, 2)
                    txt = f"{letras[idx]}) {alt}"
                    tela.blit(self.fonte_pequena.render(txt, True, (0, 0, 0)), (rect.x + 10, rect.y + 6))
                    y += 42
            # ---------- DISSERTATIVA ----------
            elif tipo == "dissertativa":
                # FIXE o número de linhas visíveis (não varie conforme input_text)
                linhas = self.linhas_visiveis
                editor_h = linhas * self.fonte_editor.get_height() + 16
                caixa = pygame.Rect(prompt.x+40, y, prompt.w-80, editor_h)
                pygame.draw.rect(tela, (52, 56, 64), caixa)
                pygame.draw.rect(tela, (70, 120, 200), caixa, 2)
                total_linhas = len(self.input_text)
                linha, coluna = self.cursor_pos
                largura_caixa = caixa.w - 30
                # Renderize só as linhas do scroll!
                for idx in range(self.scroll_offset, min(self.scroll_offset + linhas, total_linhas)):
                    y_linha = caixa.y + (idx - self.scroll_offset) * self.editor_lh + 6
                    linha_num_surface = self.fonte_editor.render(str(idx+1).rjust(2), True, (90, 160, 220))
                    tela.blit(linha_num_surface, (caixa.x-26, y_linha))
                    if idx == linha:
                        pygame.draw.rect(tela, (38, 54, 92), (caixa.x+6, y_linha-2, largura_caixa, self.editor_lh))
                    linha_texto = self.input_text[idx]
                    scroll_x = self.scroll_offset_x if idx == linha else 0
                    texto_visivel = linha_texto[scroll_x:]
                    while self.fonte_editor.size(texto_visivel)[0] > largura_caixa and len(texto_visivel) > 0:
                        texto_visivel = texto_visivel[:-1]
                    texto_surface = self.fonte_editor.render(texto_visivel, True, (255,255,255))
                    tela.blit(texto_surface, (caixa.x+18, y_linha))
                # Cursor piscando igual antes
                if self.input_ativo and self.scroll_offset <= linha < self.scroll_offset+linhas:
                    tempo = pygame.time.get_ticks()
                    if (tempo // 500) % 2 == 0:
                        y_cursor = caixa.y + (linha - self.scroll_offset) * self.editor_lh + 6
                        texto_ate_cursor = self.input_text[linha][self.scroll_offset_x:coluna]
                        cursor_x = caixa.x+18 + self.fonte_editor.size(texto_ate_cursor)[0]
                        pygame.draw.line(tela, (0,255,0), (cursor_x, y_cursor+4), (cursor_x, y_cursor+self.editor_lh-6), 2)
                y = caixa.bottom + 10

            # ---------- DRAGDROP ----------
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
                tela.blit(self.fonte_pequena.render("Blocos disponíveis:", True, (200,200,255)), (prompt.x + 40, y))
                bloco_altura = 35
                for i, (bloco, _) in enumerate(self.blocos_disponiveis):
                    rect = pygame.Rect(prompt.x + 40, y+30+i*bloco_altura, int(prompt.w*0.48), bloco_altura-5)
                    pygame.draw.rect(tela, (40, 120, 255), rect)
                    pygame.draw.rect(tela, (30, 40, 90), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_disponiveis[i] = (bloco, rect)
                tela.blit(self.fonte_pequena.render("Sua resposta:", True, (120,255,120)), (prompt.x + int(prompt.w*0.55), y))
                for i, (bloco, _) in enumerate(self.blocos_resposta):
                    rect = pygame.Rect(prompt.x + int(prompt.w*0.55), y+30+i*bloco_altura, int(prompt.w*0.43), bloco_altura-5)
                    pygame.draw.rect(tela, (80, 210, 80), rect)
                    pygame.draw.rect(tela, (30, 60, 30), rect, 2)
                    tela.blit(self.fonte_pequena.render(bloco, True, (255,255,255)), (rect.x+5, rect.y+7))
                    self.blocos_resposta[i] = (bloco, rect)
                y += 30 + max(len(self.blocos_disponiveis), len(self.blocos_resposta)) * bloco_altura

            # --- Botão ENVIAR/CONTINUAR arredondado
            btn_w, btn_h = 180, 52
            btn_x = prompt.x + (prompt.w-btn_w)//2
            btn_y = prompt.bottom - btn_h - 18
            self.rect_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            cor_btn = (0, 180, 80) if not self.feedback_ativo and self.pode_enviar() else (0, 150, 200) if self.feedback_ativo else (80, 80, 80)
            pygame.draw.rect(tela, cor_btn, self.rect_btn, border_radius=24)
            label_btn = "ENVIAR" if not self.feedback_ativo else "CONTINUAR"
            label_surface = self.fonte_pequena.render(label_btn, True, (255,255,255))
            label_rect = label_surface.get_rect(center=self.rect_btn.center)
            tela.blit(label_surface, label_rect)

            # --- Feedback padronizado abaixo do botão
            if self.resultado:
                cor = (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)
                feedback_x = self.rect_btn.right + 30
                feedback_y = self.rect_btn.y + self.rect_btn.height // 2 - self.fonte.get_height() // 2 - 8
                tela.blit(self.fonte.render(self.resultado, True, cor), (feedback_x, feedback_y))

        # Livro/ajuda
        #tela.blit(self.img_ajuda, (self.rect_livro.x, self.rect_livro.y))

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

    def ajustar_scroll_horizontal(self):
        linha, coluna = self.cursor_pos
        texto = self.input_text[linha]
        fonte = self.fonte_editor
        prompt = self.rect_prompt
        largura_caixa = prompt.w - 80 - 30
        texto_visivel = texto[self.scroll_offset_x:coluna]
        px_cursor = fonte.size(texto_visivel)[0]
        while px_cursor > largura_caixa and self.scroll_offset_x < len(texto):
            self.scroll_offset_x += 1
            texto_visivel = texto[self.scroll_offset_x:coluna]
            px_cursor = fonte.size(texto_visivel)[0]
        while px_cursor < 0 and self.scroll_offset_x > 0:
            self.scroll_offset_x -= 1
            texto_visivel = texto[self.scroll_offset_x:coluna]
            px_cursor = fonte.size(texto_visivel)[0]


    def tratar_eventos(self, eventos):
        """
        if hasattr(self, 'mouse_down_ao_entrar') and self.mouse_down_ao_entrar:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down_ao_entrar = False  # Libera eventos normalmente depois de soltar
            return
        """

        for evento in eventos:
            # Início do drag
            if self.prompt_visivel and evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo
                    # Detecta clique na barra do topo do prompt
                    header_h = 50  # igual ao usado no desenhar
                    prompt = self.rect_prompt
                    header_rect = pygame.Rect(prompt.x, prompt.y, prompt.w, header_h)
                    if header_rect.collidepoint(evento.pos):
                        self.dragging = True
                        mx, my = evento.pos
                        self.drag_offset = (mx - prompt.x, my - prompt.y)
            # Durante o drag
            elif evento.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mx, my = evento.pos
                    dx, dy = self.drag_offset
                    self.rect_prompt.x = mx - dx
                    self.rect_prompt.y = my - dy
            # Fim do drag
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and self.dragging:
                    self.dragging = False

            # Detectar X no prompt
            if self.prompt_visivel and hasattr(self, "rect_x") and evento.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_x and self.rect_x.collidepoint(evento.pos):
                    self.prompt_visivel = False
                    return

            # Resto igual ao seu código original
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
            tipo = self.exercicio_selecionado.get_tipo().lower() if self.exercicio_selecionado else ""
            if tipo == "dissertativa":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    # Editor dentro do prompt
                    caixa = pygame.Rect(self.rect_prompt.x+40, self.rect_prompt.y+180, self.rect_prompt.w-80, max(len(self.input_text),5)*self.fonte_editor.get_height()+16)
                    if caixa.collidepoint(x, y) and not self.feedback_ativo:
                        self.input_ativo = True
                        linha_clicada = (y - caixa.y) // self.fonte_editor.get_height() + self.scroll_offset
                        if 0 <= linha_clicada < len(self.input_text):
                            texto = self.input_text[linha_clicada]
                            col = 0
                            for i in range(len(texto)+1):
                                largura = self.fonte_editor.size(texto[:i])[0]
                                if caixa.x+18 + largura > x:
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
                        self.scroll_offset_x = 0
                    elif evento.key == pygame.K_BACKSPACE:
                        if coluna > 0:
                            self.input_text[linha] = self.input_text[linha][:coluna-1] + self.input_text[linha][coluna:]
                            coluna -= 1
                        elif linha > 0:
                            coluna = len(self.input_text[linha-1])
                            self.input_text[linha-1] += self.input_text[linha]
                            self.input_text.pop(linha)
                            linha -= 1
                            self.scroll_offset_x = 0
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
                            self.scroll_offset_x = 0
                    elif evento.key == pygame.K_DOWN:
                        if linha < len(self.input_text)-1:
                            linha += 1
                            coluna = min(coluna, len(self.input_text[linha]))
                            self.scroll_offset_x = 0
                    else:
                        if evento.unicode.isprintable():
                            self.input_text[linha] = self.input_text[linha][:coluna] + evento.unicode + self.input_text[linha][coluna:]
                            coluna += 1
                    linha = self.clamp(linha, 0, len(self.input_text)-1)
                    coluna = self.clamp(coluna, 0, len(self.input_text[linha]))
                    self.cursor_pos = [linha, coluna]
                    self.ajustar_scroll_horizontal()
                    if self.cursor_pos[0] < self.scroll_offset:
                        self.scroll_offset = self.cursor_pos[0]
                    elif self.cursor_pos[0] >= self.scroll_offset + self.linhas_visiveis:
                        self.scroll_offset = self.cursor_pos[0] - self.linhas_visiveis + 1
                    self.scroll_offset = self.clamp(self.scroll_offset, 0, max(0, len(self.input_text) - self.linhas_visiveis))

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Novo: "?" chama introdução
                if self.rect_q and self.rect_q.collidepoint(x, y):
                    if self.callback_rever_introducao:
                        self.callback_rever_introducao(self)
                    
                    return
                if self.exercicio_selecionado and self.exercicio_selecionado.get_tipo().lower() == "objetiva":
                    if hasattr(self, "rect_alternativas"):
                        for rect, alt, idx in self.rect_alternativas:
                            if rect.collidepoint(x, y) and not self.feedback_ativo:
                                self.alternativa_selecionada = idx
                if self.exercicio_selecionado and self.rect_btn and self.rect_btn.collidepoint(x, y):
                    if not self.feedback_ativo and self.pode_enviar():
                        self.feedback_ativo = True
                        correta = self.verificar_resposta()
                        if correta:
                            self.acertos += 1
                        else:
                            self.erros += 1
                    elif self.feedback_ativo:
                        self.indice_atual += 1
                        self.progresso_service.salvar_ou_atualizar_progresso(
                            jogador=self.jogador,
                            id_fase=self.id_fase,
                            indice_exercicio=self.indice_atual,
                            acertos=self.acertos,
                            erros=self.erros,
                            resposta_parcial=""
                        )
                        if self.indice_atual < len(self.exercicios):
                            self.exercicio_selecionado = self.exercicios[self.indice_atual]
                            self.feedback_ativo = False
                            self.resultado = ""
                            self.alternativa_selecionada = None
                            self.input_text = [""]
                            self.cursor_pos = [0, 0]
                            self.scroll_offset = 0
                            self.blocos_disponiveis = []
                            self.blocos_resposta = []
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