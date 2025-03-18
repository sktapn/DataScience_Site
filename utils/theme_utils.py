import streamlit as st

def load_themes():
    """
    Carrega e retorna os temas disponíveis para o dashboard.
    
    Returns:
        dict: Dicionário contendo as configurações de cores e estilos para cada tema.
    """
    themes = {
        "profissional": {
            "primary": "#1E88E5",
            "secondary": "#0D47A1",
            "accent": "#E3F2FD",
            "background": "#F5F7FA",
            "card": "#FFFFFF",
            "text": "#212121",
            "text_secondary": "#757575",
            "success": "#4CAF50",
            "warning": "#FFC107",
            "error": "#F44336",
            "chart_palette": ["#1E88E5", "#26A69A", "#7E57C2", "#5C6BC0", "#66BB6A"]
        },
        "elegante": {
            "primary": "#6A1B9A",
            "secondary": "#4A148C",
            "accent": "#F3E5F5",
            "background": "#F8F5FD",
            "card": "#FFFFFF",
            "text": "#212121",
            "text_secondary": "#757575",
            "success": "#66BB6A",
            "warning": "#FFA726",
            "error": "#EF5350",
            "chart_palette": ["#6A1B9A", "#8E24AA", "#AB47BC", "#CE93D8", "#E1BEE7"]
        },
        "moderno": {
            "primary": "#00897B",
            "secondary": "#00695C",
            "accent": "#E0F2F1",
            "background": "#F5FFFD",
            "card": "#FFFFFF",
            "text": "#212121",
            "text_secondary": "#757575",
            "success": "#66BB6A",
            "warning": "#FFA726",
            "error": "#EF5350",
            "chart_palette": ["#00897B", "#26A69A", "#4DB6AC", "#80CBC4", "#B2DFDB"]
        }
    }
    return themes

def initialize_theme():
    """
    Inicializa o tema na sessão do Streamlit se ainda não estiver definido.
    
    Returns:
        str: O tema atual.
    """
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'profissional'
    return st.session_state['theme']

def get_current_theme():
    """
    Retorna o tema atual com base na sessão do Streamlit.
    
    Returns:
        dict: Configurações do tema atual.
    """
    themes = load_themes()
    current_theme_name = initialize_theme()
    return themes[current_theme_name]

def apply_theme_css(theme=None):
    """
    Aplica o CSS personalizado com base no tema fornecido ou no tema atual.
    
    Args:
        theme (dict, optional): Configurações do tema. Se None, usa o tema atual.
    """
    if theme is None:
        theme = get_current_theme()
    
    css = f"""
    <style>
        /* Estilos globais */
        .main {{
            background-color: {theme["background"]};
            padding: 1rem 2rem;
        }}
        .stApp {{
            background-color: {theme["background"]};
        }}
        
        /* Tipografia */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme["text"]};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 600;
        }}
        h1 {{
            font-size: 2.2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid {theme["primary"]};
            padding-bottom: 0.5rem;
        }}
        h2 {{
            font-size: 1.8rem;
            color: {theme["primary"]};
            margin-top: 1.5rem;
        }}
        h3 {{
            font-size: 1.4rem;
            color: {theme["secondary"]};
        }}
        p, li, div {{
            color: {theme["text_secondary"]};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Cards e Containers */
        .card {{
            background-color: {theme["card"]};
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            border-top: 3px solid {theme["primary"]};
        }}
        .metric-card {{
            background-color: {theme["card"]};
            border-radius: 0.5rem;
            padding: 1.2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }}
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: {theme["primary"]};
            margin: 0.5rem 0;
        }}
        .metric-title {{
            font-size: 1rem;
            color: {theme["text_secondary"]};
            margin-bottom: 0.5rem;
        }}
        
        /* Mapa */
        .map-container {{
            background-color: {theme["card"]};
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }}
        
        /* Filtros */
        .filter-container {{
            background-color: {theme["accent"]};
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        
        /* Rodapé */
        .footer {{
            text-align: center;
            padding: 1.5rem 0;
            margin-top: 3rem;
            border-top: 1px solid #eee;
            font-size: 0.9rem;
            color: {theme["text_secondary"]};
        }}
        
        /* Indicadores */
        .indicator {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 500;
            margin-right: 0.5rem;
        }}
        .indicator-up {{
            background-color: rgba(76, 175, 80, 0.2);
            color: #2E7D32;
        }}
        .indicator-down {{
            background-color: rgba(244, 67, 54, 0.2);
            color: #C62828;
        }}
        
        /* Gráficos e visualizações */
        .chart-container {{
            background-color: {theme["card"]};
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }}
        
        /* Tabelas */
        .dataframe {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 1rem;
        }}
        .dataframe th {{
            background-color: {theme["primary"]};
            color: white;
            padding: 0.75rem;
            text-align: left;
        }}
        .dataframe td {{
            padding: 0.75rem;
            border-bottom: 1px solid #eee;
        }}
        .dataframe tr:hover {{
            background-color: {theme["accent"]};
        }}
        
        /* Botões e Interações */
        .stButton>button {{
            background-color: {theme["primary"]};
            color: white;
            border-radius: 0.25rem;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {theme["secondary"]};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_sidebar_navigation():
    """
    Cria a barra lateral de navegação com links para todas as páginas.
    """
    from datetime import datetime
    
    with st.sidebar:
        # Logo
        st.image("assets/logo.png", width=150)
        st.title("Navegação")
        
        # Seletor de tema
        theme_options = {
            "profissional": "🔵 Profissional",
            "elegante": "🟣 Elegante",
            "moderno": "🟢 Moderno"
        }
        
        selected_theme = st.selectbox(
            "Escolha um tema",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(st.session_state['theme'])
        )
        
        if selected_theme != st.session_state['theme']:
            st.session_state['theme'] = selected_theme
            st.rerun()
        
        st.divider()
        
        # Links de navegação
        st.markdown("### Análises")
        st.page_link("Home.py", label="📊 Visão Geral", icon="🏠")
        st.page_link("pages/01_Análise_Regional.py", label="🗺️ Análise Regional", icon="🌎")
        st.page_link("pages/02_Indicadores_Desnutrição.py", label="🍎 Indicadores de Desnutrição", icon="📈")
        st.page_link("pages/03_Análise_Racial.py", label="👥 Análise por Raça/Etnia", icon="👪")
        
        st.divider()
        st.markdown("### Configurações")
        st.page_link("pages/04_Configurações.py", label="⚙️ Configurações", icon="⚙️")
        
        st.divider()
        st.caption(f"© {datetime.now().year} Seu Projeto")
        st.caption("Versão 1.0.0")
