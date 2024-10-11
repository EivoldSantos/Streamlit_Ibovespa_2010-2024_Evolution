#Importando as bibliotecas

import streamlit as st
import yfinance as yf #Yahoo Finance
import pandas as pd
from datetime import timedelta
import time

@st.cache_data
def carregar_tickers():
    base_tickers = pd.read_csv ("IBOV.csv",sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers] 
    return tickers

@st.cache_data
def carregar_dados(empresas): #carregar dados
    texto_tickers = " " .join(empresas) # Esta linha cria uma string que concatena todos os símbolos das empresas fornecidas, separando-os por um espaço vazio.
    dados_acao = yf.Tickers(texto_tickers) # yf.ticker serve para carregar os dados da ação selecionada, no caso ITUB4. O .SA serve para demarcar qual bolsa procurar, no caso a de São Paulo.
    cotacoes_de_acao = dados_acao.history(start = "2010-08-01", end="2024-09-23") #Seleciona o periodo em que os dados das ações serão selecionados.
    cotacoes_de_acao = cotacoes_de_acao["Close"] #Filtra somente o dado de fechamento da ação.
    return cotacoes_de_acao

acoes = carregar_tickers()

dados = carregar_dados(acoes)

#Criando o Sidebar
st.sidebar.write("Filtros") 

#Filtro entre as Ações

selecionar_acoes = st.sidebar.multiselect("Selecione as ações",dados.columns) #.sidebar adiciona o fitro "selecionar_acoes" ao sidebar
if selecionar_acoes:
    dados = dados[selecionar_acoes]
    if len(selecionar_acoes) == 1:
        acao_unica = selecionar_acoes[0]
        dados = dados.rename(columns= {acao_unica: "Close"})


data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()

print(data_inicial)

intervalo_tempo = st.sidebar.slider("Selecione o periodo:", 
                                    min_value=data_inicial , 
                                    max_value=data_final , 
                                    value=(data_inicial,data_final),
                                    step = timedelta( days= 30 ))

#Criar a interface do Streamlit

dados = dados.loc[intervalo_tempo[0]:intervalo_tempo[1]]

st.title("Grafico de Ações")

st.write("Gráfico abaixo demonstra a evolução das ações da Ibovespa ao longo dos anos de 2010 até os dias atuais.")#markdown

st.line_chart(dados)

st.write("""@Dados retirados da Yahoo Finance e atualizados automaticamente""")

if st.button("Me aperte"):
    msg = st.toast("Parabéns")
    time.sleep(2)
    msg.toast("Você concluiu o seu primeiro código no streamlit!")
    st.balloons()
    time.sleep(4)
    st.balloons()