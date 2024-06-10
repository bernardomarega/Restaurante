import streamlit as st
import pandas as pd

st.title('Dados')

# Leitura do CSV
dados = pd.read_csv('dataset/DADOS_IFOOD_MUNICIPIO.csv', encoding='latin1', delimiter=';')


#####################################################################################
st.subheader('Descrição', divider='rainbow')

# Exemplo de texto com quebras de linha
texto = """
 - Restaurantes existentes: Foram obtidos 17 milhões de CNPJ da Receita Federal o que corresponde a 30% da base real para serem usados como cobertura de restaurantes
 - Restaurantes cadastrados no Ifood: Considerando o site do Ifood que indica que existem 300mil restaurantes cadastrados, gerei uma amostra da base da Receita de 30% dos 300mil para simular os restaurantes
 - Pedidos: foram simulados dados de pedidos para 3 meses para cada cidade
 - Cidade e UF: os dados de população foram obtidos do IBGE
 - Renda: geração aleátoria para cada cidade nos valores de 1mil, 2mil e 3mil
 - As outras informações foram geração aleatória (MUB, LEADS, etc)

 """

# Exibir o texto no Streamlit com quebras de linha
st.markdown(texto)

#####################################################################################
st.subheader('Amostra', divider='rainbow')

st.dataframe(dados.head(10))

#####################################################################################
st.subheader('Descrição', divider='rainbow')

st.dataframe(dados.describe())

#####################################################################################
st.subheader('UF e Cidade', divider='rainbow')


cidades_distintas_por_uf = dados.groupby('UF')['CIDADE'].nunique().reset_index()
st.dataframe(cidades_distintas_por_uf)

