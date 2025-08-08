import pygame
from datetime import datetime
from UI.TelaInicio import TelaInicio
from UI.TelaSave import TelaSave
from UI.TelaCriarJogador import TelaCriarJogador
from UI.TelaExercicio import TelaExercicio
from UI.TelaResultado import TelaResultado
from UI.TelaIntroducaoTopico import TelaIntroducaoTopico
from Service.Impl.FaseServiceImpl import FaseServiceImpl
from Service.Impl.SaveServiceImpl import SaveServiceImpl
from Service.Impl.JogadorServiceImpl import JogadorServiceImpl
from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(300, 30)
        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura, self.altura = self.tela.get_size()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Python Dev Tycoon")

        # Serviços
        self.fase_service = FaseServiceImpl()
        self.save_service = SaveServiceImpl()
        self.jogador_service = JogadorServiceImpl()

        # Estado do jogo
        self.save_atual = None
        self.jogador_atual = None
        self.fase_atual = 0
        self.id_fases = [1, 2, 3, 4, 5, 6, 7, 8]  # IDs das fases no banco de dados
        self.nome_topico_atual = ""
        self.tempo_inicio_jogo = 0

        # Assets
        self.fundo_principal = pygame.image.load("assets/TelaJogoIniciante.png")
        self.fundo_principal = pygame.transform.scale(self.fundo_principal, (self.largura, self.altura))

        # Telas
        self.tela_atual = "inicio"
        self.tela_inicio = TelaInicio(
            self.largura, 
            self.altura, 
            callback_iniciar=self.ir_para_tela_save
        )
        self.tela_save = None
        self.tela_criar_jogador = None
        self.tela_introducao = None
        self.tela_exercicio = None
        self.tela_resultado = None
        self.tela_exercicio_salva = None

    def ir_para_tela_save(self):
        """Navega para a tela de seleção de save"""
        self.tela_save = TelaSave(
            self.largura,
            self.altura,
            save_service=self.save_service,
            jogador_service=self.jogador_service,
            callback_selecionar_slot=self.carregar_save,
            callback_criar_jogador=self.ir_para_criacao_jogador
        )
        self.tela_atual = "save"

    def ir_para_criacao_jogador(self):
        """Navega para a tela de criação de novo jogador"""
        self.tela_criar_jogador = TelaCriarJogador(
            self.largura,
            self.altura,
            callback_confirmar=self.jogador_criado,
            callback_voltar=self.ir_para_tela_save
        )
        self.tela_atual = "criar_jogador"

    def jogador_criado(self, nome_jogador):
        """Callback quando um novo jogador é criado"""
        # Cria o jogador e o save associado
        #avisar gustavo
        id_novo_jogador = self.jogador_service.criar_jogador(nome_jogador)
        self.jogador_atual = self.jogador_service.buscar_jogador_por_id(id_novo_jogador)
        data_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        novo_save = self.save_service.adicionar_save(
            id_jogador=id_novo_jogador,
            data_save=data_formatada,
            tempo_jogo=0,
        )
        
        #não sei se essa função buscar_save_por_id é para fazer oq? tava dando erro
        #self.save_atual = self.save_service.buscar_save_por_id(novo_save)
        self.tempo_inicio_jogo = pygame.time.get_ticks()
        
        # Inicia o jogo
        self.carregar_progresso()
        self.mostrar_introducao()

    def carregar_save(self, save):
        """Carrega um save existente"""
        self.save_atual = save
        self.jogador_atual = self.jogador_service.buscar_jogador_por_id(save.get_id_jogador())
        self.tempo_inicio_jogo = pygame.time.get_ticks() - (save.get_tempo_jogo() * 1000)
        self.carregar_progresso()
        self.mostrar_introducao()

    def carregar_progresso(self):
        # Igual ao SEU código que funciona!
        
        progresso_service = ProgressoFaseServiceImpl()
        ultima_fase = progresso_service.progresso_persistencia.buscar_ultima_fase_do_jogador(self.jogador_atual.get_id_jogador())
        if ultima_fase and ultima_fase in self.id_fases:
            self.fase_atual = self.id_fases.index(ultima_fase)
        else:
            self.fase_atual = 0


    def salvar_progresso(self):
        """Atualiza o save com o progresso atual"""
        if self.save_atual:
            tempo_de_jogo = (pygame.time.get_ticks() - self.tempo_inicio_jogo) // 1000
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato legível

            # Atualiza tempo e data
            self.save_atual.set_tempo_jogo(tempo_de_jogo)
            self.save_atual.set_data_save(data_atual)

            # Atualiza o save no service
            self.save_service.atualizar_save(self.save_atual)
            self.jogador_service.avancar_fase_jogador(self.jogador_atual.get_id_jogador())

    def mostrar_introducao(self, tela_salva=None):
        id_fase = self.id_fases[self.fase_atual]
        fase = self.fase_service.buscar_fase_por_id(id_fase)
        nome_topico = fase.get_topico()
        descricao = fase.get_introducao()
        self.nome_topico_atual = nome_topico

        # --- PASSA O JOGADOR ---
        self.tela_introducao = TelaIntroducaoTopico(
            self.largura,
            self.altura,
            nome_topico,
            descricao,
            on_confirmar=self.iniciar_exercicio,
            jogador=self.jogador_atual  # <--- AQUI!
        )
        self.tela_atual = "introducao"
        if tela_salva:
            self.tela_exercicio_salva = tela_salva

    def iniciar_exercicio(self):
        q_x = int(self.largura * 0.25) + int(self.largura * 0.54) - 90
        q_y = int(self.altura * 0.13) + 10
        q_centro = (q_x + 15, q_y + 15)
        pygame.mouse.set_pos(q_centro)
        if self.tela_exercicio_salva is not None:
            self.tela_exercicio = self.tela_exercicio_salva
            self.tela_exercicio_salva = None
        else:
            self.tela_exercicio = TelaExercicio(
            self.largura,
            self.altura,
            self.nome_topico_atual,
            total_fases=len(self.id_fases),
            fases_concluidas=self.fase_atual,
            callback_rever_introducao=self.mostrar_introducao,
            jogador=self.jogador_atual,
            id_fase=self.id_fases[self.fase_atual]
        )
        # NÃO CHAME self.tela_exercicio.carregar_exercicios AQUI!

        self.tela_atual = "exercicio"


    def processar_resultado_exercicio(self):
        """Processa o resultado do exercício e mostra a tela de resultado"""
        acertou_minimo = self.tela_exercicio.acertos >= 4
        
        self.tela_resultado = TelaResultado(
            self.largura,
            self.altura,
            self.tela_exercicio.acertos,
            self.tela_exercicio.erros,
            len(self.tela_exercicio.exercicios),
            callback_avancar=self.avancar_fase,
            callback_reiniciar=self.reiniciar_exercicio,
            #callback_voltar=self.voltar_para_save,
            acertou_minimo=acertou_minimo
        )
        
        if acertou_minimo:
            self.salvar_progresso()
            
        self.tela_atual = "resultado"

    def avancar_fase(self):
        """Avança para a próxima fase do jogo"""
        if self.fase_atual < len(self.id_fases) - 1:
            self.fase_atual += 1
            self.mostrar_introducao()
        else:
            self.tela_atual = "fim"

    def reiniciar_exercicio(self):
        from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
        progresso_service = ProgressoFaseServiceImpl()
        progresso_service.deletar_progresso_por_jogador_fase(
            self.jogador_atual.get_id_jogador(),
            self.id_fases[self.fase_atual]
        )
        self.tela_exercicio_salva = None
        self.iniciar_exercicio()


    def voltar_para_save(self):
        """Volta para a tela de seleção de save"""
        self.salvar_progresso()
        self.ir_para_tela_save()

    def mostrar_tela_fim(self):
        """Mostra a tela de conclusão do jogo"""
        self.tela.fill((30, 40, 50))
        
        # Mensagem principal
        font = pygame.font.SysFont('Arial', 48, bold=True)
        texto = font.render("Parabéns! Você concluiu todos os tópicos!", True, (100, 255, 100))
        self.tela.blit(texto, (self.largura//2 - texto.get_width()//2, self.altura//2 - 60))
        
        # Estatísticas
        font_pequena = pygame.font.SysFont('Arial', 24)
        tempo_total = (pygame.time.get_ticks() - self.tempo_inicio_jogo) // 1000
        horas, minutos = tempo_total // 3600, (tempo_total % 3600) // 60
        stats_text = f"Tempo total: {horas}h {minutos}m | Tópicos completos: {len(self.id_fases)}"
        stats = font_pequena.render(stats_text, True, (200, 200, 200))
        self.tela.blit(stats, (self.largura//2 - stats.get_width()//2, self.altura//2 + 10))
        
        # Botão para voltar
        botao_voltar = pygame.Rect(self.largura//2 - 100, self.altura//2 + 80, 200, 50)
        pygame.draw.rect(self.tela, (70, 120, 200), botao_voltar, border_radius=5)
        texto_voltar = font_pequena.render("Menu Principal", True, (255, 255, 255))
        self.tela.blit(texto_voltar, (botao_voltar.centerx - texto_voltar.get_width()//2, 
                                    botao_voltar.centery - texto_voltar.get_height()//2))
        
        # Verifica clique no botão
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if botao_voltar.collidepoint(mouse_pos) and mouse_click[0]:
            self.voltar_para_save()

    def executar(self):
        """Loop principal do jogo"""
        rodando = True
        while rodando:
            dt = self.clock.tick(60)  # Limita a 60 FPS e obtém delta time
            
            # Trata eventos
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

            if not rodando:
                break

            # Renderização condicional das telas
            if self.tela_atual == "inicio":
                self.tela_inicio.tratar_eventos(eventos)
                self.tela_inicio.desenhar(self.tela)

            elif self.tela_atual == "save":
                resultado = self.tela_save.tratar_eventos(eventos)
                if resultado == "voltar":
                    self.tela_atual = "inicio"
                self.tela_save.desenhar(self.tela)

            elif self.tela_atual == "criar_jogador":
                self.tela_criar_jogador.tratar_eventos(eventos)
                self.tela_criar_jogador.atualizar(dt)
                self.tela_criar_jogador.desenhar(self.tela)

            elif self.tela_atual in ["introducao", "exercicio", "resultado"]:
                self.tela.blit(self.fundo_principal, (0, 0))  # Fundo fixo

                if self.tela_atual == "introducao":
                    self.tela_introducao.tratar_eventos(eventos)
                    self.tela_introducao.desenhar(self.tela)

                elif self.tela_atual == "exercicio":
                    self.tela_exercicio.tratar_eventos(eventos)
                    self.tela_exercicio.desenhar(self.tela)
                    if hasattr(self.tela_exercicio, 'finalizado') and self.tela_exercicio.finalizado:
                        self.processar_resultado_exercicio()

                elif self.tela_atual == "resultado":
                    self.tela_resultado.tratar_eventos(eventos)
                    self.tela_resultado.desenhar(self.tela)

            elif self.tela_atual == "fim":
                self.mostrar_tela_fim()

            pygame.display.flip()

        pygame.quit()