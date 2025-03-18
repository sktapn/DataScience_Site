import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

@st.cache_data
def load_sample_data():
    """
    Carrega dados de exemplo para o dashboard.
    Em um ambiente de produção, esta função carregaria dados reais de um banco de dados ou API.
    
    Returns:
        pandas.DataFrame: DataFrame contendo os dados de exemplo.
    """
    # Verificar se existem dados reais para carregar
    data_path = "data/dados_reais.csv"
    if os.path.exists(data_path):
        try:
            return pd.read_csv(data_path)
        except Exception as e:
            st.warning(f"Erro ao carregar dados reais: {e}. Usando dados de exemplo.")
    
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

@st.cache_data
def load_racial_data():
    """
    Carrega dados de exemplo específicos para análise racial.
    
    Returns:
        pandas.DataFrame: DataFrame contendo os dados de exemplo para análise racial.
    """
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

@st.cache_data
def load_nutrition_data():
    """
    Carrega dados de exemplo específicos para análise de desnutrição.
    
    Returns:
        pandas.DataFrame: DataFrame contendo os dados de exemplo para análise de desnutrição.
    """
    # Criar dados mais detalhados para análise de desnutrição
    regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    years = list(range(2018, 2023))
    age_groups = ['0-5 anos', '6-10 anos', '11-14 anos', '15-17 anos', 'Adultos']
    nutrition_types = ['Desnutrição Aguda', 'Desnutrição Crônica', 'Baixo Peso', 'Deficiência de Micronutrientes']
    
    # Criar DataFrame base
    data = []
    
    for region in regions:
        for year in years:
            for age in age_groups:
                for nutrition_type in nutrition_types:
                    # Definir taxas base por tipo de desnutrição
                    if nutrition_type == 'Desnutrição Aguda':
                        base_rate = 8.0
                    elif nutrition_type == 'Desnutrição Crônica':
                        base_rate = 12.0
                    elif nutrition_type == 'Baixo Peso':
                        base_rate = 10.0
                    else:  # Deficiência de Micronutrientes
                        base_rate = 15.0
                    
                    # Ajustar por faixa etária
                    if age == '0-5 anos':
                        age_factor = 1.5
                    elif age == '6-10 anos':
                        age_factor = 1.2
                    elif age == '11-14 anos':
                        age_factor = 1.0
                    elif age == '15-17 anos':
                        age_factor = 0.8
                    else:  # Adultos
                        age_factor = 0.6
                    
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
                    rate = base_rate * age_factor * regional_factor * (1 - yearly_reduction)
                    
                    # Calcular população afetada (baseado em uma população fictícia)
                    base_pop = 50000 if age == 'Adultos' else 20000
                    pop_affected = int(base_pop * age_factor * regional_factor * (1 - 0.03 * (year - 2018)))
                    
                    # Adicionar dados
                    data.append({
                        'Região': region,
                        'Ano': year,
                        'Faixa_Etária': age,
                        'Tipo_Desnutrição': nutrition_type,
                        'Taxa': rate,
                        'População_Afetada': pop_affected,
                        'Custo_Tratamento': pop_affected * (50 if nutrition_type == 'Desnutrição Aguda' else 30),
                        'Impacto_Educacional': 0.8 if age in ['6-10 anos', '11-14 anos', '15-17 anos'] else 0,
                        'Impacto_Saúde': rate * 0.2
                    })
    
    return pd.DataFrame(data)

def save_data(df, filename="dados_salvos.csv"):
    """
    Salva os dados em um arquivo CSV.
    
    Args:
        df (pandas.DataFrame): DataFrame a ser salvo.
        filename (str, optional): Nome do arquivo. Defaults to "dados_salvos.csv".
    
    Returns:
        bool: True se o salvamento for bem-sucedido, False caso contrário.
    """
    try:
        # Criar diretório de dados se não existir
        os.makedirs("data", exist_ok=True)
        
        # Salvar dados
        df.to_csv(f"data/{filename}", index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return False

def format_number(value, prefix="", suffix="", decimal_places=0):
    """
    Formata um número com prefixo, sufixo e casas decimais.
    
    Args:
        value (float): Valor a ser formatado.
        prefix (str, optional): Prefixo (ex: "R$"). Defaults to "".
        suffix (str, optional): Sufixo (ex: "%"). Defaults to "".
        decimal_places (int, optional): Número de casas decimais. Defaults to 0.
    
    Returns:
        str: Número formatado.
    """
    if decimal_places == 0:
        formatted = f"{prefix}{int(value):,}{suffix}".replace(",", ".")
    else:
        formatted = f"{prefix}{value:,.{decimal_places}f}{suffix}".replace(",", ".")
    
    return formatted

def calculate_change(current, previous):
    """
    Calcula a variação percentual entre dois valores.
    
    Args:
        current (float): Valor atual.
        previous (float): Valor anterior.
    
    Returns:
        float: Variação percentual.
    """
    if previous == 0:
        return 0
    
    return ((current - previous) / previous) * 100
