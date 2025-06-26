import wikipediaapi
import pandas as pd
from datetime import datetime

wiki = wikipediaapi.Wikipedia('pt')

def buscar_artigos(termo: str, quantidade: int = 10) -> pd.DataFrame:
    resultados = []
    for titulo in wiki.search(termo, results=quantidade):
        page = wiki.page(titulo)
        if not page.exists():
            continue
        resultados.append({
            "Artigo": page.title,
            "Link": page.fullurl,
            "data_ultima_edicao": datetime.now().date().isoformat()  # você pode ajustar isso
        })
    return pd.DataFrame(resultados)
