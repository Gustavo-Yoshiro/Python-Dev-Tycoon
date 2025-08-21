class Cliente:
    def __init__(self, id_cliente=None, nome=None, area_atuacao=None, reputacao=50, descricao=None):
        self.__id_cliente = id_cliente
        self.__nome = nome
        self.__area_atuacao = area_atuacao
        self.__reputacao = reputacao
        self.__descricao = descricao
 
    # Getters
    def get_id_cliente(self):
        return self.__id_cliente

    def get_nome(self):
        return self.__nome

    def get_area_atuacao(self):
        return self.__area_atuacao

    def get_reputacao(self):
        return self.__reputacao

    def get_descricao(self):
        return self.__descricao

    # Setters
    def set_id_cliente(self, id_cliente):
        self.__id_cliente = id_cliente

    def set_nome(self, nome):
        self.__nome = nome

    def set_area_atuacao(self, area_atuacao):
        self.__area_atuacao = area_atuacao

    def set_reputacao(self, reputacao):
        self.__reputacao = reputacao

    def set_descricao(self, descricao):
        self.__descricao = descricao