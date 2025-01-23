import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Centralizar conteúdo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Título centralizado
    st.title("🚀 Em Breve!")
    
    # Mensagem centralizada
    st.write(
        """
        Nosso site está em construção! 🚧  
        """
    )
    
    # Imagem centralizada
    st.image(
        "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
        caption="Estamos trabalhando para trazer algo incrível!",
        use_container_width=True
    )


