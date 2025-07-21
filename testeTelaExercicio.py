import pygame
from Ui.TelaExercicio import TelaExercicio
from Ui.TelaResultado import TelaResultado
from Ui.TelaIntroducaoTopico import TelaIntroducaoTopico
from Service.Impl.FaseServiceImpl import FaseServiceImpl

pygame.init()
LARGURA = 800
ALTURA = 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
id_fases = [1, 2, 3,4,5,6,7,8]
fase_atual = 0

# Service para buscar dados do tópico
fase_service = FaseServiceImpl()

tela_atual = "introducao"
tela_exercicio = None
tela_resultado = None
tela_introducao = None

# Para "voltar" do livro
tela_exercicio_salva = None

def mostrar_introducao(tela_salva=None):
    global tela_introducao, tela_atual, tela_exercicio_salva
    id_fase = id_fases[fase_atual]
    fase = fase_service.buscar_fase_por_id(id_fase)
    nome = fase.get_topico()
    descricao = fase.get_introducao()
    tela_introducao = TelaIntroducaoTopico(LARGURA, ALTURA, nome, descricao, on_confirmar=iniciar_exercicio)
    tela_atual = "introducao"
    if tela_salva:
        tela_exercicio_salva = tela_salva

def iniciar_exercicio():
    global tela_exercicio, tela_atual, tela_exercicio_salva
    if tela_exercicio_salva is not None:
        tela_exercicio = tela_exercicio_salva
        tela_exercicio_salva = None
    else:
        tela_exercicio = TelaExercicio(
            LARGURA, ALTURA,
            total_fases=len(id_fases), fases_concluidas=fase_atual,
            callback_rever_introducao=mostrar_introducao  # Passa callback do livro
        )
        tela_exercicio.carregar_exercicios(id_fase=id_fases[fase_atual])
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
    tela_exercicio_salva = None
    iniciar_exercicio()

mostrar_introducao()

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
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
