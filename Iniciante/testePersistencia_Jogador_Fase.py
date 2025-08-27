from Persistencia.Entidade.Jogador import Jogador
from Persistencia.Entidade.Fase import Fase
from Persistencia.Impl.JogadorPersistenciaImpl import JogadorPersistenciaImpl
from Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

def testar_jogador():
    print("\n🏅 Testando Jogador:")
    jogador_persistencia = JogadorPersistenciaImpl()

    # Criar um novo jogador
    novo_jogador = Jogador(
        id_jogador=None,
        nome="João Dev",
        id_fase=1,
        social=1,
        dinheiro=150.0,
        backend=2,
        frontend=3
    )

    id_jog = jogador_persistencia.salvar(novo_jogador)
    print(f"✅ Jogador salvo com ID: {id_jog}")
    jog = jogador_persistencia.buscar_por_id(id_jog)
    if jog:
        print("👤 Jogador buscado:", jog.get_nome())
    if jog:
        print(f"ID: {jog.get_id_jogador()}, Nome: {jog.get_nome()}, Fase: {jog.get_id_fase()}, "
            f"Social: {jog.get_social()}, Dinheiro: {jog.get_dinheiro()}, "
            f"Backend: {jog.get_backend()}, Frontend: {jog.get_frontend()}")

    jog.set_nome("Maria Dev Atualizada")
    jog.set_dinheiro(500.0)
    jogador_persistencia.atualizar(jog)
    print("✏️ Jogador atualizado!")

    todos = jogador_persistencia.listar_todos()
    print(f"🎲 Total de jogadores: {len(todos)},")
    if jog:
        print(f"ID: {jog.get_id_jogador()}, Nome: {jog.get_nome()}, Fase: {jog.get_id_fase()}, "
            f"Social: {jog.get_social()}, Dinheiro: {jog.get_dinheiro()}, "
            f"Backend: {jog.get_backend()}, Frontend: {jog.get_frontend()}")
    else:
        print("Jogador não encontrado!")

    # Descomente para deletar o teste
    # jogador_persistencia.deletar(id_jog)
    # print("🗑️ Jogador deletado!")

def testar_fase():
    print("\n🎓 Testando Fase:")
    fase_persistencia = FasePersistenciaImpl()

    nova_fase = Fase(
        id_fase=None,
        tipo_fase="iniciante",
        topico="variáveis",
        introducao="Aprenda sobre variáveis em Python."
    )

    id_fase = fase_persistencia.salvar(nova_fase)
    print(f"✅ Fase salva com ID: {id_fase}")

    fase = fase_persistencia.buscar_por_id(id_fase)
    if fase:
        print("📖 Fase buscada:(topico)", fase.get_topico())

    fase.set_introducao("Introdução atualizada: variáveis em Python")
    fase_persistencia.atualizar(fase)
    print("✏️ Fase atualizada!")


    todos = fase_persistencia.listar_todos()
    print(f"📚 Total de fases: {len(todos)}")

    # Descomente para deletar o teste
    # fase_persistencia.deletar(id_fase)
    # print("🗑️ Fase deletada!")

if __name__ == "__main__":
    print("🚀 Rodando testes de Jogador e Fase...")
    testar_jogador()
    #testar_fase()
