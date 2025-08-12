import pygame
import os
import math
import random
import numpy as np
import sounddevice as sd


def jingle_parabens():
        fs = 44100
        notas = [
            (523, 0.18),  # C
            (587, 0.14),  # D
            (659, 0.14),  # E
            (698, 0.13),  # F
            (784, 0.2),   # G
            (880, 0.16),  # A
            (1046, 0.25), # C (alto, fim)
        ]
        ondas = []
        for freq, dur in notas:
            t = np.linspace(0, dur, int(fs*dur), False)
            env = np.exp(-2 * t)
            onda = 0.48 * np.sin(2 * np.pi * freq * t) * env
            # Harmônico suave para brilho
            onda += 0.09 * np.sin(2 * np.pi * freq * 2 * t) * env
            ondas.append(onda)
            ondas.append(np.zeros(int(fs*0.011)))
        som = np.concatenate(ondas)
        sd.play(som, fs)
        #sd.wait()

def erro_fail():
        fs = 44100
        t = np.linspace(0, 0.7, int(fs*0.7), False)
        # Tom descendo (de 700 pra 180 Hz)
        freq = np.linspace(700, 180, t.shape[0])
        env = np.exp(-2.2 * t)
        onda = 0.5 * np.sin(2 * np.pi * freq * t) * env
        # Um pequeno “blip” para reforçar o fail
        blip_t = np.linspace(0, 0.11, int(fs*0.11), False)
        blip = 0.3 * np.sin(2*np.pi*160*blip_t) * np.exp(-12*blip_t)
        som = np.concatenate([onda, blip])
        sd.play(som, fs)
        #sd.wait()

class TelaResultado:
    def __init__(self, largura, altura, acertos, erros, total_questoes, callback_avancar, callback_reiniciar=None, acertou_minimo=True, jogador=None):
        self.largura = largura
        self.altura = altura
        self.acertos = acertos
        self.erros = erros
        self.total_questoes = total_questoes
        self.callback_avancar = callback_avancar
        self.callback_reiniciar = callback_reiniciar
        self.acertou_minimo = acertou_minimo
        self.jogador = jogador
        self.nome_jogador = jogador.get_nome() if jogador else "Visitante"
        self.painel_visivel = True

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Consolas', 28, bold=True)
        self.fonte = pygame.font.SysFont('Consolas', 22)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 20)
        self.fonte_mini = pygame.font.SysFont('Consolas', 19, bold=True)

        #caminho_img = os.path.join("Assets", "TelaJogoIniciante.png")
        #self.bg = pygame.image.load(caminho_img).convert_alpha()
        #self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        self.rect_painel = pygame.Rect(
            int(largura * 0.25),
            int(altura * 0.13),
            int(largura * 0.54),
            int(altura * 0.66)
        )
        tam = 32
        espaco = 10
        self.rect_x = pygame.Rect(
            self.rect_painel.right - tam - espaco,
            self.rect_painel.y + espaco,
            tam, tam
        )
        btn_w, btn_h = 170, 52
        btn_espaco = 26
        btn_total = btn_w * 2 + btn_espaco
        painel_cx = self.rect_painel.x + (self.rect_painel.w - btn_total) // 2
        btn_y = self.rect_painel.bottom - btn_h - 28

        self.rect_avancar = pygame.Rect(painel_cx, btn_y, btn_w, btn_h)
        self.rect_reiniciar = pygame.Rect(painel_cx + btn_w + btn_espaco, btn_y, btn_w, btn_h)

        self.anim_frame = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.som_tocado = False

        self.codigo_chars = [
            "print", "for", "def", "→", "True", "[]", "{}", "λ", "if", "else", "class", "input", '"..."', "sum", "=", "=="
        ]
        self.max_chars = 18
        self._criar_chuva_codigo()

        # Mensagens bug/error para "não passou"
        self.bugs = [
            "Traceback (most recent call last):",
            "NameError: name 'vitoria' is not defined",
            "SyntaxError: try again!",
            "Bug: resposta inesperada!",
            "Exception: Keep going!",
            "IndentationError: precisa revisar o código!",
            "Erro: precisa acertar pelo menos 4 questões.",
        ]
        self.max_bugs = 5  # Quantidade de mensagens caindo
        self._criar_bugs_caindo()

    def _criar_chuva_codigo(self):
        self.chuva = []
        painel_x1 = self.rect_painel.x + 32
        painel_x2 = self.rect_painel.right - 32
        for i in range(self.max_chars):
            txt = self.codigo_chars[i % len(self.codigo_chars)]
            x = painel_x1 + int((painel_x2-painel_x1)*((i+1)/(self.max_chars+2)))
            y = self.rect_painel.y + 60 - i*26
            vy = 3.2 + 1.0*(i%3) + (i%5)*0.18
            cor = [(210,250,170),(160,210,255),(250,220,80),(255,120,190),(170,255,230)][i%5]
            fase = (i*10)%60
            self.chuva.append([x, y, vy, txt, cor, fase, False])


    
    def _criar_bugs_caindo(self):
        self.bugs_caindo = []
        margem_x = 44
        largura_disp = self.rect_painel.w - 2 * margem_x
        painel_x1 = self.rect_painel.x + margem_x + 10
        painel_x2 = self.rect_painel.x + self.rect_painel.w - margem_x - 10

        # Usaremos a largura do texto para garantir que não vai escapar
        for i in range(self.max_bugs):
            txt = self.bugs[i % len(self.bugs)]
            surf = self.fonte_mini.render(txt, True, (255,255,255))
            w = surf.get_width()
            # Calcula o x de modo que TODO o texto caiba dentro do painel
            min_x = painel_x1
            max_x = painel_x2 - w
            if max_x < min_x:  # Caso raro texto enorme
                max_x = min_x
            x = random.randint(int(min_x), int(max_x))
            y = self.rect_painel.y + 490 - i*48
            vy = 0.8 + 0.3*random.random()
            cor = (255, 80, 80) if i==0 else (200,200,70)
            self.bugs_caindo.append([x, y, vy, txt, cor, w, min_x, max_x])

    def quebrar_linha(self, texto, fonte, largura_max):
        linhas = []
        palavras = texto.split(' ')
        atual = ""
        for palavra in palavras:
            teste = f"{atual} {palavra}" if atual else palavra
            if fonte.size(teste)[0] <= largura_max:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        if atual:
            linhas.append(atual)
        return linhas

    def desenhar(self, tela):
        if not self.painel_visivel:
            return

        #tela.blit(self.bg, (0, 0))
        painel = self.rect_painel
        painel_surf = pygame.Surface((painel.w, painel.h), pygame.SRCALPHA)
        pygame.draw.rect(painel_surf, (18, 24, 32, 210), (0, 0, painel.w, painel.h), border_radius=16)
        tela.blit(painel_surf, (painel.x, painel.y))
        pygame.draw.rect(tela, (42, 103, 188), painel, 6, border_radius=16)

        header_h = 50
        header_rect = pygame.Rect(painel.x, painel.y, painel.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header_rect, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (painel.x, painel.y + header_h), (painel.x + painel.w, painel.y + header_h), 2)

        pygame.draw.circle(tela, (255, 100, 100), self.rect_x.center, self.rect_x.w // 2)
        x_mark = self.fonte_pequena.render("x", True, (40, 0, 0))
        tela.blit(
            x_mark,
            (
                self.rect_x.x + (self.rect_x.w - x_mark.get_width()) // 2,
                self.rect_x.y + (self.rect_x.h - x_mark.get_height()) // 2,
            )
        )

        # Título
        if self.acertou_minimo:
            titulo = "Parabéns!"
            cor_titulo = (80, 255, 120)
        else:
            titulo = "Você concluiu o tópico!"
            cor_titulo = (255, 230, 70)
        titulo_surface = self.fonte_titulo.render(titulo, True, cor_titulo)
        titulo_rect = titulo_surface.get_rect(center=(painel.centerx, painel.y + header_h // 2 + 2))
        tela.blit(titulo_surface, titulo_rect)

        # Conteúdo
        margem_x = 44
        margem_y = 42
        x = painel.x + margem_x
        y = painel.y + header_h + margem_y

        usuario_txt = f"Usuário logado: {self.nome_jogador}"
        usuario_surface = self.fonte_pequena.render(usuario_txt, True, (230, 230, 90))
        tela.blit(usuario_surface, (x, y))
        y += usuario_surface.get_height() + 6

        divisoria_y = y + 4
        pygame.draw.line(
            tela,
            (80, 120, 180),
            (x, divisoria_y),
            (painel.x + painel.w - margem_x, divisoria_y),
            2
        )
        y = divisoria_y + 14

        placar = f"Acertos: {self.acertos} / {self.total_questoes}"
        tela.blit(self.fonte.render(placar, True, (255,255,255)), (x, y))
        y += 36

        erros = f"Erros: {self.erros}"
        tela.blit(self.fonte.render(erros, True, (255, 80, 80)), (x, y))
        y += 38

        if self.acertou_minimo:
            msg = "Ótimo desempenho! Você pode avançar para o próximo tópico."
            cor_msg = (200,255,200)
        else:
            msg = "Não foi dessa vez. Você precisa acertar pelo menos 4 questões. Tente novamente para avançar!"
            cor_msg = (255,180,80)
        largura_max = self.rect_painel.w - 2 * margem_x
        linhas_msg = self.quebrar_linha(msg, self.fonte_pequena, largura_max)
        for linha in linhas_msg:
            tela.blit(self.fonte_pequena.render(linha, True, cor_msg), (x, y+8))
            y += 28

        # ---- CHUVA DE CÓDIGO ----
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_update > 50:
            self.anim_frame += 1
            self.tempo_ultimo_update = agora

        if self.acertou_minimo:
            painel_x1 = self.rect_painel.x + 32
            painel_x2 = self.rect_painel.right - 32
            painel_y_top = self.rect_painel.y + 44
            painel_y_base = self.rect_painel.y + 250

            for idx, item in enumerate(self.chuva):
                x, y, vy, txt, cor, fase, quicou = item
                if y < painel_y_base:
                    y += vy + math.sin(self.anim_frame*0.2 + fase)*0.8
                    vy += 0.17
                    if y > painel_y_base:
                        y = painel_y_base
                        vy = -vy * 0.29
                        item[6] = True
                else:
                    x += math.cos(self.anim_frame*0.11 + idx)*0.7
                    y += math.sin(self.anim_frame*0.13 + idx)*0.3
                if idx % 4 == 0:
                    w, h = 56, 28
                    pygame.draw.rect(tela, cor, (x, y, w, h), border_radius=8)
                    font_code = self.fonte_mini
                    label = font_code.render(txt, True, (40,44,80))
                    tela.blit(label, (x+8, y+3))
                else:
                    font_code = self.fonte_mini
                    label = font_code.render(txt, True, cor)
                    tela.blit(label, (x, y))
                item[0] = x
                item[1] = y
                item[2] = vy

        else:
            # --------- CHUVA DE BUGS/ERROS (APENAS ENTRE MSG E BOTÕES) ----------
            base_y = self.rect_painel.y + 265
            limite_y = self.rect_avancar.y - 38
            for idx, item in enumerate(self.bugs_caindo):
                x, y, vy, txt, cor, w, min_x, max_x = item
                y += vy
                if y > limite_y:
                    y = base_y - 32
                    # Calcula NOVO x, garantindo que NUNCA passe do painel (texto inteiro dentro!)
                    x = random.randint(int(min_x), int(max_x))
                surf = self.fonte_mini.render(txt, True, cor)
                tela.blit(surf, (x, y))
                item[1] = y
                item[0] = x

        # Botão AVANÇAR
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_avancar = self.rect_avancar.collidepoint(mouse_x, mouse_y)
        cor_btn = (0, 180, 80) if (self.acertou_minimo and hover_avancar) else (0, 150, 200) if hover_avancar else (90, 90, 90)
        cor_text = (255,255,255) if self.acertou_minimo else (180,180,180)
        pygame.draw.rect(tela, cor_btn, self.rect_avancar, border_radius=24)
        avancar_surface = self.fonte_pequena.render("AVANÇAR", True, cor_text)
        tela.blit(
            avancar_surface,
            (
                self.rect_avancar.x + (self.rect_avancar.w - avancar_surface.get_width()) // 2,
                self.rect_avancar.y + (self.rect_avancar.h - avancar_surface.get_height()) // 2
            )
        )

        # Botão TENTAR DE NOVO
        hover_reiniciar = self.rect_reiniciar.collidepoint(mouse_x, mouse_y)
        cor_btn2 = (100, 100, 250) if hover_reiniciar else (70, 70, 180)
        pygame.draw.rect(tela, cor_btn2, self.rect_reiniciar, border_radius=24)
        reiniciar_surface = self.fonte_pequena.render("TENTAR DE NOVO", True, (255,255,255))
        tela.blit(
            reiniciar_surface,
            (
                self.rect_reiniciar.x + (self.rect_reiniciar.w - reiniciar_surface.get_width()) // 2,
                self.rect_reiniciar.y + (self.rect_reiniciar.h - reiniciar_surface.get_height()) // 2
            )
        )

        # ============== SOM ===============
        if not self.som_tocado:
            if self.acertou_minimo:
                jingle_parabens()   # Chama o jingle de vitória real
            else:
                erro_fail()         # Chama o som de erro/“fail” real
            self.som_tocado = True

    def tratar_eventos(self, eventos):
        if not self.painel_visivel:
            return
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if hasattr(self, "rect_x") and self.rect_x.collidepoint(x, y):
                    self.painel_visivel = False
                    return

                if self.rect_avancar.collidepoint(x, y) and self.acertou_minimo:
                    if self.callback_avancar:
                        self.callback_avancar()
                if self.rect_reiniciar.collidepoint(x, y):
                    if self.callback_reiniciar:
                        self.callback_reiniciar()
