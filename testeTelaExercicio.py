import pygame
from Ui.TelaExercicio import TelaExercicio
from Ui.TelaIntroducaoTopico import TelaIntroducaoTopico
from Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

pygame.init()
tela = pygame.display.set_mode((640, 600))
clock = pygame.time.Clock()
id_fases = [1, 2]  # lista de id das fases
fase_atual = 0
fase_persistencia = FasePersistenciaImpl()
fase = fase_persistencia.buscar_por_id(id_fases[fase_atual])

# Estado controla qual tela exibir!
estado = "introducao"
tela_intro = TelaIntroducaoTopico(fase)
tela_exercicio = TelaExercicio(640, 600, total_fases=len(id_fases), fases_concluidas=fase_atual)

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    if estado == "introducao":
        tela_intro.desenhar(tela)
        tela_intro.tratar_eventos(eventos)
        if tela_intro.entendido:
            tela_exercicio.carregar_exercicios(id_fases[fase_atual])
            estado = "exercicio"

    elif estado == "exercicio":
        tela_exercicio.desenhar(tela)
        tela_exercicio.tratar_eventos(eventos)
        if tela_exercicio.finalizado:
            if tela_exercicio.acertos >= 4 and fase_atual < len(id_fases)-1:
                fase_atual += 1
                fase = fase_persistencia.buscar_por_id(id_fases[fase_atual])
                tela_intro = TelaIntroducaoTopico(fase)
                tela_exercicio = TelaExercicio(640, 600, total_fases=len(id_fases), fases_concluidas=fase_atual)
                estado = "introducao"
            else:
                # Mostra tela final, ou pausa aqui...
                pass

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
