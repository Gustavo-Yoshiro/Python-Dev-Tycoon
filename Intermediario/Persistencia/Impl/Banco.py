import sqlite3

class BancoDeDadosIntermediario:
    def __init__(self, nome_bd="python_game.db"):
        self.nome_bd = nome_bd

    def conectar(self):
        """Estabelece conexão com o banco de dados."""
        return sqlite3.connect(self.nome_bd)

    def criarBanco(self):
        """Cria todas as tabelas necessárias com a estrutura final para o sistema de freelance."""
        con = None
        try:
            con = self.conectar()
            cursor = con.cursor()

            # Tabela cliente (com reputação e personalidade)
            # Deve ser criada antes de 'projeto_freelance'
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    area_atuacao TEXT,
                    descricao TEXT,
                    reputacao REAL DEFAULT 4.0,
                    personalidade TEXT DEFAULT 'Amigável'
                );
            """)

            # Tabela projeto_freelance (com todos os detalhes do desafio)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projeto_freelance (
                    id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    dificuldade TEXT,
                    recompensa REAL,
                    status TEXT DEFAULT 'disponivel',
                    req_backend INTEGER DEFAULT 1,
                    req_frontend INTEGER DEFAULT 1,
                    req_social INTEGER DEFAULT 1,
                    tags TEXT,
                    data_postagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    prazo_dias INTEGER DEFAULT 7,
                    tipo_desafio TEXT,
                    codigo_base TEXT,
                    testes TEXT,
                    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                );
            """)

            # Tabela jogador_projeto (relação N-N com a nova coluna)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogador_projeto (
                    id_jogador INTEGER NOT NULL,
                    id_projeto INTEGER NOT NULL,
                    status TEXT, -- em_andamento, concluido, falhou
                    detalhes_descobertos TEXT, -- Armazena detalhes extras
                    PRIMARY KEY (id_jogador, id_projeto),
                    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
                    FOREIGN KEY (id_projeto) REFERENCES projeto_freelance(id_projeto)
                );
            """)

            # Tabela chat_cliente (mensagens)
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

            # --- NOVAS TABELAS PARA O SISTEMA DE DIÁLOGO ---

            # Tabela dialogo_nos (Armazena cada "fala" ou estado da conversa)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dialogo_nos (
                    id_no INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_projeto INTEGER,
                    texto_npc TEXT NOT NULL,
                    is_inicio BOOLEAN DEFAULT 0,
                    FOREIGN KEY (id_projeto) REFERENCES projeto_freelance(id_projeto)
                );
            """)

            # Tabela dialogo_opcoes (Armazena as escolhas do jogador que conectam os nós)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dialogo_opcoes (
                    id_opcao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_no_origem INTEGER NOT NULL,
                    id_no_destino INTEGER,
                    texto_opcao TEXT NOT NULL,
                    req_social INTEGER DEFAULT 0,
                    efeito TEXT,
                    FOREIGN KEY (id_no_origem) REFERENCES dialogo_nos(id_no),
                    FOREIGN KEY (id_no_destino) REFERENCES dialogo_nos(id_no)
                );
            """)

            con.commit()
            print("Estrutura do banco de dados (freelance e diálogo) verificada/criada com sucesso.")
        except sqlite3.Error as erro:
            print("Erro ao criar a estrutura do banco:", erro)
            raise
        finally:
            if con:
                con.close()

    def apagarTabelas(self):
        """Apaga todas as tabelas relacionadas ao sistema freelance e diálogo."""
        con = None
        try:
            con = self.conectar()
            cursor = con.cursor()

            cursor.executescript("""
                DROP TABLE IF EXISTS jogador_projeto;
                DROP TABLE IF EXISTS chat_cliente;
                DROP TABLE IF EXISTS dialogo_opcoes;
                DROP TABLE IF EXISTS dialogo_nos;
                DROP TABLE IF EXISTS projeto_freelance;
                DROP TABLE IF EXISTS cliente;
            """)

            con.commit()
            print("Todas as tabelas foram apagadas com sucesso.")
        except sqlite3.Error as erro:
            print("Erro ao apagar as tabelas:", erro)
            raise
        finally:
            if con:
                con.close()