import pygame
from datetime import datetime
from Iniciante.UI.TelaInicio import TelaInicio
from Iniciante.UI.TelaSave import TelaSave
from Iniciante.UI.TelaCriarJogador import TelaCriarJogador
from Iniciante.UI.TelaExercicio import TelaExercicio
from Iniciante.UI.TelaResultado import TelaResultado
from Iniciante.UI.TelaIntroducaoTopico import TelaIntroducaoTopico
from Iniciante.Service.Impl.FaseServiceImpl import FaseServiceImpl
from Iniciante.Service.Impl.SaveServiceImpl import SaveServiceImpl
from Iniciante.Service.Impl.JogadorServiceImpl import JogadorServiceImpl
from Iniciante.Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
from Iniciante.Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
from Intermediario.UI.TelaLoja import TelaLoja
from Intermediario.Service.Impl.LojaServiceImpl import LojaServiceImpl
from Iniciante.UI.TelaMiniPythonHero import TelaMiniPythonHero




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
        self.exercicio_service = ExercicioServiceImpl()
        self.progresso_service = ProgressoFaseServiceImpl()
        
        #mini games
        self.tela_minigame = None
        self._ultimo_resultado_ok = False
        self._resultado_pendente = None
        self.MINIGAME_PASS_SCORE = 250

        # bônus acumulado pelas estrelas do Iniciante (fases 1..8)
        self.bonus_backend_iniciante = 0

        #tela loja
        self.tela_loja = None
        self.loja_service = LojaServiceImpl()
        self._ultimo_tick_loja = pygame.time.get_ticks()

        # Estado do jogo
        self.save_atual = None
        self.jogador_atual = None
        self.fase_atual = 0
        self.id_fases = [1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16]  # IDs das fases no banco de dados
        self.nome_topico_atual = ""
        self.tempo_inicio_jogo = 0

        # Assets
        self.fundo_principal = pygame.image.load("assets/TelaJogoIniciante.png")
        self.fundo_principal = pygame.transform.scale(self.fundo_principal, (self.largura, self.altura))

        self.bg_click_rect = pygame.Rect(0, 0, self.largura, self.altura)

        #self.reopen_hotspot = pygame.Rect(self.largura - 180, self.altura - 80, 160, 60)

        self.reopen_hotspot = pygame.Rect(
            int(self.largura * 0.40), 
            int(self.altura * 0.36),   
            250,  # largura
            230   # altura
        )
        self.debug_hotspot = False
        # Hotspot do notebook em PORCENTAGEM da tela (ajuste fino depois)
        #self.hotspot_pct = pygame.Rect(0.62, 0.38, 0.18, 0.15)  # x%, y%, w%, h%
        #self.debug_hotspot = False  # True = desenha contorno pra calibrar

        # cooldown pra evitar reabrir no mesmo clique
        self._last_closed_at = 0
        self.reopen_cooldown_ms = 250
        self.ui_block_until_ms = 0

        # flags pra detectar “acabou de fechar”
        self._was_intro_visible = True
        self._was_ex_visible = True
        self._was_res_visible = True
        
        #--------------------------------porta saida------------------#
        # HOTSPOT DA PORTA (sair do jogo) – valores iniciais; você ajusta depois
        self.exit_hotspot = pygame.Rect(
            int(self.largura * 0.08),  # X (esquerda)
            int(self.altura  * 0.50),  # Y (meio pra baixo)
            140,                       # largura inicial
            220                        # altura inicial
        )
        self.debug_exit_hotspot = False # True p/ ver o retângulo enquanto calibra

        #---------------------------------------------------------------#
        
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

    #alem do exit da para usar em outros se precisar
    def algum_painel_visivel(self):
        if self.tela_atual == "introducao" and self.tela_introducao:
            return self.tela_introducao.painel_visivel
        if self.tela_atual == "exercicio" and self.tela_exercicio:
            return self.tela_exercicio.prompt_visivel
        if self.tela_atual == "resultado" and self.tela_resultado:
            return self.tela_resultado.painel_visivel
        return False


    def ir_para_loja(self):
        self.tela_loja = TelaLoja(
            self.largura,
            self.altura,
            jogador=self.jogador_atual,
            loja_service=self.loja_service,
            callback_voltar=self.mostrar_introducao
        )
        self.tela_atual = "loja"


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

    def mostrar_introducao(self, tela_salva=None):
        id_fase = self.id_fases[self.fase_atual]
        fase = self.fase_service.buscar_fase_por_id(id_fase)

        # ✅ Blindagem: evita quebrar se a fase não existir no BD (ex.: transição 8→9 sem cadastro)
        if fase is None:
            print(f"[WARN] Fase {id_fase} não encontrada no banco. Encerrando para evitar crash.")
            self.tela_atual = "fim"
            return

        nome_topico = fase.get_topico()
        descricao = fase.get_introducao()
        self.nome_topico_atual = nome_topico

        self.tela_introducao = TelaIntroducaoTopico(
            self.largura,
            self.altura,
            nome_topico,
            descricao,
            on_confirmar=self.iniciar_exercicio,
            jogador=self.jogador_atual
        )
        self.tela_atual = "introducao"
        #self.iniciar_minigame()
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
            # Ajusta o progresso por categoria (0–8 iniciante, 0–8 intermediário)
            if self.fase_atual < 8:  # fases iniciante
                total_fases = 8
                fases_concluidas = self.fase_atual
            else:  # fases intermediário
                total_fases = 8
                fases_concluidas = self.fase_atual - 8

            self.tela_exercicio = TelaExercicio(
                self.largura,
                self.altura,
                self.nome_topico_atual,
                total_fases=total_fases,
                fases_concluidas=fases_concluidas,
                callback_rever_introducao=self.mostrar_introducao,
                jogador=self.jogador_atual,
                id_fase=self.id_fases[self.fase_atual]
            )
            """
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
        """
        # NÃO CHAME self.tela_exercicio.carregar_exercicios AQUI!

        self.tela_atual = "exercicio"


    def _pos_resultado(self):
        # Se foi aprovado e é Iniciante (fases 1..8), roda minigame
        fase_id = self.id_fases[self.fase_atual]
        if self._ultimo_resultado_ok and 1 <= fase_id <= 8:
            self.iniciar_minigame()
        else:
            self.avancar_fase()

    def iniciar_minigame(self):
        id_fase = self.id_fases[self.fase_atual]
        # pega o nome do tópico que você já salvou em self.nome_topico_atual
        self.tela_minigame = TelaMiniPythonHero(
            largura=self.largura,
            altura=self.altura,
            jogador=self.jogador_atual,
            id_fase=id_fase,
            nome_topico=self.nome_topico_atual,
            on_finish=self.finalizar_minigame
        )
        self.tela_atual = "minigame"

    def finalizar_minigame(self, score, stars):
        # bônus por estrelas (mantém)
        self.bonus_backend_iniciante += {0:0, 1:1, 2:2, 3:3}[int(stars)]

        # --- NOVO: contar e PERSISTIR o minigame como 5ª questão ---
        mg_pass = (score >= self.MINIGAME_PASS_SCORE)
        if self.tela_exercicio:
            total_q = len(self.tela_exercicio.exercicios)  # normalmente 4

            # atualiza contadores em memória
            if mg_pass:
                self.tela_exercicio.acertos += 1
            else:
                self.tela_exercicio.erros += 1

            # salva no BD/arquivo: indice_exercicio = 5 (MG_DONE)
            try:
                self.progresso_service.salvar_ou_atualizar_progresso(
                    jogador=self.jogador_atual,
                    id_fase=self.id_fases[self.fase_atual],
                    indice_exercicio=total_q + 1,  # 5 = minigame concluído
                    acertos=self.tela_exercicio.acertos,
                    erros=self.tela_exercicio.erros,
                    resposta_parcial="MG_DONE"
                )
            except Exception as e:
                print("[WARN] Falha ao salvar progresso do minigame:", e)
        # --- FIM NOVO ---

        # Se estávamos esperando o minigame como 5ª questão, mostra o Resultado já somando o MG
        if self._resultado_pendente:
            self._resultado_pendente = None

            total_final   = (len(self.tela_exercicio.exercicios) + 1) if self.tela_exercicio else 5
            acertou_minimo = (self.tela_exercicio.acertos >= 4)  # regra 4 de 5
            self._ultimo_resultado_ok = acertou_minimo

            if acertou_minimo:
                self.salvar_progresso()

            self.tela_resultado = TelaResultado(
                self.largura,
                self.altura,
                self.tela_exercicio.acertos,
                self.tela_exercicio.erros,
                total_final,
                callback_avancar=self.avancar_fase,      # já fez o MG → avança direto
                callback_reiniciar=self.reiniciar_exercicio,
                acertou_minimo=acertou_minimo,
                jogador=self.jogador_atual
            )
            self.tela_atual = "resultado"
            return

        # Fallback
        self.avancar_fase()





    def processar_resultado_exercicio(self):
        """Para fases 1..8: MG é a 5ª questão. Se já foi feito (índice >= 5), não reabrir MG."""
        fase_id = self.id_fases[self.fase_atual]

        if 1 <= fase_id <= 8:
            total_q = len(self.tela_exercicio.exercicios) if self.tela_exercicio else 4
            idx_atual = getattr(self.tela_exercicio, "indice_atual", total_q)

            # Se já registramos o MG como 'feito' (índice >= 5), vai direto para o Resultado.
            if idx_atual >= total_q + 1:
                acertou_minimo = (self.tela_exercicio.acertos >= 4)  # 4 de 5
                self._ultimo_resultado_ok = acertou_minimo

                self.tela_resultado = TelaResultado(
                    self.largura,
                    self.altura,
                    self.tela_exercicio.acertos,
                    self.tela_exercicio.erros,
                    total_q + 1,  # mostra 5 no total
                    callback_avancar=self.avancar_fase,      # MG já feito → avança direto
                    callback_reiniciar=self.reiniciar_exercicio,
                    acertou_minimo=acertou_minimo,
                    jogador=self.jogador_atual
                )

                if acertou_minimo:
                    self.salvar_progresso()

                self.tela_atual = "resultado"
                return

            # Terminou as 4 questões e MG ainda não foi feito → chama MG
            self._resultado_pendente = {
                "acertos": self.tela_exercicio.acertos,
                "erros":   self.tela_exercicio.erros,
                "total":   total_q  # 4; o MG vira a 5ª
            }
            self.iniciar_minigame()
            return

        # Intermediário (fases > 8): fluxo antigo
        acertou_minimo = self.tela_exercicio.acertos >= 4
        self._ultimo_resultado_ok = acertou_minimo

        self.tela_resultado = TelaResultado(
            self.largura,
            self.altura,
            self.tela_exercicio.acertos,
            self.tela_exercicio.erros,
            len(self.tela_exercicio.exercicios),
            callback_avancar=self._pos_resultado,
            callback_reiniciar=self.reiniciar_exercicio,
            acertou_minimo=acertou_minimo,
            jogador=self.jogador_atual
        )

        if acertou_minimo:
            self.salvar_progresso()

        self.tela_atual = "resultado"



    def avancar_fase(self):
        if self.fase_atual < len(self.id_fases) - 1:
            # Fase que está sendo concluída AGORA (sem mexer na tua lógica original)
            fase_concluida = self.id_fases[self.fase_atual]

            total_exercicios = len(self.exercicio_service.listar_exercicios_por_fase(fase_concluida))
            ultima_fase_no_save = self.progresso_service.progresso_persistencia.buscar_ultima_fase_do_jogador(
                self.jogador_atual.get_id_jogador()
            )

            # ✅ Regras de bônus preservadas
            if (fase_concluida == ultima_fase_no_save and
                self.progresso_service.fase_ja_concluida(
                    self.jogador_atual.get_id_jogador(),
                    fase_concluida,
                    total_exercicios
                )):
                if fase_concluida == 8:
                    backend_atual = self.jogador_atual.get_backend()
                    ganho = 10 + self.bonus_backend_iniciante  # base + bônus das estrelas
                    self.jogador_atual.set_backend(backend_atual + ganho)
                    self.jogador_service.atualizar_jogador(self.jogador_atual)
                    # reseta o acumulador para não vazar pro próximo ciclo
                    self.bonus_backend_iniciante = 0

                elif 9 <= fase_concluida <= 16:
                    backend_atual = self.jogador_atual.get_backend()
                    self.jogador_atual.set_backend(backend_atual + 5)
                    self.jogador_service.atualizar_jogador(self.jogador_atual)

            # ✅ Verifica a PRÓXIMA fase no BD ANTES de avançar o índice local
            proximo_idx = self.fase_atual + 1
            proxima_fase_id = self.id_fases[proximo_idx]

            # se a próxima fase não existir no BD, não avança e evita o crash do get_topico()
            if self.fase_service.buscar_fase_por_id(proxima_fase_id) is None:
                print(f"[WARN] Próxima fase {proxima_fase_id} não cadastrada no banco. Encerrando para evitar crash.")
                self.tela_atual = "fim"
                return

            # ✅ Agora sim: avança em memória e no BD
            self.fase_atual = proximo_idx
            self.jogador_service.avancar_fase_jogador(self.jogador_atual.get_id_jogador())

            # ✅ Anti-revisita (mantido): cria/garante progresso 'stub' na NOVA fase
            self.progresso_service.salvar_ou_atualizar_progresso(
                jogador=self.jogador_atual,
                id_fase=proxima_fase_id,
                indice_exercicio=0,
                acertos=0,
                erros=0,
                resposta_parcial=""
            )

            # Vai pra introdução da nova fase (agora garantido existir)
            self.mostrar_introducao()
        else:
            self.tela_atual = "fim"





    def reiniciar_exercicio(self):
        from Iniciante.Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
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
            
            agora = pygame.time.get_ticks()
            if self.jogador_atual and agora - self._ultimo_tick_loja >= 1000:
                self._ultimo_tick_loja = agora

                itens_andamento = self.loja_service.listar_em_andamento(self.jogador_atual.get_id_jogador())
                for item in itens_andamento:
                    novo_tempo = max(0, item.get_duracao_segundos() - 1)
                    item.set_duracao_segundos(novo_tempo)

                    if novo_tempo <= 0:
                        self.loja_service.concluir_item(item.get_id_item())
                        print(f"[OK] Item concluído: {item.get_nome()} ({item.get_categoria()})")
                    else:
                        self.loja_service.atualizar_item(item)
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
            
            elif self.tela_atual == "minigame":
                # fundo (mantém teu background)
                self.tela.blit(self.fundo_principal, (0, 0))
                self.tela_minigame.tratar_eventos(eventos)
                self.tela_minigame.desenhar(self.tela)


            elif self.tela_atual == "criar_jogador":
                self.tela_criar_jogador.tratar_eventos(eventos)
                self.tela_criar_jogador.atualizar(dt)
                self.tela_criar_jogador.desenhar(self.tela)

            elif self.tela_atual in ["introducao", "exercicio", "resultado"]:
                # fundo
                self.tela.blit(self.fundo_principal, (0, 0))

                # === HOTSPOT DA PORTA (sair do jogo) ===
                self.exit_hotspot.update(
                    int(self.largura * 0.01),  # X
                    int(self.altura  * 0.25),  # Y
                    int(self.largura * 0.06),  # largura
                    int(self.altura  * 0.49)   # altura
                )

                if getattr(self, "debug_exit_hotspot", False):
                    eh = self.exit_hotspot
                    overlay2 = pygame.Surface((eh.w, eh.h), pygame.SRCALPHA)
                    pygame.draw.rect(overlay2, (0, 0, 0, 60), overlay2.get_rect(), border_radius=18)
                    pygame.draw.rect(overlay2, (255, 120, 120, 180), overlay2.get_rect(), width=2, border_radius=18)
                    self.tela.blit(overlay2, (eh.x, eh.y))
                # === FIM DO HOTSPOT DA PORTA ===
                # --- TOOLTIP DA PORTA ---
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not self.algum_painel_visivel() and self.exit_hotspot.collidepoint((mouse_x, mouse_y)):
                    font_tooltip = pygame.font.SysFont('Arial', 20, bold=True)
                    texto_tooltip = "Sair do jogo — seu progresso já está salvo"
                    txt_surface = font_tooltip.render(texto_tooltip, True, (255, 255, 255))

                    # fundo semi-transparente para o tooltip
                    bg_surface = pygame.Surface((txt_surface.get_width() + 12, txt_surface.get_height() + 6), pygame.SRCALPHA)
                    pygame.draw.rect(bg_surface, (0, 0, 0, 180), bg_surface.get_rect(), border_radius=6)

                    # posição (um pouco acima do mouse)
                    pos_x = mouse_x + 15
                    pos_y = mouse_y - txt_surface.get_height() - 10

                    self.tela.blit(bg_surface, (pos_x, pos_y))
                    self.tela.blit(txt_surface, (pos_x + 6, pos_y + 3))


                # === BOTÃO VISÍVEL DE REABRIR (só quando o painel daquela tela estiver fechado) ===
                mostrar_hotspot = False
                if self.tela_atual == "introducao":
                    mostrar_hotspot = (self.tela_introducao is not None and not self.tela_introducao.painel_visivel)
                elif self.tela_atual == "exercicio":
                    mostrar_hotspot = (self.tela_exercicio is not None and not self.tela_exercicio.prompt_visivel)
                elif self.tela_atual == "resultado":
                    mostrar_hotspot = (self.tela_resultado is not None and not self.tela_resultado.painel_visivel)

                if mostrar_hotspot:

                    # recalcula hotspot a cada frame para ser responsivo
                    self.reopen_hotspot.update(
                        int(self.largura * 0.40),  # X
                        int(self.altura  * 0.35),  # Y
                        int(self.largura * 0.16),  # largura
                        int(self.altura  * 0.16)   # altura
                    )
                    # (opcional) visualizar durante a calibração
                    if getattr(self, "debug_hotspot", False):
                        hs = self.reopen_hotspot
                        overlay = pygame.Surface((hs.w, hs.h), pygame.SRCALPHA)
                        pygame.draw.rect(overlay, (0, 0, 0, 60), overlay.get_rect(), border_radius=18)
                        pygame.draw.rect(overlay, (110, 190, 255, 180), overlay.get_rect(), width=2, border_radius=18)
                        self.tela.blit(overlay, (hs.x, hs.y))

                # 1) fluxo normal primeiro (aqui pode FECHAR)
                if self.tela_atual == "introducao":
                    vis_before = self.tela_introducao.painel_visivel
                    self.tela_introducao.tratar_eventos(eventos)
                    self.tela_introducao.desenhar(self.tela)
                    # marcou o instante em que acabou de fechar
                    if vis_before and not self.tela_introducao.painel_visivel:
                        self._last_closed_at = pygame.time.get_ticks()

                elif self.tela_atual == "exercicio":
                    vis_before = self.tela_exercicio.prompt_visivel
                    self.tela_exercicio.tratar_eventos(eventos)
                    self.tela_exercicio.desenhar(self.tela)
                    if vis_before and not self.tela_exercicio.prompt_visivel:
                        self._last_closed_at = pygame.time.get_ticks()
                    if hasattr(self.tela_exercicio, 'finalizado') and self.tela_exercicio.finalizado:
                        self.processar_resultado_exercicio()

                elif self.tela_atual == "resultado":
                    vis_before = self.tela_resultado.painel_visivel
                    self.tela_resultado.tratar_eventos(eventos)
                    self.tela_resultado.desenhar(self.tela)
                    if vis_before and not self.tela_resultado.painel_visivel:
                        self._last_closed_at = pygame.time.get_ticks()

                # 2) reabrir via HOTSPOT (canto inferior direito) com COOLDOWN e só no MOUSEBUTTONUP
                now = pygame.time.get_ticks()
                if now - self._last_closed_at >= self.reopen_cooldown_ms:
                    for ev in eventos:
                        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.reopen_hotspot.collidepoint(ev.pos):
                            if self.tela_atual == "introducao" and not self.tela_introducao.painel_visivel:
                                self.tela_introducao.painel_visivel = True
                            elif self.tela_atual == "exercicio" and not self.tela_exercicio.prompt_visivel:
                                self.tela_exercicio.prompt_visivel = True
                                #self.tela_exercicio.dragging = False #se tiver problema com arrastar
                            elif self.tela_atual == "resultado" and not self.tela_resultado.painel_visivel:
                                self.tela_resultado.painel_visivel = True
                        
                        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.exit_hotspot.collidepoint(ev.pos):
                            if not self.algum_painel_visivel():  
                                rodando = False



            elif self.tela_atual == "fim":
                self.mostrar_tela_fim()
            elif self.tela_atual == "loja":
                self.tela_loja.tratar_eventos(eventos)
                self.tela_loja.desenhar(self.tela)

            #print(self.tela_atual)
            #aqui a tela é indrução por enquanto
            # --- BOTÃO LOJA GLOBAL (aparece em qualquer tela, se jogador for Intermediário) ---
            if self.jogador_atual and 9 <= self.jogador_atual.get_id_fase() <= 16 and self.tela_atual == "introducao":
                botao_loja = pygame.Rect(self.largura - 220, 40, 180, 50)
                pygame.draw.rect(self.tela, (70, 120, 200), botao_loja, border_radius=8)
                fonte = pygame.font.SysFont('Arial', 28, bold=True)
                texto_loja = fonte.render("Loja", True, (255, 255, 255))
                self.tela.blit(texto_loja, (botao_loja.centerx - texto_loja.get_width()//2,
                                            botao_loja.centery - texto_loja.get_height()//2))

                # --- Barra de progresso do curso ---
                itens_andamento = self.loja_service.listar_em_andamento(self.jogador_atual.get_id_jogador())

                largura_barra = 200
                altura_barra = 20
                x = botao_loja.left - largura_barra - 20
                y = botao_loja.centery - altura_barra // 2

                # Fundo da barra (sempre desenha)
                pygame.draw.rect(self.tela, (80, 80, 80), (x, y, largura_barra, altura_barra), border_radius=6)

                if itens_andamento:
                    # Existe curso em andamento
                    item = itens_andamento[0]  # só existe um
                    duracao_total = item.get_duracao_total()
                    tempo_restante = item.get_duracao_segundos()
                    progresso = (duracao_total - tempo_restante) / duracao_total if duracao_total > 0 else 0

                    pygame.draw.rect(self.tela, (70, 200, 70),
                                    (x, y, int(largura_barra * progresso), altura_barra), border_radius=6)

                    fonte_barra = pygame.font.SysFont('Arial', 18, bold=True)
                    txt = fonte_barra.render(f"{item.get_nome()} ({tempo_restante}s)", True, (255, 255, 255))
                else:
                    # Sem curso em andamento
                    fonte_barra = pygame.font.SysFont('Arial', 18, bold=True)
                    txt = fonte_barra.render("Sem curso", True, (200, 200, 200))

                # Texto centralizado na barra
                self.tela.blit(txt, (x + largura_barra // 2 - txt.get_width() // 2,
                                    y + altura_barra // 2 - txt.get_height() // 2))


                # Clique no botão Loja
                for ev in eventos:
                    if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                        if botao_loja.collidepoint(ev.pos):
                            self.ir_para_loja()



            pygame.display.flip()

        pygame.quit()