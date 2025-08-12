from Iniciante.Service.FaseService import FaseService
from Iniciante.Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl
from Iniciante.Persistencia.Entidade.Fase import Fase

class FaseServiceImpl(FaseService):
    FASES_VALIDAS = {"Iniciante", "Intermediário", "Gerência"}

    def __init__(self):
        self.fase_persistencia = FasePersistenciaImpl()

    def criar_fase(self, tipo_fase, topico, introducao):
        if not tipo_fase or not tipo_fase.strip():
            raise ValueError("Tipo da fase não pode ser vazio!")
        tipo_fase = tipo_fase.strip()
        if tipo_fase not in self.FASES_VALIDAS:
            raise ValueError(f"Tipo de fase inválido! Deve ser um de: {', '.join(self.FASES_VALIDAS)}")
        if not topico or not topico.strip():
            raise ValueError("Tópico da fase não pode ser vazio!")
        if not introducao or not introducao.strip():
            raise ValueError("Introdução não pode ser vazia!")

        nova_fase = Fase(
            id_fase=None,
            tipo_fase=tipo_fase,
            topico=topico.strip(),
            introducao=introducao.strip()
        )
        return self.fase_persistencia.salvar(nova_fase)



    def buscar_fase_por_id(self, id_fase):
        return self.fase_persistencia.buscar_por_id(id_fase)

    def listar_todas_fases(self):
        return self.fase_persistencia.listar_todos()

    def deletar_fase(self, id_fase):
        return self.fase_persistencia.deletar(id_fase)

    def atualizar_fase(self, fase):
        # Pode adicionar validações de negócio aqui antes de atualizar
        return self.fase_persistencia.atualizar(fase)
