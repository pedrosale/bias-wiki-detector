# src/wiki_fetch.py

import wikipedia
import pandas as pd
import requests
from time import sleep

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
    try:
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        data = r.json()
        page = next(iter(data["query"]["pages"].values()))
        return page["revisions"][0]["timestamp"] if "revisions" in page else None
    except Exception:
        return None

def buscar_artigos(termo: str, quantidade: int = 10) -> pd.DataFrame:
    titulos_brutos = wikipedia.search(termo, results=50)
    titulos = [t for t in titulos_brutos if termo.lower() in t.lower()]

    artigos = []
    for titulo in titulos:
        try:
            page = wikipedia.page(titulo)
            data_edicao = get_last_edit_date(titulo)
            artigos.append({
                "Artigo": titulo,
                "Link": page.url,
                "Conteudo": page.content,
                "data_ultima_edicao": data_edicao
            })
            sleep(0.2)
        except Exception:
            continue

    df = pd.DataFrame(artigos)
    df["data_ultima_edicao"] = pd.to_datetime(df["data_ultima_edicao"])
    df = df.sort_values("data_ultima_edicao", ascending=False)
    return df.head(quantidade)
