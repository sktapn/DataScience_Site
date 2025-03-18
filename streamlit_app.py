import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Importar utilitários
from utils.theme_utils import initialize_theme, get_current_theme, apply_theme_css, create_sidebar_navigation
from utils.data_utils import load_sample_data, format_number, calculate_change

# Configuração da página
st.set_page_config(
    page_title="Dashboard Social",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar e aplicar tema
initialize_theme()
current_theme = get_current_theme()
apply_theme_css(current_theme)

# Criar barra lateral de navegação
create_sidebar_navigation()

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
