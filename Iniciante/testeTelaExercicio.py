import pygame
from UI.TelaExercicio import TelaExercicio
from UI.TelaResultado import TelaResultado
from UI.TelaIntroducaoTopico import TelaIntroducaoTopico
from Service.Impl.FaseServiceImpl import FaseServiceImpl
from Persistencia.Impl.JogadorPersistenciaImpl import JogadorPersistenciaImpl
from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl

pygame.init()
pygame.key.set_repeat(300, 30)


tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
LARGURA, ALTURA = tela.get_size()

clock = pygame.time.Clock()
id_fases = [1, 2, 3,4,5,6,7,8]
fase_atual = 0

# Service para buscar dados do tópico
fase_service = FaseServiceImpl()
jogador_persistencia = JogadorPersistenciaImpl()
jogador = jogador_persistencia.buscar_por_id(2) 

# ====== AJUSTE AQUI ======
progresso_service = ProgressoFaseServiceImpl()
ultima_fase = progresso_service.progresso_persistencia.buscar_ultima_fase_do_jogador(jogador.get_id_jogador())
if ultima_fase and ultima_fase in id_fases:
    fase_atual = id_fases.index(ultima_fase)
else:
    fase_atual = 0

tela_atual = "introducao"
tela_exercicio = None
tela_resultado = None
tela_introducao = None
nome_topico_atual = ""
# Para "voltar" do livro
tela_exercicio_salva = None

def mostrar_introducao(tela_salva=None):
    global tela_introducao, tela_atual, tela_exercicio_salva, nome_topico_atual
    id_fase = id_fases[fase_atual]
    fase = fase_service.buscar_fase_por_id(id_fase)
    nome = fase.get_topico()
    descricao = fase.get_introducao()
    nome_topico_atual = nome

    # Agora passa o jogador
    tela_introducao = TelaIntroducaoTopico(
        LARGURA, ALTURA, nome, descricao, on_confirmar=iniciar_exercicio, jogador=jogador
    )
    tela_atual = "introducao"
    if tela_salva:
        tela_exercicio_salva = tela_salva



def iniciar_exercicio():
    q_x = int(LARGURA * 0.25) + int(LARGURA * 0.54) - 90
    q_y = int(ALTURA * 0.13) + 10
    q_centro = (q_x + 15, q_y + 15)
    pygame.mouse.set_pos(q_centro)
    global tela_exercicio, tela_atual, tela_exercicio_salva
    if tela_exercicio_salva is not None:
        tela_exercicio = tela_exercicio_salva
        tela_exercicio_salva = None
        #tela_exercicio.centralizar_prompt()
        #print("APÓS CENTRALIZAR:", tela_exercicio.rect_prompt.x, tela_exercicio.rect_prompt.y)
    else:
        tela_exercicio = TelaExercicio(
            LARGURA, ALTURA,
            nome_topico_atual,
            total_fases=len(id_fases), fases_concluidas=fase_atual,
            callback_rever_introducao=mostrar_introducao,  # Passa callback do livro
            jogador=jogador,
            id_fase=id_fases[fase_atual]
        )
    tela_exercicio.centralizar_prompt()
    #pygame.event.clear([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
    #tela_exercicio.carregar_exercicios(id_fase=id_fases[fase_atual])
    tela_atual = "exercicio"

def avancar():
    global fase_atual
    if fase_atual < len(id_fases) - 1:
        fase_atual += 1
        mostrar_introducao()
    else:
        global tela_atual
        tela_atual = "fim"

def reiniciar():
    global tela_exercicio_salva
    
    progresso_service = ProgressoFaseServiceImpl()
    progresso_service.deletar_progresso_por_jogador_fase(
        jogador.get_id_jogador(),
        id_fases[fase_atual]
    )

    tela_exercicio_salva = None
    iniciar_exercicio()


mostrar_introducao()

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
    if not rodando:
        break  # Sai do loop logo depois do evento QUIT!

    if tela_atual == "introducao":
        tela_introducao.tratar_eventos(eventos)
        tela_introducao.desenhar(tela)

    elif tela_atual == "exercicio":
        tela_exercicio.tratar_eventos(eventos)
        tela_exercicio.desenhar(tela)
        if tela_exercicio.finalizado:
            acertou_minimo = tela_exercicio.acertos >= 4 #ajuste a quantidade para testar 
            tela_resultado = TelaResultado(
                LARGURA, ALTURA,
                tela_exercicio.acertos, tela_exercicio.erros, len(tela_exercicio.exercicios),
                callback_avancar=avancar,
                callback_reiniciar=reiniciar,
                acertou_minimo=acertou_minimo
            )
            tela_atual = "resultado"

    elif tela_atual == "resultado":
        tela_resultado.tratar_eventos(eventos)
        tela_resultado.desenhar(tela)

    elif tela_atual == "fim":
        tela.fill((30, 30, 30))
        font = pygame.font.SysFont('Arial', 36)
        tela.blit(font.render("Parabéns! Você concluiu todos os tópicos!", True, (80,255,80)), (50, 270))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
