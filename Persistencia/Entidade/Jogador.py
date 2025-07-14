
class Jogador:
    def __init__(self, id_jogador, nome, id_fase, social, dinheiro, backend, frontend):
        self.__id_jogador = id_jogador
        self.__nome = nome
        self.__id_fase = id_fase
        self.__social = social
        self.__dinheiro = dinheiro
        self.__backend = backend
        self.__frontend = frontend

    # Getters
    def get_id_jogador(self):
        return self.__id_jogador

    def get_nome(self):
        return self.__nome

    def get_id_fase(self):
        return self.__id_fase

    def get_social(self):
        return self.__social

    def get_dinheiro(self):
        return self.__dinheiro

    def get_backend(self):
        return self.__backend

    def get_frontend(self):
        return self.__frontend

    # Setters
    def set_id_jogador(self, id_jogador):
        self.__id_jogador = id_jogador

    def set_nome(self, nome):
        self.__nome = nome

    def set_id_fase(self, id_fase):
        self.__id_fase = id_fase

    def set_social(self, social):
        self.__social = social

    def set_dinheiro(self, dinheiro):
        self.__dinheiro = dinheiro

    def set_backend(self, backend):
        self.__backend = backend

    def set_frontend(self, frontend):
        self.__frontend = frontend
