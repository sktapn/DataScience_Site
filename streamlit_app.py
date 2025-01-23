import streamlit as st

# Configurar a página
st.set_page_config(
    page_title="Em Breve!",
    page_icon="🚧",
    layout="wide"
)

# Adicionando estilo moderno
st.markdown(
    """
    <style>
    body {
        background-color: #f7f7f7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .title {
        text-align: center;
        font-size: 50px;
        color: #2a9d8f;
        font-weight: 600;
        letter-spacing: 2px;
        margin-top: 100px;
    }
    
    .message {
        text-align: center;
        font-size: 22px;
        color: #264653;
        margin-top: 20px;
        line-height: 1.6;
    }

    .image-container {
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }

    .footer {
        text-align: center;
        font-size: 16px;
        color: #8d99ae;
        margin-top: 60px;
    }

    .footer a {
        text-decoration: none;
        color: #2a9d8f;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True
)

# Título criativo com uma tipografia arrojada
st.markdown('<h1 class="title">🚀 Em Breve!</h1>', unsafe_allow_html=True)

# Mensagem profissional e detalhada
st.markdown('<p class="message">Nosso site está em construção! Estamos preparando algo exclusivo para você. Fique ligado para as novidades mais incríveis em breve! 🚧</p>', unsafe_allow_html=True)

# Imagem centralizada com efeito clean
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image(
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif", 
    caption="Estamos trabalhando para trazer algo incrível!",
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Rodapé com links modernos e simples
st.markdown('<p class="footer">Fique conectado para mais atualizações: <br> 🌟 [GitHub](https://github.com/sktapn/DataScience_HandsON)</p>', unsafe_allow_html=True)
