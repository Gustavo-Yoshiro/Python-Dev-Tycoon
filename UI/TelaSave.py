import pygame

class TelaSave:
    def __init__(self, largura, altura, id_jogador, save_service, callback_selecionar_slot):
        self.largura = largura
        self.altura = altura
        self.id_jogador = id_jogador
        self.save_service = save_service
        self.callback_selecionar_slot = callback_selecionar_slot

        self.fundo = pygame.image.load("Assets/TelaSave.png")
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        
        self.slot_imagem = pygame.image.load("Assets/SlotSave.png")
        self.slot_imagem = pygame.transform.scale(self.slot_imagem, (300, 350))
        
        self.font = pygame.font.SysFont("arial", 24)
        self.slots = self.carregar_slots()

    def carregar_slots(self):
        slots = []
        saves = self.save_service.listar_saves_do_jogador(self.id_jogador)

        for i in range(3):
            if i < len(saves):
                save = saves[i]
                slots.append({
                    "rect": pygame.Rect(150 + i * 350, 200, 300, 350),
                    "save": save
                })
            else:
                slots.append({
                    "rect": pygame.Rect(150 + i * 350, 200, 300, 350),
                    "save": None
                })
        return slots

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        for slot in self.slots:
            tela.blit(self.slot_imagem, (slot["rect"].x, slot["rect"].y))

            if slot["save"]:
                save = slot["save"]
                nome = self.font.render(f"Nome: {save.get_nome_jogo()}", True, (255, 255, 255))
                nivel = self.font.render(f"Nível: {save.get_nivel()}", True, (255, 255, 255))
                fase = self.font.render(f"Fase: {save.get_fase()}", True, (255, 255, 255))

                tela.blit(nome, (slot["rect"].x + 20, slot["rect"].y + 20))
                tela.blit(nivel, (slot["rect"].x + 20, slot["rect"].y + 60))
                tela.blit(fase, (slot["rect"].x + 20, slot["rect"].y + 100))
            else:
                vazio = self.font.render("Slot vazio", True, (200, 200, 200))
                tela.blit(vazio, (slot["rect"].x + 80, slot["rect"].y + 150))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, slot in enumerate(self.slots):
                    if slot["rect"].collidepoint(evento.pos):
                        self.callback_selecionar_slot(i + 1)
