import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io

# Definição dos temas de cores
THEMES = {
    "oceano": {
        "primary": "#3498db",
        "secondary": "#2980b9",
        "accent": "#e8f4f8",
        "background": "#eaf6ff",
        "text": "#2c3e50",
        "emoji": "🌊"
    },
    "floresta": {
        "primary": "#27ae60",
        "secondary": "#2ecc71",
        "accent": "#e8f8ef",
        "background": "#e6f7ee",
        "text": "#1e3a2b",
        "emoji": "🌿"
    },
    "lavanda": {
        "primary": "#9b59b6",
        "secondary": "#8e44ad",
        "accent": "#f5eef8",
        "background": "#f0e6f6",
        "text": "#4a235a",
        "emoji": "💜"
    },
    "sol": {
        "primary": "#f39c12",
        "secondary": "#f1c40f",
        "accent": "#fef9e7",
        "background": "#fff8e1",
        "text": "#7d6608",
        "emoji": "☀️"
    }
}

# Configuração da página
st.set_page_config(
    page_title="Explorando Dados com Charme ✨",
    page_icon="✨",
    layout="wide"
)

# Função para aplicar o tema selecionado
def apply_theme(theme_name):
    theme = THEMES[theme_name]
    
    # CSS personalizado baseado no tema
    st.markdown(f"""
    <style>
        .main {{
            background-color: {theme["background"]};
            padding: 2rem;
        }}
        .stApp {{
            background-color: {theme["background"]};
        }}
        h1, h2, h3 {{
            color: {theme["primary"]};
        }}
        .stButton>button {{
            background-color: {theme["primary"]};
            color: white;
            border-radius: 0.5rem;
            border: none;
            padding: 0.5rem 1rem;
        }}
        .stButton>button:hover {{
            background-color: {theme["secondary"]};
        }}
        .card {{
            background-color: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            border-top: 4px solid {theme["primary"]};
        }}
        .upload-box {{
            border: 2px dashed {theme["primary"]};
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
        }}
        .stat-box {{
            background-color: {theme["accent"]};
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
            margin: 0.5rem;
            border-left: 4px solid {theme["primary"]};
        }}
        .footer {{
            text-align: center;
            color: {theme["text"]};
            margin-top: 2rem;
            border-top: 1px dashed {theme["primary"]};
            padding-top: 1rem;
        }}
        .theme-selector {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .theme-button {{
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .theme-button:hover {{
            transform: scale(1.1);
        }}
        .theme-button.active {{
            border: 2px solid {theme["primary"]};
            transform: scale(1.1);
        }}
        .oceano-theme {{
            background-color: {THEMES["oceano"]["primary"]};
        }}
        .floresta-theme {{
            background-color: {THEMES["floresta"]["primary"]};
        }}
        .lavanda-theme {{
            background-color: {THEMES["lavanda"]["primary"]};
        }}
        .sol-theme {{
            background-color: {THEMES["sol"]["primary"]};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    return theme

# Inicializar o tema na sessão se não existir
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'oceano'

# Aplicar o tema atual
current_theme = apply_theme(st.session_state['theme'])

# Seletor de temas
st.markdown("""
<div class="theme-selector">
    <div class="theme-button oceano-theme" onclick="window.parent.postMessage({type: 'theme', theme: 'oceano'}, '*')" title="Tema Oceano"></div>
    <div class="theme-button floresta-theme" onclick="window.parent.postMessage({type: 'theme', theme: 'floresta'}, '*')" title="Tema Floresta"></div>
    <div class="theme-button lavanda-theme" onclick="window.parent.postMessage({type: 'theme', theme: 'lavanda'}, '*')" title="Tema Lavanda"></div>
    <div class="theme-button sol-theme" onclick="window.parent.postMessage({type: 'theme', theme: 'sol'}, '*')" title="Tema Sol"></div>
</div>
""", unsafe_allow_html=True)

# JavaScript para capturar a mudança de tema
st.markdown("""
<script>
window.addEventListener('message', function(e) {
    if (e.data.type === 'theme') {
        window.location.href = window.location.pathname + '?theme=' + e.data.theme;
    }
});
</script>
""", unsafe_allow_html=True)

# Verificar parâmetros de URL para tema
query_params = st.experimental_get_query_params()
if 'theme' in query_params and query_params['theme'][0] in THEMES:
    st.session_state['theme'] = query_params['theme'][0]
    current_theme = apply_theme(st.session_state['theme'])

# Cabeçalho principal
st.markdown(f"<h1 style='text-align: center;'>Explorando Dados com Charme {current_theme['emoji']}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Bem-vindo à sua Jornada de Dados!</p>", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([1, 3])

# Sidebar (coluna 1)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Controles Mágicos ✨</h3>", unsafe_allow_html=True)
    
    # Variáveis para os filtros
    colunas = ["Selecione uma coluna", "Idade", "Renda", "Região"]
    coluna_selecionada = st.selectbox("Escolha sua variável mágica ✨", colunas, disabled=not 'df' in st.session_state)
    
    st.markdown("<p style='margin-top: 1rem;'>Que tal um gráfico encantado? 🌈</p>", unsafe_allow_html=True)
    tipo_grafico = st.radio("", ["Barras", "Pizza", "Dispersão"], horizontal=True)
    
    st.markdown("<p style='margin-top: 1rem;'>Ajuste a magia 🪄</p>", unsafe_allow_html=True)
    ajuste = st.slider("", 0, 100, 50, disabled=not 'df' in st.session_state)
    
    gerar_btn = st.button("Gerar Gráfico Mágico ✨", disabled=not 'df' in st.session_state)
    st.markdown("</div>", unsafe_allow_html=True)

# Conteúdo principal (coluna 2)
with col2:
    # Seção de upload
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Carregue seus dados aqui e vamos explorá-los juntos!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Arraste e solte um arquivo CSV ou Excel</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv", "xlsx", "xls"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Carregar os dados
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state['df'] = df
            st.success("Arquivo carregado com sucesso! ✅")
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Visualização dos dados
    if 'df' in st.session_state:
        df = st.session_state['df']
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2>Olha só que lindo ficou! 🌟</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666;'>Visualização baseada nos dados carregados</p>", unsafe_allow_html=True)
        
        # Criar gráfico com base na seleção
        if tipo_grafico == "Barras":
            if len(df.columns) > 0:
                fig = px.bar(
                    df.head(5), 
                    x=df.columns[0], 
                    y=df.columns[1] if len(df.columns) > 1 else df.columns[0],
                    color_discrete_sequence=[current_theme["primary"]]
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif tipo_grafico == "Pizza":
            if len(df.columns) > 0:
                # Usar a primeira coluna categórica se disponível
                cat_col = df.select_dtypes(include=['object']).columns[0] if len(df.select_dtypes(include=['object']).columns) > 0 else df.columns[0]
                counts = df[cat_col].value_counts().head(5)
                
                # Criar uma paleta de cores baseada no tema atual
                colors = [
                    current_theme["primary"],
                    current_theme["secondary"],
                    "#74b9ff",  # Variação mais clara
                    "#0984e3",  # Variação mais escura
                    "#dff9fb"   # Variação muito clara
                ]
                
                fig = px.pie(
                    values=counts.values, 
                    names=counts.index,
                    color_discrete_sequence=colors
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
        
        else:  # Dispersão
            if len(df.columns) > 1:
                fig = px.scatter(
                    df.head(50), 
                    x=df.columns[0], 
                    y=df.columns[1],
                    color_discrete_sequence=[current_theme["primary"]]
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resumo dos dados
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2>Resumo dos Dados Encantados 📊</h2>", unsafe_allow_html=True)
        
        # Criar layout para as estatísticas
        stat_cols = st.columns(3)
        
        # Selecionar uma coluna numérica para estatísticas
        num_col = df.select_dtypes(include=['number']).columns[0] if len(df.select_dtypes(include=['number']).columns) > 0 else None
        
        if num_col is not None:
            with stat_cols[0]:
                st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
                st.markdown(f"{current_theme['emoji']}", unsafe_allow_html=True)
                st.markdown("<h3>Média</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: {current_theme['primary']};'>{df[num_col].mean():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with stat_cols[1]:
                st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
                st.markdown("⭐", unsafe_allow_html=True)
                st.markdown("<h3>Mediana</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: {current_theme['primary']};'>{df[num_col].median():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with stat_cols[2]:
                st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
                st.markdown(f"{current_theme['emoji']}", unsafe_allow_html=True)
                st.markdown("<h3>Máximo</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: {current_theme['primary']};'>{df[num_col].max():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Rodapé
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown(f"<p>Obrigado por explorar comigo! Feito com carinho {current_theme['emoji']}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
