import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="centered"
)

# Estilo personalizado
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        color: #333;
    }
    
    .title {
        text-align: center;
        font-size: 60px;
        color: #ff6f61;
        font-weight: 700;
        letter-spacing: 3px;
        margin-top: 100px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }

    .message {
        text-align: center;
        font-size: 24px;
        color: #444;
        margin-top: 20px;
        line-height: 1.6;
        font-weight: 400;
    }

    .image-container {
        display: flex;
        justify-content: center;
        margin-top: 50px;
    }

    .footer {
        text-align: center;
        font-size: 16px;
        color: #666;
        margin-top: 60px;
    }

    .footer a {
        text-decoration: none;
        color: #ff6f61;
        font-weight: 500;
    }

    </style>
    """, unsafe_allow_html=True
)

# Título estilizado
st.markdown('<h1 class="title">🚀 Em Breve!</h1>', unsafe_allow_html=True)

# Mensagem estilizada
st.markdown('<p class="message">Nosso site está em construção! Estamos preparando algo incrível para você. Fique ligado, o melhor está por vir! 🚧</p>', unsafe_allow_html=True)

# Imagem centralizada com estilo
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image(
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
    caption="Estamos trabalhando para trazer algo incrível!",
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Rodapé com links modernos e chamativos
st.markdown('<p class="footer">Fique conectado para mais atualizações: <br> 🌟 [GitHub](https://github.com/sktapn/DataScience_HandsON)</p>', unsafe_allow_html=True)
