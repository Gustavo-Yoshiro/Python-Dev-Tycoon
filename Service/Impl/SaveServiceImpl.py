from Service.SaveService import SaveService
from Persistencia.Impl.SavePersistenciaImpl import SavePersistenciaImpl
from Persistencia.Entidade.Save import Save

class SaveServiceImpl(SaveService):
    def __init__(self):
        self.__persistencia = SavePersistenciaImpl()

    def adicionar_save(self, save: Save):
        jogador_id = save.get_id_jogador()

        if self.__persistencia.pode_salvar(jogador_id):
            return self.__persistencia.salvar(save)
        else:
            print(f" Jogador {jogador_id} já possui 3 saves. Delete um existente para salvar novamente.")
            return None

    def buscar_save(self, id_save: int) -> Save:
        return self.__persistencia.buscar_por_id(id_save)

    def listar_saves(self) -> list:
        return self.__persistencia.listar_todos()

    def listar_saves_do_jogador(self, id_jogador: int) -> list:
        todos = self.__persistencia.listar_todos()
        return [s for s in todos if s.get_id_jogador() == id_jogador]

    def atualizar_save(self, save: Save):
        self.__persistencia.atualizar(save)

    def remover_save(self, id_save: int):
        self.__persistencia.deletar(id_save)