import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Espaçamento inicial
st.write("\n")

# Título
st.title("🚀 Em Breve!")

# Mensagem centralizada
st.write(
    """
    Nosso site está em construção e estará disponível em breve! 🚧  
    """
)

# Espaçamento
st.write("\n")

# Centralizar imagem
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
        caption="Estamos trabalhando para trazer algo incrível!",
        use_column_width=True
    )

# Rodapé com link
st.markdown(
    """
    ---
    ### Siga-nos para atualizações:  
    - 🌟 [GitHub](https://github.com/sktapn/DataScience_HandsON)
    """
)
