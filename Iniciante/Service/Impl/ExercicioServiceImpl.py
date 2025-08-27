from Iniciante.Service.ExercicioService import ExercicioService
from Iniciante.Persistencia.Impl.ExercicioPersistenciaImpl import ExercicioPersistenciaImpl
from Iniciante.Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
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
        import ast

        FASE_TO_TOPICO = {
            # INICIANTE
            1: "Saída de Dados com print()",
            2: "Entrada de Dados com input()",
            3: "Variáveis e Tipos Simples",
            4: "Operadores Aritméticos e Relacionais",
            5: "Estruturas Condicionais (if/else)",
            6: "Estruturas de Repetição (for)",
            7: "Estrutura de Repetição (while)",
            8: "Funções Simples",
            # INTERMEDIÁRIO
            9:  "f-strings e formatação",
            10: "Métodos de string",
            11: "Listas (métodos e slicing)",
            12: "Tuplas e imutabilidade",
            13: "Conjuntos (set)",
            14: "Dicionários",
            15: "List Comprehensions",
            16: "Tratamento de Erros",
        }

        topico = FASE_TO_TOPICO.get(id_fase, None)
        if not topico:
            return True, ""  # Não exige regra extra para tópicos não mapeados

        try:
            arvore = ast.parse(codigo)
            linhas = [l for l in codigo.strip().splitlines() if l.strip()]
        except Exception as e:
            return False, f"Código inválido: {e}"

        # --------- Helpers rápidos ---------
        def tem_call_nome(nome):
            return any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == nome for n in ast.walk(arvore))

        def tem_call_metodo(metodos):
            for n in ast.walk(arvore):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                    if n.func.attr in metodos:
                        return True
            return False

        def tem_no(tipo):
            return any(isinstance(n, tipo) for n in ast.walk(arvore))

        # =========================
        # INICIANTE (1..8)
        # =========================

        if topico == "Saída de Dados com print()":
            if not tem_call_nome("print"):
                return False, "Seu código deve usar print() para exibir informações na tela."
            return True, ""

        elif topico == "Entrada de Dados com input()":
            tem_input = tem_call_nome("input")
            tem_print = tem_call_nome("print")
            if not tem_input:
                return False, "Você deve usar input() para ler o valor do usuário."
            if not tem_print:
                return False, "Você deve mostrar o valor lido usando print()."
            return True, ""

        elif topico == "Variáveis e Tipos Simples":
            tem_atribuicao = tem_no(ast.Assign)
            tem_print = tem_call_nome("print")
            if not tem_atribuicao:
                return False, "Seu código deve criar pelo menos uma variável (usar =)."
            if not tem_print:
                return False, "Seu código deve exibir o valor de uma variável usando print()."
            return True, ""

        elif topico == "Operadores Aritméticos e Relacionais":
            if not any(isinstance(n, (ast.BinOp, ast.Compare)) for n in ast.walk(arvore)):
                return False, "Use algum operador aritmético ou relacional (+, -, *, /, ==, !=, etc)."
            return True, ""

        elif topico == "Estruturas Condicionais (if/else)":
            if not tem_no(ast.If):
                return False, "Você deve usar um if em seu código."
            return True, ""

        elif topico == "Estruturas de Repetição (for)":
            if not tem_no(ast.For):
                return False, "Você deve usar um laço for em seu código."
            return True, ""

        elif topico == "Estrutura de Repetição (while)":
            if not tem_no(ast.While):
                return False, "Você deve usar um laço while em seu código."
            return True, ""

        elif topico == "Funções Simples":
            if not tem_no(ast.FunctionDef):
                return False, "Você deve definir uma função usando def."
            return True, ""

        # =========================
        # INTERMEDIÁRIO (9..16)
        # =========================

        elif topico == "f-strings e formatação":
            # Exige pelo menos UMA f-string (ast.JoinedStr). Opcional: aceitar FormatSpec.
            usa_fstring = any(isinstance(n, ast.JoinedStr) for n in ast.walk(arvore))
            if not usa_fstring:
                return False, "Use ao menos uma f-string (ex.: f\"Olá, {nome}\")."
            return True, ""

        elif topico == "Métodos de string":
            # Procura chamadas a métodos típicos de str
            METODOS = {
                "strip", "lstrip", "rstrip",
                "upper", "lower", "casefold", "title",
                "startswith", "endswith",
                "split", "join", "replace",
                "find", "index", "count",
                "isalpha", "isdigit", "isalnum", "isnumeric",
            }
            if not tem_call_metodo(METODOS):
                return False, "Use pelo menos um método de string (ex.: .upper(), .split(','), .replace('a','b'))."
            return True, ""

        elif topico == "Listas (métodos e slicing)":
            # Aceita: lista literal, métodos de lista, slicing (Subscript com Slice) ou sorted()
            METODOS_LISTA = {"append", "extend", "insert", "remove", "clear", "sort", "reverse"}
            tem_lista_literal = tem_no(ast.List)
            tem_metodo_lista = tem_call_metodo(METODOS_LISTA)
            tem_sorted = tem_call_nome("sorted")

            tem_slicing = False
            for n in ast.walk(arvore):
                if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
                    tem_slicing = True
                    break

            if not (tem_lista_literal or tem_metodo_lista or tem_slicing or tem_sorted):
                return False, "Use listas com métodos (append/extend/...) ou slicing (ex.: l[1:4]) ou sorted(l)."
            return True, ""

        elif topico == "Tuplas e imutabilidade":
            # Aceita: tupla literal, desempacotamento, tuple(...)
            tem_tupla = any(isinstance(n, ast.Tuple) for n in ast.walk(arvore))
            tem_tuple_ctor = tem_call_nome("tuple")
            if not (tem_tupla or tem_tuple_ctor):
                return False, "Use uma tupla (ex.: t = (1,2) ou a,b = (1,2) ou tuple(lista))."
            return True, ""

        elif topico == "Conjuntos (set)":
            # Aceita: set literal {1,2}, set(), ou métodos típicos de set
            METODOS_SET = {
                "add", "discard", "remove", "pop",
                "update", "union", "intersection",
                "difference", "symmetric_difference",
            }
            tem_set_literal = any(isinstance(n, ast.Set) for n in ast.walk(arvore))
            tem_set_ctor = tem_call_nome("set")
            tem_metodo_set = tem_call_metodo(METODOS_SET)
            if not (tem_set_literal or tem_set_ctor or tem_metodo_set):
                return False, "Use um set (ex.: {1,2} ou set([1,2])) ou métodos como .add(), .union(), .intersection()."
            return True, ""

        elif topico == "Dicionários":
            # Aceita: dict literal, dict comprehension, dict(), ou métodos típicos
            METODOS_DICT = {"get", "keys", "values", "items", "setdefault", "pop", "clear", "update"}
            tem_dict_literal = tem_no(ast.Dict)
            tem_dict_comp = tem_no(ast.DictComp)
            tem_dict_ctor = tem_call_nome("dict")
            tem_metodo_dict = tem_call_metodo(METODOS_DICT)
            if not (tem_dict_literal or tem_dict_comp or tem_dict_ctor or tem_metodo_dict):
                return False, "Use um dicionário (ex.: {'k':1}, {k:v for ...}, dict(...)) ou métodos como .get(), .items()."
            return True, ""

        elif topico == "List Comprehensions":
            # Requer especificamente uma list comprehension
            tem_list_comp = tem_no(ast.ListComp)
            if not tem_list_comp:
                return False, "Use uma list comprehension (ex.: [i*i for i in range(5)])."
            return True, ""

        elif topico == "Tratamento de Erros":
            # Requer try/except (ou finally). Pode ter raise opcionalmente.
            tem_try = False
            for n in ast.walk(arvore):
                if isinstance(n, ast.Try) and (n.handlers or n.finalbody):
                    tem_try = True
                    break
            if not tem_try:
                return False, "Use try/except (ou try/finally) para tratar erros."
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



