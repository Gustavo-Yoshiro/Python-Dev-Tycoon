import pygame
import sys
import random
from datetime import datetime

# --- Importações de Entidades e Serviços ---
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Service.Impl.ChatClienteServiceImpl import ChatClienteServiceImpl
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl

# --- Importações das Janelas de UI ---
from Intermediario.UI.TelaFreelance import TelaFreelance
from Intermediario.UI.TelaProjeto import TelaProjeto
from Intermediario.UI.TelaChatCliente import TelaChatCliente
from Intermediario.UI.TelaResultadoFreelance import TelaResultado

# --- Constantes ---
LARGURA, ALTURA = 1280, 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Python Dev Tycoon")
JOGADOR_ID_ATUAL = 1

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # --- Carregar a imagem de fundo ---
    try:
        fundo_jogo = pygame.image.load("assets/TelaJogoIniciante.png").convert()
        fundo_jogo = pygame.transform.scale(fundo_jogo, (LARGURA, ALTURA))
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        fundo_jogo = pygame.Surface((LARGURA, ALTURA)); fundo_jogo.fill((25, 25, 35))
        
    # --- Inicialização dos Serviços ---
    projeto_service = ProjetoFreelanceServiceImpl()
    cliente_service = ClienteServiceImpl()
    chat_service = ChatClienteServiceImpl()
    jogador_projeto_service = JogadorProjetoServiceImpl()

    # --- Gerenciador de Janelas ---
    janelas_abertas = []
    menu_principal_visivel = False
    fonte_menu_principal = pygame.font.SysFont("Arial", 24, bold=True)
    
    # --- Funções de Orquestração (Callbacks) ---

    def abrir_janela_freelance():
        if any(isinstance(j, TelaFreelance) for j in janelas_abertas): return
        projetos = projeto_service.listar_projetos_disponiveis()
        janela = TelaFreelance(
            projetos=projetos,
            cliente_service=cliente_service,
            callback_ver_detalhes=abrir_janela_detalhes # <--- CORRIGIDO
        )
        janelas_abertas.append(janela)

    def abrir_janela_detalhes(projeto):
        cliente = cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        janela = TelaProjeto(
            projeto=projeto, cliente=cliente,
            callback_aceitar=aceitar_projeto,
            callback_chat=abrir_janela_chat,
            callback_voltar=abrir_janela_freelance # Voltar reabre a lista
        )
        janelas_abertas.append(janela)

    def aceitar_projeto(projeto):
        relacao = jogador_projeto_service.buscar_relacao(JOGADOR_ID_ATUAL, projeto.get_id_projeto())
        if not relacao:
            novo_projeto = JogadorProjeto(JOGADOR_ID_ATUAL, projeto.get_id_projeto(), "em_andamento")
            jogador_projeto_service.aceitar_projeto(novo_projeto)
        print(f"Projeto {projeto.get_titulo()} aceito!")
        abrir_janela_chat(projeto)

    def abrir_janela_chat(projeto):
        # Fecha outras janelas para focar no chat
        janelas_abertas.clear()
        cliente = cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        mensagens = chat_service.persistencia.listarPorCliente(cliente.get_id_cliente())
        janela = TelaChatCliente(
            projeto=projeto, cliente=cliente, mensagens=mensagens,
            callback_enviar=enviar_mensagem,
            callback_finalizar=finalizar_projeto,
            # Voltar do chat reabre a janela de detalhes
            callback_voltar=lambda: abrir_janela_detalhes(projeto) 
        )
        janelas_abertas.append(janela)

    def enviar_mensagem(projeto, texto_resposta):
        nova_msg = ChatCliente(None, JOGADOR_ID_ATUAL, projeto.get_id_cliente(), texto_resposta, 'jogador', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        chat_service.persistencia.salvar(nova_msg)
        abrir_janela_chat(projeto)

    def finalizar_projeto(projeto):
        sucesso = random.random() < 0.8
        status = "concluido" if sucesso else "falhou"
        jogador_projeto_service.atualizar_status(JOGADOR_ID_ATUAL, projeto.get_id_projeto(), status)
        abrir_janela_resultado(sucesso, projeto.get_recompensa())

    def abrir_janela_resultado(sucesso, recompensa):
        janelas_abertas.clear()
        janela = TelaResultado(sucesso, recompensa, callback_continuar=abrir_janela_freelance)
        janelas_abertas.append(janela)

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
        eventos = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if janelas_abertas:
                    janelas_abertas[-1].deve_fechar = True
                elif menu_principal_visivel:
                    menu_principal_visivel = False
                else:
                    rodando = False

            if janelas_abertas:
                janelas_abertas[-1].tratar_eventos([evento])
            else:
                if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    if menu_principal_visivel:
                        for nome, rect in botoes_principais_rects.items():
                            if rect.collidepoint(evento.pos):
                                callbacks_principais[nome]()
                                menu_principal_visivel = False
                                break
                    elif hotspot_computador.collidepoint(evento.pos):
                        menu_principal_visivel = True

        # --- Lógica de Desenho ---
        TELA.blit(fundo_jogo, (0, 0))
        
        if not janelas_abertas and menu_principal_visivel:
            for nome, rect in botoes_principais_rects.items():
                cor_fundo = (0, 0, 0, 150) if rect.collidepoint(mouse_pos) else (0, 0, 0, 100)
                cor_texto = (255, 255, 255) if rect.collidepoint(mouse_pos) else (200, 200, 200)
                fundo_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
                fundo_surf.fill(cor_fundo)
                TELA.blit(fundo_surf, rect.topleft)
                texto_surf = fonte_menu_principal.render(nome, True, cor_texto)
                TELA.blit(texto_surf, (rect.centerx - texto_surf.get_width() // 2, rect.centery - texto_surf.get_height() // 2))

        for janela in janelas_abertas:
            janela.desenhar(TELA)

        pygame.display.flip()

        # --- Limpeza de Janelas ---
        janelas_fechadas_neste_frame = any(j.deve_fechar for j in janelas_abertas)
        janelas_abertas = [j for j in janelas_abertas if not j.deve_fechar]
        
        if not janelas_abertas and janelas_fechadas_neste_frame and not menu_principal_visivel:
            menu_principal_visivel = True

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()