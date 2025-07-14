class Save:
    def __init__(self, id_save, id_jogador, data_save, tempo_jogo=0):
        self.__id_save = id_save
        self.__id_jogador = id_jogador
        self.__data_save = data_save
        self.__tempo_jogo = tempo_jogo

    def get_id_save(self):
        return self.__id_save

    def get_id_jogador(self):
        return self.__id_jogador

    def get_data_save(self):
        return self.__data_save

    def get_tempo_jogo(self):
        return self.__tempo_jogo

    def set_id_save(self, id_save):
        self.__id_save = id_save

    def set_id_jogador(self, id_jogador):
        self.__id_jogador = id_jogador

    def set_data_save(self, data_save):
        self.__data_save = data_save

    def set_tempo_jogo(self, tempo_jogo):
        self.__tempo_jogo = tempo_jogo