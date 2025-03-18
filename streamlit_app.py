import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import json
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise Social",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar utilitários de tema
def load_themes():
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

# Inicializar tema na sessão
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'profissional'

# Carregar temas
themes = load_themes()
current_theme = themes[st.session_state['theme']]

# Aplicar CSS personalizado
st.markdown(f"""
<style>
    /* Estilos globais */
    .main {{
        background-color: {current_theme["background"]};
        padding: 1rem 2rem;
    }}
    .stApp {{
        background-color: {current_theme["background"]};
    }}
    
    /* Tipografia */
    h1, h2, h3, h4, h5, h6 {{
        color: {current_theme["text"]};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }}
    h1 {{
        font-size: 2.2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid {current_theme["primary"]};
        padding-bottom: 0.5rem;
    }}
    h2 {{
        font-size: 1.8rem;
        color: {current_theme["primary"]};
        margin-top: 1.5rem;
    }}
    h3 {{
        font-size: 1.4rem;
        color: {current_theme["secondary"]};
    }}
    p, li, div {{
        color: {current_theme["text_secondary"]};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Cards e Containers */
    .card {{
        background-color: {current_theme["card"]};
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border-top: 3px solid {current_theme["primary"]};
    }}
    .metric-card {{
        background-color: {current_theme["card"]};
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
        color: {current_theme["primary"]};
        margin: 0.5rem 0;
    }}
    .metric-title {{
        font-size: 1rem;
        color: {current_theme["text_secondary"]};
        margin-bottom: 0.5rem;
    }}
    
    /* Botões e Interações */
    .stButton>button {{
        background-color: {current_theme["primary"]};
        color: white;
        border-radius: 0.25rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {current_theme["secondary"]};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {{
        background-color: {current_theme["card"]};
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 3rem;
        white-space: pre-wrap;
        background-color: {current_theme["accent"]};
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {current_theme["primary"]};
        color: white;
    }}
    
    /* Cabeçalho da página */
    .page-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eee;
    }}
    .page-title {{
        font-size: 2rem;
        font-weight: bold;
        color: {current_theme["primary"]};
        margin: 0;
    }}
    
    /* Rodapé */
    .footer {{
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 3rem;
        border-top: 1px solid #eee;
        font-size: 0.9rem;
        color: {current_theme["text_secondary"]};
    }}
    
    /* Indicadores e badges */
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
    
    /* Filtros */
    .filter-container {{
        background-color: {current_theme["accent"]};
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* Animações */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    .animate-fade-in {{
        animation: fadeIn 0.5s ease-in-out;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar para navegação e configurações
with st.sidebar:
    st.image("https://via.placeholder.com/150x80?text=LOGO", width=150)
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

# Função para carregar dados de exemplo
@st.cache_data
def load_sample_data():
    # Dados de exemplo - em um caso real, você carregaria de um arquivo ou API
    df = pd.DataFrame({
        'Região': ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'] * 5,
        'Ano': [2018, 2019, 2020, 2021, 2022] * 5,
        'Taxa_Desnutrição': [12.3, 15.7, 8.2, 6.5, 5.1, 11.8, 14.9, 7.8, 6.1, 4.8,
                            11.2, 14.1, 7.5, 5.8, 4.5, 10.5, 13.6, 7.1, 5.5, 4.2,
                            9.8, 12.9, 6.8, 5.2, 3.9],
        'População_Afetada': [250000, 890000, 120000, 550000, 95000, 240000, 870000, 115000, 530000, 90000,
                             230000, 850000, 110000, 510000, 85000, 220000, 830000, 105000, 490000, 80000,
                             210000, 810000, 100000, 470000, 75000],
        'Raça_Predominante': ['Parda', 'Parda', 'Branca', 'Branca', 'Branca', 'Parda', 'Parda', 'Branca', 'Branca', 'Branca',
                              'Parda', 'Parda', 'Branca', 'Branca', 'Branca', 'Parda', 'Parda', 'Branca', 'Branca', 'Branca',
                              'Parda', 'Parda', 'Branca', 'Branca', 'Branca']
    })
    return df

# Carregar dados
df = load_sample_data()

# Cabeçalho da página
st.markdown('<div class="page-header">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Dashboard de Análise Social</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Visão geral - Métricas principais
st.markdown("## Visão Geral")
st.markdown("Panorama dos principais indicadores sociais monitorados.")

# Métricas em cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Taxa Média de Desnutrição</div>', unsafe_allow_html=True)
    avg_malnutrition = df[df['Ano'] == df['Ano'].max()]['Taxa_Desnutrição'].mean()
    prev_avg = df[df['Ano'] == df['Ano'].max() - 1]['Taxa_Desnutrição'].mean()
    change = ((avg_malnutrition - prev_avg) / prev_avg) * 100
    
    st.markdown(f'<div class="metric-value">{avg_malnutrition:.1f}%</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-down">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-up">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">População Total Afetada</div>', unsafe_allow_html=True)
    total_affected = df[df['Ano'] == df['Ano'].max()]['População_Afetada'].sum()
    prev_total = df[df['Ano'] == df['Ano'].max() - 1]['População_Afetada'].sum()
    change = ((total_affected - prev_total) / prev_total) * 100
    
    st.markdown(f'<div class="metric-value">{total_affected:,.0f}</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-down">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-up">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Região Mais Afetada</div>', unsafe_allow_html=True)
    
    region_data = df[df['Ano'] == df['Ano'].max()].groupby('Região')['Taxa_Desnutrição'].mean().reset_index()
    most_affected = region_data.loc[region_data['Taxa_Desnutrição'].idxmax()]
    
    st.markdown(f'<div class="metric-value">{most_affected["Região"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="indicator indicator-down">{most_affected["Taxa_Desnutrição"]:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Região Menos Afetada</div>', unsafe_allow_html=True)
    
    least_affected = region_data.loc[region_data['Taxa_Desnutrição'].idxmin()]
    
    st.markdown(f'<div class="metric-value">{least_affected["Região"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="indicator indicator-up">{least_affected["Taxa_Desnutrição"]:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Gráficos principais
st.markdown("## Tendências e Comparações")

# Abas para diferentes visualizações
tab1, tab2, tab3 = st.tabs(["Tendência Temporal", "Comparação Regional", "Distribuição por Raça"])

with tab1:
    st.markdown("### Evolução da Taxa de Desnutrição ao Longo do Tempo")
    
    # Filtros
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        selected_regions = st.multiselect(
            "Selecione as regiões",
            options=df['Região'].unique(),
            default=df['Região'].unique()
        )
    with col2:
        year_range = st.slider(
            "Período",
            min_value=int(df['Ano'].min()),
            max_value=int(df['Ano'].max()),
            value=(int(df['Ano'].min()), int(df['Ano'].max()))
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados
    filtered_df = df[
        (df['Região'].isin(selected_regions)) & 
        (df['Ano'] >= year_range[0]) & 
        (df['Ano'] <= year_range[1])
    ]
    
    # Gráfico de linha
    fig = px.line(
        filtered_df.groupby(['Ano', 'Região'])['Taxa_Desnutrição'].mean().reset_index(),
        x='Ano',
        y='Taxa_Desnutrição',
        color='Região',
        markers=True,
        color_discrete_sequence=current_theme["chart_palette"],
        title="Evolução da Taxa de Desnutrição por Região (%)"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Ano",
        yaxis_title="Taxa de Desnutrição (%)",
        legend_title="Região",
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Comparação da Taxa de Desnutrição entre Regiões")
    
    # Filtros
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    selected_year = st.select_slider(
        "Selecione o ano",
        options=sorted(df['Ano'].unique()),
        value=df['Ano'].max()
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados
    year_df = df[df['Ano'] == selected_year]
    
    # Gráfico de barras
    fig = px.bar(
        year_df.groupby('Região')['Taxa_Desnutrição'].mean().reset_index().sort_values('Taxa_Desnutrição', ascending=False),
        x='Região',
        y='Taxa_Desnutrição',
        color='Região',
        color_discrete_sequence=current_theme["chart_palette"],
        title=f"Taxa de Desnutrição por Região em {selected_year} (%)"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Região",
        yaxis_title="Taxa de Desnutrição (%)",
        showlegend=False,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    # Adicionar rótulos de valor
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mapa de calor
    st.markdown("### Mapa de Intensidade por Região")
    
    # Criar dados para o mapa de calor
    region_order = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    heatmap_df = year_df.pivot_table(
        index='Região', 
        values=['Taxa_Desnutrição', 'População_Afetada'], 
        aggfunc='mean'
    ).reindex(region_order)
    
    # Normalizar população afetada para tamanho do círculo
    max_pop = heatmap_df['População_Afetada'].max()
    heatmap_df['Tamanho'] = (heatmap_df['População_Afetada'] / max_pop) * 50
    
    # Criar mapa de calor com círculos
    fig = px.scatter(
        heatmap_df.reset_index(),
        x=[1, 2, 3, 4, 5],  # Posições x arbitrárias
        y=[''] * 5,  # Todos na mesma linha
        size='Tamanho',
        color='Taxa_Desnutrição',
        hover_name='Região',
        text='Região',
        size_max=60,
        color_continuous_scale=px.colors.sequential.Reds,
        hover_data={
            'Taxa_Desnutrição': ':.1f',
            'População_Afetada': ':,.0f',
            'Tamanho': False,
            'y': False,
            'x': False
        }
    )
    
    fig.update_layout(
        height=250,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        coloraxis_colorbar=dict(title="Taxa (%)"),
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    fig.update_traces(textposition='middle center', textfont=dict(color='white', size=10))
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Distribuição da Desnutrição por Raça Predominante")
    
    # Filtros
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        selected_year_race = st.select_slider(
            "Selecione o ano",
            options=sorted(df['Ano'].unique()),
            value=df['Ano'].max(),
            key="year_race"
        )
    with col2:
        selected_races = st.multiselect(
            "Selecione as raças",
            options=df['Raça_Predominante'].unique(),
            default=df['Raça_Predominante'].unique()
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados
    race_df = df[
        (df['Ano'] == selected_year_race) & 
        (df['Raça_Predominante'].isin(selected_races))
    ]
    
    # Gráfico de barras agrupadas
    fig = px.bar(
        race_df,
        x='Região',
        y='Taxa_Desnutrição',
        color='Raça_Predominante',
        barmode='group',
        color_discrete_sequence=current_theme["chart_palette"],
        title=f"Taxa de Desnutrição por Região e Raça em {selected_year_race} (%)"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Região",
        yaxis_title="Taxa de Desnutrição (%)",
        legend_title="Raça Predominante",
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de pizza para distribuição racial
    race_distribution = race_df.groupby('Raça_Predominante')['População_Afetada'].sum().reset_index()
    
    fig = px.pie(
        race_distribution,
        values='População_Afetada',
        names='Raça_Predominante',
        title=f"Distribuição da População Afetada por Raça em {selected_year_race}",
        color_discrete_sequence=current_theme["chart_palette"],
        hole=0.4
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Segoe UI", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    fig.update_traces(textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)

# Seção de insights
st.markdown("## Principais Insights")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Tendências Observadas")
        st.markdown("""
        - A taxa de desnutrição apresenta tendência de queda em todas as regiões nos últimos 5 anos
        - O Nordeste continua sendo a região com maior incidência de desnutrição
        - A população afetada diminuiu 7.2% no último ano
        - Existe uma correlação entre raça predominante e taxas de desnutrição em determinadas regiões
        """)
    
    with col2:
        st.markdown("### Recomendações")
        st.markdown("""
        - Intensificar programas de segurança alimentar no Nordeste
        - Desenvolver políticas específicas para populações pardas e indígenas
        - Monitorar de perto as regiões com tendência de aumento recente
        - Implementar programas educacionais sobre nutrição nas áreas mais afetadas
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"© {datetime.now().year} Dashboard de Análise Social | Desenvolvido com Streamlit", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
