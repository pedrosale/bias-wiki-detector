import streamlit as st
import pandas as pd
from src.wiki_fetch import buscar_artigos
from src.detector import analisar_artigos
from utils import gerar_pdf          # ⬅️ NOVO: função que cria o PDF

# ─────────────────────────  CONFIGURAÇÃO  ─────────────────────────
st.set_page_config(page_title="Bias Wiki Detector", layout="wide")
st.title("🧠 Bias Wiki Detector")

st.markdown("""
<div style="background-color:#f0f2f6;padding:10px;border-left:5px solid #999;">
O detector pesquisa até <b>50 artigos da Wikipédia</b> cujo título contém <i>todos</i> os termos digitados, 
consulta a <i>MediaWiki&nbsp;API</i> para obter a <b>data da última edição</b> e analisa os <b>N artigos mais recentes</b>.
<br>⚠️ Artigos sem data são listados depois dos que têm data válida.
</div>

<div style="margin:18px 0 30px;">
<a href="https://github.com/pedrosale/bias-wiki-detector/blob/main/README.md" target="_blank">
📘 Definições dos tipos de viés analisados</a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────  ENTRADAS  ─────────────────────────
termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
n     = st.number_input("📄 N artigos recentes", 1, 50, 3)
executar = st.button("Analisar")

# ─────────────────────────  PROCESSAMENTO  ─────────────────────────
if "df_final" not in st.session_state or executar:
    with st.spinner("🔎 Buscando artigos…"):
        df_raw = buscar_artigos(termo, 50)

    if df_raw.empty:
        st.warning("Nenhum artigo encontrado.")
        st.stop()

    # Mantém apenas os N mais recentes
    df_raw_n = df_raw.head(n)
    st.success(f"{len(df_raw_n)} artigos selecionados para análise.")
    st.dataframe(df_raw_n[["Artigo", "Link", "data_ultima_edicao"]], use_container_width=True)

    with st.spinner("🤖 Rodando análise de viés…"):
        df_final = analisar_artigos(df_raw_n)

    # Guarda no session_state
    st.session_state.df_raw  = df_raw_n
    st.session_state.df_final = df_final

# ─────────────────────────  EXIBIÇÃO  ─────────────────────────
if "df_final" in st.session_state:

    df_raw  = st.session_state.df_raw
    df_final = st.session_state.df_final

    artigos = df_final["Artigo"].unique()
    escolhido = st.selectbox("📑 Selecione um artigo:", artigos)

    df_artigo = df_final[df_final["Artigo"] == escolhido]
    link      = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{escolhido}]({link})", unsafe_allow_html=True)

    # Blocos de viés
    for _, row in df_artigo.iterrows():
        st.markdown("---")

        with st.expander("🔴 Viés Tendencioso"):
            st.markdown(f"**Trecho:** {row.get('Trecho (Tendencioso)', '')}")
            st.markdown(f"**Tipo:** {row.get('Tipo de Viés', '')}")
            st.markdown(f"**Explicação:** {row.get('Explicação (Viés)', '')}")
            st.markdown(f"**Reescrita:** {row.get('Reescrita (Viés)', '')}")

        with st.expander("🟠 Opinião Disfarçada"):
            st.markdown(f"**Trecho:** {row.get('Trecho (Opinião disfarçada)', '')}")
            st.markdown(f"**Motivo:** {row.get('Motivo (Opinião)', '')}")
            st.markdown(f"**Reescrita:** {row.get('Reescrita (Opinião)', '')}")

        with st.expander("🟡 Ausência de Contraponto"):
            st.markdown(f"**Tema Ausente:** {row.get('Tema ausente', '')}")
            st.markdown(f"**Importância:** {row.get('Importância do Contraponto', '')}")
            st.markdown(f"**Sugestão de Inclusão:** {row.get('Sugestão de Inclusão', '')}")

    # ─────────  DOWNLOAD CSV  ─────────
    csv = df_final.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv, "bias_report.csv", mime="text/csv")

    # ─────────  DOWNLOAD PDF  ─────────
    if st.button("📄 Gerar PDF deste artigo"):
        caminho_pdf = gerar_pdf(df_artigo, escolhido)
        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="⬇️ Baixar PDF",
                data=f,
                file_name=f"{escolhido}.pdf",
                mime="application/pdf"
            )
