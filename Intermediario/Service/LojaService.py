from abc import ABC, abstractmethod

class LojaService(ABC):
    @abstractmethod
    def comprar_item(self, id_jogador: int, nome: str, categoria: str, preco: float, duracao_segundos: int):
        pass

    @abstractmethod
    def buscar_item_por_id(self, id_item: int):
        pass

    @abstractmethod
    def listar_itens_jogador(self, id_jogador: int):
        pass

    @abstractmethod
    def listar_em_andamento(self, id_jogador: int):
        pass

    @abstractmethod
    def concluir_item(self, id_item: int):
        pass

    @abstractmethod
    def deletar_item(self, id_item: int):
        pass

    @abstractmethod
    def atualizar_item(self, loja):
        pass
