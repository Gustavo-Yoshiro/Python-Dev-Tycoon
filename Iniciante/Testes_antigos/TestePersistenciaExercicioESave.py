from Persistencia.Entidade.Exercicio import Exercicio
from Persistencia.Entidade.Save import Save
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl
from Persistencia.Impl.SavePersistenciaImpl import SavePersistenciaImpl

def testar_exercicio():
    print("\n🔍 Testando Exercicio:")
    exercicio_persistencia = ExercicioPersistenciaImpl()

    novo_exercicio = Exercicio(
        id_exercicio=None,
        id_fase=1,
        dicas="Use if/else para lógica condicional",
        tipo="iniciante",
        resposta_certa="if condição:",
        resposta_erradas="switch(condição)"
    )

    id_ex = exercicio_persistencia.salvar(novo_exercicio)
    print(f"✅ Exercício salvo com ID: {id_ex}")

    ex = exercicio_persistencia.buscar_por_id(id_ex)
    if ex:
        print("📘 Exercício buscado:", ex.get_dicas())

    ex.set_dicas("Atualizado: Lógica condicional básica")
    exercicio_persistencia.atualizar(ex)
    print("✏️ Exercício atualizado!")

    todos = exercicio_persistencia.listar_todos()
    print(f"📚 Total de exercícios: {len(todos)}")

    # Uncomment para deletar o teste
    # exercicio_persistencia.deletar(id_ex)
    # print("🗑️ Exercício deletado!")

def testar_save():
    print("\n🧩 Testando Save:")
    save_persistencia = SavePersistenciaImpl()

    novo_save = Save(
        id_save=None,
        id_jogador=1,
        data_save="2025-07-13 22:30",
        tempo_jogo=400
    )

    id_sv = save_persistencia.salvar(novo_save)
    print(f"✅ Save salvo com ID: {id_sv}")

    sv = save_persistencia.buscar_por_id(id_sv)
    if sv:
        print("📁 Save encontrado para jogador:", sv.get_id_jogador())

    sv.set_tempo_jogo(480)
    save_persistencia.atualizar(sv)
    print("🕹️ Save atualizado com novo tempo!")

    todos = save_persistencia.listar_todos()
    print(f"📂 Total de saves: {len(todos)}")

    # Uncomment para deletar o teste
    # save_persistencia.deletar(id_sv)
    # print("🗑️ Save deletado!")

if __name__ == "__main__":
    print("🎮 Rodando testes do sistema...")
    testar_exercicio()
    testar_save()