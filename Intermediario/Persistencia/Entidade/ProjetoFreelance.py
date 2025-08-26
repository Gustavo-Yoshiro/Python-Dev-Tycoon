class ProjetoFreelance:
    def __init__(self, id_projeto: int, id_cliente: int, titulo: str, descricao: str,
                 dificuldade: str, recompensa: float, status: str,
                 req_backend: int, req_frontend: int, req_social: int, tags: str,
                 data_postagem: str, prazo_dias: int, tipo_desafio: str,
                 codigo_base: str, testes: str):
        
        self.__id_projeto = id_projeto
        self.__id_cliente = id_cliente
        self.__titulo = titulo
        self.__descricao = descricao
        self.__dificuldade = dificuldade
        self.__recompensa = recompensa
        self.__status = status
        self.__req_backend = req_backend
        self.__req_frontend = req_frontend
        self.__req_social = req_social
        self.__tags = tags
        self.__data_postagem = data_postagem
        self.__prazo_dias = prazo_dias
        self.__tipo_desafio = tipo_desafio
        self.__codigo_base = codigo_base
        self.__testes = testes

    # --- Getters ---
    def get_id_projeto(self) -> int: return self.__id_projeto
    def get_id_cliente(self) -> int: return self.__id_cliente
    def get_titulo(self) -> str: return self.__titulo
    def get_descricao(self) -> str: return self.__descricao
    def get_dificuldade(self) -> str: return self.__dificuldade
    def get_recompensa(self) -> float: return self.__recompensa
    def get_status(self) -> str: return self.__status
    def get_req_backend(self) -> int: return self.__req_backend
    def get_req_frontend(self) -> int: return self.__req_frontend
    def get_req_social(self) -> int: return self.__req_social
    def get_tags(self) -> str: return self.__tags
    def get_data_postagem(self) -> str: return self.__data_postagem
    def get_prazo_dias(self) -> int: return self.__prazo_dias
    def get_tipo_desafio(self) -> str: return self.__tipo_desafio
    def get_codigo_base(self) -> str: return self.__codigo_base
    def get_testes(self) -> str: return self.__testes
    
    # --- Setters ---
    def set_id_projeto(self, id_projeto: int): self.__id_projeto = id_projeto
    def set_id_cliente(self, id_cliente: int): self.__id_cliente = id_cliente
    def set_titulo(self, titulo: str): self.__titulo = titulo
    def set_descricao(self, descricao: str): self.__descricao = descricao
    def set_dificuldade(self, dificuldade: str): self.__dificuldade = dificuldade
    def set_recompensa(self, recompensa: float): self.__recompensa = recompensa
    def set_status(self, status: str): self.__status = status
    def set_req_backend(self, req_backend: int): self.__req_backend = req_backend
    def set_req_frontend(self, req_frontend: int): self.__req_frontend = req_frontend
    def set_req_social(self, req_social: int): self.__req_social = req_social
    def set_tags(self, tags: str): self.__tags = tags
    def set_data_postagem(self, data_postagem: str): self.__data_postagem = data_postagem
    def set_prazo_dias(self, prazo_dias: int): self.__prazo_dias = prazo_dias
    def set_tipo_desafio(self, tipo_desafio: str): self.__tipo_desafio = tipo_desafio
    def set_codigo_base(self, codigo_base: str): self.__codigo_base = codigo_base
    def set_testes(self, testes: str): self.__testes = testes
