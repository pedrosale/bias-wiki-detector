import json

def safe_json_parse(texto):
    """Remove blocos 
json …
 e devolve sempre uma lista de dicionários."""
    if isinstance(texto, (list, dict)):
        return texto if isinstance(texto, list) else [texto]
    
    if isinstance(texto, str):
        t = texto.strip()
        if t.startswith("
"):
            t = t.split("
")[1].strip()  # remove blocos markdown
        try:
            data = json.loads(t)
            return data if isinstance(data, list) else [data]
        except Exception:
            return [{"trecho": t}]  # fallback consistente para colunas

    return [{"trecho": str(texto)}]
