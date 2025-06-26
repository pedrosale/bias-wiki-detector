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

<div style="margin-top:15px; margin-bottom:20px;">
<a href="https://github.com/pedrosale/bias-wiki-detector/blob/main/README.md" target="_blank">
Veja aqui as definições dos tipos de viés analisados pela ferramenta</a>.
</div>



# Entrada
termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
qtd   = st.number_input("📄 Defina N", 1, 50, 3)
executar = st.button("Analisar")

# Rodar análise ou reutilizar cache
if "df_final" not in st.session_state or executar:
    with st.spinner("🔎 Buscando artigos…"):
        df_raw = buscar_artigos(termo, qtd)

    if df_raw.empty:
        st.warning("Nenhum artigo encontrado com esse termo no título.")
        st.stop()

    st.success(f"{len(df_raw)} artigos encontrados.")
    st.dataframe(df_raw[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    with st.spinner("🤖 Rodando análise de viés (OpenAI)…"):
        df_final = analisar_artigos(df_raw.head(qtd))

    st.session_state.df_final = df_final
    st.session_state.df_raw = df_raw

# Exibir resultado
if "df_final" in st.session_state:
    df_final = st.session_state.df_final
    df_raw = st.session_state.df_raw

    st.success("Análise concluída!")

    artigos = df_final["Artigo"].unique()
    escolhido = st.selectbox("🔎 Selecione um artigo para ver a análise completa:", artigos)

    df_artigo = df_final[df_final["Artigo"] == escolhido]
    link = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{escolhido}]({link})", unsafe_allow_html=True)

    for _, row in df_artigo.iterrows():
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**🟥 Trecho (Tendencioso)**")
            st.markdown(row.get("Trecho (Tendencioso)", ""))
            st.markdown("**🟧 Opinião Disfarçada**")
            st.markdown(row.get("Trecho (Opinião disfarçada)", ""))
            st.markdown("**🟨 Tema Ausente**")
            st.markdown(row.get("Tema ausente", ""))
        with col2:
            st.markdown("**Tipo de Viés:** " + row.get("Tipo de Viés", ""))
            st.markdown("**Explicação (Viés):** " + row.get("Explicação (Viés)", ""))
            st.markdown("**Reescrita (Viés):** " + row.get("Reescrita (Viés)", ""))
            st.markdown("**Motivo (Opinião):** " + row.get("Motivo (Opinião)", ""))
            st.markdown("**Reescrita (Opinião):** " + row.get("Reescrita (Opinião)", ""))
            st.markdown("**Importância do Contraponto:** " + row.get("Importância do Contraponto", ""))
            st.markdown("**Sugestão de Inclusão:** " + row.get("Sugestão de Inclusão", ""))

    csv = df_final.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv, "bias_report.csv", mime="text/csv")
