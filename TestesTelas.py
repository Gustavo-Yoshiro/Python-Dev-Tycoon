import pygame
from UI.TelaInicio import TelaInicio
from UI.TelaExercicio import TelaExercicio

pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Inicialmente mostra a tela de início
tela_atual = None

def iniciar_jogo():
    global tela_atual
    tela_exercicio = TelaExercicio(largura, altura)
    tela_exercicio.carregar_exercicios(id_fase=1)
    tela_atual = tela_exercicio

tela_inicio = TelaInicio(largura, altura, iniciar_jogo)
tela_atual = tela_inicio

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    tela_atual.tratar_eventos(eventos)
    tela_atual.desenhar(tela)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
