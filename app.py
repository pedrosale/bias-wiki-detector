import streamlit as st, pandas as pd
from src.wiki_fetch import buscar_artigos
from src.detector import analisar_artigos

st.set_page_config(page_title="Bias Wiki Detector", layout="wide")
st.title("🧠 Bias Wiki Detector")

st.markdown("""
<div style="background-color:#f0f2f6;padding:10px;border-left:5px solid #999;">
O detector pesquisa até <b>50 artigos da Wikipédia</b> cujo título contém o termo informado, 
consulta a <i>MediaWiki&nbsp;API</i> para obter a <b>data da última edição</b> e analisa os <b>N artigos mais recentes</b>.<br>
⚠️ Se a data estiver indisponível para algum artigo, ele é listado após os que possuem data válida.
</div>

<div style="margin-top:15px;">
<a href="https://github.com/pedrosale/bias-wiki-detector/blob/main/README.md" target="_blank">
Veja aqui as definições dos tipos de viés analisados pela ferramenta</a>.
</div>
""", unsafe_allow_html=True)

# Entrada
termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
qtd = st.number_input("📄 Defina N", 1, 50, 10)

if st.button("Analisar"):
    with st.spinner("🔎 Buscando artigos…"):
        df_raw = buscar_artigos(termo)

    if df_raw.empty:
        st.warning("Nenhum artigo encontrado.")
        st.stop()

    st.success(f"{len(df_raw)} artigos encontrados.")
    st.dataframe(df_raw[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    with st.spinner("🤖 Rodando análise de viés…"):
        df_final = analisar_artigos(df_raw.head(qtd))

    if df_final.empty:
        st.warning("Nenhum viés detectado.")
        st.stop()

    st.success("Análise concluída!")

    artigos = df_final["Artigo"].unique()
    artigo_escolhido = st.selectbox("🔎 Selecione um artigo para ver a análise:", artigos)

    df_artigo = df_final[df_final["Artigo"] == artigo_escolhido]
    link = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{artigo_escolhido}]({link})", unsafe_allow_html=True)

    for _, row in df_artigo.iterrows():
        st.markdown("---")
        st.markdown(f"**Trecho tendencioso:** {row['Trecho (Tendencioso)']}")
        st.markdown(f"**Tipo de viés:** {row['Tipo de Viés']}")
        st.markdown(f"**Explicação:** {row['Explicação (Viés)']}")
