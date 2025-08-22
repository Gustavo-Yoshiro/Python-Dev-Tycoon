class ProjetoFreelance:
    def __init__(self, id_projeto=None, id_cliente=None, titulo=None, descricao=None, 
                 dificuldade=1, recompensa=0, habilidade_requerida=None, status="disponivel"):
        self.__id_projeto = id_projeto
        self.__id_cliente = id_cliente
        self.__titulo = titulo
        self.__descricao = descricao
        self.__dificuldade = dificuldade
        self.__recompensa = recompensa
        self.__habilidade_requerida = habilidade_requerida
        self.__status = status


    # Getters
    def get_id_projeto(self):
        return self.__id_projeto

    def get_id_cliente(self):
        return self.__id_cliente

    def get_titulo(self):
        return self.__titulo

    def get_descricao(self):
        return self.__descricao

    def get_dificuldade(self):
        return self.__dificuldade

    def get_recompensa(self):
        return self.__recompensa

    def get_habilidade_requerida(self):
        return self.__habilidade_requerida

    def get_status(self):
        return self.__status

    # Setters
    def set_id_projeto(self, id_projeto):
        self.__id_projeto = id_projeto

    def set_id_cliente(self, id_cliente):
        self.__id_cliente = id_cliente

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_dificuldade(self, dificuldade):
        self.__dificuldade = dificuldade

    def set_recompensa(self, recompensa):
        self.__recompensa = recompensa

    def set_habilidade_requerida(self, habilidade_requerida):
        self.__habilidade_requerida = habilidade_requerida

    def set_status(self, status):
        self.__status = status