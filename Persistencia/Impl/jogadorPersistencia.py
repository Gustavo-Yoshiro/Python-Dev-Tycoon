# jogadorPersistencia.py

class JogadorPersistencia:
    def __init__(self, banco):
        self.banco = banco  # espera receber uma instância do BancoDeDados

    def criar_jogador(self, nome, id_fase=None, social=0, dinheiro=0.0, backend=0, frontend=0):
        sql = """
            INSERT INTO jogador (nome, id_fase, social, dinheiro, backend, frontend)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parametros = (nome, id_fase, social, dinheiro, backend, frontend)
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
            id_novo_jogador = cursor.lastrowid
            con.close()
            return id_novo_jogador
        except Exception as e:
            print("Erro ao criar jogador:", e)
            return None

    def listar_jogadores(self):
        sql = "SELECT * FROM jogador"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            jogadores = cursor.fetchall()
            con.close()
            return jogadores
        except Exception as e:
            print("Erro ao listar jogadores:", e)
            return []

    def buscar_jogador_por_id(self, id_jogador):
        sql = "SELECT * FROM jogador WHERE id_jogador = ?"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, (id_jogador,))
            jogador = cursor.fetchone()
            con.close()
            return jogador
        except Exception as e:
            print("Erro ao buscar jogador:", e)
            return None

    def atualizar_jogador(self, id_jogador, campos):
        # campos deve ser um dict: {'nome': 'novo nome', 'dinheiro': 200.0, ...}
        try:
            sets = ", ".join([f"{k} = ?" for k in campos.keys()])
            valores = list(campos.values()) + [id_jogador]
            sql = f"UPDATE jogador SET {sets} WHERE id_jogador = ?"
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, valores)
            con.commit()
            con.close()
            return True
        except Exception as e:
            print("Erro ao atualizar jogador:", e)
            return False

    def excluir_jogador(self, id_jogador):
        sql = "DELETE FROM jogador WHERE id_jogador = ?"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, (id_jogador,))
            con.commit()
            con.close()
            return True
        except Exception as e:
            print("Erro ao excluir jogador:", e)
            return False
