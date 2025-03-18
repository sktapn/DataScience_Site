import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="Análise Regional | Dashboard Social",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar utilitários de tema (mesmo código da página principal)
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
            "error":  "#757575",
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

# Aplicar CSS personalizado (mesmo da página principal)
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
    
    /* Mapa */
    .map-container {{
        background-color: {current_theme["card"]};
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
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
</style>
""", unsafe_allow_html=True)

# Sidebar para navegação e configurações (mesmo da página principal)
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
        'Estado': ['Amazonas', 'Bahia', 'Goiás', 'São Paulo', 'Rio Grande do Sul',
                  'Pará', 'Ceará', 'Mato Grosso', 'Rio de Janeiro', 'Paraná',
                  'Tocantins', 'Pernambuco', 'Mato Grosso do Sul', 'Minas Gerais', 'Santa Catarina',
                  'Acre', 'Maranhão', 'Distrito Federal', 'Espírito Santo', 'Rio Grande do Sul',
                  'Roraima', 'Alagoas', 'Goiás', 'São Paulo', 'Paraná'],
        'Ano': [2018, 2019, 2020, 2021, 2022] * 5,
        'Taxa_Desnutrição': [12.3, 15.7, 8.2, 6.5, 5.1, 11.8, 14.9, 7.8, 6.1, 4.8,
                            11.2, 14.1, 7.5, 5.8, 4.5, 10.5, 13.6, 7.1, 5.5, 4.2,
                            9.8, 12.9, 6.8, 5.2, 3.9],
        'População_Afetada': [250000, 890000, 120000, 550000, 95000, 240000, 870000, 115000, 530000, 90000,
                             230000, 850000, 110000, 510000, 85000, 220000, 830000, 105000, 490000, 80000,
                             210000, 810000, 100000, 470000, 75000],
        'IDH': [0.72, 0.68, 0.76, 0.82, 0.79, 0.73, 0.69, 0.77, 0.81, 0.78,
               0.74, 0.70, 0.78, 0.80, 0.77, 0.75, 0.71, 0.79, 0.79, 0.76,
               0.73, 0.67, 0.75, 0.81, 0.78],
        'PIB_Per_Capita': [18500, 15200, 25600, 39800, 33400, 19200, 16100, 26300, 38500, 32100,
                          20100, 17000, 27100, 37200, 30800, 21000, 17900, 28000, 36000, 29500,
                          19800, 16500, 26800, 38000, 31500]
    })
    return df

# Carregar dados
df = load_sample_data()

# Cabeçalho da página
st.markdown('<div class="page-header">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Análise Regional</h1>', unsafe_allow_html=True)
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
    metric_options = {
        "Taxa_Desnutrição": "Taxa de Desnutrição (%)",
        "População_Afetada": "População Afetada",
        "IDH": "Índice de Desenvolvimento Humano",
        "PIB_Per_Capita": "PIB per Capita (R$)"
    }
    
    selected_metric = st.selectbox(
        "Selecione a métrica",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x]
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filtrar dados
filtered_df = df[
    (df['Ano'] == selected_year) & 
    (df['Região'].isin(selected_regions))
]

# Mapa do Brasil com dados regionais
st.markdown("## Mapa de Distribuição Regional")
st.markdown("Visualização da distribuição geográfica dos indicadores sociais por região.")

# Simulação de mapa (em um caso real, usaríamos um mapa geográfico real)
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Criar um gráfico de dispersão simulando um mapa
# Posições aproximadas das regiões no mapa do Brasil
region_positions = {
    'Norte': (3, 8),
    'Nordeste': (6, 7),
    'Centro-Oeste': (4, 5),
    'Sudeste': (5, 3),
    'Sul': (4, 1)
}

# Preparar dados para o mapa
map_data = []
for region in filtered_df['Região'].unique():
    if region in region_positions:
        region_df = filtered_df[filtered_df['Região'] == region]
        avg_value = region_df[selected_metric].mean()
        
        # Normalizar tamanho para visualização
        if selected_metric == 'População_Afetada':
            size = (avg_value / 1000000) * 100  # Ajustar escala
            size = max(20, min(size, 100))  # Limitar tamanho
        else:
            size = avg_value * 10
            size = max(20, min(size, 100))  # Limitar tamanho
        
        map_data.append({
            'Região': region,
            'x': region_positions[region][0],
            'y': region_positions[region][1],
            'Valor': avg_value,
            'Tamanho': size
        })

map_df = pd.DataFrame(map_data)

# Criar mapa simulado
fig = px.scatter(
    map_df,
    x='x',
    y='y',
    size='Tamanho',
    color='Valor',
    hover_name='Região',
    text='Região',
    color_continuous_scale=px.colors.sequential.Blues if selected_metric != 'Taxa_Desnutrição' else px.colors.sequential.Reds,
    size_max=60,
    hover_data={
        'Valor': ':.2f',
        'x': False,
        'y': False,
        'Tamanho': False
    }
)

# Adicionar contorno do Brasil (simplificado)
# Isso é apenas uma simulação - em um caso real, usaríamos um mapa geográfico real
brazil_outline = [
    (2, 8), (4, 9), (6, 9), (7, 8), (8, 7), (8, 5), 
    (7, 3), (6, 2), (5, 1), (3, 1), (2, 2), (1, 4),
    (1, 6), (2, 8)
]

x_outline, y_outline = zip(*brazil_outline)
fig.add_trace(
    go.Scatter(
        x=x_outline,
        y=y_outline,
        mode='lines',
        line=dict(color='rgba(0,0,0,0.3)', width=2),
        hoverinfo='skip',
        showlegend=False
    )
)

fig.update_layout(
    height=500,
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 9]),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 10]),
    coloraxis_colorbar=dict(title=metric_options[selected_metric]),
    font=dict(family="Segoe UI", size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20),
    title=f"Distribuição de {metric_options[selected_metric]} por Região ({selected_year})"
)

fig.update_traces(textposition='top center', textfont=dict(size=12, family="Segoe UI"))

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Métricas por região
st.markdown("## Indicadores Regionais")
st.markdown("Comparação detalhada dos indicadores entre as diferentes regiões.")

# Criar cards para cada região
region_cols = st.columns(len(selected_regions))

for i, region in enumerate(selected_regions):
    region_data = filtered_df[filtered_df['Região'] == region]
    
    with region_cols[i]:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-title">{region}</div>', unsafe_allow_html=True)
        
        # Valor atual
        current_value = region_data[selected_metric].mean()
        
        # Valor do ano anterior
        prev_year_data = df[(df['Região'] == region) & (df['Ano'] == selected_year - 1)]
        prev_value = prev_year_data[selected_metric].mean() if not prev_year_data.empty else 0
        
        # Calcular mudança percentual
        if prev_value > 0:
            change = ((current_value - prev_value) / prev_value) * 100
        else:
            change = 0
        
        # Formatar valor com base na métrica
        if selected_metric == 'População_Afetada':
            formatted_value = f"{current_value:,.0f}"
        elif selected_metric == 'PIB_Per_Capita':
            formatted_value = f"R$ {current_value:,.2f}"
        else:
            formatted_value = f"{current_value:.2f}"
        
        st.markdown(f'<div class="metric-value">{formatted_value}</div>', unsafe_allow_html=True)
        
        # Indicador de mudança
        if selected_metric == 'Taxa_Desnutrição':
            # Para taxa de desnutrição, diminuição é positiva
            if change < 0:
                st.markdown(f'<div class="indicator indicator-up">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="indicator indicator-down">▲ {change:.1f}%</div>', unsafe_allow_html=True)
        else:
            # Para outras métricas, aumento é positivo
            if change > 0:
                st.markdown(f'<div class="indicator indicator-up">▲ {change:.1f}%</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="indicator indicator-down">▼ {abs(change):.1f}%</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Gráficos comparativos
st.markdown("## Análise Comparativa")

# Abas para diferentes visualizações
tab1, tab2 = st.tabs(["Comparação Regional", "Correlação de Indicadores"])

with tab1:
    # Gráfico de barras comparativo
    region_comparison = filtered_df.groupby('Região')[selected_metric].mean().reset_index()
    
    # Ordenar com base na métrica
    if selected_metric == 'Taxa_Desnutrição':
        region_comparison = region_comparison.sort_values(selected_metric, ascending=False)
    else:
        region_comparison = region_comparison.sort_values(selected_metric, ascending=True)
    
    fig = px.bar(
        region_comparison,
        x='Região',
        y=selected_metric,
        color='Região',
        color_discrete_sequence=current_theme["chart_palette"],
        title=f"{metric_options[selected_metric]} por Região ({selected_year})"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Região",
        yaxis_title=metric_options[selected_metric],
        showlegend=False,
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    # Adicionar rótulos de valor
    if selected_metric == 'População_Afetada':
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    elif selected_metric == 'PIB_Per_Capita':
        fig.update_traces(texttemplate='R$ %{y:,.2f}', textposition='outside')
    else:
        fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.markdown("### Detalhamento por Estado")
    
    # Agrupar por estado
    state_data = filtered_df.groupby(['Região', 'Estado'])[selected_metric].mean().reset_index()
    
    # Ordenar com base na métrica
    if selected_metric == 'Taxa_Desnutrição':
        state_data = state_data.sort_values(selected_metric, ascending=False)
    else:
        state_data = state_data.sort_values(selected_metric, ascending=True)
    
    # Formatar valores
    if selected_metric == 'População_Afetada':
        state_data[selected_metric] = state_data[selected_metric].apply(lambda x: f"{x:,.0f}")
    elif selected_metric == 'PIB_Per_Capita':
        state_data[selected_metric] = state_data[selected_metric].apply(lambda x: f"R$ {x:,.2f}")
    else:
        state_data[selected_metric] = state_data[selected_metric].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(
        state_data,
        column_config={
            "Região": st.column_config.TextColumn("Região"),
            "Estado": st.column_config.TextColumn("Estado"),
            selected_metric: st.column_config.TextColumn(metric_options[selected_metric])
        },
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.markdown("### Correlação entre Indicadores Sociais")
    
    # Selecionar indicadores para correlação
    col1, col2 = st.columns(2)
    
    with col1:
        x_metric = st.selectbox(
            "Indicador X",
            options=list(metric_options.keys()),
            format_func=lambda x: metric_options[x],
            index=3  # PIB_Per_Capita
        )
    
    with col2:
        y_metric = st.selectbox(
            "Indicador Y",
            options=list(metric_options.keys()),
            format_func=lambda x: metric_options[x],
            index=0  # Taxa_Desnutrição
        )
    
    # Gráfico de dispersão para correlação
    fig = px.scatter(
        filtered_df,
        x=x_metric,
        y=y_metric,
        color='Região',
        size='População_Afetada',
        hover_name='Estado',
        color_discrete_sequence=current_theme["chart_palette"],
        size_max=50,
        opacity=0.7,
        title=f"Correlação entre {metric_options[x_metric]} e {metric_options[y_metric]} ({selected_year})"
    )
    
    # Adicionar linha de tendência
    fig.update_layout(
        height=600,
        xaxis_title=metric_options[x_metric],
        yaxis_title=metric_options[y_metric],
        font=dict(family="Segoe UI", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
    )
    
    # Adicionar linha de tendência
    fig.update_traces(marker=dict(line=dict(width=1, color='white')))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calcular e mostrar coeficiente de correlação
    correlation = filtered_df[[x_metric, y_metric]].corr().iloc[0, 1]
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1rem;">
        <p style="font-size: 1.2rem;">Coeficiente de Correlação: <span style="font-weight: bold; color: {current_theme['primary']};">{correlation:.3f}</span></p>
        <p>
            {
                "Correlação forte negativa" if correlation <= -0.7 else
                "Correlação moderada negativa" if correlation <= -0.3 else
                "Correlação fraca negativa" if correlation < 0 else
                "Sem correlação" if correlation == 0 else
                "Correlação fraca positiva" if correlation < 0.3 else
                "Correlação moderada positiva" if correlation < 0.7 else
                "Correlação forte positiva"
            }
        </p>
    </div>
    """, unsafe_allow_html=True)

# Insights e recomendações
st.markdown("## Insights Regionais")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Principais Descobertas")
        st.markdown("""
        - Existe uma forte correlação negativa entre PIB per capita e taxa de desnutrição
        - Regiões com menor IDH apresentam maiores taxas de desnutrição
        - A região Nordeste apresenta os maiores desafios em termos de segurança alimentar
        - Estados com maior população afetada nem sempre têm as maiores taxas percentuais
        - A desigualdade regional permanece significativa apesar das melhorias gerais
        """)
    
    with col2:
        st.markdown("### Recomendações por Região")
        st.markdown("""
        - **Norte e Nordeste**: Intensificar programas de segurança alimentar e nutricional
        - **Centro-Oeste**: Focar em comunidades rurais e indígenas com acesso limitado
        - **Sudeste**: Atenção às áreas periféricas urbanas com bolsões de pobreza
        - **Sul**: Monitorar impactos sazonais e climáticos na produção de alimentos
        - **Geral**: Implementar políticas públicas que considerem as especificidades regionais
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"© {datetime.now().year} Dashboard de Análise Social | Desenvolvido com Streamlit", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
