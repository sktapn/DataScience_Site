import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Indicadores de Desnutrição | Dashboard Social",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar utilitários de tema (mesmo código das páginas anteriores)
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

# Aplicar CSS personalizado (mesmo das páginas anteriores)
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
    
    /* Filtros */
    .filter-container {{
        background-color: {current_theme["accent"]};
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
        color: {current_theme["text_secondary"]};
    }}
    
    /* Gráficos e visualizações */
    .chart-container {{
        background-color: {current_theme["card"]};
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
        background-color: {current_theme["primary"]};
        color: white;
        padding: 0.75rem;
        text-align: left;
    }}
    .dataframe td {{
        padding: 0.75rem;
        border-bottom: 1px solid #eee;
    }}
    .dataframe tr:hover {{
        background-color: {current_theme["accent"]};
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar para navegação e configurações (mesmo das páginas anteriores)
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
    # Criar dados mais detalhados para análise de desnutrição
    regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    years = list(range(2018, 2023))
    
    # Criar DataFrame base
    data = []
    
    for region in regions:
        for year in years:
            # Taxa de desnutrição geral (%)
            base_rate = 15 if region == 'Nordeste' else 12 if region == 'Norte' else 8 if region == 'Centro-Oeste' else 6 if region == 'Sudeste' else 5
            # Diminuição gradual ao longo dos anos
            yearly_reduction = 0.5 * (year - 2018)
            rate = base_rate - yearly_reduction
            
            # População afetada
            base_pop = 900000 if region == 'Nordeste' else 250000 if region == 'Norte' else 120000 if region == 'Centro-Oeste' else 550000 if region == 'Sudeste' else 95000
            pop_affected = base_pop * (1 - 0.03 * (year - 2018))
            
            # Adicionar variação para diferentes tipos de desnutrição
            data.append({
                'Região': region,
                'Ano': year,
                'Taxa_Desnutrição': rate,
                'População_Afetada': int(pop_affected),
                'Desnutrição_Aguda': rate * 0.3,  # 30% do total é desnutrição aguda
                'Desnutrição_Crônica': rate * 0.7,  # 70% do total é desnutrição crônica
                'Taxa_Mortalidade': rate * 0.15,  # Taxa de mortalidade relacionada
                'Crianças_0_5': int(pop_affected * 0.4),  # 40% são crianças de 0-5 anos
                'Crianças_6_10': int(pop_affected * 0.3),  # 30% são crianças de 6-10 anos
                'Adolescentes': int(pop_affected * 0.2),  # 20% são adolescentes
                'Adultos': int(pop_affected * 0.1),  # 10% são adultos
                'Acesso_Saúde': 85 - (15 if region == 'Nordeste' else 10 if region == 'Norte' else 5 if region == 'Centro-Oeste' else 2 if region == 'Sudeste' else 3),
                'Segurança_Alimentar': 80 - (20 if region == 'Nordeste' else 15 if region == 'Norte' else 8 if region == 'Centro-Oeste' else 5 if region == 'Sudeste' else 6)
            })
    
    return pd.DataFrame(data)

# Carregar dados
df = load_sample_data()

# Cabeçalho da página
st.markdown('<div class="page-header">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Indicadores de Desnutrição</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Filtros
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.select_slider(
        "Selecione o ano",
        options=sorted(df['Ano'].unique()),
        value=df['Ano'].max()
    )

with col2:
    selected_regions = st.multiselect(
        "Selecione as regiões",
        options=df['Região'].unique(),
        default=df['Região'].unique()
    )

with col3:
    age_groups = {
        "all": "Todos os grupos",
        "children_0_5": "Crianças (0-5 anos)",
        "children_6_10": "Crianças (6-10 anos)",
        "adolescents": "Adolescentes",
        "adults": "Adultos"
    }
    
    selected_age_group = st.selectbox(
        "Grupo etário",
        options=list(age_groups.keys()),
        format_func=lambda x: age_groups[x]
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filtrar dados
filtered_df = df[
    (df['Ano'] == selected_year) & 
    (df['Região'].isin(selected_regions))
]

# Visão geral dos indicadores
st.markdown("## Panorama da Desnutrição")

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Taxa Média de Desnutrição</div>', unsafe_allow_html=True)
    avg_rate = filtered_df['Taxa_Desnutrição'].mean()
    
    # Comparar com ano anterior
    prev_year_data = df[(df['Ano'] == selected_year - 1) & (df['Região'].isin(selected_regions))]
    prev_avg = prev_year_data['Taxa_Desnutrição'].mean() if not prev_year_data.empty else 0
    
    if prev_avg > 0:
        change = ((avg_rate - prev_avg) / prev_avg) * 100
    else:
        change = 0
    
    st.markdown(f'<div class="metric-value">{avg_rate:.1f}%</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">População Total Afetada</div>', unsafe_allow_html=True)
    
    if selected_age_group == "all":
        total_affected = filtered_df['População_Afetada'].sum()
        prev_total = prev_year_data['População_Afetada'].sum() if not prev_year_data.empty else 0
    elif selected_age_group == "children_0_5":
        total_affected = filtered_df['Crianças_0_5'].sum()
        prev_total = prev_year_data['Crianças_0_5'].sum() if not prev_year_data.empty else 0
    elif selected_age_group == "children_6_10":
        total_affected = filtered_df['Crianças_6_10'].sum()
        prev_total = prev_year_data['Crianças_6_10'].sum() if not prev_year_data.empty else 0
    elif selected_age_group == "adolescents":
        total_affected = filtered_df['Adolescentes'].sum()
        prev_total = prev_year_data['Adolescentes'].sum() if not prev_year_data.empty else 0
    else:  # adults
        total_affected = filtered_df['Adultos'].sum()
        prev_total = prev_year_data['Adultos'].sum() if not prev_year_data.empty else 0
    
    if prev_total > 0:
        change = ((total_affected - prev_total) / prev_total) * 100
    else:
        change = 0
    
    st.markdown(f'<div class="metric-value">{total_affected:,.0f}</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Taxa de Desnutrição Aguda</div>', unsafe_allow_html=True)
    
    acute_rate = filtered_df['Desnutrição_Aguda'].mean()
    prev_acute = prev_year_data['Desnutrição_Aguda'].mean() if not prev_year_data.empty else 0
    
    if prev_acute > 0:
        change = ((acute_rate - prev_acute) / prev_acute) * 100
    else:
        change = 0
    
    st.markdown(f'<div class="metric-value">{acute_rate:.1f}%</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Taxa de Desnutrição Crônica</div>', unsafe_allow_html=True)
    
    chronic_rate = filtered_df['Desnutrição_Crônica'].mean()
    prev_chronic = prev_year_data['Desnutrição_Crônica'].mean() if not prev_year_data.empty else 0
    
    if prev_chronic > 0:
        change = ((chronic_rate - prev_chronic) / prev_chronic) * 100
    else:
        change = 0
    
    st.markdown(f'<div class="metric-value">{chronic_rate:.1f}%</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Análise por tipo de desnutrição
st.markdown("## Análise por Tipo de Desnutrição")

# Abas para diferentes visualizações
tab1, tab2 = st.tabs(["Comparação Regional", "Tendência Temporal"])

with tab1:
    # Gráfico de barras empilhadas
    fig = go.Figure()
    
    # Ordenar regiões por taxa total de desnutrição
    region_order = filtered_df.groupby('Região')['Taxa_Desnutrição'].mean().sort_values(ascending=False).index.tolist()
    
    # Filtrar dados ordenados
    ordered_df = filtered_df.set_index('Região').loc[region_order].reset_index()
    
    # Adicionar barras para desnutrição aguda
    fig.add_trace(go.Bar(
        x=ordered_df['Região'],
        y=ordered_df['Desnutrição_Aguda'],
        name='Desnutrição Aguda',
        marker_color=current_theme["chart_palette"][0],
        text=ordered_df['Desnutrição_Aguda'].apply(lambda x: f'{x:.1f}%'),
        textposition='inside'
    ))
    
    # Adicionar barras para desnutrição crônica
    fig.add_trace(go.Bar(
        x=ordered_df['Região'],
        y=ordered_df['Desnutrição_Crônica'],
        name='Desnutrição Crônica',
        marker_color=current_theme["chart_palette"][1],
        text=ordered_df['Desnutrição_Crônica'].apply(lambda x: f'{x:.1f}%'),
        textposition='inside'
    ))
    
    # Configurar layout
    fig.update_layout(
        barmode='stack',
        title=f'Tipos de Desnutrição por Região ({selected_year})',
        xaxis_title='Região',
        yaxis_title='Taxa de Desnutrição (%)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=500,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de distribuição por faixa etária
    st.markdown("### Distribuição por Faixa Etária")
    
    # Preparar dados para o gráfico de pizza
    age_data = []
    for region in filtered_df['Região'].unique():
        region_df = filtered_df[filtered_df['Região'] == region]
        
        if not region_df.empty:
            age_data.append({
                'Região': region,
                'Crianças (0-5 anos)': region_df['Crianças_0_5'].sum(),
                'Crianças (6-10 anos)': region_df['Crianças_6_10'].sum(),
                'Adolescentes': region_df['Adolescentes'].sum(),
                'Adultos': region_df['Adultos'].sum()
            })
    
    age_df = pd.DataFrame(age_data)
    
    # Criar gráfico de pizza para cada região
    fig = go.Figure()
    
    # Definir cores para cada faixa etária
    age_colors = [
        current_theme["chart_palette"][0],
        current_theme["chart_palette"][1],
        current_theme["chart_palette"][2],
        current_theme["chart_palette"][3]
    ]
    
    # Criar um gráfico de barras empilhadas para distribuição etária
    fig = px.bar(
        age_df,
        x='Região',
        y=['Crianças (0-5 anos)', 'Crianças (6-10 anos)', 'Adolescentes', 'Adultos'],
        title=f'Distribuição da População Afetada por Faixa Etária ({selected_year})',
        color_discrete_sequence=age_colors,
        labels={'value': 'População Afetada', 'variable': 'Faixa Etária'}
    )
    
    fig.update_layout(
        barmode='stack',
        xaxis_title='Região',
        yaxis_title='População Afetada',
        legend_title='Faixa Etária',
        height=500,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Gráfico de linha para tendência temporal
    # Filtrar dados para as regiões selecionadas (todos os anos)
    trend_df = df[df['Região'].isin(selected_regions)]
    
    # Agrupar por ano
    yearly_data = trend_df.groupby('Ano').agg({
        'Taxa_Desnutrição': 'mean',
        'Desnutrição_Aguda': 'mean',
        'Desnutrição_Crônica': 'mean',
        'Taxa_Mortalidade': 'mean'
    }).reset_index()
    
    # Criar gráfico de linha
    fig = go.Figure()
    
    # Adicionar linha para taxa total
    fig.add_trace(go.Scatter(
        x=yearly_data['Ano'],
        y=yearly_data['Taxa_Desnutrição'],
        mode='lines+markers',
        name='Taxa Total',
        line=dict(color=current_theme["primary"], width=3),
        marker=dict(size=8)
    ))
    
    # Adicionar linha para desnutrição aguda
    fig.add_trace(go.Scatter(
        x=yearly_data['Ano'],
        y=yearly_data['Desnutrição_Aguda'],
        mode='lines+markers',
        name='Desnutrição Aguda',
        line=dict(color=current_theme["chart_palette"][0], width=2),
        marker=dict(size=6)
    ))
    
    # Adicionar linha para desnutrição crônica
    fig.add_trace(go.Scatter(
        x=yearly_data['Ano'],
        y=yearly_data['Desnutrição_Crônica'],
        mode='lines+markers',
        name='Desnutrição Crônica',
        line=dict(color=current_theme["chart_palette"][1], width=2),
        marker=dict(size=6)
    ))
    
    # Adicionar linha para taxa de mortalidade
    fig.add_trace(go.Scatter(
        x=yearly_data['Ano'],
        y=yearly_data['Taxa_Mortalidade'],
        mode='lines+markers',
        name='Taxa de Mortalidade',
        line=dict(color=current_theme["error"], width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    # Configurar layout
    fig.update_layout(
        title='Evolução das Taxas de Desnutrição ao Longo do Tempo',
        xaxis_title='Ano',
        yaxis_title='Taxa (%)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=500,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    # Adicionar rótulos de dados
    for trace in fig.data:
        fig.add_annotation(
            x=trace.x[-1],
            y=trace.y[-1],
            text=f"{trace.y[-1]:.1f}%",
            showarrow=False,
            xshift=10,
            font=dict(color=trace.line.color)
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de área para população afetada ao longo do tempo
    if selected_age_group == "all":
        # Agrupar por ano e região
        pop_trend = df[df['Região'].isin(selected_regions)].groupby(['Ano', 'Região'])['População_Afetada'].sum().reset_index()
        
        # Criar gráfico de área
        fig = px.area(
            pop_trend,
            x='Ano',
            y='População_Afetada',
            color='Região',
            title='Evolução da População Afetada por Região',
            color_discrete_sequence=current_theme["chart_palette"]
        )
    else:
        # Mapear seleção para coluna
        age_column = {
            "children_0_5": "Crianças_0_5",
            "children_6_10": "Crianças_6_10",
            "adolescents": "Adolescentes",
            "adults": "Adultos"
        }[selected_age_group]
        
        # Agrupar por ano e região
        pop_trend = df[df['Região'].isin(selected_regions)].groupby(['Ano', 'Região'])[age_column].sum().reset_index()
        
        # Criar gráfico de área
        fig = px.area(
            pop_trend,
            x='Ano',
            y=age_column,
            color='Região',
            title=f'Evolução da População Afetada ({age_groups[selected_age_group]}) por Região',
            color_discrete_sequence=current_theme["chart_palette"]
        )
    
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='População Afetada',
        legend_title='Região',
        height=500,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Fatores relacionados
st.markdown("## Fatores Relacionados à Desnutrição")

# Gráfico de correlação entre acesso à saúde e segurança alimentar
col1, col2 = st.columns(2)

with col1:
    # Gráfico de dispersão
    fig = px.scatter(
        filtered_df,
        x='Acesso_Saúde',
        y='Taxa_Desnutrição',
        color='Região',
        size='População_Afetada',
        hover_name='Região',
        color_discrete_sequence=current_theme["chart_palette"],
        size_max=50,
        opacity=0.7,
        title='Relação entre Acesso à Saúde e Taxa de Desnutrição'
    )
    
    # Adicionar linha de tendência
    fig.update_layout(
        height=400,
        xaxis_title='Acesso à Saúde (%)',
        yaxis_title='Taxa de Desnutrição (%)',
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    # Adicionar linha de tendência
    fig.update_traces(marker=dict(line=dict(width=1, color='white')))
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gráfico de dispersão
    fig = px.scatter(
        filtered_df,
        x='Segurança_Alimentar',
        y='Taxa_Desnutrição',
        color='Região',
        size='População_Afetada',
        hover_name='Região',
        color_discrete_sequence=current_theme["chart_palette"],
        size_max=50,
        opacity=0.7,
        title='Relação entre Segurança Alimentar e Taxa de Desnutrição'
    )
    
    # Adicionar linha de tendência
    fig.update_layout(
        height=400,
        xaxis_title='Segurança Alimentar (%)',
        yaxis_title='Taxa de Desnutrição (%)',
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    # Adicionar linha de tendência
    fig.update_traces(marker=dict(line=dict(width=1, color='white')))
    
    st.plotly_chart(fig, use_container_width=True)

# Indicadores de impacto
st.markdown("## Impacto da Desnutrição")

# Gráfico de barras para taxa de mortalidade
fig = px.bar(
    filtered_df.sort_values('Taxa_Mortalidade', ascending=False),
    x='Região',
    y='Taxa_Mortalidade',
    color='Região',
    color_discrete_sequence=current_theme["chart_palette"],
    title=f'Taxa de Mortalidade Relacionada à Desnutrição por Região ({selected_year})'
)

fig.update_layout(
    height=400,
    xaxis_title='Região',
    yaxis_title='Taxa de Mortalidade (%)',
    showlegend=False,
    font=dict(family="Segoe UI", size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
)

# Adicionar rótulos de valor
fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

st.plotly_chart(fig, use_container_width=True)

# Tabela de resumo
st.markdown("## Resumo dos Indicadores")

# Preparar dados para a tabela
summary_data = filtered_df.groupby('Região').agg({
    'Taxa_Desnutrição': 'mean',
    'Desnutrição_Aguda': 'mean',
    'Desnutrição_Crônica': 'mean',
    'Taxa_Mortalidade': 'mean',
    'População_Afetada': 'sum',
    'Acesso_Saúde': 'mean',
    'Segurança_Alimentar': 'mean'
}).reset_index()

# Formatar valores
summary_data['Taxa_Desnutrição'] = summary_data['Taxa_Desnutrição'].apply(lambda x: f"{x:.1f}%")
summary_data['Desnutrição_Aguda'] = summary_data['Desnutrição_Aguda'].apply(lambda x: f"{x:.1f}%")
summary_data['Desnutrição_Crônica'] = summary_data['Desnutrição_Crônica'].apply(lambda x: f"{x:.1f}%")
summary_data['Taxa_Mortalidade'] = summary_data['Taxa_Mortalidade'].apply(lambda x: f"{x:.1f}%")
summary_data['População_Afetada'] = summary_data['População_Afetada'].apply(lambda x: f"{x:,.0f}")
summary_data['Acesso_Saúde'] = summary_data['Acesso_Saúde'].apply(lambda x: f"{x:.1f}%")
summary_data['Segurança_Alimentar'] = summary_data['Segurança_Alimentar'].apply(lambda x: f"{x:.1f}%")

# Renomear colunas para exibição
summary_data = summary_data.rename(columns={
    'Taxa_Desnutrição': 'Taxa Total',
    'Desnutrição_Aguda': 'D. Aguda',
    'Desnutrição_Crônica': 'D. Crônica',
    'Taxa_Mortalidade': 'Mortalidade',
    'População_Afetada': 'Pop. Afetada',
    'Acesso_Saúde': 'Acesso à Saúde',
    'Segurança_Alimentar': 'Seg. Alimentar'
})

# Exibir tabela
st.dataframe(
    summary_data,
    use_container_width=True,
    hide_index=True
)

# Insights e recomendações
st.markdown("## Insights e Recomendações")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Principais Descobertas")
        st.markdown("""
        - A desnutrição crônica representa cerca de 70% dos casos de desnutrição
        - Existe uma forte correlação negativa entre acesso à saúde e taxa de desnutrição
        - Crianças de 0-5 anos são o grupo mais vulnerável em todas as regiões
        - A taxa de mortalidade relacionada à desnutrição está diminuindo, mas ainda é preocupante
        - Regiões com menor segurança alimentar apresentam taxas mais altas de desnutrição aguda
        """)
    
    with col2:
        st.markdown("### Recomendações")
        st.markdown("""
        - Priorizar programas de nutrição infantil para crianças menores de 5 anos
        - Fortalecer o acesso à saúde básica nas regiões Norte e Nordeste
        - Implementar programas de segurança alimentar focados em famílias vulneráveis
        - Desenvolver campanhas educativas sobre nutrição adequada
        - Monitorar continuamente os indicadores de desnutrição para intervenções rápidas
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"© {datetime.now().year} Dashboard de Análise Social | Desenvolvido com Streamlit", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
