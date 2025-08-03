import pygame
from datetime import datetime

class TelaSave:
    def __init__(self, largura, altura, id_jogador, save_service, callback_selecionar_slot):
        self.largura = largura
        self.altura = altura
        self.id_jogador = id_jogador
        self.save_service = save_service
        self.callback_selecionar_slot = callback_selecionar_slot

        # Carrega assets
        self.fundo = pygame.image.load("Assets/TelaSave.png")
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        
        self.slot_imagem = pygame.image.load("Assets/SlotSave.png")
        self.slot_imagem = pygame.transform.scale(self.slot_imagem, (300, 350))
        
        # Fontes
        self.font_titulo = pygame.font.SysFont("arial", 24, bold=True)
        self.font_normal = pygame.font.SysFont("arial", 20)
        self.font_pequena = pygame.font.SysFont("arial", 16)
        
        self.slots = self.carregar_slots()

    def carregar_slots(self):
        slots = []
        saves = self.save_service.listar_saves_do_jogador(self.id_jogador)

        for i in range(3):
            slot_rect = pygame.Rect(150 + i * 350, 200, 300, 350)
            
            if i < len(saves):
                save = saves[i]
                slots.append({
                    "rect": slot_rect,
                    "save": save,
                    "data": save.get_data_save()
                })
            else:
                slots.append({
                    "rect": slot_rect,
                    "save": None,
                    "data": None
                })
        return slots

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))
        
        # Título
        titulo = self.font_titulo.render("SELECIONE UM SLOT DE SAVE", True, (255, 255, 255))
        tela.blit(titulo, (self.largura//2 - titulo.get_width()//2, 100))

        for slot in self.slots:
            # Desenha o slot
            tela.blit(self.slot_imagem, (slot["rect"].x, slot["rect"].y))

            if slot["save"]:
                save = slot["save"]
                
                # ID do Save
                save_id = self.font_pequena.render(f"ID: {save.get_id_save()}", True, (200, 200, 200))
                tela.blit(save_id, (slot["rect"].x + 20, slot["rect"].y + 30))
                
                try:
                    if slot["data"]:
                        data_obj = datetime.strptime(slot["data"], "%Y-%m-%d %H:%M:%S")  # ajuste o formato conforme necessário
                        data_str = data_obj.strftime("%d/%m/%Y %H:%M")
                    else:
                        data_str = "Sem data"
                except Exception as e:
                    data_str = f"Erro na data: {e}"


                
                # Tempo de Jogo
                horas, resto = divmod(save.get_tempo_jogo(), 3600)
                minutos, segundos = divmod(resto, 60)
                tempo_str = f"Tempo: {int(horas)}h {int(minutos)}m"
                tempo = self.font_normal.render(tempo_str, True, (255, 255, 255))
                tela.blit(tempo, (slot["rect"].x + 20, slot["rect"].y + 110))
                
                # Informação genérica (pode ser substituída por dados reais quando disponíveis)
                info = self.font_pequena.render("Save do Jogador", True, (200, 200, 200))
                tela.blit(info, (slot["rect"].x + 20, slot["rect"].y + 150))
            else:
                vazio = self.font_normal.render("SLOT VAZIO", True, (200, 200, 200))
                tela.blit(vazio, (slot["rect"].x + 80, slot["rect"].y + 150))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botão esquerdo
                for i, slot in enumerate(self.slots):
                    if slot["rect"].collidepoint(evento.pos):
                        if slot["save"]:
                            # Se há save, retorna o ID do save
                            self.callback_selecionar_slot(slot["save"].get_id_save())
                        else:
                            # Se slot vazio, retorna o número do slot (1-3)
                            self.callback_selecionar_slot(i + 1)
                        return