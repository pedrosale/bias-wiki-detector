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

# Campos de entrada
termo = st.text_input("🔍 Termo de busca", value="inteligência artificial")
qtd   = st.number_input("📄 Defina N", 1, 50, 10)
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
        df_final = analisar_artigos(df_raw.head(qtd))

    st.success("Análise concluída!")

    artigos_unicos = df_final["Artigo"].unique()
    escolhido = st.selectbox("🔎 Selecione um artigo para ver a análise completa:", artigos_unicos)

    df_artigo = df_final[df_final["Artigo"] == escolhido]
    link = df_artigo["Link"].iloc[0]
    st.markdown(f"### 📄 [{escolhido}]({link})", unsafe_allow_html=True)

    for _, row in df_artigo.iterrows():
        st.markdown("---")

        # 🔹 1. Tendencioso
        if row["Trecho (Tendencioso)"]:
            st.markdown("#### 🎯 Viés tendencioso")
            st.markdown(f"- **Trecho:** {row['Trecho (Tendencioso)']}")
            st.markdown(f"- **Tipo:** {row['Tipo de Viés']}")
            st.markdown(f"- **Explicação:** {row['Explicação (Viés)']}")
            st.markdown(f"- **Reescrita sugerida:** {row['Reescrita (Viés)']}")

        # 🔹 2. Opinião disfarçada
        if row["Trecho (Opinião disfarçada)"]:
            st.markdown("#### 💬 Opinião disfarçada")
            st.markdown(f"- **Trecho:** {row['Trecho (Opinião disfarçada)']}")
            st.markdown(f"- **Motivo:** {row['Motivo (Opinião)']}")
            st.markdown(f"- **Reescrita sugerida:** {row['Reescrita (Opinião)']}")

        # 🔹 3. Contraponto ausente
        if row["Tema ausente"]:
            st.markdown("#### ⚖️ Contraponto ausente")
            st.markdown(f"- **Tema ausente:** {row['Tema ausente']}")
            st.markdown(f"- **Importância:** {row['Importância do Contraponto']}")
            st.markdown(f"- **Como incluir:** {row['Sugestão de Inclusão']}")

    # Botão de download
    csv = df_final.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv, "bias_report.csv", mime="text/csv")
