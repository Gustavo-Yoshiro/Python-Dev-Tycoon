import requests
import json
from Intermediario.Persistencia.Entidade.ProjetoFreelance import ProjetoFreelance

class ValidacaoServiceImpl:
    def __init__(self):
        self.api_url = "https://emkc.org/api/v2/piston/execute"

    def _executar_codigo_piston(self, codigo: str, stdin: str = "") -> str:
        """Executa um bloco de código usando a API Piston."""
        payload = {
            "language": "python",
            "version": "3.10.0",
            "files": [{"name": "main.py", "content": codigo}],
            "stdin": stdin
        }
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('run') and data['run'].get('code') == 0:
                return data['run'].get('output', '').strip()
            else:
                # Retorna o erro se houver, para o jogador poder depurar
                return data.get('run', {}).get('stderr', 'Erro de compilação').strip()
        except requests.Timeout:
            return "Erro: O código demorou muito para responder (timeout)."
        except requests.RequestException as e:
            return f"Erro de Conexão: {e}"

    def validar_solucao(self, projeto: ProjetoFreelance, codigo_jogador: str) -> dict:
        """Valida o código do jogador contra os testes definidos no projeto."""
        try:
            testes = json.loads(projeto.get_testes())
        except (json.JSONDecodeError, TypeError):
            return {"sucesso": False, "resultados": ["Erro: Formato de teste inválido no banco de dados."]}

        resultados_testes = []
        todos_passaram = True

        for i, teste in enumerate(testes):
            # Monta o código final que será enviado para a API
            # Inclui o código do jogador (que contém a função) e a chamada para testá-la
            nome_funcao = codigo_jogador.split("def ")[1].split("(")[0].strip()
            args = teste.get("entrada_funcao", [])
            # Converte args para string, tratando strings com aspas
            args_str = ", ".join([f'"{a}"' if isinstance(a, str) else str(a) for a in args])
            
            codigo_completo = f"{codigo_jogador}\n\nprint({nome_funcao}({args_str}))"

            output_real = self._executar_codigo_piston(codigo_completo)
            output_esperado = str(teste.get("saida_esperada", ""))

            if output_real == output_esperado:
                resultados_testes.append(f"✓ Teste #{i+1}: Passou!")
            else:
                todos_passaram = False
                resultados_testes.append(f"✗ Teste #{i+1}: Falhou. Esperado: '{output_esperado}', Recebido: '{output_real}'")

        return {"sucesso": todos_passaram, "resultados": resultados_testes}
