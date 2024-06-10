import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np

st.title('Segmentação (População)')

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




dadosTotal['FAIXA_POPULACAO'] = dadosTotal['POPULACAO'].apply(categorize_populacao)

#Criando o filtro
opcoes_tipo_municipio = sorted(dadosTotal['FAIXA_POPULACAO'].unique())
option = st.selectbox('Selecione o tipo de cidade', opcoes_tipo_municipio)



#selecionando os dados
dadosTotal_filtered = dadosTotal[dadosTotal['FAIXA_POPULACAO'] == option]

df_grouped = dadosTotal_filtered.groupby(['UF', 'CIDADE']).agg({
    'POPULACAO': 'max',
    'MUB': 'max',
    'RESTAURANTES': 'max'

}).reset_index()


# Adiciona a nova coluna com o cálculo
df_grouped['MUB %'] = (df_grouped['MUB'] / df_grouped['POPULACAO']) * 100.00
# Ajusta os valores da coluna COBERTURA para que não excedam 100
df_grouped['MUB %'] = df_grouped['MUB %'].clip(upper=100)

################################################################
st.subheader('População coberta', divider='rainbow')


# Obter o maior valor da coluna 'População'
maior_MUB_Perc = df_grouped['MUB %'].max()
media_MUB_Perc = df_grouped['MUB %'].median()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Maior MUB %", value=f"{maior_MUB_Perc:.2f}%")
with col2:
    st.metric(label="Média MUB %", value=f"{media_MUB_Perc:.2f}%")

st.dataframe(df_grouped,hide_index=True,use_container_width=True
)

