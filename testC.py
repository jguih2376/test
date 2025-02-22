import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def carregar_dados(tickers, data_inicio, data_fim):
    dados = {}
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
        if not hist.empty:
            dados[ticker] = hist
    return pd.DataFrame(dados)

def calcular_performance(dados):
    if not dados.empty:
        return (dados / dados.iloc[0] - 1) * 100
    return dados

def criar_grafico(ativos_selecionados, dados):
    fig = go.Figure()
    for ativo in ativos_selecionados:
        fig.add_trace(go.Scatter(
            x=dados.index,
            y=dados[ativo],
            name=ativo,
            line=dict(width=1)
        ))
    fig.update_layout(
        title='Desempenho Relativo dos Ativos (%)',
        xaxis_title='Data',
        yaxis_title='Performance (%)',
        xaxis=dict(tickformat='%m/%Y'),
        legend_title='Ativo',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)'
    )
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')
    return fig

def app():
    st.title('Análise Histórica e Desempenho Relativo')

    opcao = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

    ativos = {
        'Índices': {'IBOV': '^BVSP', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI'},
        'Commodities': {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Cobre': 'HG=F', 'WTI Oil': 'CL=F'},
        'Ações': {acao: acao + '.SA' for acao in ['ALOS3', 'ABEV3', 'PETR4', 'VALE3', 'WEGE3']}
    }

    escolha = st.multiselect(f'Selecione {opcao}', list(ativos[opcao].keys()), placeholder='Escolha os ativos')
    tickers = [ativos[opcao][e] for e in escolha]

    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
    with col2:
        data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

    if tickers:
        dados = carregar_dados(tickers, data_inicio, data_fim)
        if not dados.empty:
            fig = criar_grafico(tickers, calcular_performance(dados))
            st.plotly_chart(fig)
        else:
            st.error('Nenhum dado disponível para os ativos selecionados.')
    else:
        st.info('Selecione pelo menos um ativo para análise.')

if __name__ == '__main__':
    app()
