# main.py
import streamlit as st
import pandas as pd

from src.wiki_fetch import buscar_artigos
from src.detector import analisar_artigos

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

# Entrada do usuário
termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
n = st.number_input("📄 Defina N", min_value=1, max_value=50, value=5)

# Botão
if st.button("Analisar"):
    with st.spinner("Buscando artigos…"):
        df = buscar_artigos(termo)

    if df.empty:
        st.warning("Nenhum artigo encontrado.")
        st.stop()

    st.success(f"{len(df)} artigos encontrados.")
    st.dataframe(df[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    df_analise = analisar_artigos(df.head(n))

    if df_analise.empty:
        st.warning("Nenhum conteúdo analisado.")
        st.stop()

    st.success("Análise concluída!")

    artigos = df_analise["Artigo"].unique()
    artigo_escolhido = st.selectbox("🔎 Selecione um artigo para ver a análise:", artigos)

    df_artigo = df_analise[df_analise["Artigo"] == artigo_escolhido]
    link = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{artigo_escolhido}]({link})", unsafe_allow_html=True)

    for _, row in df_artigo.iterrows():
        st.markdown("---")
        st.markdown(f"**Trecho tendencioso:** {row['Trecho (Tendencioso)']}")
        st.markdown(f"**Tipo de viés:** {row['Tipo de Viés']}")
        st.markdown(f"**Explicação:** {row['Explicação (Viés)']}")
