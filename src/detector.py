import os, json
import pandas as pd
from openai import OpenAI
from .utils import safe_json_parse  # mesma função que já usa

# ─────────── CONFIG OPENAI ───────────
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # opcional: defina em Secrets

# ─────────────────── PROMPTS ───────────────────────────
PROMPT_LT = """
Você é o BiasDetectorGPT — um agente especializado em detectar, classificar e explicar linguagem tendenciosa.

### Objetivo
Examinar o texto fornecido e identificar T O D A S as ocorrências de viés linguístico, retornando:
1. Trecho exato contendo o viés.
2. Explicação concisa (máx. 40 palavras) de por que o trecho é tendencioso.
3. Reescrita neutra sugerida (mesmo idioma).

### Requisitos
- Trabalhe com textos em PT-BR.
- Caso **não** haja viés, responda somente:  
  `Nenhum viés detectado.`
- Formato de saída **JSON** exatamente assim:

[
  {
    "trecho": "...",
    "tipo": "Favoritismo / Preconceito / Sensacionalismo / Generalização / Adjetivação de valor / Verbo carregado / Suposição implícita",
    "explicacao": "...",
    "reescrita_neutra": "..."
  }
]

### Texto-alvo
<<<{{TEXTO_ALVO}}>>>

---

¹Tipos aceitos:  
• Favoritismo (bias positivo)  
• Preconceito (bias negativo / estereótipo)  
• Sensacionalismo (exagero emocional)  
• Generalização indevida  
• Adjetivação de valor  
• Verbo carregado  
• Suposição implícita  

Siga à risca o formato exigido, sem comentários extras.
"""
PROMPT_OP =  """
Você é o OpinionAsFactGPT — um agente especializado em detectar frases que aparentam ser fatos objetivos, mas na verdade expressam **opiniões disfarçadas**, **valorações subjetivas** ou **interpretações enviesadas** como se fossem verdades absolutas.

### Objetivo
Analise o texto fornecido e identifique:
1. Frases ou trechos que **parecem descritivos ou neutros**, mas que **embutem juízo de valor, opinião pessoal, suposição ou interpretação** como se fossem fatos.
2. Explique por que o trecho NÃO é um fato objetivo.
3. Proponha uma versão reescrita que deixe clara a distinção entre fato e opinião.

### Resposta
A saída deve ser estruturada em formato **JSON**, exatamente assim:

[
  {
    "trecho": "...",
    "motivo": "O trecho expressa uma opinião disfarçada de fato porque ...",
    "reescrita_sugerida": "..."
  }
]

### Regras
- Ignore opiniões claramente assumidas como tais (ex: 'eu acho que', 'na minha opinião').
- Concentre-se em casos onde a **linguagem transmite certeza**, mas **a afirmativa não é objetivamente verificável**.
- Caso **nenhuma** opinião disfarçada de fato seja detectada, responda apenas:  
  `Nenhuma opinião disfarçada de fato detectada.`

### Texto-alvo
<<<{{TEXTO_ALVO}}>>>

Siga à risca o formato exigido, sem comentários extras.
"""
PROMPT_CT = """
Você é o ContrapontoGPT — um agente especializado em detectar a ausência de contrapontos relevantes em textos argumentativos, informativos ou opinativos.

### Objetivo
Analise criticamente o texto fornecido e responda:
1. Quais **pontos de vista contrários**, **dados contraditórios** ou **perspectivas alternativas relevantes** deveriam estar presentes para equilibrar a argumentação.
2. Justifique por que a ausência desses contrapontos compromete a **completude, imparcialidade ou credibilidade** do texto.
3. Sugira como os contrapontos poderiam ser **introduzidos de forma construtiva**, mantendo o tom e o foco do texto.

### Formato de saída (em JSON):

[
  {
    "tema_ausente": "...",
    "por_que_e_importante": "...",
    "como_incluir": "..."
  }
]

### Regras
- Ignore contrapontos triviais ou irrelevantes.
- Foque apenas na **ausência de perspectivas relevantes**, com impacto significativo no equilíbrio informativo.
- Caso **nenhum contraponto relevante esteja ausente**, responda exatamente:  
  `Nenhum contraponto relevante ausente identificado.`

### Texto-alvo
<<<{{TEXTO_ALVO}}>>>

Siga o formato solicitado. Não inclua comentários extras.
"""
# ─────────── EXECUÇÃO GENÉRICA ───────────
def _run(prompt_tmpl: str, texto: str) -> str:
    prompt = prompt_tmpl.replace("{{TEXTO_ALVO}}", texto)
    rsp = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return rsp.choices[0].message.content

# ─────────── SEGURANÇA NO PARSING ───────────
def primeiro_item(lst, default_keys):
    if not lst or not isinstance(lst[0], dict):
        return {k: "" for k in default_keys}
    return lst[0]

# ─────────── FUNÇÃO PRINCIPAL ───────────
def analisar_artigos(df_artigos: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame com colunas:
        Artigo | Link | Conteudo  (ou Texto)
    Retorna DataFrame final com colunas de viés / opinião / contraponto.
    """
    linhas = []
    for _, row in df_artigos.iterrows():
        titulo = row.Artigo
        texto = (row.get("Conteudo") or row.get("Texto") or "")[:25_000]

        try:
            bias = safe_json_parse(_run(PROMPT_LT, texto))
            opin = safe_json_parse(_run(PROMPT_OP, texto))
            contra = safe_json_parse(_run(PROMPT_CT, texto))
        except Exception as e:
            bias = opin = contra = [{"erro": str(e)}]

        bias0 = primeiro_item(bias,   ["trecho", "tipo", "explicacao", "reescrita_neutra"])
        opin0 = primeiro_item(opin,   ["trecho", "motivo", "reescrita_sugerida"])
        contra0 = primeiro_item(contra, ["tema_ausente", "por_que_e_importante", "como_incluir"])

        linhas.append({
            "Artigo": titulo,
            "Link": row.Link,
            "Trecho (Tendencioso)":         bias0.get("trecho", ""),
            "Tipo de Viés":                 bias0.get("tipo", ""),
            "Explicação (Viés)":            bias0.get("explicacao", ""),
            "Reescrita (Viés)":             bias0.get("reescrita_neutra", ""),
            "Trecho (Opinião disfarçada)": opin0.get("trecho", ""),
            "Motivo (Opinião)":             opin0.get("motivo", ""),
            "Reescrita (Opinião)":          opin0.get("reescrita_sugerida", ""),
            "Tema ausente":                 contra0.get("tema_ausente", ""),
            "Importância do Contraponto":   contra0.get("por_que_e_importante", ""),
            "Sugestão de Inclusão":         contra0.get("como_incluir", "")
        })

    return pd.DataFrame(linhas)
