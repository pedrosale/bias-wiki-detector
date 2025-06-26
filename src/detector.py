import os, json
import pandas as pd
from openai import OpenAI
from .utils import safe_json_parse                          # mesma função que já usa

# ─────────────────── CONFIG OPENAI ────────────────────
client = OpenAI()
MODEL  = os.getenv("OPENAI_MODEL", "gpt-4o-mini")           # opc.: defina em Secrets

# ─────────────────── PROMPTS ───────────────────────────
PROMPT_LT = """<cole aqui o PROMPT_LT_DETECTOR integral>"""
PROMPT_OP = """<cole aqui o PROMPT_OPINIAO_DISFARCADA>"""
PROMPT_CT = """<cole aqui o PROMPT_CONTRAPONTO_MISSING>"""

def _run(prompt_tmpl: str, texto: str) -> str:
    prompt = prompt_tmpl.replace("{{TEXTO_ALVO}}", texto)
    rsp = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return rsp.choices[0].message.content

def analisar_artigos(df_artigos: pd.DataFrame) -> pd.DataFrame:
    """Recebe DF com colunas Artigo / Link / Conteudo. Devolve tabela final."""
    linhas = []
    for _, row in df_artigos.iterrows():
        titulo = row.Artigo
        texto  = row.Conteudo[:25_000]           # corta para economizar tokens

        try:
            bias   = safe_json_parse(_run(PROMPT_LT, texto))
            opin   = safe_json_parse(_run(PROMPT_OP, texto))
            contra = safe_json_parse(_run(PROMPT_CT, texto))
        except Exception as e:
            bias = opin = contra = [{"erro": str(e)}]

        # garante lista
        if not isinstance(bias, list):   bias   = [bias]
        if not isinstance(opin, list):   opin   = [opin]
        if not isinstance(contra, list): contra = [contra]

        # usa só o PRIMEIRO item de cada prompt
        bias0, opin0, contra0 = bias[0], opin[0], contra[0]

        linhas.append({
            "Artigo": titulo,
            "Link": row.Link,
            "Trecho (Tendencioso)": bias0.get("trecho", ""),
            "Tipo de Viés": bias0.get("tipo", ""),
            "Explicação (Viés)": bias0.get("explicacao", ""),
            "Reescrita (Viés)": bias0.get("reescrita_neutra", ""),
            "Trecho (Opinião disfarçada)": opin0.get("trecho", ""),
            "Motivo (Opinião)": opin0.get("motivo", ""),
            "Reescrita (Opinião)": opin0.get("reescrita_sugerida", ""),
            "Tema ausente": contra0.get("tema_ausente", ""),
            "Importância do Contraponto": contra0.get("por_que_e_importante", ""),
            "Sugestão de Inclusão": contra0.get("como_incluir", ""),
        })

    return pd.DataFrame(linhas)
