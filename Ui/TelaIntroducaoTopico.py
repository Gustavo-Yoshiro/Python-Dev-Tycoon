import pygame
import os

class TelaIntroducaoTopico:
    def __init__(self, largura, altura, nome_topico, descricao, on_confirmar):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.descricao = descricao
        self.on_confirmar = on_confirmar

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 28, bold=True)
        self.fonte = pygame.font.SysFont('Arial', 22)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)

        # Carrega e redimensiona a imagem para caber exatamente na tela
        caminho_img = os.path.join("Assets", "intro_pc1.png")
        self.bg = pygame.image.load(caminho_img).convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        # --- COORDENADAS DA JANELA DO MONITOR (AJUSTE SE PRECISAR) ---
        # Área da "tela" do computador (janela)
        self.janela_x = int(largura * 0.20)
        self.janela_y = int(altura * 0.16)
        self.janela_w = int(largura * 0.60)
        self.janela_h = int(altura * 0.54)

        # Barra azul do topo (onde vai o título)
        self.barra_x = self.janela_x + 12
        self.barra_y = self.janela_y + 11
        self.barra_w = self.janela_w - 24
        self.barra_h = 36  # altura da barra azul

        # Área preta do texto (dentro da janela)
        self.area_texto_x = self.barra_x
        self.area_texto_y = self.barra_y + self.barra_h + 12
        self.area_texto_w = self.barra_w
        self.area_texto_h = self.janela_h - self.barra_h - 54  # deixa espaço p/ botão

        # Botão (alinhado central na janela)
        botao_w, botao_h = 255, 30
        self.rect_confirmar = pygame.Rect(
            self.janela_x + (self.janela_w - botao_w) // 2,
            self.janela_y + self.janela_h - botao_h - 18,
            botao_w,
            botao_h
        )

    def quebrar_linha(self, texto, fonte, largura_max):
        linhas = []
        paragrafos = texto.split('\n')
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
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
        tela.blit(self.bg, (0, 0))

        # --- TÍTULO NA BARRA AZUL ---
        titulo = f"Tópico: {self.nome_topico}"
        titulo_surface = self.fonte_titulo.render(titulo, True, (130, 220, 255))
        titulo_rect = titulo_surface.get_rect()
        titulo_rect.midleft = (self.barra_x + 60, self.barra_y + self.barra_h // 2 + 40)
        tela.blit(titulo_surface, titulo_rect)

        # --- TEXTO DE INTRODUÇÃO NA ÁREA ESCURA ---
        margem_x = 60
        margem_y = 36
        x = self.area_texto_x + margem_x
        y = self.area_texto_y + margem_y
        largura_max = self.area_texto_w - 2 * margem_x

        linhas = self.quebrar_linha(self.descricao, self.fonte_pequena, largura_max)
        for linha in linhas:
            tela.blit(self.fonte_pequena.render(linha, True, (255,255,255)), (x, y))
            y += 32

        # --- BOTÃO "ENTENDIDO" VISÍVEL, COM HOVER ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_hover = self.rect_confirmar.collidepoint(mouse_x, mouse_y)

        cor_texto = (255,255,255)
        fonte_botao = self.fonte
        if botao_hover:
            cor_texto = (255, 230, 80)  # Amarelo-dourado
            fonte_botao = pygame.font.SysFont('Arial', 22, bold=True)  # Negrito no hover

        botao_surface = fonte_botao.render("ENTENDIDO", True, cor_texto)
        tela.blit(
            botao_surface,
            (
                self.rect_confirmar.x + (self.rect_confirmar.w - botao_surface.get_width()) // 2,
                self.rect_confirmar.y + (self.rect_confirmar.h - botao_surface.get_height()) // 2
            )
        )




    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_confirmar.collidepoint(x, y):
                    if self.on_confirmar:
                        self.on_confirmar()


#versão antiga mais ludica
"""
import pygame
import os

class TelaIntroducaoTopico:
    def __init__(self, largura, altura, nome_topico, descricao, on_confirmar):
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.descricao = descricao
        self.on_confirmar = on_confirmar

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 34, bold=True)
        self.fonte = pygame.font.SysFont('Arial', 24)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20)
        #self.rect_confirmar = pygame.Rect(largura // 2 - 90, altura - 90, 180, 54)
        

        # Carrega e redimensiona a imagem para caber exatamente na tela
        caminho_img = os.path.join("Assets", "intro_pc1.png")
        self.bg = pygame.image.load(caminho_img).convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (largura, altura))

        # ÁREA do quadro branco (ajuste para área clara da sua imagem)
        self.quadro_x = int(largura * 0.23)
        self.quadro_y = int(altura * 0.20)
        self.quadro_w = int(largura * 0.54)
        self.quadro_h = int(altura * 0.36)

        botao_w, botao_h = 180, 54
        self.rect_confirmar = pygame.Rect(
            self.quadro_x + self.quadro_w - botao_w - 50,     # 16 é a margem da borda direita do quadro
            self.quadro_y + self.quadro_h - botao_h - 26,     # 16 é a margem da borda inferior do quadro
            botao_w,
            botao_h
)


        # DESLOCAMENTOS (ajuste para alinhar texto dentro do quadro)
        self.text_dx = 60  # deslocamento horizontal do texto dentro do quadro (quanto maior, mais pra direita)
        self.text_dy = -50 # deslocamento vertical (negativo sobe, positivo desce)
        self.margem_dir = 45  # margem à direita (distância do texto até a borda do quadro direito)

    def quebrar_linha(self, texto, fonte, largura_max):
        linhas = []
        paragrafos = texto.split('\n')
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
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
        tela.blit(self.bg, (0, 0))

        # Título centralizado no topo
        tela.blit(self.fonte_titulo.render(f"Tópico: {self.nome_topico}", True, (0, 210, 255)), (60, 40))

        # --- TEXTO DENTRO DO QUADRO ---
        x = self.quadro_x + self.text_dx
        x_final = self.quadro_x + self.quadro_w - self.margem_dir
        largura_max = x_final - x  # calcula espaço útil para o texto!
        y = self.quadro_y + self.text_dy

        linhas = self.quebrar_linha(self.descricao, self.fonte_pequena, largura_max)
        for linha in linhas:
            tela.blit(self.fonte_pequena.render(linha, True, (255,255,255)), (x, y))
            y += 30

        # Mensagem de aviso
        tela.blit(self.fonte_pequena.render("Leia com atenção a introdução acima.", True, (255,255,100)),
                  (self.quadro_x + 55, y + 32))

        # Botão grande centralizado
        pygame.draw.rect(tela, (0, 170, 160), self.rect_confirmar, border_radius=16)
        tela.blit(self.fonte_pequena.render("ENTENDI!", True, (255,255,255)),
                  (self.rect_confirmar.x + 40, self.rect_confirmar.y + 15))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_confirmar.collidepoint(x, y):
                    if self.on_confirmar:
                        self.on_confirmar()

"""
