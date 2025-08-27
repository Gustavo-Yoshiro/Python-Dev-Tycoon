# Certifique-se de que os caminhos de importação estão corretos
from Intermediario.Service.ClienteService import ClienteService
from Intermediario.Persistencia.Impl.ClientePersistenciaImpl import ClientePersistenciaImpl
from Intermediario.Persistencia.Entidade.Cliente import Cliente

class ClienteServiceImpl(ClienteService):
    def __init__(self):
        self.persistencia = ClientePersistenciaImpl()

    def criar_cliente(self, cliente):
        """
        Cria um novo cliente.
        Validação de negócio: Garante que o cliente tenha um nome.
        """
        if not cliente.get_nome() or not cliente.get_nome().strip():
            raise ValueError("O nome do cliente não pode ser vazio.")
        return self.persistencia.salvar(cliente)

    def buscar_cliente_por_id(self, id_cliente):
        """Busca um cliente específico pelo seu ID."""
        return self.persistencia.buscar_por_id(id_cliente)

    def listar_clientes(self):
        """Retorna uma lista de todos os clientes."""
        return self.persistencia.listar_todos()

    def atualizar_cliente(self, cliente):
        """
        Atualiza um cliente existente.
        Validação de negócio: Garante que a reputação esteja entre 0 e 5.
        """
        if not 0 <= cliente.get_reputacao() <= 5:
            raise ValueError("A reputação do cliente deve estar entre 0.0 e 5.0.")
        self.persistencia.atualizar(cliente)

    def deletar_cliente(self, id_cliente):
        """Deleta um cliente pelo seu ID."""
        self.persistencia.deletar(id_cliente)
