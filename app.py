import streamlit as st, pandas as pd
from src.wiki_fetch import buscar_artigos
from src.detector import analisar_artigos

st.set_page_config(page_title="Bias Wiki Detector", layout="wide")
st.title("🧠 Bias Wiki Detector")
st.markdown("""
<div style="background-color: #f0f2f6; padding: 10px; border-left: 5px solid #999;">
🔍 Este detector busca até <b>50 artigos da Wikipedia</b> relacionados ao termo informado e analisa os <b>N primeiros da lista</b> retornada.  
⚠️ A ordem dos artigos pode não refletir os mais recentes, pois a Wikipedia API pública não fornece a data de edição diretamente.
</div>
""", unsafe_allow_html=True)


termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
qtd   = st.number_input("📄 Artigos mais recentes", 1, 50, 10)
executar = st.button("Analisar")

if executar:
    with st.spinner("🔎 Buscando artigos…"):
        df_raw = buscar_artigos(termo, qtd)

    if df_raw.empty:
        st.warning("Nenhum artigo encontrado com esse termo no título.")
        st.stop()

    st.success(f"{len(df_raw)} artigos encontrados.")
    st.dataframe(df_raw[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    with st.spinner("🤖 Rodando análise de viés (OpenAI)…"):
        df_final = analisar_artigos(df_raw)

    st.success("Análise concluída!")
    st.dataframe(df_final, use_container_width=True)

    csv = df_final.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv, "bias_report.csv", mime="text/csv")
