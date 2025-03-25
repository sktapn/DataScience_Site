import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Bibliotecas de ML
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer


# ------------------------------------------------------------------------------
# Funções auxiliares de recodificação (para o Índice de Desenvolvimento)
# ------------------------------------------------------------------------------
def recode_alimentos(valor):
    # Foco nos casos "Sim, sempre" (1.0) e "Sim, quase sempre" (0.5); senão 0.0
    if isinstance(valor, str):
        if "Sim, sempre" in valor:
            return 1.0
        elif "Sim, quase sempre" in valor:
            return 0.5
    return 0.0

def recode_tosse(valor):
    # "não" => 1.0 (melhor), "sim" => 0.0 (pior)
    if isinstance(valor, str):
        val = valor.strip().lower()
        if val == "não":
            return 1.0
        elif val == "sim":
            return 0.0
    return 0.0

def recode_cozinha(valor):
    # "sim" => 1.0, "não" => 0.0
    if isinstance(valor, str):
        val = valor.strip().lower()
        if val == "sim":
            return 1.0
        elif val == "não":
            return 0.0
    return 0.0


def main():
    st.title("App de Análise e Treinamento - Streamlit")

    st.write("""
    **Este aplicativo** demonstra:
    1. Carregamento de CSV,
    2. Pré-processamento e mapeamento,
    3. Treinamento de modelo (RandomForest) e GridSearch,
    4. Geração de diversos **gráficos** (catplot, histograma, heatmap, boxplot),
    5. Salvando o modelo final em arquivo .pkl.
    """)

    # --------------------------------------------------------------------------
    # 1) Carregar CSV (via upload)
    # --------------------------------------------------------------------------
    st.header("1) Carregar o Dataset")
    data_file = st.file_uploader("Envie o arquivo CSV (ex: Dataset_13_02.csv)", type=["csv"])
    if data_file is not None:
        df = pd.read_csv(data_file)
        st.success("Arquivo carregado com sucesso!")
        st.write("Primeiras linhas do dataset:")
        st.dataframe(df.head())
    else:
        st.info("Aguardando arquivo CSV...")
        st.stop()

    # --------------------------------------------------------------------------
    # 2) Mostrar contagens básicas (colunas categóricas)
    # --------------------------------------------------------------------------
    st.header("2) Contagem de Colunas Categóricas")
    cat_cols = df.select_dtypes(include="object").columns
    if st.checkbox("Exibir contagem de todas as colunas categóricas?"):
        for coluna in cat_cols:
            st.write(f"### Contagem para {coluna}:")
            st.write(df[coluna].value_counts())

    # --------------------------------------------------------------------------
    # 3) Geração dos SCORES e do ÍNDICE (antes de mapear para o modelo)
    # --------------------------------------------------------------------------
    st.header("3) Cálculo de Índice de Desenvolvimento (alimentos_score, tosse_score, cozinha_score)")
    df['alimentos_score'] = df['Alimentos Básicos'].apply(recode_alimentos)
    df['tosse_score'] = df['Presença de Tosse'].apply(recode_tosse)
    df['cozinha_score'] = df['Possui Cozinha'].apply(recode_cozinha)
    df['indice_desenvolvimento'] = df[['alimentos_score','tosse_score','cozinha_score']].mean(axis=1)

    st.write("### Amostra dos SCORES:")
    st.dataframe(df[['Alimentos Básicos','Presença de Tosse','Possui Cozinha',
                     'alimentos_score','tosse_score','cozinha_score','indice_desenvolvimento']].head())

    # --------------------------------------------------------------------------
    # 4) Geração de GRÁFICOS
    #    (catplot facetado, histograma, heatmap, boxplot)
    # --------------------------------------------------------------------------
    st.header("4) Visualizações Importantes")

    if st.checkbox("Gerar e exibir gráficos?"):
        # (A) Catplot facetado (Região, Nível Escolaridade, Faixa de Renda, Cor Pessoa)
        st.subheader("4.1) Catplot Facetado do Índice de Desenvolvimento")

        # Evitar erro caso colunas não existam
        # Agrupamos por 4 colunas se existirem:
        group_info = []
        if 'Região' in df.columns:
            df_regiao = df.groupby('Região')['indice_desenvolvimento'].mean().reset_index()
            df_regiao['dimensao'] = 'Região'
            df_regiao.rename(columns={'Região': 'categoria','indice_desenvolvimento': 'indice_medio'}, inplace=True)
            group_info.append(df_regiao)

        if 'Nivel Escolaridade' in df.columns:
            df_escolaridade = df.groupby('Nivel Escolaridade')['indice_desenvolvimento'].mean().reset_index()
            df_escolaridade['dimensao'] = 'Nível Escolaridade'
            df_escolaridade.rename(columns={'Nivel Escolaridade': 'categoria','indice_desenvolvimento': 'indice_medio'}, inplace=True)
            group_info.append(df_escolaridade)

        if 'Faixa de Renda' in df.columns:
            df_renda = df.groupby('Faixa de Renda')['indice_desenvolvimento'].mean().reset_index()
            df_renda['dimensao'] = 'Faixa de Renda'
            df_renda.rename(columns={'Faixa de Renda': 'categoria','indice_desenvolvimento': 'indice_medio'}, inplace=True)
            group_info.append(df_renda)

        if 'Cor Pessoa' in df.columns:
            df_cor = df.groupby('Cor Pessoa')['indice_desenvolvimento'].mean().reset_index()
            df_cor['dimensao'] = 'Cor Pessoa'
            df_cor.rename(columns={'Cor Pessoa': 'categoria','indice_desenvolvimento': 'indice_medio'}, inplace=True)
            group_info.append(df_cor)

        if len(group_info) > 0:
            df_final = pd.concat(group_info, ignore_index=True)
            media_geral = df_final['indice_medio'].mean()

            fig_cat = sns.catplot(
                data=df_final,
                x='indice_medio',
                y='categoria',
                col='dimensao',
                kind='strip',
                height=4,
                sharex=False
            )
            fig_cat.set_titles("{col_name}")
            for ax in fig_cat.axes.flat:
                ax.axvline(media_geral, linestyle='--', color='red')
                ax.set_xlabel("Índice de Desenvolvimento Médio")
                ax.tick_params(axis='y', labelsize=8)
            fig_cat.fig.subplots_adjust(left=0.3, wspace=0.4)
            fig_cat.fig.suptitle("Índice de Desenvolvimento por Dimensão", y=1.05, fontsize=14)

            st.pyplot(fig_cat.fig)
        else:
            st.write("Não foi possível gerar o catplot facetado (colunas necessárias não encontradas).")

        # (B) Histograma do índice
        st.subheader("4.2) Histograma do Índice de Desenvolvimento")
        fig_hist, ax_hist = plt.subplots()
        ax_hist.hist(df["indice_desenvolvimento"], bins=10)
        ax_hist.set_title("Distribuição do Índice de Desenvolvimento")
        ax_hist.set_xlabel("Índice de Desenvolvimento")
        ax_hist.set_ylabel("Frequência")
        st.pyplot(fig_hist)

        # (C) Heatmap de correlação (scores e índice)
        st.subheader("4.3) Heatmap de Correlação (scores e índice)")
        colunas_corr = ["alimentos_score", "tosse_score", "cozinha_score", "indice_desenvolvimento"]
        # Checamos se elas existem
        colunas_existentes = [c for c in colunas_corr if c in df.columns]
        if len(colunas_existentes) == len(colunas_corr):
            corr = df[colunas_existentes].corr()
            fig_corr, ax_corr = plt.subplots()
            sns.heatmap(corr, annot=True, fmt=".2f", ax=ax_corr)
            ax_corr.set_title("Matriz de Correlação (Scores vs Índice)")
            st.pyplot(fig_corr)
        else:
            st.write("Colunas necessárias para heatmap não encontradas.")

        # (D) Boxplot (exemplo: alimentos_score vs indice)
        st.subheader("4.4) Boxplot do Índice vs. alimentos_score")
        if 'alimentos_score' in df.columns:
            fig_box, ax_box = plt.subplots()
            sns.boxplot(x=df["alimentos_score"], y=df["indice_desenvolvimento"], ax=ax_box)
            ax_box.set_title("Boxplot do Índice de Desenvolvimento por 'alimentos_score'")
            ax_box.set_xlabel("alimentos_score (0=ruim, 0.5=parcial, 1=bom)")
            ax_box.set_ylabel("Índice de Desenvolvimento")
            st.pyplot(fig_box)
        else:
            st.write("Coluna alimentos_score não encontrada.")


    # --------------------------------------------------------------------------
    # 5) Mapeamento e Pré-processamento para o Modelo
    # --------------------------------------------------------------------------
    st.header("5) Treinamento do Modelo (RandomForest)")
    if st.checkbox("Executar Treinamento e Otimização do Modelo?"):
        st.write("Iniciando pré-processamento para o modelo...")

        # 5.1) Criação de colunas binárias de Benefícios
        beneficio_map = {
            "A": "Programa Bolsa Família (PBF)",
            "B": "Benefício de Prestação Continuada (BPC/LOAS)",
            "C": "Bolsa ou benefício da Prefeitura Municipal",
            "D": "Bolsa ou benefício do Governo do Estado",
            "E": "Pensão",
            "F": "Aposentadoria",
            "G": "Outro benefício"
        }
        df["Beneficios"] = df["Beneficios"].astype(str).str.strip()
        for codigo in beneficio_map.keys():
            df[f"Beneficio_{codigo}"] = df["Beneficios"].apply(lambda x: 1 if codigo in x else 0)
        df["Total_Beneficios"] = df[[f"Beneficio_{c}" for c in beneficio_map.keys()]].sum(axis=1)

        # 5.2) Mapeamentos
        mapeamento = {
            "Região": {"Norte": 1, "Nordeste": 2, "Sudeste": 3, "Sul": 4, "Centro-Oeste": 5},
            "Sexo": {"Masculino": 1, "Feminino": 2},
            "Tipo de Domicílio": {"Casa": 1, "Apartamento": 2, "Outros": 3},
            "Possui Cozinha": {"Sim": 1, "Não": 0},
            "Ocupação": {
                "Próprio de algum morador - já pago": 1,
                "Próprio de algum morador - ainda pagando": 2,
                "Alugado": 3,
                "Cedido por empregador": 4,
                "Cedido de outra forma": 5,
                "Outra condição": 6
            },
            "Situação do Registro": {"Urbano": 1, "Rural": 2},
            "Presença de Tosse": {"Sim": 1, "Não": 2, "Não sabe/ não quis responder": 9},
            "Tipo de Respiração": {"Sim": 1, "Não": 2, "Não sabe/ não quis responder": 9},
            "Alimentos Básicos": {
                "Não": 1, "Sim, raramente": 2, "Sim, às vezes": 3,
                "Sim, quase sempre": 4, "Sim, sempre": 5,
                "Não se cozinha em casa": 6
            },
            "Nivel Escolaridade": {
                "Sem estudo": 0,
                "1° ano do ensino fundamental": 1,
                "1ª série/ 2°ano do ensino fundamental": 2,
                "2ª série/ 3°ano do ensino fundamental": 3,
                "3ª série/ 4°ano do ensino fundamental": 4,
                "4ª série/ 5°ano do ensino fundamental": 5,
                "5ª série/ 6°ano do ensino fundamental": 6,
                "6ª série/ 7°ano do ensino fundamental": 7,
                "7ª série/ 8°ano do ensino fundamental": 8,
                "8ª série/ 9°ano do ensino fundamental": 9,
                "1°ano do ensino médio": 10,
                "2°ano do ensino médio": 11,
                "3°ano do ensino médio": 12,
                "Ensino superior incompleto": 13,
                "Ensino superior completo": 14
            },
            "Faixa de Renda": {
                "Sem renda": 1, "Até R$ 1.000,00": 2, "De R$ 1.001,00 até R$ 2.000,00": 3,
                "De R$ 2.001,00 até R$ 3.000,00": 4, "De R$ 3.001,00 até R$ 5.000,00": 5,
                "De R$ 5.001,00 até R$ 10.000,00": 6, "R$ 10.001,00 ou mais": 7
            },
            "Cor Pessoa": {
                "Branca": 1, "Preta": 2,
                "Amarela (origem japonesa, chinesa, coreana etc.)": 3,
                "Parda (mulata, cabocla, cafuza, mameluca ou mestiça)": 4,
                "Indígena": 5,
                "Não sabe/não quis responder": 9
            }
        }

        # Ajuste para "Idade em Meses", se existir
        if "Idade em Meses" in df.columns:
            df["Idade em Meses"] = (
                df["Idade em Meses"]
                .astype(str)
                .str.replace("meses", "")
                .str.strip()
            )
            df["Idade em Meses"] = pd.to_numeric(df["Idade em Meses"], errors="coerce")

        for col_map, dic_map in mapeamento.items():
            if col_map in df.columns:
                df[col_map] = df[col_map].map(dic_map).fillna(9)

        # Verificar dados faltantes
        faltantes = df.isnull().sum()
        st.write("**Dados faltantes após mapeamento**:")
        st.write(faltantes)

        # ----------------------------------------------------------------------
        # Preparação para treinamento
        # ----------------------------------------------------------------------
        # Tratar 'Presença de Tosse'
        imputer_y = SimpleImputer(strategy='most_frequent')
        if 'Presença de Tosse' not in df.columns:
            st.error("Coluna 'Presença de Tosse' não está no dataset!")
            st.stop()
        df['Presença de Tosse'] = imputer_y.fit_transform(df[['Presença de Tosse']]).ravel()

        # Definir X e y
        drop_cols = ['Presença de Tosse', 'Data de Nascimento']
        for c in drop_cols:
            if c not in df.columns:
                drop_cols.remove(c)

        X = df.drop(columns=drop_cols, axis=1)
        y = df['Presença de Tosse']

        numeric_columns = X.select_dtypes(include=['int64','float64']).columns
        categorical_columns = X.select_dtypes(include=['object']).columns

        # Imputers
        imputer_numeric = SimpleImputer(strategy='mean')
        X[numeric_columns] = imputer_numeric.fit_transform(X[numeric_columns])

        imputer_categorical = SimpleImputer(strategy='most_frequent')
        X[categorical_columns] = imputer_categorical.fit_transform(X[categorical_columns])

        for col_ in categorical_columns:
            le = LabelEncoder()
            X[col_] = le.fit_transform(X[col_].astype(str))

        # Balanceamento
        smote = SMOTE(random_state=42)
        X_balanced, y_balanced = smote.fit_resample(X, y)

        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, y_balanced, test_size=0.2, random_state=42
        )

        st.write(f"**X_train**: {X_train.shape}, **X_test**: {X_test.shape}")

        # ----------------------------------------------------------------------
        # 5.1) Modelo SEM ajustes
        # ----------------------------------------------------------------------
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        st.write("### Acurácia do modelo (sem ajustes):", acc)
        st.text("Classification Report (sem ajustes):")
        st.text(classification_report(y_test, y_pred))

        # ----------------------------------------------------------------------
        # 5.2) GridSearch
        # ----------------------------------------------------------------------
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        }
        st.write("Realizando GridSearchCV... (pode levar tempo)")

        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42),
            param_grid,
            cv=5,
            scoring='accuracy'
        )
        grid_search.fit(X_train, y_train)

        st.write("**Melhores parâmetros**:", grid_search.best_params_)

        # 5.3) Modelo com melhores parâmetros
        best_model = grid_search.best_estimator_
        best_model.fit(X_train, y_train)
        joblib.dump(best_model, 'modelo_melhorado.pkl')

        y_pred_improved = best_model.predict(X_test)
        acc_improved = accuracy_score(y_test, y_pred_improved)
        st.write("### Acurácia do modelo (otimizado):", acc_improved)
        st.text("Classification Report (otimizado):")
        st.text(classification_report(y_test, y_pred_improved))

        # Exemplo de uso do modelo (pegando 1 amostra do X_test)
        novo_dado = X_test.iloc[0].to_frame().T
        previsao = best_model.predict(novo_dado)
        st.write(f"**Predição para exemplo de teste**: {'Sim' if previsao[0] == 1 else 'Não'}")
        st.success("Treinamento e otimização concluídos! Modelo salvo em 'modelo_melhorado.pkl'.")


if __name__ == "__main__":
    main()
