import wikipedia
import pandas as pd
import requests
from time import sleep

# Configurações
wikipedia.set_lang("pt")
UA = "BiasWikiDetector/1.0 (Pedro Amorim; contato: pedro@email.com)"

def _get_last_edit_date(titulo):
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

def buscar_artigos(termo, quantidade=5):
    titulos_raw = wikipedia.search(termo, results=50)  # busca até 50
    titulos = [t for t in titulos_raw if termo.lower() in t.lower()]
    artigos = []

    for titulo in titulos:
        try:
            pagina = wikipedia.page(titulo)
            data_edicao = _get_last_edit_date(titulo)
            artigos.append({
                "Artigo": titulo,
                "Conteudo": pagina.content,
                "Link": pagina.url,
                "data_ultima_edicao": data_edicao or "Indisponível"
            })
            sleep(0.2)  # respeita a API
        except Exception as e:
            print(f"❌ Falha em '{titulo}': {e}")

    df = pd.DataFrame(artigos)
    df["data_ultima_edicao"] = pd.to_datetime(df["data_ultima_edicao"], errors="coerce")
    df = df.sort_values("data_ultima_edicao", ascending=False)

    return df.head(quantidade)
