import pygame
from UI.TelaInicio import TelaInicio
from UI.TelaSave import TelaSave
from UI.TelaExercicio import TelaExercicio
from UI.TelaResultado import TelaResultado
from UI.TelaIntroducaoTopico import TelaIntroducaoTopico
from Service.Impl.FaseServiceImpl import FaseServiceImpl
from Service.Impl.SaveServiceImpl import SaveServiceImpl

class GameManager:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura, self.altura = self.tela.get_size()
        self.clock = pygame.time.Clock()

        self.id_jogador = 1
        self.fase_service = FaseServiceImpl()
        self.save_service = SaveServiceImpl()

        self.id_fases = [1, 2, 3, 4, 5, 6, 7, 8]
        self.fase_atual = 0
        self.nome_topico_atual = ""

        self.fundo_principal = pygame.image.load("assets/TelaJogoIniciante.png")
        self.fundo_principal = pygame.transform.scale(self.fundo_principal, (self.largura, self.altura))

        self.tela_atual = "inicio"
        self.tela_inicio = TelaInicio(self.largura, self.altura, callback_iniciar=self.mostrar_save)
        self.tela_save = None
        self.tela_introducao = None
        self.tela_exercicio = None
        self.tela_resultado = None
        self.tela_exercicio_salva = None

    def mostrar_save(self):
        self.tela_save = TelaSave(
            self.largura, self.altura,
            id_jogador=self.id_jogador,
            save_service=self.save_service,
            callback_selecionar_slot=self.iniciar_jogo_com_save
        )
        self.tela_atual = "save"

    def iniciar_jogo_com_save(self, id_save_ou_slot):
        print(f"Iniciando com save/slot: {id_save_ou_slot}")
        self.mostrar_introducao()

    def mostrar_introducao(self, tela_salva=None):
        id_fase = self.id_fases[self.fase_atual]
        fase = self.fase_service.buscar_fase_por_id(id_fase)
        nome = fase.get_topico()
        descricao = fase.get_introducao()
        self.nome_topico_atual = nome
        self.tela_introducao = TelaIntroducaoTopico(
            self.largura, self.altura, nome, descricao,
            on_confirmar=self.iniciar_exercicio
        )
        self.tela_atual = "introducao"
        if tela_salva:
            self.tela_exercicio_salva = tela_salva

    def iniciar_exercicio(self):
        if self.tela_exercicio_salva is not None:
            self.tela_exercicio = self.tela_exercicio_salva
            self.tela_exercicio_salva = None
        else:
            self.tela_exercicio = TelaExercicio(
                self.largura, self.altura,
                self.nome_topico_atual,
                total_fases=len(self.id_fases), fases_concluidas=self.fase_atual,
                callback_rever_introducao=self.mostrar_introducao
            )
            self.tela_exercicio.carregar_exercicios(id_fase=self.id_fases[self.fase_atual])
        self.tela_atual = "exercicio"

    def avancar(self):
        if self.fase_atual < len(self.id_fases) - 1:
            self.fase_atual += 1
            self.mostrar_introducao()
        else:
            self.tela_atual = "fim"

    def reiniciar(self):
        self.tela_exercicio_salva = None
        self.iniciar_exercicio()

    def executar(self):
        rodando = True
        while rodando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

            if not rodando:
                break

            if self.tela_atual == "inicio":
                self.tela_inicio.tratar_eventos(eventos)
                self.tela_inicio.desenhar(self.tela)

            elif self.tela_atual == "save":
                self.tela_save.tratar_eventos(eventos)
                self.tela_save.desenhar(self.tela)

            elif self.tela_atual in ["introducao", "exercicio", "resultado"]:
                self.tela.blit(self.fundo_principal, (0, 0))  # fundo fixo

                if self.tela_atual == "introducao":
                    self.tela_introducao.tratar_eventos(eventos)
                    self.tela_introducao.desenhar(self.tela)

                elif self.tela_atual == "exercicio":
                    self.tela_exercicio.tratar_eventos(eventos)
                    self.tela_exercicio.desenhar(self.tela)
                    if self.tela_exercicio.finalizado:
                        acertou_minimo = self.tela_exercicio.acertos >= 4
                        self.tela_resultado = TelaResultado(
                            self.largura, self.altura,
                            self.tela_exercicio.acertos, self.tela_exercicio.erros, len(self.tela_exercicio.exercicios),
                            callback_avancar=self.avancar,
                            callback_reiniciar=self.reiniciar,
                            acertou_minimo=acertou_minimo
                        )
                        self.tela_atual = "resultado"

                elif self.tela_atual == "resultado":
                    self.tela_resultado.tratar_eventos(eventos)
                    self.tela_resultado.desenhar(self.tela)

            elif self.tela_atual == "fim":
                self.tela.fill((30, 30, 30))
                font = pygame.font.SysFont('Arial', 36)
                texto = font.render("Parabéns! Você concluiu todos os tópicos!", True, (80, 255, 80))
                self.tela.blit(texto, (self.largura//2 - texto.get_width()//2, self.altura//2))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
