import pygame

class TelaSave:
    def __init__(self, largura, altura, save_service, jogador_service, callback_selecionar_slot, callback_criar_jogador):
        self.largura = largura
        self.altura = altura
        self.save_service = save_service
        self.jogador_service = jogador_service
        self.callback_selecionar_slot = callback_selecionar_slot
        self.callback_criar_jogador = callback_criar_jogador
        
        # Configuração visual
        self.fundo = pygame.Surface((largura, altura))
        self.fundo.fill((30, 30, 40))
        
        # Fontes
        self.fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_normal = pygame.font.SysFont("Arial", 32)
        self.fonte_pequena = pygame.font.SysFont("Arial", 24)
        
        # Slots de save
        self.slots = []
        self.criar_slots()
        
        # Botão voltar
        self.botao_voltar = pygame.Rect(50, 50, 120, 50)
        
        # Estado
        self.saves = self.save_service.listar_saves()
        self.slots_usados = {save.get_id_jogador(): save for save in self.saves}

    def criar_slots(self):
        """Cria os retângulos para os slots de save"""
        slot_width = self.largura * 0.7
        slot_height = 120
        start_y = 180
        
        for i in range(3):
            rect = pygame.Rect(
                (self.largura - slot_width) // 2,
                start_y + i * (slot_height + 20),
                slot_width,
                slot_height
            )
            self.slots.append(rect)

    def desenhar(self, tela):
        # Fundo
        tela.blit(self.fundo, (0, 0))
        
        # Título
        titulo = self.fonte_titulo.render("Selecionar Save", True, (255, 255, 255))
        tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 80))
        
        # Botão voltar
        pygame.draw.rect(tela, (70, 70, 70), self.botao_voltar, border_radius=5)
        texto_voltar = self.fonte_normal.render("Voltar", True, (255, 255, 255))
        tela.blit(texto_voltar, (
            self.botao_voltar.x + (self.botao_voltar.width - texto_voltar.get_width()) // 2,
            self.botao_voltar.y + (self.botao_voltar.height - texto_voltar.get_height()) // 2
        ))
        
        # Slots de save
        for i, slot in enumerate(self.slots):
            # Fundo do slot
            cor_slot = (80, 80, 90) if i % 2 == 0 else (70, 70, 80)
            pygame.draw.rect(tela, cor_slot, slot, border_radius=10)
            pygame.draw.rect(tela, (100, 100, 110), slot, width=3, border_radius=10)
            
            if i < len(self.saves):
                self.desenhar_slot_preenchido(tela, slot, i)
            else:
                self.desenhar_slot_vazio(tela, slot, i)

    def desenhar_slot_preenchido(self, tela, slot, indice):
        save = self.saves[indice]
        jogador = self.jogador_service.buscar_jogador_por_id(save.get_id_jogador())
        
        # Nome do save e jogador
        texto_nome = self.fonte_normal.render(
            f"{'Save'} - {jogador.get_nome()}", 
            True, (255, 255, 255)
        )
        tela.blit(texto_nome, (slot.x + 20, slot.y + 20))
        
        # Data e progresso
        data_formatada = save.get_data_save()
        texto_data = self.fonte_pequena.render(
            f"Criado em: {data_formatada}", 
            True, (200, 200, 200)
        )
        tela.blit(texto_data, (slot.x + 20, slot.y + 60))
        
        '''# Progresso
        texto_progresso = self.fonte_pequena.render(
            f"Progresso: {save.get_progresso()}/8 tópicos", 
            True, (180, 220, 180)
        )
        tela.blit(texto_progresso, (slot.x + slot.width - 250, slot.y + 60))'''

    def desenhar_slot_vazio(self, tela, slot, indice):
        # Texto "Slot vazio"
        texto_vazio = self.fonte_normal.render("Slot Vazio - Novo Jogo", True, (180, 180, 180))
        tela.blit(texto_vazio, (slot.x + 20, slot.y + 20))
        
        # Ícone de "+"
        texto_mais = self.fonte_titulo.render("+", True, (150, 150, 150))
        tela.blit(texto_mais, (
            slot.x + slot.width - 50, 
            slot.y + (slot.height - texto_mais.get_height()) // 2
        ))

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                
                # Verifica botão voltar
                if self.botao_voltar.collidepoint(pos):
                    return "voltar"
                
                # Verifica slots
                for i, slot in enumerate(self.slots):
                    if slot.collidepoint(pos):
                        if i < len(self.saves):
                            # Slot com save existente
                            self.callback_selecionar_slot(self.saves[i])
                            return "carregar"
                        else:
                            # Slot vazio - criar novo jogador
                            nome_padrao = f"Save {i+1}"
                            self.callback_criar_jogador()
                            return "novo_jogador"
        return None