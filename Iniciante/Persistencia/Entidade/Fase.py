class Fase:
    def __init__(self, id_fase, tipo_fase, topico, introducao):
        self.__id_fase = id_fase
        self.__tipo_fase = tipo_fase
        self.__topico = topico
        self.__introducao = introducao

    # Getters
    def get_id_fase(self):
        return self.__id_fase

    def get_tipo_fase(self):
        return self.__tipo_fase

    def get_topico(self):
        return self.__topico

    def get_introducao(self):
        return self.__introducao

    # Setters
    def set_id_fase(self, id_fase):
        self.__id_fase = id_fase

    def set_tipo_fase(self, tipo_fase):
        self.__tipo_fase = tipo_fase

    def set_topico(self, topico):
        self.__topico = topico

    def set_introducao(self, introducao):
        self.__introducao = introducao
