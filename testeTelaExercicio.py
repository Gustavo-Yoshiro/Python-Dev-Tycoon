import pygame
from Ui.TelaExercicio import TelaExercicio

pygame.init()
tela = pygame.display.set_mode((640, 600))
clock = pygame.time.Clock()
tela_exercicio = TelaExercicio(640, 600)
tela_exercicio.carregar_exercicios(id_fase=1)  # Mude o ID para o que quiser testar

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    tela_exercicio.tratar_eventos(eventos)
    tela_exercicio.desenhar(tela)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
