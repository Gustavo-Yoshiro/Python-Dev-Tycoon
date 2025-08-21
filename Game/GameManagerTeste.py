import pygame
import sys
import random
from datetime import datetime

# --- Importações de Entidades (para criar objetos) ---
from Intermediario.Persistencia.Entidade.ChatCliente import ChatCliente
from Intermediario.Persistencia.Entidade.JogadorProjeto import JogadorProjeto

# --- Importações de SERVIÇO (a única camada que a UI conhece) ---
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Service.Impl.ClienteServiceImpl import ClienteServiceImpl
from Intermediario.Service.Impl.ChatClienteServiceImpl import ChatClienteServiceImpl
from Intermediario.Service.Impl.JogadorProjetoServiceImpl import JogadorProjetoServiceImpl

# --- Importações das classes de UI ---
from Intermediario.UI.TelaIntermediario import TelaIntermediario
from Intermediario.UI.TelaFreelance import TelaFreelance
from Intermediario.UI.TelaProjeto import TelaProjeto
from Intermediario.UI.TelaChatCliente import TelaChatCliente
from Intermediario.UI.TelaResultadoFreelance import TelaResultado

# --- Constantes ---
LARGURA, ALTURA = 1280, 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Python Dev Tycoon")
JOGADOR_ID_ATUAL = 1  # Fixo por enquanto, viria de um save no futuro

# --- Estados do Jogo ---
ESTADO_TELA_INTERMEDIARIA = "TELA_INTERMEDIARIA"
ESTADO_TELA_FREELANCE = "TELA_FREELANCE"
ESTADO_TELA_PROJETO = "TELA_PROJETO"
ESTADO_TELA_CHAT = "TELA_CHAT"
ESTADO_TELA_RESULTADO = "TELA_RESULTADO"

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # --- INICIALIZAÇÃO DOS SERVIÇOS ---
    try:
        projeto_service = ProjetoFreelanceServiceImpl()
        cliente_service = ClienteServiceImpl()
        chat_service = ChatClienteServiceImpl()
        jogador_projeto_service = JogadorProjetoServiceImpl()
    except Exception as e:
        print(f"Erro fatal ao inicializar serviços: {e}")
        sys.exit()

    # --- Variáveis de controle de fluxo e dados ---
    estado_atual = ESTADO_TELA_INTERMEDIARIA
    tela_ativa = None
    
    # --- Funções de Callback (A "cola" que une UI e Lógica) ---

    def ir_para_freelance():
        nonlocal estado_atual, tela_ativa
        try:
            lista_projetos = projeto_service.listar_projetos_disponiveis()
            estado_atual = ESTADO_TELA_FREELANCE
            tela_ativa = TelaFreelance(
                LARGURA, ALTURA,
                projetos=lista_projetos,
                callback_selecionar=selecionar_projeto,
                callback_voltar=voltar_para_intermediaria
            )
        except Exception as e:
            print(f"Erro ao carregar projetos do serviço: {e}")

    def selecionar_projeto(projeto):
        nonlocal estado_atual, tela_ativa
        cliente = cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        estado_atual = ESTADO_TELA_PROJETO
        tela_ativa = TelaProjeto(
            LARGURA, ALTURA,
            projeto=projeto,
            cliente=cliente,
            callback_aceitar=aceitar_projeto,
            callback_voltar=ir_para_freelance
        )

    def aceitar_projeto(projeto):
        nonlocal estado_atual, tela_ativa
        try:
            # Verifica se o jogador já aceitou este projeto para não duplicar
            relacao_existente = jogador_projeto_service.buscar_relacao(JOGADOR_ID_ATUAL, projeto.get_id_projeto())
            if not relacao_existente:
                novo_projeto_aceito = JogadorProjeto(
                    id_jogador=JOGADOR_ID_ATUAL,
                    id_projeto=projeto.get_id_projeto(),
                    status="em_andamento"
                )
                jogador_projeto_service.aceitar_projeto(novo_projeto_aceito)
            
            # Após aceitar (ou se já aceitou), abre o chat
            abrir_chat(projeto)
            
        except Exception as e:
            print(f"Erro ao aceitar projeto: {e}")

    def abrir_chat(projeto):
        nonlocal estado_atual, tela_ativa
        cliente = cliente_service.buscar_cliente_por_id(projeto.get_id_cliente())
        # Use o método correto do seu serviço para buscar a conversa
        mensagens = chat_service.persistencia.listarPorCliente(cliente.get_id_cliente())
        
        estado_atual = ESTADO_TELA_CHAT
        tela_ativa = TelaChatCliente(
            LARGURA, ALTURA,
            projeto=projeto, cliente=cliente, mensagens=mensagens,
            callback_enviar=enviar_mensagem,
            callback_finalizar=finalizar_projeto,
            callback_voltar=lambda: selecionar_projeto(projeto) # Volta para os detalhes do projeto
        )

    def enviar_mensagem(projeto, texto_resposta):
        """Salva a mensagem do jogador no banco e recarrega a tela de chat."""
        try:
            nova_mensagem = ChatCliente(
                id_chat=None, # O ID será gerado pelo banco
                id_jogador=JOGADOR_ID_ATUAL,
                id_cliente=projeto.get_id_cliente(),
                mensagem=texto_resposta,
                enviado_por='jogador',
                data_envio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            chat_service.persistencia.salvar(nova_mensagem) # Usa o método de salvar da persistencia
            
            # Recarrega a tela de chat para mostrar a nova mensagem
            abrir_chat(projeto)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    def finalizar_projeto(projeto):
        """Simula a lógica de finalização do projeto e mostra o resultado."""
        # LÓGICA DE JOGO: Aqui você verificaria as habilidades do jogador
        # contra a dificuldade do projeto para determinar o sucesso.
        # Por enquanto, vamos simular com 80% de chance de sucesso.
        sucesso = random.random() < 0.8 
        
        if sucesso:
            jogador_projeto_service.atualizar_status(JOGADOR_ID_ATUAL, projeto.get_id_projeto(), "concluido")
            mostrar_resultado(True, projeto.get_recompensa())
        else:
            jogador_projeto_service.atualizar_status(JOGADOR_ID_ATUAL, projeto.get_id_projeto(), "falhou")
            mostrar_resultado(False, 0)
            
    def mostrar_resultado(sucesso, recompensa):
        nonlocal estado_atual, tela_ativa
        estado_atual = ESTADO_TELA_RESULTADO
        tela_ativa = TelaResultado(
            LARGURA, ALTURA,
            sucesso=sucesso,
            recompensa=recompensa,
            callback_continuar=ir_para_freelance # Após o resultado, volta à lista de freelances
        )

    def voltar_para_intermediaria():
        nonlocal estado_atual, tela_ativa
        estado_atual = ESTADO_TELA_INTERMEDIARIA
        criar_tela_intermediaria()

    def criar_tela_intermediaria():
        nonlocal tela_ativa
        tela_ativa = TelaIntermediario(
            LARGURA, ALTURA,
            callback_exercicios=lambda: print("Indo para Exercícios..."),
            callback_freelancer=ir_para_freelance,
            callback_loja=lambda: print("Indo para Loja...")
        )

    # --- Inicialização ---
    criar_tela_intermediaria()
    rodando = True
    
    # --- LOOP PRINCIPAL ---
    while rodando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        
        if tela_ativa:
            tela_ativa.tratar_eventos(eventos)
            tela_ativa.desenhar(TELA)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()