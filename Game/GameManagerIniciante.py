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
from Intermediario.UI.TelaMiniPythonHero import TelaMiniPythonHero
from Intermediario.UI.TelaCobraCodigo import TelaCobraCodigo
from Intermediario.UI.TelaEscolhaMiniGame import TelaEscolhaMiniGame
from Intermediario.UI.TelaBugSquashArcade import TelaBugSquashArcade
from Intermediario.UI.TelaPyFootTactics import TelaPyFootTactics

from Intermediario.UI.TelaIntermediario import TelaIntermediario
#audio minigames
from Intermediario.Utils.audio_core import AudioEngine
from Intermediario.Utils.sfx_pyfoot import SFXPyFoot
from Intermediario.Utils.sfx_bug import SFXBug
from Intermediario.Utils.sfx_cobra import SFXCobra
from Intermediario.Utils.sfx_hero import SFXHero
#tela historia
from Iniciante.UI.TelaHistoria import TelaHistoria 
from Intermediario.UI.TelaHistoriaIntermediario import TelaHistoriaIntermediario

##### free lancer
# --- FREELANCER (UI + serviços do Intermediário) ---
from Intermediario.UI.TelaFreelance import TelaFreelance
from Intermediario.UI.TelaDesenvolvimento import TelaDesenvolvimento
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl
from Intermediario.Service.Impl.ValidacaoServiceImpl import ValidacaoServiceImpl
from Intermediario.Service.Impl.DialogoServiceImpl import DialogoServiceImpl
from Intermediario.UI.TelaProjeto import TelaProjeto

#elementos tela inter
from Intermediario.UI.HUDIntermediario import HUDIntermediario







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
        self.MINIGAME_PASS_SCORE = 360
        self.tela_minigame = None
        self.tela_escolha_mg = None

        self._tela_antes_menu = None

        # serviços freelancer
        self.projeto_service = ProjetoFreelanceServiceImpl()
        self.cliente_service = ClienteServiceImpl()
        self.jogador_projeto_service = JogadorProjetoServiceImpl()
        self.validacao_service = ValidacaoServiceImpl()
        self.dialogo_service = DialogoServiceImpl()  

        # telas freelancer
        self.tela_freelance = None
        self.tela_desenvolvimento = None
        self.tela_detalhes_projeto = None  # Adicione para a tela de negociação
    
        # estado freelancer
        self.projeto_ativo_freelance = None
        self.ultima_tela_antes_freelance = None
        
        self.audio = AudioEngine()   # motor único
        self.sfx = None 

        # bônus acumulado pelas estrelas do Iniciante (fases 1..8)
        self.bonus_backend_iniciante = 0

        #tela intermediario
        self.tela_intermediario = None
        # hotspot do monitor para abrir o menu do Intermediário
        self.menu_hotspot = pygame.Rect(
            int(self.largura * 0.40),
            int(self.altura  * 0.36),
            250, 230
        )


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

        #historia intermediario
        self.tela_historia_inter = None          # NOVO
        self._hist_inter_shown = False  

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
        
        #tela hisotria
        self.tela_historia = None

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

        ####testando video
        try:
            import cv2 as _cv2
        except Exception:
            _cv2 = None
        self.cv2 = _cv2

        self._bg_video_cap = None
        self._bg_video_frame_ms = 0
        self._bg_video_accum_ms = 0
        self._bg_video_size = (self.largura, self.altura)

        self.hud = HUDIntermediario(self.largura, self.altura)


    def mostrar_historia_intermediario(self):
        """Abre a história de transição para o Intermediário e, ao confirmar, vai para a introdução da fase."""
        self.tela_historia_inter = TelaHistoriaIntermediario(
            self.largura,
            self.altura,
            on_confirmar=self.mostrar_introducao  # volta pro fluxo normal
        )
        self.tela_atual = "historia_inter"


    #alem do exit da para usar em outros se precisar
    def algum_painel_visivel(self):
        if self.tela_atual == "introducao" and self.tela_introducao:
            return self.tela_introducao.painel_visivel
        if self.tela_atual == "exercicio" and self.tela_exercicio:
            return self.tela_exercicio.prompt_visivel
        if self.tela_atual == "resultado" and self.tela_resultado:
            return self.tela_resultado.painel_visivel
        return False

    def ir_para_freelancer(self):
        print("DEBUG: Indo para freelance")
        self.tela_intermediario = None
        self.ultima_tela_antes_freelance = self.tela_atual

        self.projeto_ativo_freelance = self.jogador_projeto_service.buscar_projeto_ativo(
            self.jogador_atual.get_id_jogador()
        )
        print(f"DEBUG: Projeto ativo: {self.projeto_ativo_freelance}")

        projetos_info = []
        if not self.projeto_ativo_freelance:
            projetos_info = self.projeto_service.listar_projetos_para_jogador(self.jogador_atual)
            print(f"DEBUG: {len(projetos_info)} projetos disponíveis")

        self.tela_freelance = TelaFreelance(
            self.largura,
            self.altura,
            projeto_ativo=self.projeto_ativo_freelance,
            projetos_info=projetos_info,
            cliente_service=self.cliente_service,
            callback_abrir_desenvolvimento=self.iniciar_fluxo_de_trabalho
        )
        self.tela_atual = "freelance"
        print("DEBUG: Tela freelance criada")

    def iniciar_fluxo_de_trabalho(self, projeto):
        print(f"DEBUG: Fluxo iniciado para projeto {projeto.get_id_projeto()}")
        projeto_ativo_atual = self.jogador_projeto_service.buscar_projeto_ativo(
            self.jogador_atual.get_id_jogador()
        )

        if projeto_ativo_atual and projeto.get_id_projeto() == projeto_ativo_atual.get_id_projeto():
            self.abrir_desenvolvimento(projeto)
        else:
            self.abrir_tela_detalhes(projeto)

        self.tela_freelance = None  # fecha depois da transição

    def abrir_tela_detalhes(self, projeto, no_dialogo_atual=None):
        print("DEBUG: Criando tela de detalhes")
        from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente

        cliente = self.cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        mensagens = []

        if no_dialogo_atual is None:
            no_dialogo_atual = self.dialogo_service.iniciar_conversa(projeto.get_id_projeto())

        opcoes_disponiveis = []
        if no_dialogo_atual:
            mensagem_para_exibir = ChatCliente(
                id_chat=None,
                id_jogador=self.jogador_atual.get_id_jogador(),
                id_cliente=projeto.get_id_cliente(),
                mensagem=no_dialogo_atual.get_texto_npc(),
                enviado_por='cliente',
                data_envio=None
            )
            mensagens.append(mensagem_para_exibir)
            opcoes_disponiveis = self.dialogo_service.buscar_opcoes_disponiveis(
                no_dialogo_atual.get_id_no(),
                self.jogador_atual
            )

        self.tela_detalhes_projeto = TelaProjeto(
            self.largura,
            self.altura,
            projeto=projeto,
            cliente=cliente,
            jogador=self.jogador_atual,
            mensagens=mensagens,
            opcoes_dialogo_atuais=opcoes_disponiveis,
            callback_aceitar=self.aceitar_projeto,
            callback_enviar_mensagem=self.enviar_mensagem,
            callback_voltar=self.ir_para_freelancer
        )
        self.tela_atual = "detalhes_projeto"
        print("DEBUG: Tela de detalhes criada")

    def aceitar_projeto(self, projeto):
        print(f"DEBUG: Tentando aceitar projeto {projeto.get_id_projeto()}")
        sucesso = self.jogador_projeto_service.aceitar_projeto(self.jogador_atual, projeto)
        if sucesso:
            self.abrir_desenvolvimento(projeto)
        else:
            print("Não foi possível aceitar o contrato. Verifique os logs do serviço.")
            self.ir_para_freelancer()

        self.tela_detalhes_projeto = None

    def enviar_mensagem(self, projeto, opcao_escolhida):
        print(f"DEBUG: Enviando mensagem com opção {opcao_escolhida.get_id_opcao()}")
        proximo_no = self.dialogo_service.buscar_proximo_no(opcao_escolhida.get_id_no_destino())
        self.abrir_tela_detalhes(projeto, proximo_no)

    def abrir_desenvolvimento(self, projeto):
        print(f"DEBUG: Abrindo IDE para projeto {projeto.get_id_projeto()}")

        cliente = self.cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        jogador = self.jogador_service.buscar_jogador_por_id(self.jogador_atual.get_id_jogador())

        self.tela_desenvolvimento = TelaDesenvolvimento(
            self.largura,
            self.altura,
            projeto=projeto,
            jogador=jogador,
            cliente=cliente,
            callback_validar=self.validar_solucao_jogador,
            callback_entregar=self.entregar_projeto,
            callback_desistir=self.desistir_projeto
        )
        self.tela_atual = "desenvolvimento"
        print("DEBUG: Tela desenvolvimento aberta")

        # Fecha qualquer tela anterior
        self.tela_freelance = None
        self.tela_detalhes_projeto = None

    def validar_solucao_jogador(self, projeto, codigo_jogador):
        return self.validacao_service.validar_solucao(projeto, codigo_jogador)

    def entregar_projeto(self, projeto):
        print(f"DEBUG: Entregando projeto {projeto.get_id_projeto()}")
        self.jogador_projeto_service.finalizar_projeto(self.jogador_atual, projeto)
        self.ir_para_freelancer()
        self.tela_desenvolvimento = None

    def desistir_projeto(self, projeto):
        print(f"DEBUG: Desistindo do projeto {projeto.get_id_projeto()}")
        self.jogador_projeto_service.desistir_projeto(self.jogador_atual, projeto)
        self.ir_para_freelancer()
        self.tela_desenvolvimento = None


    def fechar_menu_intermediario(self):
        # fecha o menu e volta pra tela que já estava (introducao/exercicio/resultado)
        self.tela_intermediario = None
        if self._tela_antes_menu:
            self.tela_atual = self._tela_antes_menu
        #self._tela_antes_menu = None


    #testando tela intermediaria
    def is_intermediario(self) -> bool:
        return 9 <= self.id_fases[self.fase_atual] <= 16

    def abrir_menu_intermediario(self):
        if not self.is_intermediario():
            return
        self._tela_antes_menu = self.tela_atual
        self.tela_intermediario = TelaIntermediario(
            callback_exercicios=self.mostrar_introducao,
            callback_freelancer=self.ir_para_freelancer,
            callback_loja=self.ir_para_loja,
        )
        self.tela_atual = "menu_intermediario"

    def _menu_ir_exercicios(self):
        # Fecha o menu e vai para exercícios
        self.tela_intermediario = None
        self.iniciar_exercicio()

    


    def ir_para_loja(self):
        self.tela_intermediario = None
        self.tela_loja = TelaLoja(
            self.largura,
            self.altura,
            jogador=self.jogador_atual,
            loja_service=self.loja_service,
            callback_voltar=self.fechar_menu_intermediario
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
        #self.mostrar_introducao()
        # A tela de história, ao ser confirmada, chamará self.mostrar_introducao
        self.tela_historia = TelaHistoria(self.largura, self.altura, on_confirmar=self.mostrar_introducao)
        self.tela_atual = "historia"

    def _refletir_bonus_conclusao(self, item):
        try:
            # ===== Opção A: concluir_item já atualiza o jogador no BD =====
            # Recarrega o jogador do BD e pronto (HUD atualiza no próximo frame).
            self.jogador_atual = self.jogador_service.buscar_jogador_por_id(
                self.jogador_atual.get_id_jogador()
            )
            return

            # ===== Opção B: concluir_item NÃO atualiza o jogador no BD =====
            # (Se for o seu caso, comente o 'return' acima e use este bloco.)
            cat = (getattr(item, "get_categoria", lambda: "")() or "").lower()
            bonus = getattr(item, "get_bonus", lambda: 1)()  # se tiver esse método; senão troque por 1

            if   cat == "social":
                self.jogador_atual.set_social(self.jogador_atual.get_social() + bonus)
            elif cat == "backend":
                self.jogador_atual.set_backend(self.jogador_atual.get_backend() + bonus)
            elif cat == "frontend":
                self.jogador_atual.set_frontend(self.jogador_atual.get_frontend() + bonus)
            elif cat == "dinheiro":
                self.jogador_atual.set_dinheiro(self.jogador_atual.get_dinheiro() + bonus)
            elif cat == "energia":
                self.jogador_atual.set_energia(self.jogador_atual.get_energia() + bonus)
            # acrescente outros atributos que sua loja possa dar

            self.jogador_service.atualizar_jogador(self.jogador_atual)
        except Exception as e:
            print("[WARN] Falha ao refletir bônus do item:", e)

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

    
    def _set_fundo(self, path: str):
        """Se path for vídeo, liga modo vídeo; senão, carrega imagem normal."""
        # Fecha vídeo anterior, se existir
        if self._bg_video_cap is not None:
            try:
                self._bg_video_cap.release()
            except Exception:
                pass
            self._bg_video_cap = None
            self._bg_video_frame_ms = 0
            self._bg_video_accum_ms = 0

        ext = path.lower().rsplit('.', 1)[-1]
        if ext in ("mp4", "avi", "mov", "mkv", "webm") and self.cv2 is not None:
            cap = self.cv2.VideoCapture(path)
            if cap.isOpened():
                fps = cap.get(self.cv2.CAP_PROP_FPS) or 30.0
                self._bg_video_cap = cap
                self._bg_video_frame_ms = max(1, int(1000.0 / fps))
                # carrega o primeiro frame pra já desenhar algo
                self._update_fundo(0)  # força primeira leitura
                return

        # fallback: imagem estática
        try:
            img = pygame.image.load(path).convert()
            self.fundo_principal = pygame.transform.scale(img, (self.largura, self.altura))
        except Exception as e:
            print("[WARN] Falha ao carregar fundo estático:", e)
            self.fundo_principal = pygame.Surface((self.largura, self.altura))
            self.fundo_principal.fill((20, 20, 30))

    def _update_fundo(self, dt_ms: int):
            """Atualiza o frame do vídeo de fundo (se houver)."""
            if self._bg_video_cap is None:
                return
            self._bg_video_accum_ms += dt_ms
            if self._bg_video_accum_ms < self._bg_video_frame_ms:
                return
            self._bg_video_accum_ms = 0

            ok, frame = self._bg_video_cap.read()
            if not ok:
                # loop
                self._bg_video_cap.set(self.cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = self._bg_video_cap.read()
                if not ok:
                    return

            # BGR -> RGB
            frame = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
            # resize para tela
            frame = self.cv2.resize(frame, self._bg_video_size, interpolation=self.cv2.INTER_LINEAR)

            # cria Surface sem cópia extra (frombuffer)
            surf = pygame.image.frombuffer(frame.tobytes(), self._bg_video_size, "RGB")
            # importante: converter para a mesma pixel format do display (evita bugs de alpha)
            self.fundo_principal = surf.convert()



    def mostrar_introducao(self, tela_salva=None):
        self.tela_intermediario = None
        id_fase = self.id_fases[self.fase_atual]
        fase = self.fase_service.buscar_fase_por_id(id_fase)

        # ✅ Blindagem: evita quebrar se a fase não existir no BD
        if fase is None:
            print(f"[WARN] Fase {id_fase} não encontrada no banco. Encerrando para evitar crash.")
            self.tela_atual = "fim"
            return

        # >>> TROCA DE FUNDO AQUI <<<
        if id_fase <= 8:
            bg = "assets/Personagem_Bebendo_Café_em_Anime.mp4"
            self.exit_hotspot.update(
                int(self.largura * 0.08),
                int(self.altura  * 0.28),
                int(self.largura * 0.05),
                int(self.altura  * 0.48)
            )
        else:
            bg = "assets/Personagem_Bebendo_Café_em_Anime.mp4"
        self._set_fundo(bg)
        # <<< FIM TROCA >>>

        nome_topico = fase.get_topico()
        descricao = fase.get_introducao()
        self.nome_topico_atual = nome_topico

        self.tela_introducao = TelaIntroducaoTopico(
            self.largura, self.altura,
            nome_topico, descricao,
            on_confirmar=self.iniciar_exercicio,
            jogador=self.jogador_atual
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
        
        # NÃO CHAME self.tela_exercicio.carregar_exercicios AQUI!

        self.tela_atual = "exercicio"


    def _on_bug_finish(self, result: dict):
        # result esperado: {"score", "passed", "squashed", "misses", "hint_uses", "time_spent"}
        score = int(result.get("score", 0))
        # mapeia score -> estrelas (mantém tua mecânica de bônus)
        if score >= int(self.MINIGAME_PASS_SCORE * 1.50):
            stars = 3
        elif score >= int(self.MINIGAME_PASS_SCORE * 1.15):
            stars = 2
        elif score >= self.MINIGAME_PASS_SCORE:
            stars = 1
        else:
            stars = 0
        # reusa teu fluxo padrão
        self.finalizar_minigame(score, stars)

    def _pos_resultado(self):
        # Se foi aprovado e é Iniciante (fases 1..8), roda minigame
        fase_id = self.id_fases[self.fase_atual]
        if self._ultimo_resultado_ok and 1 <= fase_id <= 16:
            self.iniciar_minigame()
        else:
            self.avancar_fase()

    def _gerar_seq_por_topico(self, topico):
        t = (topico or "").lower()
        if "print" in t:
            return ["print('Olá')", "print('Boa tarde')"]
        if "input" in t:
            return ["n = int(input())", "print(n)"]
        if "for" in t:
            return ["for i in range(3):", "print(i)"]
        if "if" in t:
            return ["x = 5", "if x > 0:", "print('ok')"][:2]  # mantem 2 passos se preferir
        return ["print('ok')", "print('fim')"]


    def _iniciar_minigame_escolhido(self, tipo):
        id_fase = self.id_fases[self.fase_atual]

        # sempre derruba qualquer ambient anterior
        if self.audio:
            self.audio.stop_ambient()

        # zera e cria o wrapper correto
        self.sfx = None

        if tipo == "cobra":
            self.sfx = SFXCobra(self.audio)
            seq_alvo = self._gerar_seq_por_topico(self.nome_topico_atual)
            self.tela_minigame = TelaCobraCodigo(
                largura=self.largura,
                altura=self.altura,
                jogador=self.jogador_atual,
                id_fase=id_fase,
                nome_topico=self.nome_topico_atual,
                on_finish=self.finalizar_minigame,
                sequencia_alvo=seq_alvo,
                sfx=self.sfx
            )

        elif tipo == "bug":
            self.sfx = SFXBug(self.audio)   # <<— SFX DO BUG É ESSE
            self.tela_minigame = TelaBugSquashArcade(
                largura=self.largura,
                altura=self.altura,
                topic_title=self.nome_topico_atual,
                on_finish=self._on_bug_finish,      # recebe dict e mapeia para estrelas
                pass_score=self.MINIGAME_PASS_SCORE,
                round_seconds=35,
                sfx=self.sfx
            )

        elif tipo == "pyfoot":
            self.sfx = SFXPyFoot(self.audio)
            #self.sfx.start_ambient(vol=0.45)
            self.tela_minigame = TelaPyFootTactics(
                largura=self.largura,
                altura=self.altura,
                topic_title=self.nome_topico_atual,
                on_finish=self._on_bug_finish,      # também retorna dict
                pass_score=self.MINIGAME_PASS_SCORE,
                total_seconds=45,
                rounds=14,
                sfx=self.sfx
            )
            # torcida SÓ aqui
            self.sfx.start_ambient(vol=0.60)

        else:  # "hero"
            self.sfx = SFXHero(self.audio)
            self.sfx.start_ambient(vol=0.38)
            self.tela_minigame = TelaMiniPythonHero(
                largura=self.largura,
                altura=self.altura,
                jogador=self.jogador_atual,
                id_fase=id_fase,
                nome_topico=self.nome_topico_atual,
                on_finish=self.finalizar_minigame,
                sfx=self.sfx
            )

        self.tela_atual = "minigame"


    def iniciar_minigame(self):
        # Abre hub de escolha; quando escolher, chamamos _iniciar_minigame_escolhido(...)
        self.tela_escolha_mg = TelaEscolhaMiniGame(
            self.largura,
            self.altura,
            on_choose=self._iniciar_minigame_escolhido
        )
        self.tela_atual = "escolha_mg"


    def finalizar_minigame(self, score, stars):
        # bônus por estrelas (mantém)
        if self.audio: 
            self.audio.stop_ambient()
        self.sfx = None
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
        """Para fases 1..16: MG é a 5ª questão. Se já foi feito (índice >= 5), não reabrir MG."""
        fase_id = self.id_fases[self.fase_atual]

        if 1 <= fase_id <= 16:
            total_q = len(self.tela_exercicio.exercicios) if self.tela_exercicio else 4
            idx_atual = getattr(self.tela_exercicio, "indice_atual", total_q)

            # Se o MG já foi registrado como 'feito' (índice >= 5), mostra Resultado direto.
            if idx_atual >= total_q + 1:
                acertou_minimo = (self.tela_exercicio.acertos >= 4)  # 4 de 5
                self._ultimo_resultado_ok = acertou_minimo

                self.tela_resultado = TelaResultado(
                    self.largura,
                    self.altura,
                    self.tela_exercicio.acertos,
                    self.tela_exercicio.erros,
                    total_q + 1,  # 5 no total (4 + MG)
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

        # (Opcional) Fases > 16: mantém fluxo antigo como fallback
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
            # Fase que está sendo concluída AGORA
            fase_concluida = self.id_fases[self.fase_atual]

            # Alinha o "total necessário" à regra 4 + MG = 5 nas fases 1..16
            raw_total_exs = len(self.exercicio_service.listar_exercicios_por_fase(fase_concluida))
            total_necessario = 5 if 1 <= fase_concluida <= 16 else raw_total_exs

            ultima_fase_no_save = self.progresso_service.progresso_persistencia.buscar_ultima_fase_do_jogador(
                self.jogador_atual.get_id_jogador()
            )

            # Compat com saves antigos (que podem ter parado no 4 antes do MG)
            concluiu_novo = self.progresso_service.fase_ja_concluida(
                self.jogador_atual.get_id_jogador(), fase_concluida, total_necessario
            )
            concluiu_compat = False
            if 1 <= fase_concluida <= 16 and not concluiu_novo:
                # Tolerar "4" como fase concluída se existir legado
                concluiu_compat = self.progresso_service.fase_ja_concluida(
                    self.jogador_atual.get_id_jogador(), fase_concluida, 4
                )

            if (fase_concluida == ultima_fase_no_save) and (concluiu_novo or concluiu_compat):
                # >>> bônus ao encerrar o INICIANTE (fase 8)
                if fase_concluida == 8:
                    backend_atual = self.jogador_atual.get_backend()
                    social_atual = self.jogador_atual.get_social()
                    frontend_atual = self.jogador_atual.get_frontend()
                    ganho = 10  # se quiser somar as estrelas: 10 + self.bonus_backend_iniciante
                    self.jogador_atual.set_backend(backend_atual + ganho)
                    self.jogador_atual.set_social(social_atual + 5)
                    self.jogador_atual.set_frontend(frontend_atual + 5)
                    self.jogador_atual.set_dinheiro(200)
                    self.jogador_service.atualizar_jogador(self.jogador_atual)
                    self.bonus_backend_iniciante = 0

                # >>> bônus por tópico no INTERMEDIÁRIO (9..16)
                elif 9 <= fase_concluida <= 16:
                    backend_atual = self.jogador_atual.get_backend()
                    self.jogador_atual.set_backend(backend_atual + 5)
                    self.jogador_service.atualizar_jogador(self.jogador_atual)

            # Verifica a PRÓXIMA fase no BD antes de avançar
            proximo_idx = self.fase_atual + 1
            proxima_fase_id = self.id_fases[proximo_idx]
            if self.fase_service.buscar_fase_por_id(proxima_fase_id) is None:
                print(f"[WARN] Próxima fase {proxima_fase_id} não cadastrada no banco. Encerrando para evitar crash.")
                self.tela_atual = "fim"
                return

            # Avança em memória e no BD
            self.fase_atual = proximo_idx
            self.jogador_service.avancar_fase_jogador(self.jogador_atual.get_id_jogador())
            self.jogador_atual = self.jogador_service.buscar_jogador_por_id( self.jogador_atual.get_id_jogador() )

            # Anti-revisita: cria/garante progresso 'stub' na NOVA fase
            self.progresso_service.salvar_ou_atualizar_progresso(
                jogador=self.jogador_atual,
                id_fase=proxima_fase_id,
                indice_exercicio=0,
                acertos=0,
                erros=0,
                resposta_parcial=""
            )

            # Vai pra introdução da nova fase
            if proxima_fase_id == 9 and not self._hist_inter_shown:
                self._hist_inter_shown = True
                self.mostrar_historia_intermediario()
            else:
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

    def desenhar_barra_curso(self):
        """Barra de progresso do curso (fica sempre visível no Intermediário)."""
        if not (self.jogador_atual and 9 <= self.jogador_atual.get_id_fase() <= 16):
            return

        # posição fixa no topo-direito
        largura_barra = 240
        altura_barra  = 22
        x = self.largura - largura_barra - 20
        y = 20

        # fundo
        pygame.draw.rect(self.tela, (80, 80, 80), (x, y, largura_barra, altura_barra), border_radius=6)

        # progresso (se tiver curso em andamento)
        itens_andamento = self.loja_service.listar_em_andamento(self.jogador_atual.get_id_jogador())
        fonte_barra = pygame.font.SysFont('Arial', 18, bold=True)
        if itens_andamento:
            item = itens_andamento[0]
            duracao_total  = item.get_duracao_total()
            tempo_restante = item.get_duracao_segundos()
            progresso = (duracao_total - tempo_restante) / duracao_total if duracao_total > 0 else 0.0
            pygame.draw.rect(self.tela, (70, 200, 70), (x, y, int(largura_barra * progresso), altura_barra), border_radius=6)
            txt = fonte_barra.render(f"{item.get_nome()} ({tempo_restante}s)", True, (255, 255, 255))
        else:
            txt = fonte_barra.render("Sem curso", True, (200, 200, 200))

        # texto centralizado
        self.tela.blit(txt, (x + largura_barra // 2 - txt.get_width() // 2,
                            y + altura_barra // 2 - txt.get_height() // 2))


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
                        # >>> ATUALIZA O JOGADOR EM MEMÓRIA PRA HUD REFLETIR AGORA
                        self._refletir_bonus_conclusao(item)
                    else:
                        self.loja_service.atualizar_item(item)
            # Trata eventos
            eventos = pygame.event.get()
            
            for evento in eventos:
                # --- TOGGLE do MENU INTERMEDIÁRIO no mesmo hotspot ---
                if (
                    evento.type == pygame.MOUSEBUTTONUP and evento.button == 1
                    and self.menu_hotspot.collidepoint(evento.pos)
                ):
                    if self.algum_painel_visivel():
                        # não faz nada se um painel modal estiver aberto
                        pass
                    elif self.tela_atual == "menu_intermediario":
                        # se já está no menu, fecha
                        self.fechar_menu_intermediario()

                    elif self.tela_atual in ("introducao", "exercicio", "resultado"):
                        if self.is_intermediario():
                            # 9..16 → abre o menu do Intermediário
                            self._tela_antes_menu = self.tela_atual
                            self.abrir_menu_intermediario()
                        else:
                            # 1..8 → reabre o painel da tela atual
                            if self.tela_atual == "introducao" and self.tela_introducao:
                                self.tela_introducao.painel_visivel = True
                            elif self.tela_atual == "exercicio" and self.tela_exercicio:
                                self.tela_exercicio.prompt_visivel = True
                            elif self.tela_atual == "resultado" and self.tela_resultado:
                                self.tela_resultado.painel_visivel = True

                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

            if not rodando:
                break

           
            self._update_fundo(dt)
            self.tela.blit(self.fundo_principal, (0, 0))
            # Renderização condicional das telas
            if self.tela_atual == "inicio":
                self.tela_inicio.tratar_eventos(eventos)
                self.tela_inicio.desenhar(self.tela)

            elif self.tela_atual == "historia":
                if self.tela_historia:
                    self.tela_historia.tratar_eventos(eventos)
                    self.tela_historia.desenhar(self.tela)
            elif self.tela_atual == "historia_inter":                     # NOVO
                if self.tela_historia_inter:
                    self.tela_historia_inter.tratar_eventos(eventos)
                    self.tela_historia_inter.desenhar(self.tela)


            elif self.tela_atual == "save":
                resultado = self.tela_save.tratar_eventos(eventos)
                if resultado == "voltar":
                    self.tela_atual = "inicio"
                self.tela_save.desenhar(self.tela)
            
            elif self.tela_atual == "minigame":
                # fundo (mantém teu background)
                #self.tela.blit(self.fundo_principal, (0, 0))
                self.tela_minigame.tratar_eventos(eventos)
                self.tela_minigame.desenhar(self.tela)

            elif self.tela_atual == "freelance":
                if self.tela_freelance:
                    self.tela_freelance.tratar_eventos(eventos)

                    if getattr(self.tela_freelance, "deve_fechar", False):
                        print("DEBUG: Fechando tela freelance")
                        self.tela_freelance = None
                        if hasattr(self, 'ultima_tela_antes_freelance') and self.ultima_tela_antes_freelance:
                            self.tela_atual = "menu_intermediario"
                            print(f"DEBUG: Voltando para {self.ultima_tela_antes_freelance}")
                        else:
                            self.tela_atual = "menu_intermediario"
                            print("DEBUG: Voltando para menu intermediário")
                    elif self.tela_freelance:
                        self.tela_freelance.desenhar(self.tela)

            elif self.tela_atual == "detalhes_projeto":
                if self.tela_detalhes_projeto:
                    self.tela_detalhes_projeto.tratar_eventos(eventos)

                    if getattr(self.tela_detalhes_projeto, "deve_fechar", False):
                        print("DEBUG: Fechando tela de detalhes")
                        self.tela_detalhes_projeto = None
                        self.tela_atual = "menu_intermediario"
                    elif self.tela_detalhes_projeto:
                        self.tela_detalhes_projeto.desenhar(self.tela)

            elif self.tela_atual == "desenvolvimento":
                if self.tela_desenvolvimento:
                    self.tela_desenvolvimento.tratar_eventos(eventos)

                    if getattr(self.tela_desenvolvimento, "deve_fechar", False):
                        print("DEBUG: Fechando tela de desenvolvimento")
                        self.tela_desenvolvimento = None
                        self.tela_atual = "menu_intermediario"  # ← volta direto pro menu
                        print("DEBUG: Voltando para menu intermediário")

                    elif self.tela_desenvolvimento:
                        self.tela_desenvolvimento.desenhar(self.tela)

            # Dentro do método executar()

            elif self.tela_atual == "menu_intermediario":
                #self.tela.blit(self.fundo_principal, (0, 0))

                if self.tela_intermediario is not None:
                    self.tela_intermediario.tratar_eventos(eventos)

                    # Esta verificação agora só vai ser acionada de verdade pelo clique no 'X',
                    # pois os outros botões destroem o menu antes que este código rode.
                    if getattr(self.tela_intermediario, 'deve_fechar', False):
                        self.fechar_menu_intermediario()

                # Apenas desenha o menu se ele ainda existir (não foi fechado por um callback ou pelo 'X')
                if self.tela_intermediario is not None:
                    self.tela_intermediario.desenhar(self.tela)



            elif self.tela_atual == "criar_jogador":
                self.tela_criar_jogador.tratar_eventos(eventos)
                self.tela_criar_jogador.atualizar(dt)
                self.tela_criar_jogador.desenhar(self.tela)
            elif self.tela_atual == "escolha_mg":
                #self.tela.blit(self.fundo_principal, (0, 0))
                self.tela_escolha_mg.tratar_eventos(eventos)
                self.tela_escolha_mg.desenhar(self.tela)

            elif self.tela_atual in ["introducao", "exercicio", "resultado"]:
                # fundo
                #self.tela.blit(self.fundo_principal, (0, 0))

                # === HOTSPOT DA PORTA (sair do jogo) ===
                """
                self.exit_hotspot.update(
                    int(self.largura * 0.01),  # X
                    int(self.altura  * 0.25),  # Y
                    int(self.largura * 0.06),  # largura
                    int(self.altura  * 0.49)   # altura
                )
                """

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
                        # DESATIVANDO A REABERTURA DOS PAINÉIS
                        # if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.reopen_hotspot.collidepoint(ev.pos):
                        #     if self.tela_atual == "introducao" and not self.tela_introducao.painel_visivel:
                        #         self.tela_introducao.painel_visivel = True
                        #     elif self.tela_atual == "exercicio" and not self.tela_exercicio.prompt_visivel:
                        #         self.tela_exercicio.prompt_visivel = True
                        #         #self.tela_exercicio.dragging = False #se tiver problema com arrastar
                        #     elif self.tela_atual == "resultado" and not self.tela_resultado.painel_visivel:
                        #         self.tela_resultado.painel_visivel = True
                        
                        # A LÓGICA DA PORTA DE SAÍDA CONTINUA FUNCIONANDO
                        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.exit_hotspot.collidepoint(ev.pos):
                            if not self.algum_painel_visivel():  
                                rodando = False



            elif self.tela_atual == "fim":
                self.mostrar_tela_fim()
            elif self.tela_atual == "loja":
                self.tela_loja.tratar_eventos(eventos)
                self.tela_loja.desenhar(self.tela)

            current_id = self.id_fases[self.fase_atual] if self.jogador_atual else 0
            if (
                9 <= current_id <= 16
                and self.tela_atual not in ("historia", "historia_inter")
            ):
                itens_andamento = self.loja_service.listar_em_andamento(self.jogador_atual.get_id_jogador())
                self.hud.desenhar(self.tela, self.jogador_atual, itens_andamento)




            if self.debug_hotspot:
                pygame.draw.rect(self.tela, (0, 255, 0, 100), self.menu_hotspot, 2) # Desenha contorno verde
            if self.debug_exit_hotspot:
                pygame.draw.rect(self.tela, (255, 0, 0, 100), self.exit_hotspot, 2) # Desenha contorno vermelho
            pygame.display.flip()

        # ao sair do loop principal
        try:
            if getattr(self, "sfx", None):
                # wrappers não precisam fechar nada
                pass
            if getattr(self, "audio", None):
                self.audio.stop_ambient()
                self.audio.close()
        except Exception:
            pass

        pygame.quit()