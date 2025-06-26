# src/wiki_fetch.py

import wikipedia
import pandas as pd
import requests
from time import sleep
from urllib.parse import quote

# --- Configuração ---
wikipedia.set_lang("pt")
UA = "BiasWikiDetector/1.0 (Pedro Amorim; contato: pedro@email.com)"

def buscar_artigos(termo: str, max_art=50):
    """Busca artigos da Wikipedia em português cujo título contém exatamente o termo informado."""
    
    titulos_brutos = wikipedia.search(termo, results=max_art)
    titulos = [t for t in titulos_brutos if termo.lower() in t.lower()]

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
        except Exception as e:
            print(f"⚠️ Erro ao buscar data de '{titulo}': {e}")
            return None

    artigos = []
    for titulo in titulos:
        try:
            page = wikipedia.page(title=titulo, auto_suggest=False, redirect=False)
            data_edicao = get_last_edit_date(titulo)
            link_corrigido = f"https://pt.wikipedia.org/wiki/{quote(page.title)}"

            artigos.append({
                "Artigo": page.title,  # usa o título real para evitar redirecionamento
                "Link": link_corrigido,
                "Conteudo": page.content,
                "data_ultima_edicao": data_edicao
            })
            sleep(0.2)
        except Exception as e:
            print(f"❌ Falha em '{titulo}': {e}")

    df = pd.DataFrame(artigos)
    df["data_ultima_edicao"] = pd.to_datetime(df["data_ultima_edicao"])
    df = df.sort_values("data_ultima_edicao", ascending=False)
    return df
