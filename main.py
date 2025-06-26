# main.py
import streamlit as st
import pandas as pd

from src.wiki_fetch import buscar_artigos
from src.detector import analisar_artigos

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(page_title="Bias Wiki Detector", layout="wide")
st.title("🧠 Bias Wiki Detector")

st.markdown(
    """
<div style="background-color:#f0f2f6;padding:10px;border-left:5px solid #999;">
O detector pesquisa até <b>50 artigos da Wikipédia</b> cujo título contém o termo informado, 
consulta a <i>MediaWiki&nbsp;API</i> para obter a <b>data da última edição</b> e analisa os <b>N artigos mais recentes</b>.<br>
⚠️ Se a data estiver indisponível para algum artigo, ele é listado após os que possuem data válida.
</div>

<div style="margin-top:12px;">
🔗 <a href="https://github.com/pedrosale/bias-wiki-detector/blob/main/README.md" target="_blank">
Veja aqui a definição completa dos tipos de viés analisados</a>.
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Entrada do usuário
# ─────────────────────────────────────────────
termo_busca = st.text_input("🔍 Termo de busca", value="inteligência artificial")
n_artigos   = st.number_input("📄 Defina N", min_value=1, max_value=50, value=5)

# ─────────────────────────────────────────────
# Botão de execução
# ─────────────────────────────────────────────
if st.button("Analisar"):
    with st.spinner("🔎 Buscando artigos…"):
        df_raw = buscar_artigos(termo_busca)
    if df_raw.empty:
        st.warning("Nenhum artigo encontrado.")
        st.stop()

    st.success(f"{len(df_raw)} artigos encontrados.")
    st.dataframe(df_raw[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    # Limita aos N mais recentes escolhidos
    df_analise = analisar_artigos(df_raw.head(n_artigos))

    if df_analise.empty:
        st.warning("Não foi possível analisar os artigos.")
        st.stop()

    st.success("Análise concluída!")

    # ─────────── Seletor de artigo ───────────
    artigo_escolhido = st.selectbox(
        "🔎 Selecione um artigo para ver a análise completa:",
        df_analise["Artigo"].unique(),
    )

    df_artigo = df_analise[df_analise["Artigo"] == artigo_escolhido]

    # Cabeçalho com link clicável
    link_artigo = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{artigo_escolhido}]({link_artigo})", unsafe_allow_html=True)

    # Exibe cada bloco de viés / opinião / contraponto
    for _, row in df_artigo.iterrows():
        st.markdown("---")
        st.markdown(f"**Trecho tendencioso:** {row['Trecho (Tendencioso)']}")
        st.markdown(f"**Tipo de viés:** {row['Tipo de Viés']}")
        st.markdown(f"**Explicação:** {row['Explicação (Viés)']}")

        # Caso existam colunas extras, exiba condicionalmente
        if row.get("Trecho (Opinião disfarçada)", ""):
            st.markdown(f"**Trecho – Opinião disfarçada:** {row['Trecho (Opinião disfarçada)']}")
            st.markdown(f"**Motivo:** {row['Motivo (Opinião)']}")
            st.markdown(f"**Reescrita sugerida:** {row['Reescrita (Opinião)']}")

        if row.get("Tema ausente", ""):
            st.markdown(f"**Tema ausente:** {row['Tema ausente']}")
            st.markdown(f"**Importância do contraponto:** {row['Importância do Contraponto']}")
            st.markdown(f"**Como incluir:** {row['Sugestão de Inclusão']}")

    # Opcional: download do CSV filtrado
    csv_bytes = df_analise.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar CSV completo",
        csv_bytes,
        "bias_wiki_report.csv",
        mime="text/csv",
    )
