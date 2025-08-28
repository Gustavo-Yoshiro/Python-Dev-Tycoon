import pygame
from Intermediario.UI.Janela import Janela
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl
from Intermediario.Service.Impl.DialogoServiceImpl import DialogoServiceImpl

class TelaProjeto(Janela):
    def __init__(self, largura_tela, altura_tela, projeto, cliente, jogador, mensagens, 
                 opcoes_dialogo_atuais, callback_aceitar, callback_enviar_mensagem, callback_voltar, detalhes_adicionais=None):
        
        painel_w = int(largura_tela * 0.65)
        painel_h = int(altura_tela * 0.8)
        painel_x = int((largura_tela - painel_w) / 2)
        painel_y = int((altura_tela - painel_h) / 2)

        super().__init__(x=painel_x, y=painel_y, largura=painel_w, altura=painel_h, 
                         titulo=f"[ CANAL DE NEGOCIAÇÃO ]: {cliente.get_nome()}")
        
        self.cor_fundo = (18, 24, 32)
        self.cor_borda = (130, 220, 255)
        self.cor_titulo_bg = (28, 34, 42)

        self.projeto = projeto
        self.cliente = cliente
        self.jogador = jogador
        self.mensagens = mensagens
        self.opcoes_dialogo = opcoes_dialogo_atuais
        self.callback_aceitar = callback_aceitar
        self.callback_enviar_mensagem = callback_enviar_mensagem
        self.callback_voltar = callback_voltar
        self.detalhes_adicionais = detalhes_adicionais
        
        self.service = JogadorProjetoServiceImpl()
        self.serviceNo = DialogoServiceImpl()

        # Paleta de Cores e Fontes
        self.COR_TEXTO_PRIMARIO = (255, 190, 0)
        self.COR_TEXTO_SECUNDARIO = (130, 220, 255)
        self.COR_TEXTO_CORPO = (200, 200, 200)
        self.COR_FUNDO_CHAT = (10, 12, 15)
        self.COR_HOVER_OPCAO = (40, 50, 65)
        self.COR_BOTAO_ACEITAR = (0, 180, 80)
        self.COR_BOTAO_ACEITAR_HOVER = (0, 210, 100)
        self.COR_BOTAO_VOLTAR = (100, 100, 100)
        self.COR_BOTAO_VOLTAR_HOVER = (120, 120, 120)
        self.COR_ESTRELA = (255, 190, 0)
        
        self.fonte_h2 = pygame.font.SysFont('Consolas', 18, bold=True)
        self.fonte_corpo = pygame.font.SysFont('Consolas', 16)
        self.fonte_logo = pygame.font.SysFont('Consolas', 28, bold=True)
        
        self.botoes_dialogo_rects = {}
        self.botao_voltar_rect = pygame.Rect(20, self.rect.height - 70, 150, 50)
        self.botao_aceitar_rect = pygame.Rect(self.rect.width - 220, self.rect.height - 70, 200, 50)

    def desenhar_texto_quebra_linha(self, tela, texto, rect, fonte, cor):
        """Desenha texto com quebra de linha automática dentro de um retângulo."""
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ''
        
        for palavra in palavras:
            teste_linha = f"{linha_atual} {palavra}".strip()
            if fonte.size(teste_linha)[0] <= rect.width:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        linhas.append(linha_atual)
        
        y = rect.y
        for linha in linhas:
            if y + fonte.get_height() > rect.bottom:
                break
            linha_surf = fonte.render(linha, True, cor)
            tela.blit(linha_surf, (rect.x, y))
            y += fonte.get_height()
        return y

    def desenhar_conteudo(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        
        # --- Seção 1: Perfil do Cliente (Topo) ---
        area_cliente = pygame.Rect(self.rect.x + 20, self.rect.y + 40, self.rect.width - 40, 64)
        logo_rect = pygame.Rect(area_cliente.x, area_cliente.y, 64, 64)
        pygame.draw.rect(tela, (40, 50, 65), logo_rect, border_radius=5)
        inicial = self.cliente.get_nome()[0].upper()
        inicial_surf = self.fonte_logo.render(inicial, True, self.COR_TEXTO_SECUNDARIO)
        tela.blit(inicial_surf, (logo_rect.centerx - inicial_surf.get_width()/2, logo_rect.centery - inicial_surf.get_height()/2))
        
        texto_cliente = f"{self.cliente.get_nome()} ({self.cliente.get_personalidade()})"
        cliente_surf = self.fonte_h2.render(texto_cliente, True, self.COR_TEXTO_CORPO)
        tela.blit(cliente_surf, (logo_rect.right + 15, logo_rect.y + 5))

        reputacao = self.cliente.get_reputacao()
        estrelas = "★" * int(reputacao) + "☆" * (5 - int(reputacao))
        reputacao_texto = f"Reputação Contigo: {reputacao:.1f} {estrelas}"
        reputacao_surf = self.fonte_corpo.render(reputacao_texto, True, self.COR_ESTRELA)
        tela.blit(reputacao_surf, (logo_rect.right + 15, logo_rect.y + 30))
        
        pagamento_texto = f"R$ {self.projeto.get_recompensa():.2f}"
        pagamento_surf = self.fonte_h2.render(pagamento_texto, True, (0, 220, 120))
        pagamento_rect = pagamento_surf.get_rect(topright=(area_cliente.right, logo_rect.y + 5))
        tela.blit(pagamento_surf, pagamento_rect)

        pagamento_label_surf = self.fonte_corpo.render("Pagamento do Contrato", True, self.COR_TEXTO_CORPO)
        pagamento_label_rect = pagamento_label_surf.get_rect(topright=(area_cliente.right, logo_rect.y + 35))
        tela.blit(pagamento_label_surf, pagamento_label_rect)
        
        # --- Seção 2: Descrição do Projeto ---
        info_y = area_cliente.bottom + 15
        pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (self.rect.x + 20, info_y), (self.rect.right - 20, info_y), 1)
        
        briefing_rect = pygame.Rect(self.rect.x + 20, info_y + 10, self.rect.width - 40, 60)
        y_apos_briefing = self.desenhar_texto_quebra_linha(tela, f"Briefing: {self.projeto.get_descricao()}", briefing_rect, self.fonte_h2, self.COR_TEXTO_CORPO)
        
        # --- NOVA SECÇÃO: Requisitos ---
        req_y = y_apos_briefing + 10
        pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (self.rect.x + 20, req_y), (self.rect.right - 20, req_y), 1)
        req_header_surf = self.fonte_h2.render("[ REQUISITOS TÉCNICOS ]", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(req_header_surf, (self.rect.x + 20, req_y + 10))

        req_backend_surf = self.fonte_corpo.render(f"Backend: Nível {self.projeto.get_req_backend()}", True, self.COR_TEXTO_CORPO)
        tela.blit(req_backend_surf, (self.rect.x + 30, req_y + 40))
        req_frontend_surf = self.fonte_corpo.render(f"Frontend: Nível {self.projeto.get_req_frontend()}", True, self.COR_TEXTO_CORPO)
        tela.blit(req_frontend_surf, (self.rect.x + 250, req_y + 40))
        req_social_surf = self.fonte_corpo.render(f"Social: Nível {self.projeto.get_req_social()}", True, self.COR_TEXTO_CORPO)
        tela.blit(req_social_surf, (self.rect.x + 470, req_y + 40))
        
        # --- Seção 3: Terminal de Chat ---
        chat_y_inicio = req_y + 70 # Posição Y onde o chat começa
        rodape_y_inicio = self.rect.y + self.rect.height - 80 # Posição Y onde o rodapé começa
        chat_height = rodape_y_inicio - chat_y_inicio # Calcula a altura para preencher o espaço

        area_chat = pygame.Rect(self.rect.x + 20, chat_y_inicio, self.rect.width - 40, chat_height)
        pygame.draw.rect(tela, self.COR_FUNDO_CHAT, area_chat, border_radius=8)
        
        log_header = self.fonte_h2.render("[ LOG DE COMUNICAÇÃO ]", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(log_header, (area_chat.x + 10, area_chat.y + 10))

        log_area = pygame.Rect(area_chat.x + 10, area_chat.y + 40, area_chat.width - 20, area_chat.height - 130)
        log_y = log_area.y
        for msg in self.mensagens:
            remetente_cor = self.COR_TEXTO_SECUNDARIO if msg.get_enviado_por() != 'jogador' else (200, 200, 90)
            remetente_surf = self.fonte_corpo.render(f"<{msg.get_enviado_por().upper()}>:", True, remetente_cor)
            tela.blit(remetente_surf, (log_area.x, log_y))
            
            area_msg = pygame.Rect(log_area.x + 140, log_y, log_area.width - 140, log_area.height - (log_y - log_area.y))
            log_y = self.desenhar_texto_quebra_linha(tela, msg.get_mensagem(), area_msg, self.fonte_corpo, self.COR_TEXTO_CORPO)
            log_y += 5

        area_resposta = pygame.Rect(area_chat.x, area_chat.bottom - 90, area_chat.width, 90)
        pygame.draw.line(tela, self.COR_TEXTO_PRIMARIO, (area_resposta.left, area_resposta.top), (area_resposta.right, area_resposta.top), 1)
        
        prompt_surf = self.fonte_h2.render("Suas Respostas:", True, self.COR_TEXTO_PRIMARIO)
        tela.blit(prompt_surf, (area_resposta.x + 10, area_resposta.y + 10))
        
        self.botoes_dialogo_rects.clear()
        y_opcao = area_resposta.y + 40; x_opcao = area_resposta.x + 10
        for i, opcao in enumerate(self.opcoes_dialogo):
            texto_opcao = f"[{i+1}] {opcao.get_texto_opcao()}"; 
            opcao_rect = self.fonte_corpo.render(texto_opcao, True, self.COR_TEXTO_CORPO).get_rect(topleft=(x_opcao, y_opcao))
            
            if x_opcao + opcao_rect.width > area_resposta.right - 10:
                y_opcao += 30; x_opcao = area_resposta.x + 10; opcao_rect.topleft = (x_opcao, y_opcao)
            x_opcao += opcao_rect.width + 25
            
            self.botoes_dialogo_rects[opcao] = opcao_rect
            cor_texto = self.COR_TEXTO_PRIMARIO if opcao_rect.collidepoint(mouse_pos) else self.COR_TEXTO_CORPO
            opcao_surf = self.fonte_corpo.render(texto_opcao, True, cor_texto)
            tela.blit(opcao_surf, opcao_rect)

        # --- Seção 4: Rodapé de Ações ---
        voltar_abs_rect = self.botao_voltar_rect.move(self.rect.topleft)
        aceitar_abs_rect = self.botao_aceitar_rect.move(self.rect.topleft)
        
        cor_voltar = self.COR_BOTAO_VOLTAR_HOVER if voltar_abs_rect.collidepoint(mouse_pos) else self.COR_BOTAO_VOLTAR
        pygame.draw.rect(tela, cor_voltar, voltar_abs_rect, border_radius=8)
        voltar_surf = self.fonte_h2.render("Voltar", True, (255,255,255))
        tela.blit(voltar_surf, (voltar_abs_rect.centerx - voltar_surf.get_width()/2, voltar_abs_rect.centery - voltar_surf.get_height()/2))

        cor_aceitar = self.COR_BOTAO_ACEITAR_HOVER if aceitar_abs_rect.collidepoint(mouse_pos) else self.COR_BOTAO_ACEITAR
        pygame.draw.rect(tela, cor_aceitar, aceitar_abs_rect, border_radius=8)
        aceitar_surf = self.fonte_h2.render("Aceitar Contrato", True, (255,255,255))
        tela.blit(aceitar_surf, (aceitar_abs_rect.centerx - aceitar_surf.get_width()/2, aceitar_abs_rect.centery - aceitar_surf.get_height()/2))
        
    def tratar_eventos_conteudo(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_aceitar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_aceitar(self.projeto); self.deve_fechar = True; return
                if self.botao_voltar_rect.move(self.rect.topleft).collidepoint(evento.pos):
                    self.callback_voltar(); self.deve_fechar = True; return
                
                for opcao, rect in self.botoes_dialogo_rects.items():
                    if rect.collidepoint(evento.pos):
                        self.callback_enviar_mensagem(self.projeto, opcao)
                        if opcao.get_efeito() is not None and "REVELAR_DETALHES" in opcao.get_efeito():
                            id_no = opcao.get_id_no_destino()
                            no = self.serviceNo.buscar_proximo_no(id_no)
                            detalhe_tecnico = no.get_texto_npc()
                            self.service.atualizar_detalhes(self.jogador.get_id_jogador(),self.projeto.get_id_projeto(),detalhe_tecnico)
                        else:
                            pass
                        self.deve_fechar = True; return

    def tratar_eventos(self, eventos):
        super().tratar_eventos(eventos)
        self.tratar_eventos_conteudo(eventos)

    def update(self, dt):
        pass
