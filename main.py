import wikipedia
import pandas as pd
import requests
from datetime import datetime
import json

# Configuração
wikipedia.set_lang("pt")
UA = "BiasWikiDetector/1.0 (Pedro Amorim; contato: pedro@email.com)"

def get_last_edit_date(titulo):
    url = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvprop": "timestamp",
        "titles": titulo,
    }
    headers = {"User-Agent": UA}
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    data = r.json()
    page = next(iter(data["query"]["pages"].values()))
    return page["revisions"][0]["timestamp"] if "revisions" in page else None

def buscar_artigos(termo, qtd=10):
    titulos = wikipedia.search(termo, results=50)
    artigos = []

    for titulo in titulos:
        if termo.lower() not in titulo.lower():
            continue  # filtra por título contendo termo

        try:
            page = wikipedia.page(titulo)
            data_edicao = get_last_edit_date(titulo)
            artigos.append({
                "artigo": titulo,
                "link": page.url,
                "conteudo": page.content,
                "data_ultima_edicao": data_edicao
            })
        except Exception:
            continue

    df = pd.DataFrame(artigos)
    df["data_ultima_edicao"] = pd.to_datetime(df["data_ultima_edicao"])
    df = df.sort_values("data_ultima_edicao", ascending=False).head(qtd)
    return df[["artigo", "link", "data_ultima_edicao"]]
