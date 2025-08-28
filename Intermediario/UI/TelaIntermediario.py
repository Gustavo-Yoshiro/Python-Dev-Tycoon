import pygame

class TelaIntermediario:
    def __init__(self, callback_exercicios, callback_freelancer, callback_loja):
        self.largura_tela, self.altura_tela = pygame.display.get_surface().get_size()

        self.callbacks = {
            "Exercícios": callback_exercicios,
            "Freelance": callback_freelancer,
            "Loja": callback_loja
        }

        self.fonte_botao = pygame.font.SysFont("Arial", 26, bold=True)

        # Botões alinhados à direita e centralizados verticalmente
        largura_botao = 250
        altura_botao = 55
        espacamento = 15
        margem_direita = 50

        x_pos = (self.largura_tela // 2) + 100  # 100 pixels à direita do centro

        total_altura = (altura_botao * 3) + (espacamento * 2)
        y_inicio = (self.altura_tela - total_altura) // 2

        self.botoes_rect = {
            "Exercícios": pygame.Rect(x_pos, y_inicio, largura_botao, altura_botao),
            "Freelance": pygame.Rect(x_pos, y_inicio + altura_botao + espacamento, largura_botao, altura_botao),
            "Loja": pygame.Rect(x_pos, y_inicio + (altura_botao + espacamento) * 2, largura_botao, altura_botao)
        }

        self.cooldown_clique = 100
        self.ultimo_clique_time = 0
        self.deve_fechar = False

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()

        for texto, rect in self.botoes_rect.items():
            if rect.collidepoint(mouse_pos):
                cor_fundo = (0, 100, 200, 220)
                cor_borda = (0, 180, 255)
                cor_texto = (255, 255, 255)
            else:
                cor_fundo = (0, 80, 160, 180)
                cor_borda = (0, 120, 200)
                cor_texto = (220, 220, 220)

            botao_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(botao_surface, cor_fundo, (0, 0, rect.width, rect.height), border_radius=12)
            pygame.draw.rect(botao_surface, cor_borda, (0, 0, rect.width, rect.height), width=2, border_radius=12)

            texto_render = self.fonte_botao.render(texto, True, cor_texto)
            texto_x = (rect.width - texto_render.get_width()) // 2
            texto_y = (rect.height - texto_render.get_height()) // 2
            botao_surface.blit(texto_render, (texto_x, texto_y))

            tela.blit(botao_surface, rect.topleft)

            if rect.collidepoint(mouse_pos):
                brilho_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                pygame.draw.rect(brilho_surface, (255, 255, 255, 60), (0, 0, rect.width, rect.height), border_radius=12)
                tela.blit(brilho_surface, rect.topleft)

    def tratar_eventos(self, eventos):
        tempo_atual = pygame.time.get_ticks()
        evento_consumido = False

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if tempo_atual - self.ultimo_clique_time < self.cooldown_clique:
                    continue

                mouse_pos = pygame.mouse.get_pos()

                for texto, rect in self.botoes_rect.items():
                    if rect.collidepoint(mouse_pos):
                        self.ultimo_clique_time = tempo_atual
                        self._feedback_clique_rapido(rect)
                        self.callbacks[texto]()
                        self.deve_fechar = True
                        evento_consumido = True
                        break

                evento_consumido = True

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.deve_fechar = True
                    evento_consumido = True

        return evento_consumido

    def _feedback_clique_rapido(self, rect):
        surface = pygame.display.get_surface()
        clique_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(clique_surface, (255, 255, 255, 80), (0, 0, rect.width, rect.height), border_radius=12)
        surface.blit(clique_surface, rect.topleft)
        pygame.display.update(rect)

    def update(self, dt):
        pass

    def deve_fechar(self):
        return self.deve_fechar