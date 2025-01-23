import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Título
st.title("🚀 Em Breve!")

# Mensagem
st.write(
    """
    Nosso site está em construção e estará disponível em breve! 🚧
    """
)

# Imagem ou GIF opcional
st.image(
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
    caption="Estamos trabalhando para trazer algo incrível!",
    use_column_width=True
)

# Rodapé
st.markdown(
    """
    ---
    Siga-nos para atualizações:  
    - [Github](https://github.com/sktapn/DataScience_HandsON)  
    """
)
