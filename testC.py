import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.express as px

# Função para carregar dados
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
def calcular_valorizacao(dados):
    if dados.empty:
        return pd.DataFrame()
    
    df_var = pd.DataFrame(index=dados.columns)
    df_var['Último Preço'] = dados.iloc[-1]
    
    # Retornos considerando períodos específicos
    df_var['1 Dia (%)'] = ((dados.iloc[-1] / dados.iloc[-2]) - 1) * 100 if len(dados) > 1 else None
    df_var['1 Semana (%)'] = ((dados.iloc[-1] / dados.iloc[-5]) - 1) * 100 if len(dados) > 5 else None
    df_var['1 Mês (%)'] = ((dados.iloc[-1] / dados.iloc[-21]) - 1) * 100 if len(dados) > 21 else None
    df_var['1 Ano (%)'] = ((dados.iloc[-1] / dados.iloc[0]) - 1) * 100  # Comparação com o início da amostra
    
    return df_var.round(2)

# Função para exibir gráfico de barras
def exibir_grafico_valorizacao(df_valorizacao):
    fig = px.bar(df_valorizacao.T, title="Valorização Histórica (%)", labels={"index": "Ativo", "value": "Valorização (%)"})
    fig.update_layout(barmode='group', xaxis_title="Ativos", yaxis_title="Valorização (%)", showlegend=False)
    st.plotly_chart(fig)

# Simulação de seleção no Streamlit
st.subheader("Desempenho Histórico dos Ativos")

# Seleção de tickers e datas
tickers = st.multiselect("Selecione os ativos:", ["AAPL", "GOOGL", "MSFT"], default=["AAPL", "GOOGL"])
data_inicio = st.date_input("Data de início", pd.to_datetime('2020-01-01').date())
data_fim = st.date_input("Data de término", pd.to_datetime('today').date())

# Botão para gerar a valorização
if st.button("Gerar Valorização"):
    dados = carregar_dados(tickers, data_inicio, data_fim)
    if not dados.empty:
        # Calcular valorização
        df_valorizacao = calcular_valorizacao(dados)
        st.dataframe(df_valorizacao)
        # Exibir gráfico de barras
        exibir_grafico_valorizacao(df_valorizacao)
    else:
        st.warning("Nenhum dado disponível para os tickers selecionados.")
