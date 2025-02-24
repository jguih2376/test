import pandas as pd
import streamlit as st
import yfinance as yf

# Função para carregar dados históricos dos ativos
@st.cache_data(ttl=600)
def carregar_dados(tickers, data_inicio, data_fim):
    if not tickers:
        return pd.DataFrame()

    dados = {}
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
        dados[ticker] = hist

    return pd.DataFrame(dados).dropna()

# Função para calcular valorização histórica
def calcular_valorizacao(dados, data_inicio):
    if dados.empty:
        return pd.DataFrame()
    
    df_var = pd.DataFrame(index=dados.columns)
    df_var['Último Preço (R$)'] = dados.iloc[-1]

    # Captura o preço da data de início selecionada (ou do primeiro disponível)
    preco_inicio = dados.loc[dados.index[dados.index >= pd.to_datetime(data_inicio)], :].iloc[0] if not dados.empty else None

    df_var['Desde Data Selecionada (%)'] = ((dados.iloc[-1] / preco_inicio) - 1) * 100 if preco_inicio is not None else None
    df_var['1 Dia (%)'] = ((dados.iloc[-1] / dados.iloc[-2]) - 1) * 100 if len(dados) > 1 else None
    df_var['1 Semana (%)'] = ((dados.iloc[-1] / dados.iloc[-5]) - 1) * 100 if len(dados) > 5 else None
    df_var['1 Mês (%)'] = ((dados.iloc[-1] / dados.iloc[-21]) - 1) * 100 if len(dados) > 21 else None
    df_var['1 Ano (%)'] = ((dados.iloc[-1] / dados.iloc[0]) - 1) * 100  # Comparação com o primeiro dia disponível

    return df_var.round(2)

# Interface no Streamlit
st.subheader("📊 Desempenho Histórico dos Ativos")

tickers = st.multiselect("Selecione os ativos:", ["AAPL", "GOOGL", "MSFT"], default=["AAPL", "GOOGL"])
data_inicio = st.date_input("Data de início", pd.to_datetime('2020-01-01').date())
data_fim = st.date_input("Data de término", pd.to_datetime('today').date())

if st.button("Gerar Valorização"):
    dados = carregar_dados(tickers, data_inicio, data_fim)
    
    if not dados.empty:
        df_valorizacao = calcular_valorizacao(dados, data_inicio)
        st.dataframe(df_valorizacao)
    else:
        st.warning("Nenhum dado disponível para os tickers selecionados.")
