import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Centralizar apenas o título
st.markdown(
    """
    <h1 style="text-align: center;">🚀 Em Breve!</h1>
    """, 
    unsafe_allow_html=True
)

# Mensagem
st.write(
    """
    Nosso site está em construção e estará disponível em breve! 🚧  
    Estamos trabalhando para trazer algo incrível para você. Fique ligado! 🔧✨
    """
)

# Imagem ou GIF
st.image(
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
    caption="Estamos trabalhando para trazer algo incrível!",
    use_container_width=True
)

# Rodapé com link
st.markdown(
    """
    ---
    ### Siga-nos para atualizações:  
    - 🌟 [GitHub](https://github.com/sktapn/DataScience_HandsON)
    """
)
