import sqlite3

class BancoDeDadosIntermediario:
    def __init__(self, nome_bd="python_game.db"):
        self.nome_bd = nome_bd

    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        return sqlite3.connect(self.nome_bd)

    def criarBanco(self):
        """Cria todas as tabelas necessárias para o sistema (fase intermediária)"""
        try:
            con = self.conectar()
            cursor = con.cursor()

            # Tabela cliente (NPCs que oferecem trabalhos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    area_atuacao TEXT,
                    reputacao INTEGER DEFAULT 50,
                    descricao TEXT
                );
            """)

            # Tabela projeto_freelance (trabalhos disponíveis)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projeto_freelance (
                    id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    dificuldade INTEGER NOT NULL,
                    recompensa INTEGER NOT NULL,
                    habilidade_requerida TEXT,
                    status TEXT DEFAULT 'disponivel',
                    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
                );
            """)

            # Tabela jogador_projeto (histórico de projetos aceitos pelo jogador)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogador_projeto (
                    id_jogador INTEGER NOT NULL,
                    id_projeto INTEGER NOT NULL,
                    status TEXT DEFAULT 'em_andamento',
                    PRIMARY KEY (id_jogador, id_projeto),
                    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
                    FOREIGN KEY (id_projeto) REFERENCES projeto_freelance(id_projeto)
                );
            """)

            # Tabela chat_cliente (mensagens trocadas entre jogador e cliente)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_cliente (
                    id_chat INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_jogador INTEGER NOT NULL,
                    id_cliente INTEGER NOT NULL,
                    mensagem TEXT NOT NULL,
                    enviado_por TEXT NOT NULL,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
                    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                );
            """)

            con.commit()
            print("Banco criado com sucesso.")
        except sqlite3.Error as erro:
            print("Erro ao criar o banco:", erro)
            raise
        finally:
            con.close()