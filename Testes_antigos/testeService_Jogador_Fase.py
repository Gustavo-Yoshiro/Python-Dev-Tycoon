from Service.Impl.JogadorServiceImpl import JogadorServiceImpl
from Service.Impl.FaseServiceImpl import FaseServiceImpl
from Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl
from Persistencia.Entidade.Jogador import Jogador
from Persistencia.Entidade.Fase import Fase

def testar_fase_service():
    print("\n🎓 Testando FaseService:")
    fase_service = FaseServiceImpl()

    # Tenta criar cada fase possível (evita duplicar)
    for tipo in ["Iniciante", "Intermediário", "Gerência"]:
        try:
            id_fase = fase_service.criar_fase(
                tipo_fase=tipo,
                topico=f"Topico {tipo}",
                introducao=f"Bem-vindo à fase {tipo}!"
            )
            print(f"✅ Fase '{tipo}' criada com ID: {id_fase}")
        except Exception as e:
            print(f"⚠️ {tipo}: {e}")

    todas_fases = fase_service.listar_todas_fases()
    print(f"📚 Total de fases cadastradas: {len(todas_fases)}")
    for f in todas_fases:
        print(f"  ID {f.get_id_fase()}: {f.get_tipo_fase()} - {f.get_topico()}")

def testar_jogador_service():
    print("\n🏅 Testando JogadorService:")
    jogador_service = JogadorServiceImpl()
    fase_service = FaseServiceImpl()
    # Criar novo jogador (sempre começa na primeira fase "Iniciante")
    try:
        id_jogador = jogador_service.criar_jogador("Jogador Teste4")
        print(f"✅ Jogador criado com ID: {id_jogador}")
    except Exception as e:
        print(f"❌ Erro ao criar jogador: {e}")
        return

    # Buscar e mostrar dados
    jog = jogador_service.buscar_jogador_por_id(id_jogador)
    if jog:
        id_fase = jog.get_id_fase()
        fase_service = FaseServiceImpl()
        fase = fase_service.buscar_fase_por_id(id_fase)
        nome_fase = fase.get_tipo_fase() if fase else "Fase não encontrada"
        print(f"👤 Nome: {jog.get_nome()}, Fase: {nome_fase} (ID {id_fase}),Front: {jog.get_frontend()}, Back-End: {jog.get_backend()}, social: {jog.get_social()}, Dinheiro: {jog.get_dinheiro()}")


    # Premiar o jogador
    novo_dinheiro = jogador_service.premiar_jogador(id_jogador, 200.0)
    print(f"💰 Após premiação, dinheiro: {novo_dinheiro}")

    # Evoluir backend do jogador
    jogador_service.evoluir_atributo(id_jogador, "backend", 5)
    jog = jogador_service.buscar_jogador_por_id(id_jogador)
    print(f"🛠️ Backend atualizado: {jog.get_backend()}")

    # Trocar jogador para fase "Intermediário"
    # Busca fase intermediário
    fase_db = FasePersistenciaImpl()
    fases_inter = [f for f in fase_db.listar_todos() if f.get_tipo_fase() == "Intermediário"]
    if fases_inter:
        id_fase_inter = fases_inter[0].get_id_fase()
        jogador_service.mudar_fase(id_jogador, id_fase_inter)
        jog = jogador_service.buscar_jogador_por_id(id_jogador)
        print(f"🔄 Fase do jogador agora: {jog.get_id_fase()} (Intermediário)")

    # Trocar jogador para fase "Iniciante"
    fase_db = FasePersistenciaImpl()
    fases_ini = [f for f in fase_db.listar_todos() if f.get_tipo_fase() == "Iniciante"]
    if fases_ini:
        id_fase_ini = fases_ini[0].get_id_fase()
        jogador_service.mudar_fase(id_jogador, id_fase_ini)
        jog = jogador_service.buscar_jogador_por_id(id_jogador)
        fase = fase_db.buscar_por_id(jog.get_id_fase())
        nome_fase = fase.get_tipo_fase() if fase else "Fase não encontrada"
        print(f"🔄 Fase do jogador agora: {nome_fase} (ID {jog.get_id_fase()})")


    # Listar todos jogadores
    todos = jogador_service.listar_todos_jogadores()
    print(f"🎲 Total de jogadores: {len(todos)}")
    for jog in todos:
        print(f"  ID: {jog.get_id_jogador()} | Nome: {jog.get_nome()} | Dinheiro: {jog.get_dinheiro()}")

    # Descomente para deletar o teste!
    # jogador_service.deletar_jogador(id_jogador)
    # print("🗑️ Jogador deletado!")

if __name__ == "__main__":
    print("🚀 Testando Service de Fase e Jogador!")
    testar_fase_service()
    testar_jogador_service()
