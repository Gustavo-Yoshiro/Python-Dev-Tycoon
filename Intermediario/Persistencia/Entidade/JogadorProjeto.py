class JogadorProjeto:
    def __init__(self, id_jogador=None, id_projeto=None, status="em_andamento"):
        self.__id_jogador = id_jogador
        self.__id_projeto = id_projeto
        self.__status = status

   
    # Getters
    def get_id_jogador(self):
        return self.__id_jogador

    def get_id_projeto(self):
        return self.__id_projeto

    def get_status(self):
        return self.__status

    # Setters
    def set_id_jogador(self, id_jogador):
        self.__id_jogador = id_jogador

    def set_id_projeto(self, id_projeto):
        self.__id_projeto = id_projeto

    def set_status(self, status):
        self.__status = status