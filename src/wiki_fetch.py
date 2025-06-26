import wikipedia
import pandas as pd

def buscar_artigos(termo, quantidade=5):
    wikipedia.set_lang("pt")
    titulos = wikipedia.search(termo, results=quantidade)

    artigos = []
    for titulo in titulos:
        try:
            pagina = wikipedia.page(titulo)
            artigos.append({
                "Artigo": titulo,
                "Texto": pagina.content,
                "Link": pagina.url,
                "data_ultima_edicao": "",  # a API não retorna isso
            })
        except Exception as e:
            print(f"Erro ao buscar página {titulo}: {e}")
            continue

    return pd.DataFrame(artigos)
