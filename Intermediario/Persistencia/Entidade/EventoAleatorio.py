class EventoAleatorio:
    def __init__(self, id_evento, titulo, descricao, dificuldade, recompensa_dinheiro, 
                 resposta_certa, resposta_errada, entrada_teste, 
                 tempo_aparecer_min, tempo_aparecer_max, tempo_para_fazer, status="ativo"):
        self.__id_evento = id_evento
        self.__titulo = titulo
        self.__descricao = descricao
        self.__dificuldade = dificuldade
        self.__recompensa_dinheiro = recompensa_dinheiro
        self.__resposta_certa = resposta_certa
        self.__resposta_errada = resposta_errada
        self.__entrada_teste = entrada_teste
        self.__tempo_aparecer_min = tempo_aparecer_min
        self.__tempo_aparecer_max = tempo_aparecer_max
        self.__tempo_para_fazer = tempo_para_fazer
        self.__status = status

    # --- Getters ---
    def get_id_evento(self):
        return self.__id_evento

    def get_titulo(self):
        return self.__titulo

    def get_descricao(self):
        return self.__descricao

    def get_dificuldade(self):
        return self.__dificuldade

    def get_recompensa_dinheiro(self):
        return self.__recompensa_dinheiro

    def get_resposta_certa(self):
        return self.__resposta_certa

    def get_resposta_errada(self):
        return self.__resposta_errada

    def get_entrada_teste(self):
        return self.__entrada_teste

    def get_tempo_aparecer_min(self):
        return self.__tempo_aparecer_min

    def get_tempo_aparecer_max(self):
        return self.__tempo_aparecer_max

    def get_tempo_para_fazer(self):
        return self.__tempo_para_fazer

    def get_status(self):
        return self.__status

    # --- Setters ---
    def set_id_evento(self, id_evento):
        self.__id_evento = id_evento

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_dificuldade(self, dificuldade):
        self.__dificuldade = dificuldade

    def set_recompensa_dinheiro(self, recompensa_dinheiro):
        self.__recompensa_dinheiro = recompensa_dinheiro

    def set_resposta_certa(self, resposta_certa):
        self.__resposta_certa = resposta_certa

    def set_resposta_errada(self, resposta_errada):
        self.__resposta_errada = resposta_errada

    def set_entrada_teste(self, entrada_teste):
        self.__entrada_teste = entrada_teste

    def set_tempo_aparecer_min(self, tempo_aparecer_min):
        self.__tempo_aparecer_min = tempo_aparecer_min

    def set_tempo_aparecer_max(self, tempo_aparecer_max):
        self.__tempo_aparecer_max = tempo_aparecer_max

    def set_tempo_para_fazer(self, tempo_para_fazer):
        self.__tempo_para_fazer = tempo_para_fazer

    def set_status(self, status):
        self.__status = status
