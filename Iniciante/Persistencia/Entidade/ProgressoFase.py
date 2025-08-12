class ProgressoFase:
    def __init__(
        self, id_progresso=None, id_jogador=None, id_fase=None,
        indice_exercicio=0, acertos=0, erros=0,
        resposta_parcial="", atualizado_em=None
    ):
        self.__id_progresso = id_progresso
        self.__id_jogador = id_jogador
        self.__id_fase = id_fase
        self.__indice_exercicio = indice_exercicio
        self.__acertos = acertos
        self.__erros = erros
        self.__resposta_parcial = resposta_parcial
        self.__atualizado_em = atualizado_em

    # Getters
    def get_id_progresso(self):
        return self.__id_progresso

    def get_id_jogador(self):
        return self.__id_jogador

    def get_id_fase(self):
        return self.__id_fase

    def get_indice_exercicio(self):
        return self.__indice_exercicio

    def get_acertos(self):
        return self.__acertos

    def get_erros(self):
        return self.__erros

    def get_resposta_parcial(self):
        return self.__resposta_parcial

    def get_atualizado_em(self):
        return self.__atualizado_em

    # Setters
    def set_id_progresso(self, id_progresso):
        self.__id_progresso = id_progresso

    def set_id_jogador(self, id_jogador):
        self.__id_jogador = id_jogador

    def set_id_fase(self, id_fase):
        self.__id_fase = id_fase

    def set_indice_exercicio(self, indice_exercicio):
        self.__indice_exercicio = indice_exercicio

    def set_acertos(self, acertos):
        self.__acertos = acertos

    def set_erros(self, erros):
        self.__erros = erros

    def set_resposta_parcial(self, resposta_parcial):
        self.__resposta_parcial = resposta_parcial

    def set_atualizado_em(self, atualizado_em):
        self.__atualizado_em = atualizado_em
