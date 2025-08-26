# Este arquivo contém as entidades para o sistema de diálogo dinâmico.

class DialogoNo:
    """Representa um ponto único na conversa (a fala de um NPC)."""
    def __init__(self, id_no: int, id_projeto: int, texto_npc: str, is_inicio: bool):
        self.__id_no = id_no
        self.__id_projeto = id_projeto
        self.__texto_npc = texto_npc
        self.__is_inicio = is_inicio

    # --- Getters ---
    def get_id_no(self) -> int: return self.__id_no
    def get_id_projeto(self) -> int: return self.__id_projeto
    def get_texto_npc(self) -> str: return self.__texto_npc
    def get_is_inicio(self) -> bool: return self.__is_inicio

    # --- Setters ---
    def set_id_no(self, id_no: int): self.__id_no = id_no
    def set_id_projeto(self, id_projeto: int): self.__id_projeto = id_projeto
    def set_texto_npc(self, texto_npc: str): self.__texto_npc = texto_npc
    def set_is_inicio(self, is_inicio: bool): self.__is_inicio = is_inicio


class DialogoOpcao:
    """Representa uma escolha que o jogador pode fazer, conectando dois nós de diálogo."""
    def __init__(self, id_opcao: int, id_no_origem: int, id_no_destino: int, 
                 texto_opcao: str, req_social: int, efeito: str):
        self.__id_opcao = id_opcao
        self.__id_no_origem = id_no_origem
        self.__id_no_destino = id_no_destino
        self.__texto_opcao = texto_opcao
        self.__req_social = req_social
        self.__efeito = efeito

    # --- Getters ---
    def get_id_opcao(self) -> int: return self.__id_opcao
    def get_id_no_origem(self) -> int: return self.__id_no_origem
    def get_id_no_destino(self) -> int: return self.__id_no_destino
    def get_texto_opcao(self) -> str: return self.__texto_opcao
    def get_req_social(self) -> int: return self.__req_social
    def get_efeito(self) -> str: return self.__efeito

    # --- Setters ---
    def set_id_opcao(self, id_opcao: int): self.__id_opcao = id_opcao
    def set_id_no_origem(self, id_no_origem: int): self.__id_no_origem = id_no_origem
    def set_id_no_destino(self, id_no_destino: int): self.__id_no_destino = id_no_destino
    def set_texto_opcao(self, texto_opcao: str): self.__texto_opcao = texto_opcao
    def set_req_social(self, req_social: int): self.__req_social = req_social
    def set_efeito(self, efeito: str): self.__efeito = efeito
