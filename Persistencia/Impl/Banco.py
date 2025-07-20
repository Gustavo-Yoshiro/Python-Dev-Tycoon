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
