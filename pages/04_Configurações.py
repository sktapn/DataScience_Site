import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Configurações | Dashboard Social",
    page_icon="⚙️",
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
    
    /* Configurações */
    .settings-section {{
        background-color: {current_theme["card"]};
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }}
    
    /* Tema */
    .theme-preview {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }}
    .color-sample {{
        width: 100px;
        height: 50px;
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 500;
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

# Cabeçalho da página
st.markdown('<div class="page-header">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Configurações</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Configurações do Dashboard
st.markdown("## Configurações do Dashboard")

# Abas para diferentes configurações
tab1, tab2, tab3 = st.tabs(["Aparência", "Dados", "Sobre"])

with tab1:
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown("### Tema do Dashboard")
    
    # Seletor de tema
    theme_options = {
        "profissional": "🔵 Profissional",
        "elegante": "🟣 Elegante",
        "moderno": "🟢 Moderno"
    }
    
    selected_theme = st.selectbox(
        "Escolha um tema para o dashboard",
        options=list(theme_options.keys()),
        format_func=lambda x: theme_options[x],
        index=list(theme_options.keys()).index(st.session_state['theme']),
        key="theme_settings"
    )
    
    # Mostrar preview do tema
    st.markdown("#### Preview do Tema")
    st.markdown('<div class="theme-preview">', unsafe_allow_html=True)
    
    # Cores primárias
    st.markdown(f'<div class="color-sample" style="background-color: {themes[selected_theme]["primary"]}">Primária</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="color-sample" style="background-color: {themes[selected_theme]["secondary"]}">Secundária</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="color-sample" style="background-color: {themes[selected_theme]["accent"]}; color: {themes[selected_theme]["text"]}">Destaque</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar tema
    if st.button("Aplicar Tema") and selected_theme != st.session_state['theme']:
        st.session_state['theme'] = selected_theme
        st.success(f"Tema {theme_options[selected_theme]} aplicado com sucesso!")
        st.rerun()
    
    st.markdown("### Outras Configurações de Aparência")
    
    # Modo escuro
    enable_dark_mode = st.toggle("Habilitar modo escuro (em desenvolvimento)", value=False, disabled=True)
    
    # Tamanho da fonte
    font_size = st.select_slider(
        "Tamanho da fonte",
        options=["Pequeno", "Médio", "Grande"],
        value="Médio",
        disabled=True
    )
    
    st.info("Mais opções de personalização estarão disponíveis em breve!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown("### Configurações de Dados")
    
    # Upload de dados
    st.markdown("#### Carregar Novos Dados")
    st.markdown("Faça upload de um arquivo CSV ou Excel com seus próprios dados.")
    
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Carregar os dados
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
            
            # Mostrar preview dos dados
            st.markdown("#### Preview dos Dados")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Opções de processamento
            st.markdown("#### Opções de Processamento")
            
            process_data = st.checkbox("Processar dados automaticamente", value=True)
            replace_existing = st.checkbox("Substituir dados existentes", value=False)
            
            if st.button("Salvar Dados"):
                st.success("Dados salvos com sucesso! O dashboard será atualizado na próxima vez que for carregado.")
                # Aqui você implementaria a lógica para salvar os dados
        
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
    
    # Configurações de cache
    st.markdown("#### Configurações de Cache")
    
    cache_ttl = st.slider(
        "Tempo de vida do cache (minutos)",
        min_value=5,
        max_value=60,
        value=30,
        step=5
    )
    
    if st.button("Limpar Cache"):
        st.success("Cache limpo com sucesso!")
        # Aqui você implementaria a lógica para limpar o cache
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown("### Sobre o Dashboard")
    
    st.markdown("""
    #### Dashboard de Análise Social
    
    **Versão:** 1.0.0
    
    **Desenvolvido por:** Sua Equipe
    
    **Descrição:** Este dashboard foi desenvolvido para análise de indicadores sociais, com foco em desnutrição, distribuição regional e análise racial.
    
    **Tecnologias utilizadas:**
    - Streamlit
    - Pandas
    - Plotly
    - Python
    
    **Contato:** seu.email@exemplo.com
    """)
    
    st.markdown("#### Documentação")
    
    st.markdown("""
    Para mais informações sobre como utilizar este dashboard, consulte a documentação completa:
    
    - [Guia do Usuário](#)
    - [Documentação Técnica](#)
    - [FAQ](#)
    """)
    
    st.markdown("#### Licença")
    
    st.markdown("""
    Este projeto está licenciado sob a licença MIT.
    
    Copyright (c) 2023 Sua Equipe
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Exportar configurações
st.markdown("## Exportar Configurações")

with st.container():
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    
    st.markdown("Você pode exportar suas configurações atuais para usar em outras instâncias do dashboard.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exportar Configurações"):
            # Criar um dicionário com as configurações
            config = {
                "theme": st.session_state['theme'],
                "cache_ttl": cache_ttl,
                "dark_mode": enable_dark_mode,
                "font_size": font_size,
                "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Converter para JSON
            config_json = json.dumps(config, indent=4)
            
            # Exibir para download
            st.download_button(
                label="Baixar Configurações",
                data=config_json,
                file_name="dashboard_config.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("#### Importar Configurações")
        config_file = st.file_uploader("Carregar arquivo de configurações", type=["json"])
        
        if config_file is not None:
            try:
                # Carregar configurações
                config = json.load(config_file)
                
                # Exibir configurações
                st.json(config)
                
                if st.button("Aplicar Configurações Importadas"):
                    # Aplicar configurações
                    if "theme" in config:
                        st.session_state['theme'] = config["theme"]
                    
                    st.success("Configurações aplicadas com sucesso!")
                    st.rerun()
            
            except Exception as e:
                st.error(f"Erro ao carregar configurações: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"© {datetime.now().year} Dashboard de Análise Social | Desenvolvido com Streamlit", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
