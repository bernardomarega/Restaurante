import streamlit as st
import pandas as pd
import altair as alt

st.title('Receita Federal (Abertura)')

# Leitura do CSV
dados = pd.read_csv('dataset/DADOS_ABERTURA.csv', encoding='latin1', delimiter=';')


#####################################################################################
st.subheader('CNPJ abertos de restaurantes', divider='rainbow')

dados['MES'] = pd.to_datetime(dados['MES_ABERTURA'].astype(str), format='%Y%m')

# Filtrar os meses a partir de 202301
df_filtered = dados[dados['MES'] >= '2023-01-01']

# Criar o gráfico de barras com Altair
chart = alt.Chart(df_filtered).mark_bar(size=20).encode(
    x=alt.X('MES:T', axis=alt.Axis(format='%Y-%m', title='Mês')),
    y=alt.Y('QTDE:Q', title='Quantidade')
).properties(
    title='Quantidade por Mês'
)
# Exibir o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)


