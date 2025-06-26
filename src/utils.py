import json
import tempfile
from weasyprint import HTML


def safe_json_parse(texto):
    """
    Remove blocos ```json … ``` e devolve sempre uma lista de dicionários.
    Útil para garantir consistência em parsing de LLMs.
    """
    if isinstance(texto, (list, dict)):
        return texto if isinstance(texto, list) else [texto]
    
    if isinstance(texto, str):
        t = texto.strip()
        if t.startswith("```"):
            t = t.split("```")[1].strip()  # remove blocos markdown
        try:
            data = json.loads(t)
            return data if isinstance(data, list) else [data]
        except Exception:
            return [{"trecho": t}]  # fallback consistente para colunas

    return [{"trecho": str(texto)}]


def gerar_pdf(df, artigo_nome):
    """
    Gera um PDF com base na análise de viés do DataFrame fornecido.
    """
    html = f"<h1>Análise do artigo: {artigo_nome}</h1><hr>"
    
    for _, row in df.iterrows():
        html += "<div style='margin-bottom:30px;'>"

        html += f"<h3>🟥 Tendencioso</h3><p>{row.get('Trecho (Tendencioso)', '')}</p>"
        html += f"<b>Tipo:</b> {row.get('Tipo de Viés', '')}<br>"
        html += f"<b>Explicação:</b> {row.get('Explicação (Viés)', '')}<br>"
        html += f"<b>Reescrita:</b> {row.get('Reescrita (Viés)', '')}<br><br>"

        html += f"<h3>🟧 Opinião Disfarçada</h3><p>{row.get('Trecho (Opinião disfarçada)', '')}</p>"
        html += f"<b>Motivo:</b> {row.get('Motivo (Opinião)', '')}<br>"
        html += f"<b>Reescrita:</b> {row.get('Reescrita (Opinião)', '')}<br><br>"

        html += f"<h3>🟨 Contraponto Ausente</h3><p>{row.get('Tema ausente', '')}</p>"
        html += f"<b>Importância:</b> {row.get('Importância do Contraponto', '')}<br>"
        html += f"<b>Sugestão:</b> {row.get('Sugestão de Inclusão', '')}<br>"

        html += "</div><hr>"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        HTML(string=html).write_pdf(tmpfile.name)
        return tmpfile.name
