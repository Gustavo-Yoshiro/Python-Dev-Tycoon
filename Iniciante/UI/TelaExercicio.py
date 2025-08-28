import pygame
from Iniciante.Service.Impl.ExercicioServiceImpl import ExercicioServiceImpl
from Iniciante.Service.Impl.ProgressoFaseServiceImpl import ProgressoFaseServiceImpl
import random
import os
from Game.ApiPiston import executar_codigo_piston

# Views
from Iniciante.UI.View.ObjectiveView import ObjectiveView
from Iniciante.UI.View.DragDropView import DragDropView
from Iniciante.UI.View.DissertativeView import DissertativeView


class TelaExercicio:
    def __init__(self, largura, altura, nome_topico, total_fases=1, fases_concluidas=0, callback_rever_introducao=None, jogador=None, id_fase=None):
        # Básicos
        self.largura = largura
        self.altura = altura
        self.nome_topico = nome_topico
        self.total_fases = total_fases
        self.fases_concluidas = fases_concluidas
        self.callback_rever_introducao = callback_rever_introducao
        self.jogador = jogador
        self.id_fase = id_fase
        self.nome_jogador = jogador.get_nome() if jogador else ""

        self.popup_saida = False
        self._popup_btn_rect = None
        self.rect_info_saida = None

        self.dragging = False
        self.drag_offset = (0, 0)
        
        # Serviços
        self.exercicio_service = ExercicioServiceImpl()
        self.progresso_service = ProgressoFaseServiceImpl()

        # Carrega exercícios e progresso do jogador nesta fase
        self.exercicios, progresso = self.exercicio_service.carregar_exercicios(self.id_fase, self.jogador)
        try:
            if self.id_fase <= 16 and len(self.exercicios) > 4:
                objs  = [e for e in self.exercicios if e.get_tipo().lower() == "objetiva"][:2]
                diss  = [e for e in self.exercicios if e.get_tipo().lower() == "dissertativa"][:1]
                drags = [e for e in self.exercicios if e.get_tipo().lower() == "dragdrop"][:1]
                compact = objs + diss + drags
                if len(compact) < 4:
                    resto = [e for e in self.exercicios if e not in compact]
                    compact += resto[:(4-len(compact))]
                self.exercicios = compact
        except Exception:
            pass

        if progresso:
            self.indice_atual = progresso.get_indice_exercicio()
            self.acertos = progresso.get_acertos()
            self.erros = progresso.get_erros()
        else:
            self.indice_atual = 0
            self.acertos = 0
            self.erros = 0

        if self.exercicios and self.indice_atual >= len(self.exercicios):
            self.finalizado = True
            self.exercicio_selecionado = None
        else:
            self.finalizado = False
            self.exercicio_selecionado = self.exercicios[self.indice_atual] if self.exercicios else None
        
        self.resultado = ""
        self.feedback_ativo = False
        self.resposta_usuario = ""
        
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Consolas', 24)
        self.fonte_pequena = pygame.font.SysFont('Consolas', 18)
        self.fonte_editor = pygame.font.SysFont('Consolas', 20)
        self.editor_lh = self.fonte_editor.get_height()
        
        self.rect_livro = pygame.Rect(int(largura * 0.85), int(altura * 0.12), 48, 48)
        self.img_ajuda = pygame.image.load(os.path.join("Assets", "ajuda.png")).convert_alpha()
        self.img_ajuda = pygame.transform.smoothscale(self.img_ajuda, (self.rect_livro.width, self.rect_livro.height))

        self.prompt_visivel = True
        self.prompt_msg = ""
        self.rect_prompt = pygame.Rect(int(largura * 0.25), int(altura * 0.13), int(largura * 0.54), int(altura * 0.66))
        self.rect_q = None
        self.rect_x = None
        self.rect_btn = None

        self.mouse_down_ao_entrar = pygame.mouse.get_pressed()[0]

        # Views
        self.view_objetiva = ObjectiveView(self.fonte, self.fonte_pequena)
        self.view_dragdrop = DragDropView(self.fonte, self.fonte_pequena)
        self.view_dissertativa = DissertativeView(self.fonte, self.fonte_pequena, self.fonte_editor, linhas_visiveis=5)

        if self.exercicio_selecionado:
            t = self.exercicio_selecionado.get_tipo().lower()
            if t == "objetiva":
                self.view_objetiva.set_exercicio(self.exercicio_selecionado)
            elif t == "dragdrop":
                self.view_dragdrop.set_exercicio(self.exercicio_selecionado)
            elif t == "dissertativa":
                self.view_dissertativa.set_exercicio(self.exercicio_selecionado)

    # --------------------- Utils locais ---------------------
    @staticmethod
    def clamp(val, mini, maxi):
        return max(mini, min(val, maxi))

    @staticmethod
    def quebrar_texto(texto, fonte, largura_max):
        palavras = texto.split(' ')
        linhas = []
        linha = ''
        for palavra in palavras:
            teste = linha + palavra + ' '
            if fonte.size(teste)[0] > largura_max:
                linhas.append(linha.strip())
                linha = palavra + ' '
            else:
                linha = teste
        if linha.strip():
            linhas.append(linha.strip())
        return linhas

    @staticmethod
    def ajustar_fonte_para_caber(texto, fonte_base, largura_max, altura_max, min_font=13, espacamento=4):
        font_size = fonte_base.get_height()
        fonte = fonte_base
        while font_size >= min_font:
            linhas = TelaExercicio.quebrar_texto(texto, fonte, largura_max)
            total_h = len(linhas) * (fonte.get_height() + espacamento)
            if total_h <= altura_max:
                return fonte, linhas
            font_size -= 1
            fonte = pygame.font.SysFont('Consolas', font_size)
        linhas = TelaExercicio.quebrar_texto(texto, fonte, largura_max)
        max_linhas = max(1, altura_max // (fonte.get_height() + espacamento))
        if len(linhas) > max_linhas:
            linhas = linhas[:max_linhas-1] + ["..."]
        return fonte, linhas

    def _feedback_objetiva(self, exercicio, alternativa_escolhida: str) -> str:
        """
        Explica por que a alternativa escolhida está certa/errada.
        NUNCA revela a correta quando a escolha está errada.
        Cobre todas as questões objetivas das fases 1..8 (iniciante).
        """
        q = (exercicio.get_pergunta() or "").lower().strip()
        a = (alternativa_escolhida or "").strip()

        # Helper para comparação tolerante a espaços/maíusculas
        def _eq(opt: str) -> bool:
            return ' '.join(a.lower().split()) == ' '.join(opt.lower().split())

        # ========================== FASE 1: print() ==========================
        if "exibe um texto na tela" in q:
            if _eq("print()"):          return "Correta: é a função padrão do Python para exibir valores."
            if _eq("show()"):           return "Errada: 'show()' não é função nativa do Python."
            if _eq("output()"):         return "Errada: 'output()' não existe no Python padrão."
            if _eq("display()"):        return "Errada: 'display()' é de ambientes como IPython/Jupyter, não o print padrão."
            return "Revise o comando usado para exibir valores na tela com Python."

        if "resultado de 5 + 3" in q:
            if _eq("print(5 + 3)"):     return "Correta: a expressão é avaliada e o resultado (8) é impresso."
            if _eq('print("5 + 3")'):   return "Errada: entre aspas é texto literal; não calcula a soma."
            if _eq("print(5,+,3)"):     return "Errada: isso não é sintaxe válida do Python."
            if _eq("print(8)"):         return "Parcial: imprime 8, mas não mostra o cálculo solicitado."
            return "Revise: para mostrar o resultado de uma expressão, imprima a expressão, não uma string."

        # ========================== FASE 2: input() ==========================
        if "lê um texto digitado pelo usuário" in q:
            if _eq("input()"):          return "Correta: lê uma string digitada pelo usuário."
            if _eq("scan()"):           return "Errada: não é função do Python padrão."
            if _eq("read()"):           return "Errada: não é a função usada para entrada pelo teclado em Python."
            if _eq("get()"):            return "Errada: não é a função padrão para leitura de entrada em Python."
            return "Revise o comando padrão de leitura pelo teclado em Python."

        if "guarda o nome digitado" in q:
            if _eq('nome = input("Digite seu nome: ")'): return "Correta: lê a entrada e atribui à variável."
            if _eq("input(nome)"):                      return "Errada: usa 'nome' como mensagem; não atribui o valor lido."
            if _eq("nome == input()"):                  return "Errada: '==' compara; para guardar é necessário '='."
            if _eq('input("Digite seu nome: ") = nome'):return "Errada: ordem de atribuição invertida em Python."
            return "Revise a diferença entre atribuição (=) e comparação (==)."

        # ========================== FASE 3: variáveis ==========================
        if "variável inteira chamada idade" in q:
            if _eq("idade = 20"):       return "Correta: inteiro sem aspas representa número."
            if _eq('idade = "20"'):     return "Errada: com aspas vira string, não inteiro."
            if _eq("int idade = 20"):   return "Errada: isso é sintaxe de C/Java, não de Python."
            if _eq("let idade = 20"):   return "Errada: 'let' não existe em Python."
            return "Revise a sintaxe de atribuição e tipos (int vs string)."

        if "variável chamada cidade com valor 'são paulo'" in q:
            if _eq("cidade = 'São Paulo'"): return "Correta: atribuição literal de string."
            if _eq("cidade == 'São Paulo'"):return "Errada: '==' faz comparação, não atribuição."
            if _eq("let cidade = 'São Paulo'"): return "Errada: 'let' não existe no Python."
            if _eq("cidade := 'São Paulo'"):   return "Errada: ':=' (walrus) não é para atribuição normal."
            return "Revise: atribuição usa '=' e strings precisam de aspas."

        # ========================== FASE 4: Operadores ==========================
        if "verifica igualdade" in q:
            if _eq("=="):               return "Correta: '==' compara se os valores são iguais."
            if _eq("="):                return "Errada: '=' faz atribuição."
            if _eq("!="):               return "Errada: esse operador significa 'diferente de'."
            if _eq("=>"):               return "Errada: operador inválido em Python."
            return "Revise os operadores de comparação do Python."

        if "usado para 'diferente de'" in q or "diferente de" in q:
            if _eq("!="):               return "Correta: indica desigualdade."
            if _eq("=/="):              return "Errada: não é operador do Python."
            if _eq("=="):               return "Errada: esse é o operador de igualdade."
            if _eq("<>"):               return "Errada: era do Python 2; não é usado no Python 3."
            return "Revise o operador de desigualdade do Python."

        if "resultado de 3 + 2 * 2" in q:
            if _eq("7"):                return "Correta: multiplicação tem precedência sobre soma."
            if _eq("10") or _eq("9") or _eq("12"):
                return "Errada: lembre que * e / têm precedência sobre + e -; use parênteses se precisar mudar a ordem."
            return "Revise a ordem de precedência dos operadores."

        # ========================== FASE 5: If/Else ==========================
        if "qual destas estruturas é correta" in q:
            if _eq("if x > 10: print(x)"):             return "Correta: usa dois-pontos e indentação, como pede o Python."
            if _eq("if x > 10 then print(x)"):         return "Errada: 'then' não faz parte da sintaxe do Python."
            if _eq("if (x > 10) { print(x) }"):        return "Errada: chaves não são usadas para blocos em Python."
            if _eq("if x > 10 do print(x)"):           return "Errada: 'do' não existe nessa construção em Python."
            return "Revise a sintaxe de if/elif/else no Python (dois-pontos e indentação)."

        if "como se escreve o bloco else" in q:
            if _eq("else:"):            return "Correta: bloco else termina com dois-pontos."
            if _eq("else"):             return "Errada: falta ':' ao final."
            if _eq("else {}"):          return "Errada: Python não usa chaves para blocos."
            if _eq("else then:"):       return "Errada: 'then' não é parte da sintaxe do Python."
            return "Revise a estrutura de blocos com dois-pontos e indentação."

        # ========================== FASE 6: For ==========================
        if "imprime os números de 1 a 3" in q:
            if _eq("for i in range(1, 4): print(i)"):  return "Correta: range(1,4) gera 1, 2 e 3."
            if _eq("for i = 1 to 3: print(i)"):        return "Errada: essa sintaxe não é Python."
            if _eq("for i in 1..3: print(i)"):         return "Errada: intervalo '1..3' não existe em Python."
            if _eq("for (i = 1; i <= 3; i++): print(i)"): return "Errada: isso é estilo C; Python usa 'for ... in ...'."
            return "Revise como o range funciona e a sintaxe do for em Python."

        if "faz o corpo executar exatamente 5 vezes" in q:
            if _eq("for i in range(5):"):              return "Correta: range(5) produz 5 iterações (0..4)."
            if _eq("for i in 5:"):                     return "Errada: inteiros não são iteráveis."
            if _eq("for i in range(1,5):"):            return "Errada: executa 4 vezes (1,2,3,4)."
            if _eq("for i = 1 to 5:"):                 return "Errada: essa sintaxe não é do Python."
            return "Revise a assinatura de range e contagem de iterações."

        # ========================== FASE 7: While ==========================
        if ("o que faz este código?" in q and "while x <=" in q) or ("x = 1 while x <=" in q):
            if _eq("Imprime 1, 2 e 3"):               return "Correta: imprime e incrementa até x ultrapassar 3."
            if _eq("Não faz nada"):                    return "Errada: há um laço que imprime valores."
            if _eq("Imprime infinitamente"):          return "Errada: como x é incrementado, o laço termina."
            if _eq("Erro de sintaxe"):                return "Errada: com quebras/indentação corretas, o código é válido."
            return "Revise a mecânica do while: condição, corpo e incremento."

        if "como sair do laço antes do fim" in q:
            if _eq("break"):                           return "Correta: encerra o laço imediatamente."
            if _eq("stop"):                            return "Errada: 'stop' não é comando do Python."
            if _eq("end"):                             return "Errada: 'end' não encerra laço em Python."
            if _eq("exit"):                            return "Errada: 'exit' não é o comando apropriado para sair do laço."
            return "Revise os comandos de controle de laço (break/continue)."

        # ========================== FASE 8: Funções ==========================
        if "qual comando define uma função" in q or "define uma função em python" in q:
            if _eq("def soma(a, b):"):                 return "Correta: 'def nome(parâmetros):' é a sintaxe correta."
            if _eq("function soma(a, b):"):            return "Errada: 'function' não é usado em Python."
            if _eq("def soma(a, b) end"):              return "Errada: 'end' não fecha blocos em Python; usa-se indentação."
            if _eq("func soma(a, b):"):                return "Errada: 'func' não é palavra-chave do Python."
            return "Revise a palavra-chave 'def' e o uso de dois-pontos com indentação."

        if "retorna o dobro de x" in q:
            if _eq("def dobro(x): return x * 2"):      return "Correta: a função retorna o resultado calculado."
            if _eq("def dobro(x): print(x * 2)"):      return "Errada: 'print' só exibe; a questão pede retorno."
            if _eq("def dobro(): return x * 2"):       return "Errada: falta o parâmetro 'x'."
            if _eq("function dobro(x): return x * 2"):  return "Errada: 'function' não é sintaxe do Python."
            return "Revise: retornar valor usa 'return', e parâmetros devem estar na assinatura."

        # ========================== GENÉRICO (não revelar correta) ==========================
        # Se chegou aqui, a questão NÃO é uma das objetivas do iniciante mapeadas.
        # Damos um conselho neutro sem revelar a alternativa correta.
        return "Revise o conteúdo do tópico e a sintaxe do Python para essa situação."

        # --- FASE 9: f-strings ---
        if "usa f-string corretamente" in q:
            if a == 'print(f"Olá, {nome}")': return "Correta: f antes da string e {nome} para interpolar."
            if a == 'print("Olá, {nome}")':  return "Errada: sem f a chave não é interpolada."
            if a == 'print(f"Olá, nome")':   return "Errada: imprime a palavra 'nome'."
            if a == 'print("fOlá, {nome}")': return "Errada: o f está dentro das aspas."
        if "duas casas decimais usando f-string" in q:
            if a == 'print(f"Preço: {preco:.2f}")': return "Correta: :.2f formata com 2 casas."
            return "Errada: a sintaxe de formatação está incorreta."

        # --- FASE 10: métodos de string ---
        if "todo o texto em maiúsculas" in q:
            if a == "upper()":      return "Correta: s.upper()."
            if a == "capitalize()": return "Errada: só a 1ª letra da frase."
            if a == "title()":      return "Errada: 1ª letra de cada palavra."
            if a == "max()":        return "Errada: não é método de string."
        if "divide a string em uma lista de palavras" in q:
            if a == "split()":      return "Correta: separa por espaços por padrão."
            if a == "join()":       return "Errada: faz o inverso (junta)."
            if a == "replace()":    return "Errada: troca trechos."
            if a == "separate()":   return "Errada: não existe."

        # --- FASE 11: listas ---
        if "adiciona um item ao final da lista" in q:
            if a == "append()": return "Correta: lista.append(x)."
            if a == "add()":    return "Errada: add() é de set."
            if a == "push()":   return "Errada: estilo de outras linguagens."
            if a == "insert()": return "Errada: insert() precisa de índice."
        if "ordena a lista em ordem crescente" in q:
            if a == "sort()":   return "Correta: lista.sort() ordena in-place."
            if a == "order()":  return "Errada: não existe."
            if a == "reverse()":return "Errada: só inverte."
            if a == "sorted()": return "Parcial: sorted(lista) retorna NOVA lista; a pergunta pediu método da lista."

        # --- FASE 12: tuplas ---
        if "cria uma tupla com 1 e 2" in q:
            if a == "(1, 2)": return "Correta: tupla usa parênteses."
            return "Errada: [] é lista, {} é set/dict."
        if "conta quantas vezes um valor aparece" in q:
            if a == "count()": return "Correta: t.count(valor)."
            return "Errada: métodos/nome incorretos."

        # --- FASE 13: conjuntos (set) ---
        if "cria um conjunto com 1,2,3" in q:
            if a == "{1, 2, 3}": return "Correta: chaves com elementos únicos."
            return "Errada: [] é lista, () é tupla."
        if "união de dois conjuntos" in q:
            if a == "|": return "Correta: A | B é união."
            if a == "&": return "Errada: '&' é interseção."
            if a == "-": return "Errada: '-' é diferença."
            if a == "+": return "Errada: '+' não é definido para set."

        # --- FASE 14: dicionários ---
        if "cria dicionário com nome='ana'" in q:
            if a == "{'nome': 'Ana'}": return "Correta: {'chave': valor}."
            if a == "{nome: 'Ana'}":   return "Errada: chave sem aspas vira variável (NameError)."
            if a == "[nome:'Ana']":    return "Errada: colchetes não definem dict."
            if a == "dict(nome='Ana')":return "Parcial: funciona, mas foi pedida a sintaxe literal com chaves."
        if "retorna as chaves de um dicionário" in q:
            if a == "keys()":   return "Correta: d.keys()."
            if a == "values()": return "Errada: retorna valores."
            if a == "items()":  return "Errada: retorna pares (chave, valor)."
            if a == "get_keys()":return "Errada: não existe."

        # --- FASE 15: list comprehensions ---
        if "cria lista de 0 a 4" in q:
            if a == "[x for x in range(5)]": return "Correta: gera 0..4."
            return "Errada: sintaxe de comprehension incorreta."
        if "números pares até 5" in q:
            if a == "[x for x in range(6) if x % 2 == 0]": return "Correta: filtra pares em 0..5."
            return "Errada: posição do 'if' e/ou sintaxe incorreta."

        # --- FASE 16: try/except ---
        if "inicia um bloco de tratamento de erros" in q:
            if a == "try": return "Correta: bloco try/except."
            return "Errada: 'catch' não é Python; 'except' não inicia bloco."
        if "captura especificamente valueerror" in q:
            if a == "except ValueError:": return "Correta: captura ValueError."
            return "Errada: sintaxe correta é 'except TipoDeErro:' com dois-pontos."

        # Fallback genérico
        return f"Alternativa correta: {correta}"

    def centralizar_prompt(self):
        self.rect_prompt.x = int(self.largura * 0.25)
        self.rect_prompt.y = int(self.altura * 0.13)

    # --------------------- Render ---------------------
    def desenhar(self, tela):
        if not self.prompt_visivel:
            return

        prompt = self.rect_prompt
        prompt_surf = pygame.Surface((prompt.w, prompt.h), pygame.SRCALPHA)
        pygame.draw.rect(prompt_surf, (18, 24, 32, 210), (0, 0, prompt.w, prompt.h), border_radius=16)
        tela.blit(prompt_surf, (prompt.x, prompt.y))
        pygame.draw.rect(tela, (42, 103, 188), prompt, 6, border_radius=16)

        # HEADER
        header_h = 50
        header_rect = pygame.Rect(prompt.x, prompt.y, prompt.w, header_h)
        pygame.draw.rect(tela, (28, 44, 80), header_rect, border_radius=14)
        pygame.draw.line(tela, (60, 160, 255), (prompt.x, prompt.y+header_h), (prompt.x+prompt.w, prompt.y+header_h), 2)
        
        # Título
        txt = self.fonte.render(self.nome_topico, True, (230, 240, 255))
        tela.blit(txt, (prompt.x+24, prompt.y+10))

        usuario_txt = f"Usuário logado: {self.nome_jogador}"
        usuario_surface = self.fonte_pequena.render(usuario_txt, True, (230, 230, 90))
        tela.blit(usuario_surface, (prompt.x + 28, prompt.y + header_h + 6))
        y_usuario = prompt.y + header_h + 6 + usuario_surface.get_height() + 4
        pygame.draw.line(tela, (80, 120, 180), (prompt.x + 28, y_usuario), (prompt.x + prompt.w - 28, y_usuario), 2)

        # ? e X
        self.rect_q = pygame.Rect(prompt.right-90, prompt.y+10, 30, 30)
        self.rect_x = pygame.Rect(prompt.right-45, prompt.y+10, 30, 30)
        pygame.draw.circle(tela, (110, 190, 255), self.rect_q.center, 15)
        q_mark = self.fonte_pequena.render("?", True, (28, 44, 80))
        tela.blit(q_mark, (self.rect_q.x+8, self.rect_q.y+3))
        pygame.draw.circle(tela, (255, 100, 100), self.rect_x.center, 15)
        x_mark = self.fonte_pequena.render("x", True, (40, 0, 0))
        tela.blit(x_mark, (self.rect_x.x+9, self.rect_x.y+4))

        # Tooltips
        mx, my = pygame.mouse.get_pos()
        if self.rect_q.collidepoint(mx, my):
            texto_ajuda = "Clique para ver a introdução do tópico novamente."
            largura_balao = self.fonte_pequena.size(texto_ajuda)[0] + 32
            altura_balao = 40
            surf = pygame.Surface((largura_balao, altura_balao), pygame.SRCALPHA)
            pygame.draw.rect(surf, (40,60,110, 220), (0,0,largura_balao,altura_balao), border_radius=12)
            pygame.draw.rect(surf, (110,190,255), (0,0,largura_balao,altura_balao), 2, border_radius=12)
            tip = self.fonte_pequena.render(texto_ajuda, True, (255,255,255))
            surf.blit(tip, (16,10))
            tela.blit(surf, (mx-largura_balao//2, my-altura_balao-8))
        elif self.rect_x.collidepoint(mx, my):
            texto_ajuda = "Não se preocupe, seu progresso é salvo automaticamente."
            largura_balao = self.fonte_pequena.size(texto_ajuda)[0] + 32
            altura_balao = 40
            surf = pygame.Surface((largura_balao, altura_balao), pygame.SRCALPHA)
            pygame.draw.rect(surf, (40,60,110, 220), (0,0,largura_balao,altura_balao), border_radius=12)
            pygame.draw.rect(surf, (110,190,255), (0,0,largura_balao,altura_balao), 2, border_radius=12)
            tip = self.fonte_pequena.render(texto_ajuda, True, (255,255,255))
            surf.blit(tip, (16,10))
            tela.blit(surf, (mx-largura_balao//2, my-altura_balao-8))

        # -------- Barras de Progresso --------
        BAR_HEIGHT = 28
        espaco_usuario = usuario_surface.get_height() + 18
        y_barras = prompt.y + header_h + espaco_usuario

        bar1_rect = pygame.Rect(prompt.x+40, y_barras, prompt.w-80, BAR_HEIGHT)
        bar2_rect = pygame.Rect(prompt.x+40, y_barras+42, prompt.w-80, BAR_HEIGHT)

        # barra 1 (tópicos)
        barra1_perc = self.fases_concluidas / self.total_fases if self.total_fases > 0 else 0
        pygame.draw.rect(tela, (46, 48, 80), bar1_rect, border_radius=12)
        pygame.draw.rect(tela, (255, 204, 72), (bar1_rect.x, bar1_rect.y, int(barra1_perc*bar1_rect.w), bar1_rect.h), border_radius=12)
        t1 = self.fonte_pequena.render(f"Tópicos: {self.fases_concluidas}/{self.total_fases}", True, (60, 60, 90))
        tela.blit(t1, (bar1_rect.x+8, bar1_rect.y + (BAR_HEIGHT - t1.get_height()) // 2))

        # barra 2 (questões + MG para iniciante)
        tem_mg = (self.id_fase is not None and self.id_fase <= 16)
        if tem_mg:
            pygame.draw.rect(tela, (0,0,0,0), bar2_rect)
            seg_total = 5
            seg_gap = 6
            seg_w = (bar2_rect.w - seg_gap*(seg_total-1)) // seg_total
            concluidos = max(0, min(self.indice_atual, 4))
            for i in range(seg_total):
                seg_x = bar2_rect.x + i * (seg_w + seg_gap)
                seg = pygame.Rect(seg_x, bar2_rect.y, seg_w, bar2_rect.h)
                pygame.draw.rect(tela, (46, 48, 80), seg, border_radius=8)
                if i < concluidos:
                    pygame.draw.rect(tela, (84, 240, 200), seg, border_radius=8)
                if i == self.indice_atual and i < 4 and not self.finalizado:
                    pygame.draw.rect(tela, (70, 200, 170), seg, 3, border_radius=8)
                if i == 4:
                    pygame.draw.rect(tela, (110, 190, 255), seg, 2, border_radius=8)
                    mg_lbl = self.fonte_pequena.render("MiniGame", True, (160, 200, 255))
                    tela.blit(mg_lbl, (seg.centerx - mg_lbl.get_width()//2, seg.centery - mg_lbl.get_height()//2))
                    if self.finalizado:
                        glow = pygame.Surface((seg.w, seg.h), pygame.SRCALPHA)
                        glow.fill((110, 190, 255, 60))
                        tela.blit(glow, (seg.x, seg.y))
            t2_text = f"Questões {min(self.indice_atual+1,4)}/{4}"
            t2 = self.fonte_pequena.render(t2_text, True, (40, 130, 110))
            tela.blit(t2, (bar2_rect.x+8, bar2_rect.y + (BAR_HEIGHT - t2.get_height()) // 2))
        else:
            barra2_perc = (self.indice_atual+1)/len(self.exercicios) if self.exercicios else 0
            pygame.draw.rect(tela, (46, 48, 80), bar2_rect, border_radius=12)
            pygame.draw.rect(tela, (84, 240, 200), (bar2_rect.x, bar2_rect.y, int(bar2_rect.w*barra2_perc), bar2_rect.h), border_radius=12)
            t2 = self.fonte_pequena.render(f"Questão {self.indice_atual+1}/{len(self.exercicios) if self.exercicios else 1}", True, (40, 130, 110))
            tela.blit(t2, (bar2_rect.x+8, bar2_rect.y + (BAR_HEIGHT - t2.get_height()) // 2))

        # ---------------------- Área de conteúdo e botão ----------------------
        y = bar2_rect.bottom + 24
        largura_max = prompt.w - 80

        # Botão ENVIAR/CONTINUAR
        btn_w, btn_h = 180, 52
        btn_x = prompt.x + (prompt.w - btn_w) // 2
        btn_y = prompt.bottom - btn_h - 18

        altura_total = btn_y - y - 16
        content_rect = pygame.Rect(prompt.x + 40, y, prompt.w - 80, max(0, altura_total))

        if self.finalizado:
            msg = f"Quiz finalizado!"
            placar = f"Acertos: {self.acertos} | Erros: {self.erros} de {len(self.exercicios)}"
            tela.blit(self.fonte.render(msg, True, (0, 255, 255)), (prompt.x + 30, y+40))
            tela.blit(self.fonte_pequena.render(placar, True, (255, 255, 255)), (prompt.x + 30, y+100))
            return

        if self.exercicio_selecionado:
            tipo = self.exercicio_selecionado.get_tipo().lower()

            if tipo == "objetiva":
                if self.view_objetiva.exercicio != self.exercicio_selecionado:
                    self.view_objetiva.set_exercicio(self.exercicio_selecionado)
                self.view_objetiva.draw(tela, content_rect, feedback_ativo=self.feedback_ativo)

            elif tipo == "dissertativa":
                if self.view_dissertativa.exercicio != self.exercicio_selecionado:
                    self.view_dissertativa.set_exercicio(self.exercicio_selecionado)
                self.view_dissertativa.draw(tela, content_rect, feedback_ativo=self.feedback_ativo)

            elif tipo == "dragdrop":
                if self.view_dragdrop.exercicio != self.exercicio_selecionado:
                    self.view_dragdrop.set_exercicio(self.exercicio_selecionado)
                self.view_dragdrop.draw(tela, content_rect, feedback_ativo=self.feedback_ativo)

        # --- Botão ENVIAR/CONTINUAR
        self.rect_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pode = self.pode_enviar()
        cor_btn = (0, 180, 80) if not self.feedback_ativo and pode else (0, 150, 200) if self.feedback_ativo else (80, 80, 80)
        pygame.draw.rect(tela, cor_btn, self.rect_btn, border_radius=24)
        label_btn = "ENVIAR" if not self.feedback_ativo else "CONTINUAR"
        fonte_btn, linhas_btn = self.ajustar_fonte_para_caber(label_btn, self.fonte_pequena, btn_w-10, btn_h-10)
        y_btn = self.rect_btn.y + (btn_h - sum(self.fonte_pequena.get_height() for _ in linhas_btn)) // 2
        for l_btn in linhas_btn:
            txtsurf = self.fonte_pequena.render(l_btn, True, (255,255,255))
            tela.blit(txtsurf, (self.rect_btn.x + (btn_w - txtsurf.get_width()) // 2, y_btn))
            y_btn += self.fonte_pequena.get_height()

        # --- Feedback
        if self.resultado:
            cor = (0, 255, 0) if "Correta" in self.resultado else (255, 0, 0)
            feedback_x = self.rect_btn.right + 30
            feedback_y = self.rect_btn.y + self.rect_btn.height // 2 - self.fonte_pequena.get_height() // 2 - 8
            msg_curta = "Resposta Correta!" if "Correta" in self.resultado else "Resposta Incorreta!"
            fonte_fb, linhas_fb = self.ajustar_fonte_para_caber(msg_curta, self.fonte_pequena, 220, self.rect_btn.h-2)
            y_fb = feedback_y
            for l_fb in linhas_fb:
                tela.blit(fonte_fb.render(l_fb, True, cor), (feedback_x, y_fb))
                y_fb += fonte_fb.get_height()
            if ("Saída:" in self.resultado) or ("Feedback:" in self.resultado):
                icon_x = feedback_x + sum(fonte_fb.size(l)[0] for l in linhas_fb) + 18
                icon_rect = pygame.Rect(icon_x, feedback_y, 24, 24)
                pygame.draw.circle(tela, (100, 180, 255), icon_rect.center, 12)
                i_mark = self.fonte_pequena.render("i", True, (30, 50, 80))
                tela.blit(i_mark, (icon_rect.x + 6, icon_rect.y + 2))
                self.rect_info_saida = icon_rect
            else:
                self.rect_info_saida = None

            if self.rect_info_saida and self.rect_info_saida.collidepoint(pygame.mouse.get_pos()):
                texto_ajuda = "Ver saída do seu código"
                largura_balao = self.fonte_pequena.size(texto_ajuda)[0] + 24
                altura_balao = 32
                mx, my = pygame.mouse.get_pos()
                surf = pygame.Surface((largura_balao, altura_balao), pygame.SRCALPHA)
                pygame.draw.rect(surf, (40,60,110, 220), (0,0,largura_balao,altura_balao), border_radius=8)
                pygame.draw.rect(surf, (110,190,255), (0,0,largura_balao,altura_balao), 2, border_radius=8)
                tip = self.fonte_pequena.render(texto_ajuda, True, (255,255,255))
                surf.blit(tip, (12,8))
                tela.blit(surf, (mx-largura_balao//2, my-altura_balao-6))

        # --- Popup de saída (dissertativa)
        if self.popup_saida:
            # popup maior
            largura, altura = 640, 420
            popup_x = self.largura // 2 - largura // 2
            popup_y = self.altura // 2 - altura // 2

            surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(surf, (30, 44, 70, 232), (0, 0, largura, altura), border_radius=20)
            pygame.draw.rect(surf, (120, 180, 255), (0, 0, largura, altura), 3, border_radius=20)

            # --- Cabeçalho
            surf.blit(self.fonte.render("Detalhes:", True, (230, 230, 90)), (20, 20))

            # --- Extrai blocos (Feedback e/ou Saída), sem se misturar
            conteudo_feedback = None
            conteudo_saida = None

            if "Feedback:" in self.resultado:
                after = self.resultado.split("Feedback:", 1)[-1]
                # se também existir "Saída:" depois, corta aqui para não misturar
                if "Saída:" in after:
                    after = after.split("Saída:", 1)[0]
                conteudo_feedback = after

            if "Saída:" in self.resultado:
                conteudo_saida = self.resultado.split("Saída:", 1)[-1]

            sections = []
            if conteudo_feedback and conteudo_feedback.strip():
                sections.append(("Feedback", conteudo_feedback))
            if conteudo_saida and conteudo_saida.strip():
                sections.append(("Saída", conteudo_saida))

            if not sections:
                sections = [("Detalhes", "Sem detalhes disponíveis.")]

            # --- Render do conteúdo
            def _sanitize(txt: str) -> str:
                txt = (txt or "").replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
                # mantém quebras de linha e substitui caracteres não imprimíveis
                return ''.join(c if c.isprintable() or c in "\n" else '?' for c in txt)

            y_popup = 66
            max_lines = 18  # limite visível, depois mostramos [...]
            line_count = 0

            for titulo_sec, texto in sections:
                # título da seção
                sec_title = f"{titulo_sec}:"
                surf.blit(self.fonte_pequena.render(sec_title, True, (230, 230, 120)), (18, y_popup))
                y_popup += 28

                texto = _sanitize(texto)
                # quebra por linhas e faz word-wrap em cada linha
                for linha in texto.split("\n"):
                    if line_count >= max_lines:
                        break
                    wraps = self.quebrar_texto(linha, self.fonte_pequena, largura - 40)
                    for wl in wraps:
                        if line_count >= max_lines:
                            break
                        surf.blit(self.fonte_pequena.render(wl, True, (230, 230, 230)), (18, y_popup))
                        y_popup += 22
                        line_count += 1
                if line_count >= max_lines:
                    break

                y_popup += 6  # respiro entre seções

            if line_count >= max_lines:
                surf.blit(self.fonte_pequena.render("[...]", True, (220, 180, 180)), (18, y_popup))

            # --- Botão FECHAR
            btn_rect = pygame.Rect(largura - 100, altura - 50, 86, 36)
            pygame.draw.rect(surf, (255, 90, 90), btn_rect, border_radius=12)
            fechar_label = self.fonte_pequena.render("FECHAR", True, (255, 255, 255))
            surf.blit(fechar_label, (btn_rect.x + (btn_rect.w - fechar_label.get_width()) // 2,
                                    btn_rect.y + (btn_rect.h - fechar_label.get_height()) // 2))

            tela.blit(surf, (popup_x, popup_y))
            self._popup_btn_rect = pygame.Rect(popup_x + btn_rect.x, popup_y + btn_rect.y, btn_rect.w, btn_rect.h)
        else:
            self._popup_btn_rect = None


    # --------------------- Envio/validação ---------------------
    def pode_enviar(self):
        if not self.exercicio_selecionado:
            return False
        tipo = self.exercicio_selecionado.get_tipo().lower()
        if tipo == "objetiva":
            return self.view_objetiva.can_submit()
        elif tipo == "dragdrop":
            return self.view_dragdrop.can_submit()
        else:
            return self.view_dissertativa.can_submit()

    def normaliza_saida(saida):
        return ' '.join(saida.strip().split())
    
    def verificar_resposta(self):
        if not self.exercicio_selecionado:
            return False
        tipo = self.exercicio_selecionado.get_tipo().lower()

        if tipo == "objetiva":
            resposta = self.view_objetiva.get_user_answer()
            correta_txt = (self.exercicio_selecionado.get_resposta_certa() or "").strip().lower()
            if resposta is None:
                self.resultado = "Resposta Incorreta!"
                return False

            correta = (resposta.strip().lower() == correta_txt)

            # Gera texto de explicação (sem destacar nada na UI)
            explic = self._feedback_objetiva(self.exercicio_selecionado, resposta)
            base = "Resposta Correta!" if correta else "Resposta Incorreta!"
            self.resultado = base + (f"\nFeedback: {explic}" if explic else "")
            return correta

        elif tipo == "dragdrop":
            resposta_user = self.view_dragdrop.get_user_answer()
            resposta_certa = (self.exercicio_selecionado.get_resposta_certa() or "").replace("\r\n", "\n")
            correta = (resposta_user.strip() == resposta_certa.strip())
            self.resultado = "Resposta Correta!" if correta else "Resposta Incorreta!"
            return correta

        elif tipo == "dissertativa":
            codigo_usuario = self.view_dissertativa.get_codigo_usuario()
            entrada_teste = self.exercicio_selecionado.get_entrada_teste() or ""
            saida_usuario = executar_codigo_piston(codigo_usuario, entrada_teste=entrada_teste)
            resposta_certa = (self.exercicio_selecionado.get_resposta_certa() or "").strip()
            if saida_usuario.strip() == resposta_certa:
                valido, mensagem = self.exercicio_service.validar_codigo_ast_por_topico(codigo_usuario, self.id_fase)
                if valido:
                    self.resultado = f"Resposta Correta!\nSaída: {saida_usuario}"
                    return True
                else:
                    self.resultado = f"Resposta Incorreta!\nSaída: {saida_usuario}\n{mensagem}"
                    return False
            else:
                self.resultado = f"Resposta Incorreta!\nSaída: {saida_usuario}"
        return False

    # --------------------- Eventos ---------------------
    def tratar_eventos(self, eventos):
        if not self.prompt_visivel:
            return

        # TRAVA enquanto popup ativo
        if self.popup_saida:
            for evento in eventos:
                if self._popup_btn_rect and evento.type == pygame.MOUSEBUTTONDOWN:
                    if self._popup_btn_rect.collidepoint(evento.pos):
                        self.popup_saida = False
            return
        
        for evento in eventos:
            if hasattr(self, "rect_info_saida") and self.rect_info_saida:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_info_saida.collidepoint(evento.pos):
                        self.popup_saida = True
            if hasattr(self, "_popup_btn_rect") and self._popup_btn_rect:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self._popup_btn_rect.collidepoint(evento.pos):
                        self.popup_saida = False

            # Drag da moldura
            if self.prompt_visivel and evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    header_h = 50
                    prompt = self.rect_prompt
                    header_rect = pygame.Rect(prompt.x, prompt.y, prompt.w, header_h)
                    if header_rect.collidepoint(evento.pos):
                        self.dragging = True
                        mx, my = evento.pos
                        self.drag_offset = (mx - prompt.x, my - prompt.y)
            elif evento.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mx, my = evento.pos
                    dx, dy = self.drag_offset
                    self.rect_prompt.x = mx - dx
                    self.rect_prompt.y = my - dy
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and self.dragging:
                    self.dragging = False

            # X fechar
            if self.prompt_visivel and hasattr(self, "rect_x") and evento.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_x and self.rect_x.collidepoint(evento.pos):
                    self.dragging = False
                    self.prompt_visivel = False
                    return

            # Delegação por tipo
            tipo = self.exercicio_selecionado.get_tipo().lower() if self.exercicio_selecionado else ""

            if tipo == "dragdrop":
                self.view_dragdrop.handle_event(evento, feedback_ativo=self.feedback_ativo)

            elif tipo == "dissertativa":
                self.view_dissertativa.handle_event(evento, feedback_ativo=self.feedback_ativo)

            elif tipo == "objetiva":
                self.view_objetiva.handle_event(evento, feedback_ativo=self.feedback_ativo)

            # "?" introdução
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rect_q and self.rect_q.collidepoint(x, y):
                    if self.callback_rever_introducao:
                        self.callback_rever_introducao(self)
                    return

                # Botão ENVIAR/CONTINUAR
                if self.exercicio_selecionado and self.rect_btn and self.rect_btn.collidepoint(x, y):
                    if not self.feedback_ativo and self.pode_enviar():
                        self.feedback_ativo = True
                        correta = self.verificar_resposta()
                        if correta:
                            self.acertos += 1
                        else:
                            self.erros += 1
                    elif self.feedback_ativo:
                        # Avança
                        self.indice_atual += 1
                        self.progresso_service.salvar_ou_atualizar_progresso(
                            jogador=self.jogador,
                            id_fase=self.id_fase,
                            indice_exercicio=self.indice_atual,
                            acertos=self.acertos,
                            erros=self.erros,
                            resposta_parcial=""
                        )
                        if self.indice_atual < len(self.exercicios):
                            self.exercicio_selecionado = self.exercicios[self.indice_atual]
                            self.feedback_ativo = False
                            self.resultado = ""
                            # Reset por tipo
                            t = self.exercicio_selecionado.get_tipo().lower()
                            if t == "objetiva":
                                self.view_objetiva.set_exercicio(self.exercicio_selecionado)
                                self.view_dragdrop.reset()
                                self.view_dissertativa.reset()
                            elif t == "dragdrop":
                                self.view_dragdrop.set_exercicio(self.exercicio_selecionado)
                                self.view_objetiva.reset()
                                self.view_dissertativa.reset()
                            else:
                                self.view_dissertativa.set_exercicio(self.exercicio_selecionado)
                                self.view_objetiva.reset()
                                self.view_dragdrop.reset()
                        else:
                            self.finalizado = True
