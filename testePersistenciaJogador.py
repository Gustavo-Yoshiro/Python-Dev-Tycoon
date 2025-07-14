from Persistencia.Impl.Banco import BancoDeDados
from Persistencia.Impl.jogadorPersistencia  import JogadorPersistencia

# 1. Instancia o banco (não cria tabelas de novo, só conecta)
banco = BancoDeDados()
# Se nunca rodou antes, pode rodar banco.criarBanco()

# 2. Instancia a persistência do jogador
jogador_db = JogadorPersistencia(banco)

# 3. CRIAR jogador
id_novo = jogador_db.criar_jogador(
    nome="TesteUser",
    id_fase=1,
    social=0,
    dinheiro=150.0,
    backend=2,
    frontend=1
)
print(f"Novo jogador criado: {id_novo}")

# 4. LISTAR todos jogadores
print("\nTodos jogadores:")
for jogador in jogador_db.listar_jogadores():
    print(jogador)

# 5. BUSCAR jogador pelo ID
print("\nBuscar jogador pelo ID:")
print(jogador_db.buscar_jogador_por_id(id_novo))

# 6. ATUALIZAR jogador
jogador_db.atualizar_jogador(id_novo, {"dinheiro": 999.0, "nome": "NovoNome"})
print("\nApós atualização:")
print(jogador_db.buscar_jogador_por_id(id_novo))

# 7. EXCLUIR jogador
jogador_db.excluir_jogador(id_novo)
print("\nApós exclusão:")
print(jogador_db.buscar_jogador_por_id(id_novo))
