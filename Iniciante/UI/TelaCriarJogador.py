import pygame

class TelaCriarJogador:
    def __init__(self, largura, altura, callback_confirmar, callback_voltar=None):
        self.largura = largura
        self.altura = altura
        self.callback_confirmar = callback_confirmar
        self.callback_voltar = callback_voltar
        
        # Configurações visuais
        self.fundo = pygame.Surface((largura, altura))
        self.fundo.fill((40, 45, 60))
        
        # Fontes
        self.fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_normal = pygame.font.SysFont("Arial", 36)
        self.fonte_pequena = pygame.font.SysFont("Arial", 24)
        
        # Campo de entrada
        self.nome = ""
        self.campo_entrada = pygame.Rect(largura//2 - 250, altura//2 - 25, 500, 50)
        self.ativo = False
        self.cursor_visivel = True
        self.tempo_cursor = 0
        
        # Botões
        self.botao_confirmar = pygame.Rect(largura//2 - 120, altura//2 + 100, 240, 60)
        self.botao_voltar = pygame.Rect(50, 50, 120, 50)
        
        # Mensagens
        self.mensagem_erro = ""
        self.tempo_mensagem = 0

    def desenhar(self, tela):
        # Fundo
        tela.blit(self.fundo, (0, 0))
        
        # Título
        titulo = self.fonte_titulo.render("Criar Novo Jogador", True, (255, 255, 255))
        tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 100))
        
        # Botão voltar (se houver callback)
        if self.callback_voltar:
            pygame.draw.rect(tela, (70, 70, 70), self.botao_voltar, border_radius=5)
            texto_voltar = self.fonte_pequena.render("Voltar", True, (255, 255, 255))
            tela.blit(texto_voltar, (
                self.botao_voltar.x + (self.botao_voltar.width - texto_voltar.get_width()) // 2,
                self.botao_voltar.y + (self.botao_voltar.height - texto_voltar.get_height()) // 2
            ))
        
        # Campo de entrada
        cor_borda = (100, 150, 255) if self.ativo else (80, 80, 80)
        pygame.draw.rect(tela, (30, 30, 40), self.campo_entrada, border_radius=5)
        pygame.draw.rect(tela, cor_borda, self.campo_entrada, width=3, border_radius=5)
        
        # Texto do campo
        texto_nome = self.fonte_normal.render(self.nome, True, (255, 255, 255))
        largura_maxima = self.campo_entrada.width - 30
        if texto_nome.get_width() > largura_maxima:
            # Corta o texto se for muito grande
            tela.blit(texto_nome, (self.campo_entrada.x + 15, self.campo_entrada.y + 10), 
                     (texto_nome.get_width() - largura_maxima, 0, largura_maxima, texto_nome.get_height()))
        else:
            tela.blit(texto_nome, (self.campo_entrada.x + 15, self.campo_entrada.y + 10))
        
        # Cursor piscante
        if self.ativo and self.cursor_visivel:
            cursor_x = self.campo_entrada.x + 20 + min(texto_nome.get_width(), largura_maxima)
            pygame.draw.line(tela, (255, 255, 255), 
                           (cursor_x, self.campo_entrada.y + 10),
                           (cursor_x, self.campo_entrada.y + 40), 2)
        
        # Label do campo
        label = self.fonte_pequena.render("Nome do Jogador:", True, (200, 200, 200))
        tela.blit(label, (self.campo_entrada.x, self.campo_entrada.y - 30))
        
        # Botão confirmar
        cor_botao = (80, 120, 200) if self.nome else (80, 80, 80)
        pygame.draw.rect(tela, cor_botao, self.botao_confirmar, border_radius=5)
        pygame.draw.rect(tela, (100, 140, 220), self.botao_confirmar, width=2, border_radius=5)
        
        texto_confirmar = self.fonte_normal.render("Confirmar", True, (255, 255, 255))
        tela.blit(texto_confirmar, (
            self.botao_confirmar.x + (self.botao_confirmar.width - texto_confirmar.get_width()) // 2,
            self.botao_confirmar.y + (self.botao_confirmar.height - texto_confirmar.get_height()) // 2
        ))
        
        # Mensagem de erro
        if self.mensagem_erro and pygame.time.get_ticks() - self.tempo_mensagem < 3000:
            texto_erro = self.fonte_pequena.render(self.mensagem_erro, True, (255, 100, 100))
            tela.blit(texto_erro, (
                (self.largura - texto_erro.get_width()) // 2,
                self.botao_confirmar.y + 80
            ))

    def atualizar(self, dt):
        # Atualiza piscar do cursor
        self.tempo_cursor += dt
        if self.tempo_cursor >= 500:  # 0.5 segundos
            self.tempo_cursor = 0
            self.cursor_visivel = not self.cursor_visivel

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique no campo de entrada
                if self.campo_entrada.collidepoint(evento.pos):
                    self.ativo = True
                else:
                    self.ativo = False
                
                # Verifica clique no botão confirmar
                if self.botao_confirmar.collidepoint(evento.pos) and self.nome:
                    self.confirmar()
                
                # Verifica clique no botão voltar
                if self.callback_voltar and self.botao_voltar.collidepoint(evento.pos):
                    self.callback_voltar()
            
            elif evento.type == pygame.KEYDOWN and self.ativo:
                if evento.key == pygame.K_RETURN and self.nome:
                    self.confirmar()
                elif evento.key == pygame.K_BACKSPACE:
                    self.nome = self.nome[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    if self.callback_voltar:
                        self.callback_voltar()
                elif len(self.nome) < 20:  # Limite de caracteres
                    self.nome += evento.unicode

    def confirmar(self):
        if len(self.nome.strip()) < 3:
            self.mensagem_erro = "O nome deve ter pelo menos 3 caracteres"
            self.tempo_mensagem = pygame.time.get_ticks()
        else:
            self.callback_confirmar(self.nome.strip())