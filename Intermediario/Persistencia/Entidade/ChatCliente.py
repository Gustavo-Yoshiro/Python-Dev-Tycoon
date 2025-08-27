class ChatCliente:
    def __init__(self, id_chat, id_jogador, id_cliente, mensagem, enviado_por, data_envio=None):
        self.__id_chat = id_chat
        self.__id_jogador = id_jogador
        self.__id_cliente = id_cliente
        self.__mensagem = mensagem
        self.__enviado_por = enviado_por
        self.__data_envio = data_envio

    # --- Getters ---
    def get_id_chat(self):
        return self.__id_chat

    def get_id_jogador(self):
        return self.__id_jogador

    def get_id_cliente(self):
        return self.__id_cliente

    def get_mensagem(self):
        return self.__mensagem

    def get_enviado_por(self):
        return self.__enviado_por

    def get_data_envio(self):
        return self.__data_envio

    # --- Setters ---
    def set_id_chat(self, id_chat):
        self.__id_chat = id_chat

    def set_mensagem(self, mensagem):
        self.__mensagem = mensagem
