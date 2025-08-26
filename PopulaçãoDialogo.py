from Intermediario.Service.Impl.DialogoServiceImpl import DialogoServiceImpl
from Intermediario.Service.Impl.ProjetoFreelanceServiceImpl import ProjetoFreelanceServiceImpl
from Intermediario.Persistencia.Entidade.Dialogo import DialogoNo, DialogoOpcao
from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

def popular_dialogos(dialogo_service, projeto_service):
    """Popula as árvores de diálogo para os projetos existentes."""
    
    print("Limpando diálogos antigos...")
    # É uma boa prática limpar os diálogos antigos antes de inserir os novos
    # Você precisaria adicionar métodos para isso na sua persistência/serviço
    # Ex: dialogo_service.deletar_todos_dialogos()
    
    # --- Diálogo para o Projeto "Calculadora de Café" (ID 1) ---
    # Busca o projeto pelo título para garantir que temos o ID correto
    projetos = projeto_service.persistencia.listar_disponiveis()
    proj_cafe = next((p for p in projetos if p.get_titulo() == 'Calculadora de Café'), None)

    if proj_cafe:
        print(f"Criando diálogo para o projeto: {proj_cafe.get_titulo()}")
        # Nós da Conversa
        no1 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj_cafe.get_id_projeto(), 'Olá! Que bom que se interessou. Preciso de uma ajudinha com os cálculos na minha cafeteria.', True))
        no2 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj_cafe.get_id_projeto(), 'É bem simples: uma função que receba o preço e a quantidade, e retorne o valor total formatado.', False))
        no3 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj_cafe.get_id_projeto(), 'O pagamento é R$ 100.00. É um trabalho rápido, então o valor é fixo.', False))
        no4 = dialogo_service.no_persistencia.salvar(DialogoNo(None, proj_cafe.get_id_projeto(), 'Entendo. Pela sua confiança, posso aumentar para R$ 120.00. É o meu melhor preço.', False))

        # Opções que Conectam os Nós
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no1.get_id_no(), no2.get_id_no(), 'Claro! Conte-me mais sobre o projeto.', 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no1.get_id_no(), no3.get_id_no(), 'Antes de mais nada, vamos falar do pagamento.', 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no2.get_id_no(), no3.get_id_no(), 'Parece simples. E sobre a recompensa?', 1, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no3.get_id_no(), None, 'Entendido. Aceito o trabalho por R$ 100.00.', 1, 'ACEITAR_PROJETO'))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no3.get_id_no(), no4.get_id_no(), '[Social 3] Acredito que minha experiência justifica um valor maior.', 3, None))
        dialogo_service.opcao_persistencia.salvar(DialogoOpcao(None, no4.get_id_no(), None, 'Fechado! Aceito por R$ 120.00.', 1, 'ACEITAR_PROJETO_COM_BONUS'))
    else:
        print("Projeto 'Calculadora de Café' não encontrado para criar diálogo.")

    # Adicione aqui a lógica para outros projetos...

if __name__ == "__main__":
    print("Iniciando a população de Diálogos...")
    
    db_manager = BancoDeDadosIntermediario()


    dialogo_service = DialogoServiceImpl()
    projeto_service = ProjetoFreelanceServiceImpl()

    popular_dialogos(dialogo_service, projeto_service)

    print("\nPopulação de Diálogos concluída!")
