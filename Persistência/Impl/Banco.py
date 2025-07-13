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

            # Tabela de perfis de usuário
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
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

    def atualizar(self, tabela, id_registro, campos):
        """Atualiza um registro no banco de dados"""
        try:
            con = self.conectar()
            cursor = con.cursor()
            
            sets = ", ".join([f"{k} = ?" for k in campos.keys()])
            valores = list(campos.values()) + [id_registro]
            
            sql = f"UPDATE {tabela} SET {sets} WHERE id = ?"
            cursor.execute(sql, valores)
            con.commit()
            return True
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar {tabela}:", erro)
            raise
        finally:
            con.close()