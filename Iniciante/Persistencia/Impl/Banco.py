import sqlite3

class BancoDeDados:
    def __init__(self, nome_bd="python_game.db"):
        self.nome_bd = nome_bd

    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        return sqlite3.connect(self.nome_bd)

    def criarBanco(self):
        """Cria todas as tabelas necessárias para o sistema"""
        try:
            con = self.conectar()
            cursor = con.cursor()

            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS jogador (
                            id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            id_fase INTEGER,
                            social INTEGER DEFAULT 0,
                            dinheiro REAL DEFAULT 0.0,
                            backend INTEGER DEFAULT 0,
                            frontend INTEGER DEFAULT 0,
                            FOREIGN KEY (id_fase) REFERENCES fase(id_fase)
                        );
                    """)

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS fase (
                                    id_fase INTEGER PRIMARY KEY AUTOINCREMENT,
                                    tipo_fase TEXT NOT NULL,
                                    topico TEXT NOT NULL,
                                    introdução TEXT NOT NULL
                                );
                                """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS exercicio (
                                id_exercicio INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_fase INTEGER NOT NULL,
                                dicas TEXT NOT NULL,
                                pergunta TEXT NOT NULL,
                                tipo TEXT NOT NULL CHECK(tipo IN ('objetiva', 'dissertativa','dragdrop')),
                                resposta_certa TEXT NOT NULL,
                                resposta_errada TEXT,
                                entrada_teste TEXT,
                                FOREIGN KEY (id_fase) REFERENCES fase(id_fase)
                            );
                        """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS save (
                                id_save INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_jogador INTEGER NOT NULL,
                                data_save TEXT NOT NULL,
                                tempo_jogo INTEGER DEFAULT 0,
                                FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador)
                            );
                        """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS progresso_fase (
                                id_progresso INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_jogador INTEGER NOT NULL,
                                id_fase INTEGER NOT NULL,
                                indice_exercicio INTEGER DEFAULT 0,
                                acertos INTEGER DEFAULT 0,
                                erros INTEGER DEFAULT 0,
                                resposta_parcial TEXT,
                                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
                                FOREIGN KEY (id_fase) REFERENCES fase(id_fase)
                            );
                        """)
            
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS loja (
                                id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_jogador INTEGER NOT NULL,           -- quem comprou
                                nome TEXT NOT NULL,                    -- ex: "Front-end" ou "Social"
                                categoria TEXT NOT NULL,               -- ex: "iniciante", "intermediario", "avancado"
                                preco REAL NOT NULL,
                                duracao_segundos INTEGER,              -- tempo de conclusão (NULL se não usar)
                                status TEXT DEFAULT 'andamento',       -- "andamento", "concluido", "usado"
                                duracao_total INTEGER,
                                FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador)
                            );
                        """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS evento (
                            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,                     -- Nome curto do evento (ex: "Hackathon do Google")
                            descricao TEXT NOT NULL,                  -- Texto descritivo, contextualizando o convite
                            dificuldade TEXT NOT NULL CHECK(dificuldade IN ('facil', 'medio', 'dificil')),
                            recompensa_dinheiro REAL NOT NULL,        -- Dinheiro ganho ao concluir
                            resposta_certa TEXT NOT NULL,             -- Resposta correta esperada
                            resposta_errada TEXT,                     -- (opcional) respostas comuns erradas
                            entrada_teste TEXT,                       -- caso queira validar (igual ao exercicio)
                            tempo_aparecer_min INTEGER,               -- intervalo mínimo para reaparecer (segundos)
                            tempo_aparecer_max INTEGER,               -- intervalo máximo para reaparecer (segundos)
                            tempo_para_fazer INTEGER,                 -- limite de tempo (segundos) após aceitar
                            status TEXT DEFAULT 'ativo'               -- "ativo" ou "usado" (evitar repetir logo em seguida)
                        );

                                                   
                           """)



            con.commit()
        except sqlite3.Error as erro:
            print("Erro ao criar o banco:", erro)
            raise
        finally:
            con.close()


    def executar(self, sql, parametros=()):
        """Executa uma query que não retorna resultados (INSERT, UPDATE, DELETE)"""
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
            return cursor.lastrowid
        except sqlite3.Error as erro:
            print("Erro ao executar SQL:", erro)
            raise
        finally:
            con.close()

    def executar_query(self, sql, parametros=(), fetchone=False):
        """Executa uma query que retorna resultados (SELECT)"""
        try:
            con = self.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            return cursor.fetchone() if fetchone else cursor.fetchall()
        except sqlite3.Error as erro:
            print("Erro ao consultar o banco de dados:", erro)
            raise
        finally:
            con.close()
    
    def executar_multiplos(self, comandos):
        """Executa múltiplos comandos SQL em uma única transação"""
        try:
            con = self.conectar()
            cursor = con.cursor()
            con.execute("BEGIN")
            for sql, params in comandos:
                cursor.execute(sql, params)
            con.commit()
        except sqlite3.Error as erro:
            con.rollback()
            print("Erro ao executar múltiplos comandos:", erro)
            raise
        finally:
            con.close()
    def executar_e_retornar_id(self, sql: str, parametros: tuple) -> int:
        con = self.conectar()
        try:
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
            return cursor.lastrowid
        finally:
            con.close()