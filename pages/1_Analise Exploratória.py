import streamlit as st
import pandas as pd

st.title('Análise Exploratória')

# Leitura do CSV
dados = pd.read_csv('dataset/DADOS_IFOOD_MUNICIPIO.csv', encoding='latin1', delimiter=';')
dados['DATA'] = pd.to_datetime(dados['ANOMES'].astype(str), format='%Y%m')

#################################################
st.subheader('Qual é o número de restaurantes (absoluto) que foram reativados por mês?', divider='rainbow')

soma = dados['REATIVACAO'].sum()

# Agrupar por mês e somar o campo 'reativacao'
resultado = dados.groupby(dados['DATA'].dt.to_period('M'))['REATIVACAO'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=soma)
with col2:
    st.dataframe(resultado)


#################################################

st.subheader('Qual é o número de restaurantes (absoluto) que deram churn por mês?', divider='rainbow')

soma = dados['CHURN'].sum()

# Agrupar por mês e somar o campo 'reativacao'
resultado = dados.groupby(dados['DATA'].dt.to_period('M'))['CHURN'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=soma)
with col2:
    st.dataframe(resultado)

#################################################

st.subheader('Qual é o número de restaurantes ativos por mês?', divider='rainbow')

soma = dados['RESTAURANTES'].sum()


# Agrupar por mês e somar o campo 'reativacao'
resultado = dados.groupby(dados['DATA'].dt.to_period('M'))['RESTAURANTES'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=soma)
with col2:
    st.dataframe(resultado)

#####################################################################################
st.subheader('Qual é a média de mub no primeiro quartil?', divider='rainbow')


# Calcula o primeiro quartil (Q1)
Q1 = dados['MUB'].quantile(0.25)

# Filtra os dados até o primeiro quartil
dados_primeiro_quartil = dados[dados['MUB'] <= Q1]

# Calcula a média da população no primeiro quartil
media_primeiro_quartil = dados_primeiro_quartil['MUB'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=f"{media_primeiro_quartil:.2f}")

#####################################################################################
st.subheader('Qual é a média de pedidos no terceiro quartil do mub?', divider='rainbow')

# Calcula o quartil
Q2 = dados['MUB'].quantile(0.50)
Q3 = dados['MUB'].quantile(0.75)

# Filtra os dados até o primeiro quartil
dados_terceiro_quartil = dados[(dados['MUB'] > Q2) & (dados['MUB'] <= Q3)]

# Calcula a média da população no primeiro quartil
media_pedidos_3_quartil = dados_terceiro_quartil['PEDIDOS'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=f"{media_pedidos_3_quartil:.2f}")

