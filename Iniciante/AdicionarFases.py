from Iniciante.Persistencia.Entidade.Fase import Fase
from Iniciante.Persistencia.Impl.FasePersistenciaImpl import FasePersistenciaImpl

fases = [
    Fase(None, "iniciante", "Saída de Dados com print()",
         "No Python, usamos o comando print() para mostrar informações na tela. Ele é a ferramenta básica para apresentar mensagens, resultados de cálculos ou qualquer dado para o jogador e para o usuário dos seus programas. Tudo o que você quiser exibir, basta colocar dentro dos parênteses, entre aspas, se for texto. Isso fará aparecer a frase exatamente como está no seu jogo ou programa. Você pode usar o print() para exibir números, textos, contas e até várias informações de uma vez só!\nExemplo:\nprint(\"Bem-vindo ao Python Dev Tycoon!\")"),

    Fase(None, "iniciante", "Entrada de Dados com input()",
         "O comando input() serve para receber informações do usuário. Sempre que você quiser que o jogador ou usuário digite algo enquanto o programa roda, use input(). O valor digitado pode ser guardado em uma variável para ser usado depois.\nExemplo:\nnome = input(\"Digite seu nome: \")\nprint(\"Olá,\", nome)"),

    Fase(None, "iniciante", "Variáveis e Tipos Simples",
         "Variáveis são \"caixinhas\" onde você pode guardar informações para usar mais tarde no seu programa: números, textos, resultados de contas, etc. No Python, basta escolher um nome e usar o sinal = para guardar o valor. O tipo da variável (texto, número, etc.) é definido automaticamente pelo valor que você atribui.\nExemplo:\nidade = 18  # inteiro\nnome = \"Ana\"  # texto"),

    Fase(None, "iniciante", "Operadores Aritméticos e Relacionais",
         "Operadores aritméticos permitem fazer contas: soma (+), subtração (-), multiplicação (*), divisão (/) e muito mais. Operadores relacionais comparam valores, como saber se um número é igual (==), diferente (!=), maior (>), menor (<), etc.\nExemplo:\nresultado = 5 + 3\nprint(10 > 2)"),

    Fase(None, "iniciante", "Estruturas Condicionais (if/else)",
         "Estruturas condicionais permitem que o programa tome decisões com base em alguma condição. Usamos if para dizer \"se algo for verdade, faça isso\", e else para \"senão, faça aquilo\". Pode usar também o elif para mais de uma opção.\nExemplo:\nif idade >= 18:\n    print(\"Maior de idade\")\nelse:\n    print(\"Menor de idade\")"),

    Fase(None, "iniciante", "Estruturas de Repetição (for)",
         "O laço for é usado para repetir um bloco de código várias vezes. Muito útil para listas, contagens e repetições automáticas.\nExemplo:\nfor i in range(1, 6):\n    print(i)"),

    Fase(None, "iniciante", "Estrutura de Repetição (while)",
         "O laço while repete o código enquanto uma condição for verdadeira. Você pode usar quando não sabe quantas vezes vai repetir.\nExemplo:\nnumero = 1\nwhile numero <= 3:\n    print(numero)\n    numero += 1"),

    Fase(None, "iniciante", "Funções Simples",
         "Funções servem para organizar o código em blocos reutilizáveis. Você cria uma função usando def, dá um nome a ela e depois pode chamar quantas vezes quiser.\nExemplo:\ndef saudacao():\n    print(\"Bem-vindo!\")\nsaudacao()")
]

persistencia = FasePersistenciaImpl()
for fase in fases:
    persistencia.salvar(fase)