class Exercicio:
    def __init__(self, id_exercicio, id_fase, dicas, pergunta, tipo, resposta_certa, resposta_erradas):
        self.__id_exercicio = id_exercicio
        self.__id_fase = id_fase
        self.__dicas = dicas
        self.__pergunta = pergunta
        self.__tipo = tipo 
        self.__resposta_certa = resposta_certa
        self.__resposta_erradas = resposta_erradas

    def get_id_exercicio(self):
        return self.__id_exercicio

    def get_id_fase(self):
        return self.__id_fase

    def get_dicas(self):
        return self.__dicas

    def get_pergunta(self):
        return self.__pergunta

    def get_tipo(self):
        return self.__tipo

    def get_resposta_certa(self):
        return self.__resposta_certa

    def get_resposta_erradas(self):
        return self.__resposta_erradas

    def set_id_exercicio(self, id_exercicio):
        self.__id_exercicio = id_exercicio

    def set_id_fase(self, id_fase):
        self.__id_fase = id_fase

    def set_dicas(self, dicas):
        self.__dicas = dicas

    def set_pergunta(self, pergunta):
        self.__pergunta = pergunta

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def set_resposta_certa(self, resposta_certa):
        self.__resposta_certa = resposta_certa

    def set_resposta_erradas(self, resposta_erradas):
        self.__resposta_erradas = resposta_erradas