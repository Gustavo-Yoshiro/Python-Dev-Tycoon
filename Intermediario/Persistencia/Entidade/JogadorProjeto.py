class JogadorProjeto:
    def __init__(self, id_jogador, id_projeto, status, detalhes_descobertos=None):
        self.__id_jogador = id_jogador
        self.__id_projeto = id_projeto
        self.__status = status
        self.__detalhes_descobertos = detalhes_descobertos

    # --- Getters ---
    def get_id_jogador(self):
        return self.__id_jogador

    def get_id_projeto(self):
        return self.__id_projeto

    def get_status(self):
        return self.__status

    def get_detalhes_descobertos(self):
        return self.__detalhes_descobertos

    # --- Setters ---
    def set_status(self, status):
        self.__status = status
        
    def set_detalhes_descobertos(self, detalhes):
        self.__detalhes_descobertos = detalhes
