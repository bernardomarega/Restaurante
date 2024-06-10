import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Correlação')

# Leitura do CSV para um DataFrame do Pandas
dados = pd.read_csv('dataset/DADOS_IFOOD_MUNICIPIO.csv', encoding='latin1', delimiter=';')

def interpretar_correlacao(valor_correlacao):
    if 0.00 <= abs(valor_correlacao) <= 0.19:
        return "Uma correlação bem fraca"
    elif 0.20 <= abs(valor_correlacao) <= 0.39:
        return "Uma correlação fraca"
    elif 0.40 <= abs(valor_correlacao) <= 0.69:
        return "Uma correlação moderada"
    elif 0.70 <= abs(valor_correlacao) <= 0.89:
        return "Uma correlação forte"
    elif 0.90 <= abs(valor_correlacao) <= 1.00:
        return "Uma correlação muito forte"
    else:
        return "Valor de correlação fora do intervalo esperado"




###############################################################################################

st.subheader('Existe alguma correlação entre pedidos e número de restaurantes?', divider='rainbow')


correlacao = dados[['RESTAURANTES', 'PEDIDOS']].corr(method='pearson')
valor_correlacao = correlacao.loc['RESTAURANTES', 'PEDIDOS']

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=f"{valor_correlacao:.4f}")
    st.write(f"Interpretação: {interpretar_correlacao(valor_correlacao)}")

with col2:
    # Exibir a correlação
    st.write("Matriz de Correlação:")
    st.dataframe(correlacao)

fig, ax = plt.subplots()
ax.scatter(dados['RESTAURANTES'], dados['PEDIDOS'])
ax.set_xlabel('RESTAURANTES')
ax.set_ylabel('PEDIDOS')
ax.set_title('Gráfico de Dispersão entre RESTAURANTES e PEDIDOS')

st.pyplot(fig)


###############################################################################################

st.subheader('Existe alguma correlação entre a renda média da região e o mub?', divider='rainbow')


correlacao = dados[['RENDA', 'MUB']].corr(method='pearson')
valor_correlacao = correlacao.loc['RENDA', 'MUB']

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Resposta", value=valor_correlacao)
    st.write(f"Interpretação: {interpretar_correlacao(valor_correlacao)}")

with col2:
    # Exibir a correlação
    st.write("Matriz de Correlação:")
    st.dataframe(correlacao)

fig, ax = plt.subplots()
ax.scatter(dados['RENDA'], dados['MUB'])
ax.set_xlabel('RENDA')
ax.set_ylabel('MUB')
ax.set_title('Gráfico de Dispersão entre RENDA e MUB')

st.pyplot(fig)