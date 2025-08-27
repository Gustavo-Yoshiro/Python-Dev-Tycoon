class JogadorProjeto:
    def __init__(self, id_jogador, id_projeto, status):
        self.__id_jogador = id_jogador
        self.__id_projeto = id_projeto
        self.__status = status

    def get_id_jogador(self):
        return self.__id_jogador

    def get_id_projeto(self):
        return self.__id_projeto

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
