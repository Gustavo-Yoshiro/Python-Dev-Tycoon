class Loja:
    def __init__(self, id_item, id_jogador, nome, categoria, preco, duracao_segundos, status, duracao_total):
        self.__id_item = id_item
        self.__id_jogador = id_jogador
        self.__nome = nome
        self.__categoria = categoria
        self.__preco = preco
        self.__duracao_segundos = duracao_segundos
        self.__status = status
        self.__duracao_total = duracao_total

    # Getters
    def get_id_item(self):
        return self.__id_item

    def get_id_jogador(self):
        return self.__id_jogador

    def get_nome(self):
        return self.__nome

    def get_categoria(self):
        return self.__categoria

    def get_preco(self):
        return self.__preco

    def get_duracao_segundos(self):
        return self.__duracao_segundos

    def get_status(self):
        return self.__status

    def get_inicio(self):
        return self.__inicio

    def get_fim(self):
        return self.__fim
    
    def get_duracao_total(self):           # 👈 getter novo
        return self.__duracao_total

    # Setters
    def set_id_item(self, id_item):
        self.__id_item = id_item

    def set_id_jogador(self, id_jogador):
        self.__id_jogador = id_jogador

    def set_nome(self, nome):
        self.__nome = nome

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def set_preco(self, preco):
        self.__preco = preco

    def set_duracao_segundos(self, duracao_segundos):
        self.__duracao_segundos = duracao_segundos

    def set_status(self, status):
        self.__status = status

    def set_inicio(self, inicio):
        self.__inicio = inicio

    def set_fim(self, fim):
        self.__fim = fim

    def set_duracao_total(self, duracao_total):   # 👈 setter novo
        self.__duracao_total = duracao_total
    