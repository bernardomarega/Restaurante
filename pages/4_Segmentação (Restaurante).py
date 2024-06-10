import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np

st.title('Segmentação (Restaurante)')

# Leitura do CSV
dadosTotal = pd.read_csv('dataset/DADOS_IFOOD_MUNICIPIO.csv', encoding='latin1', delimiter=';')

cutoff_value = 10 # % ideal de resturantes por cidade



########################
def categorize_populacao(pop):
    if pop < 200000:
        return 'a) 0-200.000 habitantes'
    elif pop < 400000:
        return 'b) 200.000-400.000 habitantes'
    elif pop < 600000:
        return 'c) 400.000-600.000 habitantes'
    elif pop < 800000:
        return 'd) 600.000-800.000 habitantes'
    elif pop < 1000000:
        return 'e) 800.000-1.000.000 habitantes'
    else:
        return 'f) 1.000.000+ habitantes'

################################################################
st.subheader('Restaurantes da Receita Federal x Clientes', divider='rainbow')


dadosTotal['FAIXA_POPULACAO'] = dadosTotal['POPULACAO'].apply(categorize_populacao)

#Criando o filtro
opcoes_tipo_municipio = sorted(dadosTotal['FAIXA_POPULACAO'].unique())
option = st.selectbox('Selecione o tipo de cidade', opcoes_tipo_municipio)



#selecionando os dados
dadosTotal_filtered = dadosTotal[dadosTotal['FAIXA_POPULACAO'] == option]

df_grouped = dadosTotal_filtered.groupby(['UF', 'CIDADE']).agg({
    'RECEITA_RESTAURANTE_ATIVO': 'max',
    'RESTAURANTES': 'max',
    'POPULACAO': 'mean'
}).reset_index()

# Adiciona a nova coluna com o cálculo
df_grouped['COBERTURA'] = (df_grouped['RESTAURANTES'] / df_grouped['RECEITA_RESTAURANTE_ATIVO']) * 100.00
# Ajusta os valores da coluna COBERTURA para que não excedam 100
df_grouped['COBERTURA'] = df_grouped['COBERTURA'].clip(upper=100)

# Cria as colunas de flag
df_grouped['FLAG_COBERTURA_00_20'] = df_grouped['COBERTURA'].apply(lambda x: 1 if 0 <= x <= 20 else 0)
df_grouped['FLAG_COBERTURA_20_40'] = df_grouped['COBERTURA'].apply(lambda x: 1 if 20 < x <= 40 else 0)
df_grouped['FLAG_COBERTURA_40_60'] = df_grouped['COBERTURA'].apply(lambda x: 1 if 40 < x <= 60 else 0)
df_grouped['FLAG_COBERTURA_60_80'] = df_grouped['COBERTURA'].apply(lambda x: 1 if 60 < x <= 80 else 0)
df_grouped['FLAG_COBERTURA_80_100'] = df_grouped['COBERTURA'].apply(lambda x: 1 if x > 80 else 0)

#renomeando a coluna
df_grouped = df_grouped.rename(columns={'RECEITA_RESTAURANTE_ATIVO': 'POTENCIAL'})

#mudando a ordem
new_order = ['UF', 'CIDADE', 'COBERTURA', 'POTENCIAL', 'RESTAURANTES', 'POPULACAO']
df_grouped = df_grouped[new_order]


# Conta o número de registros no DataFrame
num_cidades = df_grouped.shape[0]

# Cidades abaixo do Cuteoff
num_cidades_abaixo = df_grouped[df_grouped['COBERTURA'] <= cutoff_value]['CIDADE'].nunique()

num_cidades_abaixo_Perc = (num_cidades_abaixo/num_cidades)*100.00 


# Cidades acima do Cuteoff
num_cidades_acim_Perc = 100.00 - num_cidades_abaixo_Perc



# Calcula o valor médio da coluna COBERTURA, ignorando valores infinitos se houver
media_cobertura = df_grouped.replace([np.inf, -np.inf], np.nan)['COBERTURA'].mean()


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Cidades", value=num_cidades)
with col2:
    st.metric(label="Cobertura desejada", value=f"{cutoff_value:.2f}%")
with col3:
    st.metric(label="Cobertura média", value= f"{media_cobertura:.2f}%")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Cidades abaixo da cobertura desejada", value=f"{num_cidades_abaixo_Perc:.2f}%")
with col2:
    st.metric(label="Cidades acima da cobertura desejada", value=f"{num_cidades_acim_Perc:.2f}%")


#Resultado na tela
st.data_editor(
    df_grouped,
    column_config={
        "COBERTURA": st.column_config.ProgressColumn(
            "COBERTURA",
            help="Cobertura",
            format="%d",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    use_container_width=True
)

################################################################
st.subheader('População coberta', divider='rainbow')



