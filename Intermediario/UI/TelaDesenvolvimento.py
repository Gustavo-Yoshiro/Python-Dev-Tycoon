import pygame
from Intermediario.UI.Janela import Janela

class TelaDesenvolvimento(Janela):
    def __init__(self, largura_tela, altura_tela, projeto, cliente, callback_validar, callback_desistir):
        super().__init__(x=50, y=50, largura=1180, altura=620, titulo=f"[ IDE F.L.N.C.R. ]: {projeto.get_titulo()}")

        self.cor_fundo = (28, 34, 42)
        self.cor_borda = (130, 220, 255)
        self.cor_titulo_bg = (18, 24, 32)

        self.projeto = projeto
        self.cliente = cliente
        self.callback_validar = callback_validar
        self.callback_desistir = callback_desistir

        # Paleta e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (220, 220, 220)
        self.COR_FUNDO_EDITOR = (10, 12, 15)
        self.COR_SUCESSO = (0, 220, 120)
        self.COR_FALHA = (220, 50, 50)

        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_code = pygame.font.SysFont('Consolas', 16)
        self.fonte_terminal = pygame.font.SysFont('Consolas', 14)

        # Lógica do Editor de Texto
        self.linhas_codigo = projeto.get_codigo_base().split('\n')
        self.linha_ativa = 0
        self.cursor_pos = 0
        self.input_ativo = True # Começa ativo por padrão
        
        self.resultados_testes = ["Terminal de Validação. Pressione 'Executar Testes' para verificar seu código."]

    def desenhar_conteudo(self, tela):
        # Layout de 3 painéis: Briefing (esquerda), Editor (centro), Terminal (baixo)
        briefing_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 40, 350, self.rect.height - 60)
        editor_rect = pygame.Rect(briefing_rect.right + 15, self.rect.y + 40, self.rect.width - briefing_rect.width - 45, self.rect.height - 200)
        terminal_rect = pygame.Rect(editor_rect.left, editor_rect.bottom + 15, editor_rect.width, 130)

        # --- Painel de Briefing ---
        pygame.draw.rect(tela, self.cor_fundo, briefing_rect, border_radius=8)
        # (Desenhar aqui a descrição do projeto, requisitos, etc.)

        # --- Painel do Editor de Código ---
        pygame.draw.rect(tela, self.COR_FUNDO_EDITOR, editor_rect)
        y_linha = editor_rect.y + 10
        for i, linha in enumerate(self.linhas_codigo):
            cor_texto = self.COR_TEXTO_PRIMARIO if i == self.linha_ativa and self.input_ativo else self.COR_TEXTO_CORPO
            linha_surf = self.fonte_code.render(linha, True, cor_texto)
            tela.blit(linha_surf, (editor_rect.x + 10, y_linha))
            y_linha += self.fonte_code.get_height()

        # --- Painel do Terminal ---
        pygame.draw.rect(tela, self.COR_FUNDO_EDITOR, terminal_rect)
        y_terminal = terminal_rect.y + 10
        for linha_resultado in self.resultados_testes:
            cor = self.COR_SUCESSO if "✓" in linha_resultado else self.COR_FALHA if "✗" in linha_resultado else self.COR_TEXTO_CORPO
            resultado_surf = self.fonte_terminal.render(linha_resultado, True, cor)
            tela.blit(resultado_surf, (terminal_rect.x + 10, y_terminal))
            y_terminal += self.fonte_terminal.get_height()

        # Botões
        self.botao_executar_rect = pygame.Rect(briefing_rect.left, briefing_rect.bottom - 120, briefing_rect.width - 30, 50)
        self.botao_entregar_rect = pygame.Rect(briefing_rect.left, briefing_rect.bottom - 60, briefing_rect.width - 30, 50)
        pygame.draw.rect(tela, (0, 150, 200), self.botao_executar_rect, border_radius=5)
        pygame.draw.rect(tela, (0, 180, 80), self.botao_entregar_rect, border_radius=5)

    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and self.input_ativo:
                linha_atual = self.linhas_codigo[self.linha_ativa]
                if evento.key == pygame.K_BACKSPACE:
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:-1]
                elif evento.key == pygame.K_RETURN:
                    self.linhas_codigo.insert(self.linha_ativa + 1, "")
                    self.linha_ativa += 1
                else:
                    self.linhas_codigo[self.linha_ativa] += evento.unicode
            
            if evento.type == pygame.MOUSEBUTTONUP:
                if self.botao_executar_rect.collidepoint(evento.pos):
                    codigo_final = "\n".join(self.linhas_codigo)
                    resultado_validacao = self.callback_validar(self.projeto, codigo_final)
                    self.resultados_testes = resultado_validacao["resultados"]
                    # Se sucesso, habilitar o botão de entregar
