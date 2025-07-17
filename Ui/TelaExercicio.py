# Ui/TelaExercicio.py

import pygame
from Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl

class TelaExercicio:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont('Arial', 24)
        self.fonte_pequena = pygame.font.SysFont('Arial', 18)
        self.exercicio_service = ExercicioServiceImpl()
        self.exercicios = []
        self.exercicio_selecionado = None
        self.input_ativo = False
        self.resposta_usuario = ""
        self.resultado = ""
        self.caixa_input = pygame.Rect(50, 400, 400, 40)

    def carregar_exercicios(self, id_fase):
        self.exercicios = self.exercicio_service.listar_exercicios_por_fase(id_fase)
        self.exercicio_selecionado = None
        self.resposta_usuario = ""
        self.resultado = ""

    def desenhar(self, tela):
        tela.fill((30, 30, 30))

        y = 50
        tela.blit(self.fonte.render("Escolha um exercício:", True, (255, 255, 255)), (50, 10))
        for i, exercicio in enumerate(self.exercicios):
            cor = (200, 255, 200) if exercicio == self.exercicio_selecionado else (200, 200, 255)
            texto = f"{i+1}. {exercicio.get_tipo().capitalize()} | Dica: {exercicio.get_dicas()}"
            pygame.draw.rect(tela, cor, (40, y, 500, 30), 0)
            tela.blit(self.fonte_pequena.render(texto, True, (0, 0, 0)), (50, y + 5))
            y += 40

        # Se algum exercício foi selecionado, mostra o enunciado e input de resposta
        if self.exercicio_selecionado:
            y += 10
            tela.blit(self.fonte.render("Enunciado:", True, (255, 255, 0)), (50, y))
            y += 30
            tela.blit(self.fonte_pequena.render(self.exercicio_selecionado.get_dicas(), True, (255, 255, 255)), (50, y))

            # Caixa de input para resposta
            pygame.draw.rect(tela, (255, 255, 255), self.caixa_input, 2)
            resp_surface = self.fonte_pequena.render(self.resposta_usuario, True, (255, 255, 255))
            tela.blit(resp_surface, (self.caixa_input.x + 5, self.caixa_input.y + 10))

            # Resultado da verificação (após responder)
            if self.resultado:
                tela.blit(self.fonte.render(self.resultado, True, (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)), (50, self.caixa_input.y + 50))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Selecionar exercício pelo clique
                y_ref = 50
                for i, exercicio in enumerate(self.exercicios):
                    if 40 <= x <= 540 and y_ref <= y <= y_ref + 30:
                        self.exercicio_selecionado = exercicio
                        self.input_ativo = True
                        self.resposta_usuario = ""
                        self.resultado = ""
                    y_ref += 40
                # Ativar input se clicar na caixa
                if self.caixa_input.collidepoint(x, y):
                    self.input_ativo = True

            if evento.type == pygame.KEYDOWN and self.input_ativo:
                if evento.key == pygame.K_RETURN:
                    # Enviar resposta e verificar
                    if self.exercicio_selecionado:
                        correta = self.exercicio_service.verificar_resposta(
                            self.exercicio_selecionado.get_id_exercicio(),
                            self.resposta_usuario
                        )
                        self.resultado = "Resposta Correta!" if correta else "Resposta Incorreta!"
                        self.input_ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    self.resposta_usuario = self.resposta_usuario[:-1]
                else:
                    # Adiciona caracter digitado (limite simples)
                    if len(self.resposta_usuario) < 80 and evento.unicode.isprintable():
                        self.resposta_usuario += evento.unicode

