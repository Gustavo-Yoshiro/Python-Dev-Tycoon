import pygame
from UI.TelaInicio import TelaInicio
from UI.TelaSave import TelaSave

pygame.init()

LARGURA, ALTURA = 1280, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teste - TelaSave")

relogio = pygame.time.Clock()

# Estados
tela_atual = None

def iniciar_jogo():
    global tela_atual
    tela_atual = TelaSave(LARGURA, ALTURA, callback_selecionar_slot=slot_selecionado)

def slot_selecionado(slot_id):
    print(f"Slot {slot_id} selecionado!")
    # Aqui você pode mudar para outra tela ou carregar o jogo

# Começa com a tela de início
tela_atual = TelaInicio(LARGURA, ALTURA, callback_iniciar=iniciar_jogo)

# Loop principal
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
