import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Personalizando o estilo com CSS
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        color: #2d3748;
        font-weight: bold;
        margin-top: 50px;
    }
    .message {
        text-align: center;
        font-size: 20px;
        color: #4A90E2;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #8A8D92;
        margin-top: 40px;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Centralizando o título com uma fonte elegante
st.markdown('<h1 class="title">🚀 Em Breve!</h1>', unsafe_allow_html=True)

# Mensagem com estilo moderno
st.markdown('<p class="message">Nosso site está em construção! 🚧 Estamos preparando algo incrível para você. Fique ligado!</p>', unsafe_allow_html=True)

# Imagem com estilo refinado
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image(
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
    caption="Estamos trabalhando para trazer algo incrível!",
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Rodapé simples e elegante
st.markdown('<p class="footer">Siga-nos para atualizações: <br> 🌟 [GitHub](https://github.com/sktapn/DataScience_HandsON)</p>', unsafe_allow_html=True)
