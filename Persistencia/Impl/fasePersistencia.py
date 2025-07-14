# fasePersistencia.py

class FasePersistencia:
    def __init__(self, banco):
        self.banco = banco

    def criar_fase(self, tipo_fase, topico, introducao):
        sql = """
            INSERT INTO fase (tipo_fase, topico, introdução)
            VALUES (?, ?, ?)
        """
        parametros = (tipo_fase, topico, introducao)
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, parametros)
            con.commit()
            id_nova_fase = cursor.lastrowid
            con.close()
            return id_nova_fase
        except Exception as e:
            print("Erro ao criar fase:", e)
            return None

    def listar_fases(self):
        sql = "SELECT * FROM fase"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            fases = cursor.fetchall()
            con.close()
            return fases
        except Exception as e:
            print("Erro ao listar fases:", e)
            return []

    def buscar_fase_por_id(self, id_fase):
        sql = "SELECT * FROM fase WHERE id_fase = ?"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, (id_fase,))
            fase = cursor.fetchone()
            con.close()
            return fase
        except Exception as e:
            print("Erro ao buscar fase:", e)
            return None

    def atualizar_fase(self, id_fase, tipo_fase=None, topico=None, introducao=None):
        try:
            updates = []
            params = []
            if tipo_fase is not None:
                updates.append("tipo_fase = ?")
                params.append(tipo_fase)
            if topico is not None:
                updates.append("topico = ?")
                params.append(topico)
            if introducao is not None:
                updates.append("introdução = ?")
                params.append(introducao)
            if not updates:
                print("Nenhum campo para atualizar.")
                return False
            params.append(id_fase)
            sql = f"UPDATE fase SET {', '.join(updates)} WHERE id_fase = ?"
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, params)
            con.commit()
            con.close()
            return True
        except Exception as e:
            print("Erro ao atualizar fase:", e)
            return False

    def excluir_fase(self, id_fase):
        sql = "DELETE FROM fase WHERE id_fase = ?"
        try:
            con = self.banco.conectar()
            cursor = con.cursor()
            cursor.execute(sql, (id_fase,))
            con.commit()
            con.close()
            return True
        except Exception as e:
            print("Erro ao excluir fase:", e)
            return False
