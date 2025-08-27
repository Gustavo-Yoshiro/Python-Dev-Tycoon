class Cliente:
    def __init__(self, id_cliente: int, nome: str, area_atuacao: str, descricao: str, reputacao: float, personalidade: str):
        self.__id_cliente = id_cliente
        self.__nome = nome
        self.__area_atuacao = area_atuacao
        self.__descricao = descricao
        self.__reputacao = reputacao
        self.__personalidade = personalidade
    
    # --- Getters ---
    def get_id_cliente(self) -> int:
        return self.__id_cliente

    def get_nome(self) -> str:
        return self.__nome

    def get_area_atuacao(self) -> str:
        return self.__area_atuacao

    def get_descricao(self) -> str:
        return self.__descricao

    def get_reputacao(self) -> float:
        return self.__reputacao

    def get_personalidade(self) -> str:
        return self.__personalidade
    
    # --- Setters ---
    def set_id_cliente(self, id_cliente: int):
        self.__id_cliente = id_cliente
        
    def set_nome(self, nome: str):
        self.__nome = nome

    def set_area_atuacao(self, area_atuacao: str):
        self.__area_atuacao = area_atuacao

    def set_descricao(self, descricao: str):
        self.__descricao = descricao

    def set_reputacao(self, reputacao: float):
        self.__reputacao = reputacao

    def set_personalidade(self, personalidade: str):
        self.__personalidade = personalidade
