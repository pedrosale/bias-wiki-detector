import streamlit as st
from main import buscar_artigos

st.set_page_config(page_title="Bias Wiki Detector", layout="wide")

st.title("🧠 Bias Wiki Detector")
st.markdown("Pesquise artigos recentes da Wikipedia contendo o termo desejado.")

# Entrada do usuário
termo = st.text_input("🔍 Termo de busca:", value="inteligência artificial")
qtd = st.number_input("📄 Quantidade de artigos mais recentes:", min_value=1, max_value=50, value=10)

# Botão de execução
if st.button("🔎 Buscar artigos"):
    with st.spinner("Buscando artigos..."):
        df = buscar_artigos(termo, qtd)
        if not df.empty:
            st.success(f"{len(df)} artigos encontrados.")
            st.dataframe(df.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Nenhum artigo encontrado com esse termo no título.")
