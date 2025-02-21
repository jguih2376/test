import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.markdown('---')

# Função para carregar os dados usando yfinance
@st.cache_data


def carregar_dados(tickers, data_inicio, data_fim, tipo='acoes'):
    dados = {}
    for ticker in tickers:
            hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
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

st.subheader('Desempenho Relativo')

# Seleção de datas
data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

# Listas de tickers para cada categoria
indices = {
    'IBOV': '^BVSP',
    'S&P500': '^GSPC',     
    'NASDAQ': '^IXIC',
    'FTSE100': '^FTSE',
    'DAX': '^GDAXI',
    'CAC40': '^FCHI',
    'SSE Composite': '000001.SS',
    'Nikkei225': '^N225',
    'Merval': '^MERV'
}
commodities = {
    'Ouro': 'GC=F',
    'Prata': 'SI=F',
    'Platinum': 'PL=F',     
    'Cobre': 'HG=F',
    'WTI Oil': 'CL=F',
    'Brent Oil': 'BZ=F',
    'Milho': 'ZC=F',
    'Soja': 'ZS=F',
    'Café': 'KC=F'
}
acoes = ['ITUB4', 'BBAS3', 'ABEV3', 'WEGE3', 'RENT3', 'JBSS3', 'ELET3']
acoes_dict =  {acao: acao + '.SA' for acao in acoes}

# Dicionário de categorias
categorias = {
    'Índices': list(indices.keys()),
    'Commodities': list(commodities.keys()),
    'Ações': list(acoes_dict.keys()),
}

# Seleção de categoria
categoria_selecionada = st.radio('Selecione a categoria:', options=list(categorias.keys()))

# Seleção de ativos com base na categoria selecionada
ativos_selecionados = st.multiselect('Selecione:', options=categorias[categoria_selecionada], placeholder="Ativos")

# Carregar os dados
if categoria_selecionada == 'Índices':
    tickers = [indices[ativo] for ativo in ativos_selecionados]
elif categoria_selecionada == 'Commodities':
    tickers = [commodities[ativo] for ativo in ativos_selecionados]
else:
    tickers = ativos_selecionados

dados = carregar_dados(tickers, data_inicio, data_fim)

# Verificar se há dados carregados antes de calcular a performance
if not dados.empty:
    dados = calcular_performance(dados)

# Exibir o gráfico
if ativos_selecionados:
    fig = criar_grafico(ativos_selecionados, dados)
    st.plotly_chart(fig)
else:
    st.write('Selecione pelo menos um ativo.')
