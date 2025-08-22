import requests

def executar_codigo_piston(codigo, versao="3.10.0",entrada_teste=""):
        
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {
            "language": "python",
            "version": versao,
            "files": [{"name": "main.py", "content": codigo}],
            "stdin": entrada_teste if entrada_teste else "",
            "args": [],
        }
        try:
            resp = requests.post(url, json=payload, timeout=8)
            resp.raise_for_status()
            saida = resp.json()
            if 'output' in saida:
                return saida['output'].strip()
            elif 'run' in saida and 'stdout' in saida['run']:
                return saida['run']['stdout'].strip()
            elif 'stdout' in saida:
                return saida['stdout'].strip()
            else:
                return "[SEM OUTPUT]"
        except Exception as e:
            return f"Erro: {e}"