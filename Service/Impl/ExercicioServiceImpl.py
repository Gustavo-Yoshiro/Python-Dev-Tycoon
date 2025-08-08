from Service.ExercicioService import ExercicioService
from Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl
from Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
import ast

class ExercicioServiceImpl(ExercicioService):
    def __init__(self):
        self.__persistencia = ExercicioPersistenciaImpl()

    def listar_exercicios_por_fase(self, id_fase: int) -> list:
        todos = self.__persistencia.listar_todos()
        return [e for e in todos if e.get_id_fase() == id_fase]

    def verificar_resposta(self, id_exercicio: int, resposta_usuario: str) -> bool:
        exercicio = self.__persistencia.buscar_por_id(id_exercicio)
        if not exercicio:
            print(" Exercício não encontrado.")
            return False
        return resposta_usuario.strip().lower() == exercicio.get_resposta_certa().strip().lower()

    def obter_dicas(self, id_exercicio: int) -> str:
        exercicio = self.__persistencia.buscar_por_id(id_exercicio)
        return exercicio.get_dicas() if exercicio else " Dica não disponível."
    
    def carregar_exercicios(self, id_fase, jogador):
        progresso_service = ProgressoFaseServiceImpl()
        progresso = progresso_service.buscar_progresso_por_jogador_fase(jogador.get_id_jogador(), id_fase)
        exercicios = self.listar_exercicios_por_fase(id_fase)
        if progresso:
            indice_atual = progresso.get_indice_exercicio()
            acertos = progresso.get_acertos()
            erros = progresso.get_erros()
            # Retorna tudo para usar na tela!
            return exercicios, progresso
        else:
            return exercicios, None


    

    def validar_codigo_ast_por_topico(self, codigo, id_fase):
        FASE_TO_TOPICO = {
            1: "Saída de Dados com print()",
            2: "Entrada de Dados com input()",
            3: "Variáveis e Tipos Simples",
            4: "Operadores Aritméticos e Relacionais",
            5: "Estruturas Condicionais (if/else)",
            6: "Estruturas de Repetição (for)",
            7: "Estrutura de Repetição (while)",
            8: "Funções Simples",
        }
        topico = FASE_TO_TOPICO.get(id_fase, None)
        if not topico:
            return True, ""  # Não exige regra extra para tópicos não mapeados

        try:
            arvore = ast.parse(codigo)
            linhas = [l for l in codigo.strip().splitlines() if l.strip()]
        except Exception as e:
            return False, f"Código inválido: {e}"

        # Fase 1 - print()
        if topico == "Saída de Dados com print()":
            tem_print = any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print" for n in ast.walk(arvore))
            if not tem_print:
                return False, "Seu código deve usar print() para exibir informações na tela."
            return True, ""

        # Fase 2 - input()
        elif topico == "Entrada de Dados com input()":
            tem_input = any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "input" for n in ast.walk(arvore))
            tem_print = any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print" for n in ast.walk(arvore))
            if not tem_input:
                return False, "Você deve usar input() para ler o valor do usuário."
            if not tem_print:
                return False, "Você deve mostrar o valor lido usando print()."
            return True, ""

        # Fase 3 - variáveis
        elif topico == "Variáveis e Tipos Simples":
            tem_atribuicao = any(isinstance(n, ast.Assign) for n in ast.walk(arvore))
            tem_print = any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print" for n in ast.walk(arvore))
            if not tem_atribuicao:
                return False, "Seu código deve criar pelo menos uma variável (usar =)."
            if not tem_print:
                return False, "Seu código deve exibir o valor de uma variável usando print()."
            return True, ""

        # Fase 4 - operadores
        elif topico == "Operadores Aritméticos e Relacionais":
            tem_operador = any(isinstance(n, (ast.BinOp, ast.Compare)) for n in ast.walk(arvore))
            if not tem_operador:
                return False, "Use algum operador aritmético ou relacional (+, -, *, /, ==, !=, etc)."
            return True, ""

        # Fase 5 - if/else
        elif topico == "Estruturas Condicionais (if/else)":
            tem_if = any(isinstance(n, ast.If) for n in ast.walk(arvore))
            if not tem_if:
                return False, "Você deve usar um if em seu código."
            return True, ""

        # Fase 6 - for
        elif topico == "Estruturas de Repetição (for)":
            tem_for = any(isinstance(n, ast.For) for n in ast.walk(arvore))
            if not tem_for:
                return False, "Você deve usar um laço for em seu código."
            return True, ""

        # Fase 7 - while
        elif topico == "Estrutura de Repetição (while)":
            tem_while = any(isinstance(n, ast.While) for n in ast.walk(arvore))
            if not tem_while:
                return False, "Você deve usar um laço while em seu código."
            return True, ""

        # Fase 8 - funções
        elif topico == "Funções Simples":
            tem_funcao = any(isinstance(n, ast.FunctionDef) for n in ast.walk(arvore))
            if not tem_funcao:
                return False, "Você deve definir uma função usando def."
            return True, ""

        # Qualquer outro caso
        return True, ""

    
    """
    @staticmethod
    def extrai_linhas_print(saida, prompt_count=1):
        
        #Remove as linhas de prompt do input da saída e retorna só as linhas do print().
        #Se prompt_count=1, ignora a primeira linha (normal para 1 input com prompt).
        
        if not saida:
            return ""
        linhas = [l for l in saida.strip().splitlines() if l.strip()]
        return "\n".join(linhas[prompt_count:]) if len(linhas) > prompt_count else ""
    """



