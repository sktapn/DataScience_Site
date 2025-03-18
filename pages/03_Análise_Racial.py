import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Análise por Raça/Etnia | Dashboard Social",
    page_icon="👥",
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
    # Criar dados mais detalhados para análise racial
    regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    years = list(range(2018, 2023))
    races = ['Branca', 'Preta', 'Parda', 'Indígena', 'Amarela']
    
    # Criar DataFrame base
    data = []
    
    for region in regions:
        for year in years:
            for race in races:
                # Definir taxas base por raça (simulando desigualdades)
                if race == 'Branca':
                    base_rate = 5.0
                    base_pop = 120000
                elif race == 'Preta':
                    base_rate = 12.0
                    base_pop = 180000
                elif race == 'Parda':
                    base_rate = 14.0
                    base_pop = 250000
                elif race == 'Indígena':
                    base_rate = 18.0
                    base_pop = 80000
                else:  # Amarela
                    base_rate = 4.0
                    base_pop = 50000
                
                # Ajustar por região
                if region == 'Nordeste':
                    regional_factor = 1.4
                elif region == 'Norte':
                    regional_factor = 1.3
                elif region == 'Centro-Oeste':
                    regional_factor = 1.1
                elif region == 'Sudeste':
                    regional_factor = 0.9
                else:  # Sul
                    regional_factor = 0.8
                
                # Ajustar por ano (melhoria gradual)
                yearly_reduction = 0.05 * (year - 2018)
                
                # Calcular taxa final
                rate = base_rate * regional_factor * (1 - yearly_reduction)
                
                # Calcular população afetada
                pop_affected = int(base_pop * regional_factor * (1 - 0.03 * (year - 2018)))
                
                # Adicionar dados
                data.append({
                    'Região': region,
                    'Ano': year,
                    'Raça': race,
                    'Taxa_Desnutrição': rate,
                    'População_Afetada': pop_affected,
                    'Acesso_Saúde': 85 - (base_rate * 2),
                    'Renda_Média': 2500 - (base_rate * 100),
                    'Escolaridade_Média': 10 - (base_rate * 0.2),
                    'Acesso_Saneamento': 90 - (base_rate * 2.5)
                })
    
    return pd.DataFrame(data)

# Carregar dados
df = load_sample_data()

# Cabeçalho da página
st.markdown('<div class="page-header">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Análise por Raça/Etnia</h1>', unsafe_allow_html=True)
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
    selected_races = st.multiselect(
        "Selecione as raças/etnias",
        options=df['Raça'].unique(),
        default=df['Raça'].unique()
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filtrar dados
filtered_df = df[
    (df['Ano'] == selected_year) & 
    (df['Região'].isin(selected_regions)) &
    (df['Raça'].isin(selected_races))
]

# Visão geral dos indicadores por raça/etnia
st.markdown("## Panorama por Raça/Etnia")

# Gráfico de barras para taxa de desnutrição por raça
fig = px.bar(
    filtered_df.groupby('Raça')['Taxa_Desnutrição'].mean().reset_index().sort_values('Taxa_Desnutrição', ascending=False),
    x='Raça',
    y='Taxa_Desnutrição',
    color='Raça',
    color_discrete_sequence=current_theme["chart_palette"],
    title=f'Taxa de Desnutrição por Raça/Etnia ({selected_year})'
)

fig.update_layout(
    height=400,
    xaxis_title='Raça/Etnia',
    yaxis_title='Taxa de Desnutrição (%)',
    showlegend=False,
    font=dict(family="Segoe UI", size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
)

# Adicionar rótulos de valor
fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

st.plotly_chart(fig, use_container_width=True)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

# Encontrar raça com maior taxa
max_race_data = filtered_df.groupby('Raça')['Taxa_Desnutrição'].mean().reset_index()
max_race = max_race_data.loc[max_race_data['Taxa_Desnutrição'].idxmax()]

# Encontrar raça com menor taxa
min_race = max_race_data.loc[max_race_data['Taxa_Desnutrição'].idxmin()]

# Calcular disparidade
disparity = max_race['Taxa_Desnutrição'] / min_race['Taxa_Desnutrição']

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Raça Mais Afetada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{max_race["Raça"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="indicator indicator-down">{max_race["Taxa_Desnutrição"]:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Raça Menos Afetada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{min_race["Raça"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="indicator indicator-up">{min_race["Taxa_Desnutrição"]:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Disparidade Racial</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{disparity:.1f}x</div>', unsafe_allow_html=True)
    st.markdown('<div class="indicator indicator-down">Diferença entre extremos</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # População total afetada
    total_affected = filtered_df['População_Afetada'].sum()
    
    # Comparar com ano anterior
    prev_year_data = df[
        (df['Ano'] == selected_year - 1) & 
        (df['Região'].isin(selected_regions)) &
        (df['Raça'].isin(selected_races))
    ]
    prev_total = prev_year_data['População_Afetada'].sum() if not prev_year_data.empty else 0
    
    if prev_total > 0:
        change = ((total_affected - prev_total) / prev_total) * 100
    else:
        change = 0
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">População Total Afetada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{total_affected:,.0f}</div>', unsafe_allow_html=True)
    
    if change < 0:
        st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Análise por região e raça
st.markdown("## Análise Cruzada: Região x Raça/Etnia")

# Abas para diferentes visualizações
tab1, tab2 = st.tabs(["Comparação Regional", "Tendência Temporal"])

with tab1:
    # Gráfico de barras agrupadas
    region_race_df = filtered_df.groupby(['Região', 'Raça'])['Taxa_Desnutrição'].mean().reset_index()
    
    fig = px.bar(
        region_race_df,
        x='Região',
        y='Taxa_Desnutrição',
        color='Raça',
        barmode='group',
        color_discrete_sequence=current_theme["chart_palette"],
        title=f'Taxa de Desnutrição por Região e Raça/Etnia ({selected_year})'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title='Região',
        yaxis_title='Taxa de Desnutrição (%)',
        legend_title='Raça/Etnia',
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mapa de calor
    st.markdown("### Mapa de Calor: Intensidade da Desnutrição por Região e Raça")
    
    # Criar dados para o mapa de calor
    heatmap_df = filtered_df.pivot_table(
        index='Região', 
        columns='Raça', 
        values='Taxa_Desnutrição', 
        aggfunc='mean'
    )
    
    # Criar mapa de calor
    fig = px.imshow(
        heatmap_df,
        text_auto='.1f',
        color_continuous_scale=px.colors.sequential.Reds,
        title=f'Mapa de Calor: Taxa de Desnutrição por Região e Raça ({selected_year})'
    )
    
    fig.update_layout(
        height=450,
        xaxis_title='Raça/Etnia',
        yaxis_title='Região',
        font=dict(family="Segoe UI", size=12),
        coloraxis_colorbar=dict(title="Taxa (%)"),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Gráfico de linha para tendência temporal por raça
    # Filtrar dados para as regiões selecionadas (todos os anos)
    trend_df = df[
        (df['Região'].isin(selected_regions)) &
        (df['Raça'].isin(selected_races))
    ]
    
    # Agrupar por ano e raça
    yearly_race_data = trend_df.groupby(['Ano', 'Raça'])['Taxa_Desnutrição'].mean().reset_index()
    
    # Criar gráfico de linha
    fig = px.line(
        yearly_race_data,
        x='Ano',
        y='Taxa_Desnutrição',
        color='Raça',
        markers=True,
        color_discrete_sequence=current_theme["chart_palette"],
        title='Evolução da Taxa de Desnutrição por Raça/Etnia ao Longo do Tempo'
    )
    
    # Configurar layout
    fig.update_layout(
        height=500,
        xaxis_title='Ano',
        yaxis_title='Taxa de Desnutrição (%)',
        legend_title='Raça/Etnia',
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    # Adicionar rótulos de dados para o último ano
    for race in selected_races:
        race_data = yearly_race_data[yearly_race_data['Raça'] == race]
        if not race_data.empty:
            last_year_data = race_data[race_data['Ano'] == race_data['Ano'].max()]
            if not last_year_data.empty:
                fig.add_annotation(
                    x=last_year_data['Ano'].values[0],
                    y=last_year_data['Taxa_Desnutrição'].values[0],
                    text=f"{last_year_data['Taxa_Desnutrição'].values[0]:.1f}%",
                    showarrow=False,
                    xshift=10,
                    font=dict(size=10)
                )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de área para população afetada ao longo do tempo
    # Agrupar por ano e raça
    pop_trend = trend_df.groupby(['Ano', 'Raça'])['População_Afetada'].sum().reset_index()
    
    # Criar gráfico de área
    fig = px.area(
        pop_trend,
        x='Ano',
        y='População_Afetada',
        color='Raça',
        title='Evolução da População Afetada por Raça/Etnia',
        color_discrete_sequence=current_theme["chart_palette"]
    )
    
    fig.update_layout(
        height=500,
        xaxis_title='Ano',
        yaxis_title='População Afetada',
        legend_title='Raça/Etnia',
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Fatores socioeconômicos
st.markdown("## Fatores Socioeconômicos por Raça/Etnia")

# Gráfico de radar para comparação de fatores socioeconômicos
st.markdown("### Comparação de Indicadores Socioeconômicos por Raça/Etnia")

# Preparar dados para o gráfico de radar
radar_df = filtered_df.groupby('Raça').agg({
    'Acesso_Saúde': 'mean',
    'Renda_Média': 'mean',
    'Escolaridade_Média': 'mean',
    'Acesso_Saneamento': 'mean',
    'Taxa_Desnutrição': 'mean'
}).reset_index()

# Criar gráfico de radar
fig = go.Figure()

# Categorias para o radar
categories = ['Acesso à Saúde', 'Renda Média', 'Escolaridade', 'Saneamento', 'Taxa de Desnutrição*']

# Adicionar uma linha para cada raça
for i, race in enumerate(radar_df['Raça']):
    race_data = radar_df[radar_df['Raça'] == race]
    
    # Normalizar os dados para uma escala de 0-100
    # Para Taxa_Desnutrição, invertemos a escala (menor é melhor)
    values = [
        race_data['Acesso_Saúde'].values[0],
        race_data['Renda_Média'].values[0] / 25,  # Normalizar para escala 0-100
        race_data['Escolaridade_Média'].values[0] * 10,  # Normalizar para escala 0-100
        race_data['Acesso_Saneamento'].values[0],
        100 - race_data['Taxa_Desnutrição'].values[0] * 5  # Inverter e normalizar
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=race,
        line_color=current_theme["chart_palette"][i % len(current_theme["chart_palette"])],
        opacity=0.7
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=True,
    title='Comparação de Indicadores Socioeconômicos por Raça/Etnia',
    height=600,
    font=dict(family="Segoe UI", size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig, use_container_width=True)
st.caption("* Para Taxa de Desnutrição, a escala foi invertida (valores mais altos indicam menor taxa)")

# Correlação entre fatores socioeconômicos e desnutrição
st.markdown("### Correlação entre Fatores Socioeconômicos e Desnutrição")

# Selecionar fator para análise
factor_options = {
    "Renda_Média": "Renda Média",
    "Escolaridade_Média": "Escolaridade Média (anos)",
    "Acesso_Saúde": "Acesso à Saúde (%)",
    "Acesso_Saneamento": "Acesso a Saneamento (%)"
}

selected_factor = st.selectbox(
    "Selecione o fator socioeconômico",
    options=list(factor_options.keys()),
    format_func=lambda x: factor_options[x]
)

# Gráfico de dispersão
fig = px.scatter(
    filtered_df,
    x=selected_factor,
    y='Taxa_Desnutrição',
    color='Raça',
    size='População_Afetada',
    hover_name='Região',
    color_discrete_sequence=current_theme["chart_palette"],
    size_max=50,
    opacity=0.7,
    title=f'Relação entre {factor_options[selected_factor]} e Taxa de Desnutrição'
)

# Adicionar linha de tendência
fig.update_layout(
    height=500,
    xaxis_title=factor_options[selected_factor],
    yaxis_title='Taxa de Desnutrição (%)',
    font=dict(family="Segoe UI", size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
)

# Adicionar linha de tendência
fig.update_traces(marker=dict(line=dict(width=1, color='white')))

# Adicionar linha de tendência para cada raça
for race in selected_races:
    race_df = filtered_df[filtered_df['Raça'] == race]
    if len(race_df) > 1:  # Precisa de pelo menos 2 pontos para uma linha de tendência
        fig.add_trace(
            go.Scatter(
                x=race_df[selected_factor],
                y=race_df['Taxa_Desnutrição'],
                mode='lines',
                name=f'Tendência - {race}',
                line=dict(dash='dash', width=1),
                showlegend=False
            )
        )

st.plotly_chart(fig, use_container_width=True)

# Tabela de resumo
st.markdown("## Resumo dos Indicadores por Raça/Etnia")

# Preparar dados para a tabela
summary_data = filtered_df.groupby('Raça').agg({
    'Taxa_Desnutrição': 'mean',
    'População_Afetada': 'sum',
    'Acesso_Saúde': 'mean',
    'Renda_Média': 'mean',
    'Escolaridade_Média': 'mean',
    'Acesso_Saneamento': 'mean'
}).reset_index()

# Formatar valores
summary_data['Taxa_Desnutrição'] = summary_data['Taxa_Desnutrição'].apply(lambda x: f"{x:.1f}%")
summary_data['População_Afetada'] = summary_data['População_Afetada'].apply(lambda x: f"{x:,.0f}")
summary_data['Acesso_Saúde'] = summary_data['Acesso_Saúde'].apply(lambda x: f"{x:.1f}%")
summary_data['Renda_Média'] = summary_data['Renda_Média'].apply(lambda x: f"R$ {x:,.2f}")
summary_data['Escolaridade_Média'] = summary_data['Escolaridade_Média'].apply(lambda x: f"{x:.1f} anos")
summary_data['Acesso_Saneamento'] = summary_data['Acesso_Saneamento'].apply(lambda x: f"{x:.1f}%")

# Renomear colunas para exibição
summary_data = summary_data.rename(columns={
    'Taxa_Desnutrição': 'Taxa de Desnutrição',
    'População_Afetada': 'População Afetada',
    'Acesso_Saúde': 'Acesso à Saúde',
    'Renda_Média': 'Renda Média',
    'Escolaridade_Média': 'Escolaridade',
    'Acesso_Saneamento': 'Acesso a Saneamento'
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
        - Existe uma disparidade significativa nas taxas de desnutrição entre diferentes grupos raciais
        - A população indígena apresenta as maiores taxas de desnutrição em todas as regiões
        - Há uma forte correlação entre renda média, escolaridade e taxas de desnutrição
        - A disparidade racial é mais acentuada nas regiões Norte e Nordeste
        - O acesso a saneamento básico é um fator determinante para as taxas de desnutrição
        """)
    
    with col2:
        st.markdown("### Recomendações")
        st.markdown("""
        - Desenvolver políticas públicas específicas para populações indígenas e comunidades tradicionais
        - Implementar programas de segurança alimentar com foco em equidade racial
        - Ampliar o acesso à educação e saúde em comunidades vulneráveis
        - Criar indicadores de monitoramento que considerem o recorte racial
        - Promover pesquisas e estudos sobre os determinantes sociais da desnutrição com enfoque racial
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"© {datetime.now().year} Dashboard de Análise Social | Desenvolvido com Streamlit", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
