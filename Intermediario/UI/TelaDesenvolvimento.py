import pygame
from Intermediario.UI.Janela import Janela

class TelaDesenvolvimento(Janela):
    def __init__(self, largura_tela, altura_tela, projeto, cliente, callback_validar, callback_entregar, callback_desistir):
        
        painel_w = int(largura_tela * 0.8)
        painel_h = int(altura_tela * 0.85)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, 
                         titulo=f"[ AMBIENTE DE DESENVOLVIMENTO ]: {projeto.get_titulo()}")
        
        self.cor_fundo = (18, 24, 32)
        self.cor_borda = (42, 103, 188)
        self.cor_titulo_bg = (28, 44, 80)

        self.projeto = projeto
        self.cliente = cliente
        self.callback_validar = callback_validar
        self.callback_entregar = callback_entregar
        self.callback_desistir = callback_desistir

        # Paleta de Cores e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (220, 220, 220)
        self.COR_FUNDO_EDITOR = (10, 12, 15)
        self.COR_SUCESSO = (0, 220, 120)
        self.COR_FALHA = (220, 50, 50)
        self.COR_BOTAO_EXECUTAR = (0, 150, 200)
        self.COR_BOTAO_ENTREGAR = (0, 180, 80)
        self.COR_BOTAO_DESISTIR = (180, 40, 40)

        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_code = pygame.font.SysFont('Consolas', 16)
        self.fonte_terminal = pygame.font.SysFont('Consolas', 14)
        self.fonte_popup = pygame.font.SysFont('Consolas', 16)

        # Lógica do Editor de Texto
        self.linhas_codigo = projeto.get_codigo_base().split('\n')
        self.linha_ativa = 0
        self.cursor_pos = len(self.linhas_codigo[0]) if self.linhas_codigo else 0
        self.input_ativo = True
        
        self.cursor_visivel = True
        self.cursor_timer = 0
        self.cursor_intervalo = 500
        
        self.resultados_testes = [] # Armazena o log detalhado
        self.feedback_resumido = "Terminal de Validação. Pressione 'Executar Testes'."
        self.testes_passaram = False
        
        # Lógica do Popup de Saída
        self.popup_saida = False
        self._popup_btn_rect = None
        self.rect_info_saida = None

    def update(self, dt):
        """Método chamado a cada frame para lógicas de tempo, como o cursor piscando."""
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_intervalo:
            self.cursor_timer = 0
            self.cursor_visivel = not self.cursor_visivel

    def desenhar_texto_quebra_linha(self, tela, texto, rect, fonte, cor):
        """
        Desenha texto com quebra de linha automática dentro de um retângulo,
        respeitando parágrafos definidos por '\n'.
        """
        y = rect.y
        paragrafos = texto.splitlines()

        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            linha_atual = ''
            for palavra in palavras:
                teste_linha = f"{linha_atual} {palavra}".strip()
                if fonte.size(teste_linha)[0] <= rect.width:
                    linha_atual = teste_linha
                else:
                    if y + fonte.get_height() > rect.bottom: return y
                    linha_surf = fonte.render(linha_atual, True, cor)
                    tela.blit(linha_surf, (rect.x, y))
                    y += fonte.get_height()
                    linha_atual = palavra
            
            if y + fonte.get_height() > rect.bottom: return y
            linha_surf = fonte.render(linha_atual, True, cor)
            tela.blit(linha_surf, (rect.x, y))
            y += fonte.get_height()
        
        return y

    def _desenhar_popup_saida(self, tela):
        """Desenha o popup com o log detalhado dos testes, igual ao da TelaExercicio."""
        largura, altura = 600, 400
        popup_x = self.rect.centerx - largura // 2
        popup_y = self.rect.centery - altura // 2
        
        surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(surf, (30, 44, 70, 232), (0,0,largura,altura), border_radius=20)
        pygame.draw.rect(surf, (120,180,255), (0,0,largura,altura), 3, border_radius=20)
        
        surf.blit(self.fonte_h2.render("Log de Execução dos Testes:", True, (230,230,90)), (20, 20))

        y_popup = 65
        for linha in self.resultados_testes:
            if y_popup > altura - 50:
                surf.blit(self.fonte_popup.render("[...]", True, (220,180,180)), (20, y_popup))
                break
            cor = self.COR_SUCESSO if "✓" in linha else self.COR_FALHA if "✗" in linha else self.COR_TEXTO_CORPO
            
            area_linha_popup = pygame.Rect(20, y_popup, largura - 40, altura - y_popup - 20)
            y_popup = self.desenhar_texto_quebra_linha(surf, linha, area_linha_popup, self.fonte_popup, cor)
            y_popup += 5

        btn_rect = pygame.Rect(largura-110, altura-50, 90, 38)
        pygame.draw.rect(surf, (255, 90, 90), btn_rect, border_radius=12)
        fechar_label = self.fonte_h2.render("FECHAR", True, (255,255,255))
        surf.blit(fechar_label, (btn_rect.centerx - fechar_label.get_width()/2, btn_rect.centery - fechar_label.get_height()/2))
        
        tela.blit(surf, (popup_x, popup_y))
        self._popup_btn_rect = pygame.Rect(popup_x + btn_rect.x, popup_y + btn_rect.y, btn_rect.w, btn_rect.h)

    def desenhar_conteudo(self, tela):
        briefing_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 40, 350, self.rect.height - 60)
        self.editor_rect = pygame.Rect(briefing_rect.right + 15, self.rect.y + 40, self.rect.width - briefing_rect.width - 45, self.rect.height - 200)
        terminal_rect = pygame.Rect(self.editor_rect.left, self.editor_rect.bottom + 15, self.editor_rect.width, 130)

        # --- Painel de Briefing ---
        pygame.draw.rect(tela, self.cor_fundo, briefing_rect, border_radius=8)
        cliente_surf = self.fonte_h2.render(f"Cliente: {self.cliente.get_nome()}", True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(cliente_surf, (briefing_rect.x + 15, briefing_rect.y + 15))
        desc_label_surf = self.fonte_h2.render("Objetivo do Contrato:", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(desc_label_surf, (briefing_rect.x + 15, briefing_rect.y + 50))
        desc_rect_area = pygame.Rect(briefing_rect.x + 15, briefing_rect.y + 80, briefing_rect.width - 30, 200)
        self.desenhar_texto_quebra_linha(tela, self.projeto.get_descricao(), desc_rect_area, self.fonte_code, self.COR_TEXTO_CORPO)

        # --- Painel do Editor de Código ---
        pygame.draw.rect(tela, self.COR_FUNDO_EDITOR, self.editor_rect)
        y_linha = self.editor_rect.y + 10
        for i, linha in enumerate(self.linhas_codigo):
            linha_surf = self.fonte_code.render(linha, True, self.COR_TEXTO_CORPO)
            tela.blit(linha_surf, (self.editor_rect.x + 10, y_linha))
            if i == self.linha_ativa and self.input_ativo and self.cursor_visivel:
                texto_ate_cursor = linha[:self.cursor_pos]
                cursor_x = self.editor_rect.x + 10 + self.fonte_code.size(texto_ate_cursor)[0]
                pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (cursor_x, y_linha), (cursor_x, y_linha + self.fonte_code.get_height()), 2)
            y_linha += self.fonte_code.get_height()

        # --- Painel do Terminal ---
        pygame.draw.rect(tela, self.COR_FUNDO_EDITOR, terminal_rect)
        cor_feedback = self.COR_SUCESSO if self.testes_passaram else self.COR_FALHA if len(self.resultados_testes) > 0 else self.COR_TEXTO_CORPO
        feedback_surf = self.fonte_terminal.render(self.feedback_resumido, True, cor_feedback)
        tela.blit(feedback_surf, (terminal_rect.x + 10, terminal_rect.y + 10))

        if self.resultados_testes:
            icon_x = terminal_rect.x + 15 + feedback_surf.get_width()
            icon_rect = pygame.Rect(icon_x, terminal_rect.y + 8, 24, 24)
            pygame.draw.circle(tela, (100, 180, 255), icon_rect.center, 12)
            i_mark = self.fonte_h2.render("i", True, (30, 50, 80))
            tela.blit(i_mark, (icon_rect.centerx - i_mark.get_width()/2, icon_rect.centery - i_mark.get_height()/2))
            self.rect_info_saida = icon_rect
        else:
            self.rect_info_saida = None

        # Botões no painel de Briefing
        self.botao_executar_rect = pygame.Rect(briefing_rect.left + 15, briefing_rect.bottom - 180, briefing_rect.width - 30, 50)
        self.botao_entregar_rect = pygame.Rect(briefing_rect.left + 15, briefing_rect.bottom - 120, briefing_rect.width - 30, 50)
        self.botao_desistir_rect = pygame.Rect(briefing_rect.left + 15, briefing_rect.bottom - 60, briefing_rect.width - 30, 50)
        
        pygame.draw.rect(tela, self.COR_BOTAO_EXECUTAR, self.botao_executar_rect, border_radius=5)
        exec_surf = self.fonte_h2.render("Executar Testes", True, (255,255,255))
        tela.blit(exec_surf, (self.botao_executar_rect.centerx - exec_surf.get_width()/2, self.botao_executar_rect.centery - exec_surf.get_height()/2))
        
        if self.testes_passaram:
            pygame.draw.rect(tela, self.COR_BOTAO_ENTREGAR, self.botao_entregar_rect, border_radius=5)
            entregar_surf = self.fonte_h2.render("Entregar Projeto", True, (255,255,255))
            tela.blit(entregar_surf, (self.botao_entregar_rect.centerx - entregar_surf.get_width()/2, self.botao_entregar_rect.centery - entregar_surf.get_height()/2))
        else:
            pygame.draw.rect(tela, (80,80,80), self.botao_entregar_rect, border_radius=5)
            entregar_surf = self.fonte_h2.render("Entregar Projeto (Bloqueado)", True, (150,150,150))
            tela.blit(entregar_surf, (self.botao_entregar_rect.centerx - entregar_surf.get_width()/2, self.botao_entregar_rect.centery - entregar_surf.get_height()/2))

        pygame.draw.rect(tela, self.COR_BOTAO_DESISTIR, self.botao_desistir_rect, border_radius=5)
        desistir_surf = self.fonte_h2.render("Desistir do Contrato", True, (255,255,255))
        tela.blit(desistir_surf, (self.botao_desistir_rect.centerx - desistir_surf.get_width()/2, self.botao_desistir_rect.centery - desistir_surf.get_height()/2))

        if self.popup_saida:
            self._desenhar_popup_saida(tela)

    def _get_posicao_cursor_pelo_mouse(self, pos_mouse):
        linha_texto = self.linhas_codigo[self.linha_ativa]
        pos_x_relativa = pos_mouse[0] - (self.editor_rect.x + 10)
        melhor_distancia, melhor_indice = float('inf'), 0
        for i in range(len(linha_texto) + 1):
            largura_sub_texto = self.fonte_code.size(linha_texto[:i])[0]
            distancia = abs(pos_x_relativa - largura_sub_texto)
            if distancia < melhor_distancia:
                melhor_distancia, melhor_indice = distancia, i
            else:
                break
        return melhor_indice

    def tratar_eventos_conteudo(self, eventos):
        if self.popup_saida:
            for evento in eventos:
                if self._popup_btn_rect and evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    if self._popup_btn_rect.collidepoint(evento.pos): self.popup_saida = False
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_executar_rect.collidepoint(evento.pos):
                    codigo_final = "\n".join(self.linhas_codigo)
                    resultado_validacao = self.callback_validar(self.projeto, codigo_final)
                    self.resultados_testes = resultado_validacao["resultados"]
                    self.testes_passaram = resultado_validacao["sucesso"]
                    self.feedback_resumido = "Sucesso: Todos os testes passaram!" if self.testes_passaram else "Falha: Verifique o log de testes."
                elif self.testes_passaram and self.botao_entregar_rect.collidepoint(evento.pos):
                    self.callback_entregar(self.projeto); self.deve_fechar = True
                elif self.botao_desistir_rect.collidepoint(evento.pos):
                    self.callback_desistir(self.projeto); self.deve_fechar = True
                elif self.rect_info_saida and self.rect_info_saida.collidepoint(evento.pos):
                    self.popup_saida = True
                elif self.editor_rect.collidepoint(evento.pos):
                    self.input_ativo = True
                    clique_y = evento.pos[1] - (self.editor_rect.y + 10)
                    self.linha_ativa = min(len(self.linhas_codigo) - 1, max(0, clique_y // self.fonte_code.get_height()))
                    self.cursor_pos = self._get_posicao_cursor_pelo_mouse(evento.pos)

            if evento.type == pygame.KEYDOWN and self.input_ativo:
                linha_atual = self.linhas_codigo[self.linha_ativa]
                if evento.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos-1] + linha_atual[self.cursor_pos:]
                        self.cursor_pos -= 1
                elif evento.key == pygame.K_RETURN:
                    parte_restante = linha_atual[self.cursor_pos:]
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos]
                    self.linhas_codigo.insert(self.linha_ativa + 1, parte_restante)
                    self.linha_ativa += 1; self.cursor_pos = 0
                elif evento.key == pygame.K_UP:
                    self.linha_ativa = max(0, self.linha_ativa - 1)
                    self.cursor_pos = min(self.cursor_pos, len(self.linhas_codigo[self.linha_ativa]))
                elif evento.key == pygame.K_DOWN:
                    self.linha_ativa = min(len(self.linhas_codigo) - 1, self.linha_ativa + 1)
                    self.cursor_pos = min(self.cursor_pos, len(self.linhas_codigo[self.linha_ativa]))
                elif evento.key == pygame.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                elif evento.key == pygame.K_RIGHT:
                    self.cursor_pos = min(len(linha_atual), self.cursor_pos + 1)
                elif evento.key == pygame.K_TAB:
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos] + '    ' + linha_atual[self.cursor_pos:]
                    self.cursor_pos += 4
                else:
                    self.linhas_codigo[self.linha_ativa] = linha_atual[:self.cursor_pos] + evento.unicode + linha_atual[self.cursor_pos:]
                    self.cursor_pos += len(evento.unicode)

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)
