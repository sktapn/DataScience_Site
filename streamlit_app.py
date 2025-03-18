import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io

# Configuração da página
st.set_page_config(
    page_title="Explorando Dados com Charme ✨",
    page_icon="✨",
    layout="wide"
)

# Estilização CSS personalizada
st.markdown("""
<style>
    .main {
        background-color: #f8e6ff;
        padding: 2rem;
    }
    .stApp {
        background-color: #f8e6ff;
    }
    h1, h2, h3 {
        color: #ff7e67;
    }
    .stButton>button {
        background-color: #ff7e67;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #ff6b52;
    }
    .card {
        background-color: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .upload-box {
        border: 2px dashed #ff7e67;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .stat-box {
        background-color: #fff5f3;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #666;
        margin-top: 2rem;
        border-top: 1px dashed #ff7e67;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown("<h1 style='text-align: center;'>Explorando Dados com Charme ✨</h1>", unsafe_allow_html=True)
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
                    color_discrete_sequence=['#ff7e67']
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
                
                fig = px.pie(
                    values=counts.values, 
                    names=counts.index,
                    color_discrete_sequence=['#ff7e67', '#ffb347', '#9ee7e3', '#a992fa', '#ff9cee']
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
                    color_discrete_sequence=['#ff7e67']
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
                st.markdown("❤️", unsafe_allow_html=True)
                st.markdown("<h3>Média</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: #ff7e67;'>{df[num_col].mean():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with stat_cols[1]:
                st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
                st.markdown("⭐", unsafe_allow_html=True)
                st.markdown("<h3>Mediana</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: #ff7e67;'>{df[num_col].median():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with stat_cols[2]:
                st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
                st.markdown("❤️", unsafe_allow_html=True)
                st.markdown("<h3>Máximo</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: #ff7e67;'>{df[num_col].max():.2f}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Rodapé
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("<p>Obrigado por explorar comigo! Feito com carinho ❤️</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
