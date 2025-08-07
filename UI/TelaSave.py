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
        self.fundo = pygame.image.load("Assets/TelaSave.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        
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
        """Cria os retângulos para os slots de save (empilhados verticalmente)"""
        slot_width = self.largura * 0.7
        slot_height = 120
        start_y = 180

        self.slots = []

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
        
       # Paleta de cores combinando com o fundo
        COR_SLOT_1 = (20, 30, 60, 120)   # tom mais escuro
        COR_SLOT_HOVER_1 = (120, 250, 200, 220)
        COR_BORDA = (60, 90, 140)  # azul médio para bordas

        pos_mouse = pygame.mouse.get_pos()

        for i, slot in enumerate(self.slots):
            slot_surface = pygame.Surface((slot.width, slot.height), pygame.SRCALPHA)

            mouse_em_cima = slot.collidepoint(pos_mouse)

            if mouse_em_cima:
                cor_slot = COR_SLOT_HOVER_1 
            else:
                cor_slot = COR_SLOT_1 

            pygame.draw.rect(slot_surface, cor_slot, slot_surface.get_rect(), border_radius=10)
            tela.blit(slot_surface, (slot.x, slot.y))

            pygame.draw.rect(tela, COR_BORDA, slot, width=3, border_radius=10)
            
            if i < len(self.saves):
                self.desenhar_slot_preenchido(tela, slot, i)
            else:
                self.desenhar_slot_vazio(tela, slot, i)

    def desenhar_slot_preenchido(self, tela, slot, indice):
        save = self.saves[indice]
        jogador = self.jogador_service.buscar_jogador_por_id(save.get_id_jogador())

        # Parte da imagem (simula screenshot ou avatar)
        imagem_dummy = pygame.Surface((100, 75))
        imagem_dummy.fill((50, 100, 150))  # Cor exemplo
        tela.blit(imagem_dummy, (slot.x + 15, slot.y + 20))

        # Nome do save
        texto_nome = self.fonte_normal.render(
            f"{jogador.get_nome()}", True, (0, 0, 0)
        )
        tela.blit(texto_nome, (slot.x + 130, slot.y + 20))

        # Fase atual
        '''progresso = self.jogador_service.buscar_progresso(jogador.get_id_jogador())
        texto_fase_str = f"Fase: {progresso['fase']}" if progresso else "Fase: N/A"
        texto_fase = self.fonte_normal.render(texto_fase_str, True, (0, 0, 0))
        tela.blit(texto_fase, (slot.x + 130, slot.y + 50))'''

        # Data
        texto_data = self.fonte_pequena.render(
            save.get_data_save(), True, (100, 100, 100)
        )
        tela.blit(texto_data, (slot.x + slot.width - 150, slot.y + 20))


    def desenhar_slot_vazio(self, tela, slot, indice):
        
        # Texto “New Game”
        texto = self.fonte_normal.render("Novo Jogo", True, (60, 60, 60))
        tela.blit(texto, (slot.x + 110, slot.y + (slot.height - texto.get_height()) // 2))

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