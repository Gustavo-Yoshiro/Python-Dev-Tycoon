from Intermediario.Service.ClienteService import ClienteService
from Intermediario.Persistencia.Impl.ClientePersistenciaImpl import ClientePersistenciaImpl
from Intermediario.Persistencia.Entidade.Cliente import Cliente

class ClienteServiceImpl(ClienteService):
    def __init__(self, persistencia: ClientePersistenciaImpl):
        self.persistencia = persistencia

    def criar_cliente(self, cliente: Cliente):
        if not cliente.get_nome():
            raise ValueError("O cliente precisa ter um nome.")
        return self.persistencia.salvar(cliente)

    def buscar_cliente_por_id(self, id_cliente: int) -> Cliente:
        return self.persistencia.buscar_por_id(id_cliente)

    def listar_clientes(self) -> list[Cliente]:
        return self.persistencia.listar_todos()

    def atualizar_cliente(self, cliente: Cliente):
        if cliente.get_reputacao() < 0 or cliente.get_reputacao() > 100:
            raise ValueError("Reputação deve estar entre 0 e 100.")
        self.persistencia.atualizar(cliente)

    def deletar_cliente(self, id_cliente: int):
        self.persistencia.deletar(id_cliente)