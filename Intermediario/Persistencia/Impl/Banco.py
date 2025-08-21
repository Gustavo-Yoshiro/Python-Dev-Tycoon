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

            # Tabela cliente (modo freelancer)
            cursor.execute("""
              -- Cliente (NPCs que oferecem trabalhos)
                CREATE TABLE cliente (
                    id_cliente SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    area_atuacao VARCHAR(100), -- Ex: Web, Mobile, Data Science
                    reputacao INT DEFAULT 50, -- reputação do NPC com o jogador (0 a 100)
                    descricao TEXT -- pode guardar "história" ou detalhes do cliente
                );
            """)

            # Tabela freelancer (desafios)
            cursor.execute("""
                        -- Projeto Freelance (trabalhos que aparecem na aba freelancer)
            CREATE TABLE projeto_freelance (
                id_projeto SERIAL PRIMARY KEY,
                id_cliente INT NOT NULL REFERENCES cliente(id_cliente) ON DELETE CASCADE,
                titulo VARCHAR(150) NOT NULL,
                descricao TEXT NOT NULL,
                dificuldade INT NOT NULL, -- 1 = fácil, 2 = médio, 3 = difícil
                recompensa INT NOT NULL, -- dinheiro que o jogador recebe
                habilidade_requerida VARCHAR(100), -- exemplo: "Python", "Banco de Dados"
                status VARCHAR(20) DEFAULT 'disponivel' 
                -- disponivel, em_andamento, concluido
            );
            """)

            # Tabela freelancer_jogador (histórico do jogador)
            cursor.execute("""
                -- Ligação entre Jogador e Projeto (quando ele aceita um job)
                CREATE TABLE jogador_projeto (
                    id_jogador INT NOT NULL REFERENCES jogador(id_jogador) ON DELETE CASCADE,
                    id_projeto INT NOT NULL REFERENCES projeto_freelance(id_projeto) ON DELETE CASCADE,
                    status VARCHAR(20) DEFAULT 'em_andamento', 
                    -- em_andamento, concluido, falhou
                    PRIMARY KEY (id_jogador, id_projeto)
                );

            """)
            cursor.execute("""
            -- Chat / Negociação com cliente
                CREATE TABLE chat_cliente (
                    id_chat SERIAL PRIMARY KEY,
                    id_jogador INT NOT NULL REFERENCES jogador(id_jogador) ON DELETE CASCADE,
                    id_cliente INT NOT NULL REFERENCES cliente(id_cliente) ON DELETE CASCADE,
                    mensagem TEXT NOT NULL,
                    enviado_por VARCHAR(20) NOT NULL, 
                    -- 'jogador' ou 'cliente'
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
        """)

            con.commit()
        except sqlite3.Error as erro:
            print("Erro ao criar o banco:", erro)
            raise
        finally:
            con.close()

   
