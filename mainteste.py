import pygame
import sys
import random
from datetime import datetime

# --- Importações de Entidades e Serviços ---
# Certifique-se de que os caminhos de importação correspondem à sua estrutura de pastas
from Iniciante.Persistencia.Entidade.Jogador import Jogador
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Iniciante.Service.Impl.JogadorServiceImpl import JogadorServiceImpl
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl
# from Intermediario.Service.Impl.ValidacaoServiceImpl import ValidacaoServiceImpl # Para o futuro IDE

# --- Importações das Janelas de UI ---
from Intermediario.UI.TelaFreelance import TelaFreelance
from Intermediario.UI.TelaProjeto import TelaProjeto
# from Intermediario.UI.TelaDesenvolvimento import TelaDesenvolvimento # Para o futuro IDE
from Intermediario.UI.Janela import Janela


# --- Constantes ---
LARGURA, ALTURA = 1280, 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Python Dev Tycoon - F.L.N.C.R. System")
JOGADOR_ID_ATUAL = 1 # ID do jogador fixo para testes

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # --- Carregar a imagem de fundo ---
    try:
        fundo_jogo = pygame.image.load("assets/TelaJogoIniciante.png").convert()
        fundo_jogo = pygame.transform.scale(fundo_jogo, (LARGURA, ALTURA))
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo: {e}")
        fundo_jogo = pygame.Surface((LARGURA, ALTURA)); fundo_jogo.fill((25, 25, 35))
        
    # --- Inicialização dos Serviços ---
    projeto_service = ProjetoFreelanceServiceImpl()
    cliente_service = ClienteServiceImpl()
    jogador_service = JogadorServiceImpl()
    jogador_projeto_service = JogadorProjetoServiceImpl()
    # validacao_service = ValidacaoServiceImpl() # Para o futuro IDE

    # Carrega o jogador atual do banco de dados
    JOGADOR_ATUAL = jogador_service.buscar_jogador_por_id(1)
    if not JOGADOR_ATUAL:
        print("ERRO FATAL: Jogador com ID 1 não encontrado no banco de dados.")
        return

    # --- Gerenciador de Janelas ---
    janelas_abertas = []
    menu_principal_visivel = False
    fonte_menu_principal = pygame.font.SysFont("Arial", 24, bold=True)
    
    # --- Funções de Orquestração (Callbacks) ---

    def abrir_janela_freelance():
        """Abre a janela principal de freelance, que se adapta se houver um projeto ativo."""
        janelas_abertas.clear()
        
        projeto_ativo = jogador_projeto_service.buscar_projeto_ativo(JOGADOR_ATUAL.get_id_jogador())
        
        projetos_info = []
        if not projeto_ativo:
            # Usa o serviço refatorado para obter a lista de projetos com o status de requisitos
            projetos_info = projeto_service.listar_projetos_para_jogador(JOGADOR_ATUAL)

        janela = TelaFreelance(
            LARGURA, ALTURA,
            projeto_ativo=projeto_ativo,
            projetos_info=projetos_info,
            cliente_service=cliente_service,
            callback_abrir_desenvolvimento=abrir_janela_detalhes # Clicar em um projeto abre os detalhes
        )
        janelas_abertas.append(janela)

    def abrir_janela_detalhes(projeto):
        """Abre o Dossiê de Contrato (Painel de Análise Estratégica)."""
        janelas_abertas.clear()
        
        cliente = cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        
        janela = TelaProjeto(
            LARGURA, ALTURA,
            projeto=projeto,
            cliente=cliente,
            jogador=JOGADOR_ATUAL,
            callback_aceitar=aceitar_projeto,
            callback_voltar=abrir_janela_freelance
        )
        janelas_abertas.append(janela)

    def aceitar_projeto(projeto):
        """Lógica final para aceitar um contrato, chamada pela TelaProjeto."""
        # 1. Checa se o jogador já tem um projeto ativo
        if jogador_projeto_service.buscar_projeto_ativo(JOGADOR_ATUAL.get_id_jogador()):
            print("ERRO: Jogador já possui um projeto ativo.")
            # Idealmente, mostrar uma mensagem visual para o jogador
            return

        # 2. Checa se o jogador tem os requisitos de skill
        tem_req = (JOGADOR_ATUAL.get_nivel_backend() >= projeto.get_req_backend() and
                   JOGADOR_ATUAL.get_nivel_frontend() >= projeto.get_req_frontend() and
                   JOGADOR_ATUAL.get_nivel_social() >= projeto.get_req_social())

        if not tem_req:
            print("SKILLS INSUFICIENTES! Não é possível aceitar este contrato.")
            return
            
        # 3. Se tudo estiver certo, aceita o projeto
        # (Aqui você chamaria o service para criar a relação jogador_projeto no banco)
        print(f"Contrato '{projeto.get_titulo()}' aceito com sucesso!")
        
        # 4. Volta para a tela de freelance, que agora mostrará o painel de projeto ativo
        abrir_janela_freelance()

    # --- Callbacks do Menu Principal ---
    callbacks_principais = {
        "Freelance": abrir_janela_freelance,
        "Exercícios": lambda: print("Abrir janela de exercícios..."),
        "Loja": lambda: print("Abrir janela da loja...")
    }
    
    botoes_principais_rects = {
        "Freelance": pygame.Rect(150, 280, 200, 50),
        "Exercícios": pygame.Rect(150, 340, 200, 50),
        "Loja": pygame.Rect(150, 400, 200, 50)
    }
    
    hotspot_computador = pygame.Rect(int(LARGURA * 0.40), int(ALTURA * 0.36), 250, 230)

    # --- Loop Principal do Jogo ---
    rodando = True
    while rodando:
        dt = clock.tick(60)
        eventos = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in eventos:
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if janelas_abertas: janelas_abertas[-1].deve_fechar = True
                elif menu_principal_visivel: menu_principal_visivel = False
                else: rodando = False

            if janelas_abertas:
                janelas_abertas[-1].tratar_eventos([evento])
            else:
                if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    if menu_principal_visivel:
                        for nome, rect in botoes_principais_rects.items():
                            if rect.collidepoint(evento.pos):
                                callbacks_principais[nome](); menu_principal_visivel = False; break
                    elif hotspot_computador.collidepoint(evento.pos):
                        menu_principal_visivel = True

        if janelas_abertas:
            janela_topo = janelas_abertas[-1]
            if hasattr(janela_topo, 'update'): janela_topo.update(dt)

        TELA.blit(fundo_jogo, (0, 0))
        
        if not janelas_abertas and menu_principal_visivel:
            for nome, rect in botoes_principais_rects.items():
                cor_fundo = (0, 0, 0, 150) if rect.collidepoint(mouse_pos) else (0, 0, 0, 100)
                cor_texto = (255, 255, 255) if rect.collidepoint(mouse_pos) else (200, 200, 200)
                fundo_surf = pygame.Surface(rect.size, pygame.SRCALPHA); fundo_surf.fill(cor_fundo)
                TELA.blit(fundo_surf, rect.topleft)
                texto_surf = fonte_menu_principal.render(nome, True, cor_texto)
                TELA.blit(texto_surf, (rect.centerx - texto_surf.get_width() // 2, rect.centery - texto_surf.get_height() // 2))

        for janela in janelas_abertas:
            janela.desenhar(TELA)

        pygame.display.flip()

        janelas_fechadas_neste_frame = any(j.deve_fechar for j in janelas_abertas)
        janelas_abertas = [j for j in janelas_abertas if not j.deve_fechar]
        
        if not janelas_abertas and janelas_fechadas_neste_frame and not menu_principal_visivel:
            menu_principal_visivel = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
