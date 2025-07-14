from Persistência.Impl.Banco import BancoDeDados
from Persistência.Impl.fasePersistencia  import FasePersistencia

# 1. Instanciar banco e persistência de fase
banco = BancoDeDados()
fase_db = FasePersistencia(banco)

# 2. CRIAR uma fase nova
id_nova_fase = fase_db.criar_fase(
    tipo_fase="iniciante",
    topico="print",
    introducao="Aprenda a usar print para mostrar mensagens na tela."
)
print(f"Nova fase criada com id: {id_nova_fase}")

# 3. LISTAR todas as fases
print("\nTodas as fases:")
for fase in fase_db.listar_fases():
    print(fase)

# 4. BUSCAR fase por ID
print("\nBuscar fase pelo ID:")
print(fase_db.buscar_fase_por_id(id_nova_fase))

# 5. ATUALIZAR fase
fase_db.atualizar_fase(id_nova_fase, introducao="Introdução atualizada para print.")
print("\nApós atualização:")
print(fase_db.buscar_fase_por_id(id_nova_fase))

# 6. EXCLUIR fase
fase_db.excluir_fase(id_nova_fase)
print("\nApós exclusão:")
print(fase_db.buscar_fase_por_id(id_nova_fase))
