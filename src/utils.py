# src/utils.py

import json

def safe_json_parse(texto):
    """Remove blocos ```json … ``` e devolve lista/dict; senão devolve string."""
    if isinstance(texto, (list, dict)):
        return texto
    if isinstance(texto, str):
        t = texto.strip()
        if t.startswith("```"):
            t = t.split("```")[1].strip()  # remove marcadores markdown
        try:
            return json.loads(t)
        except Exception:
            return t
    return texto
