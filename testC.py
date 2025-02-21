import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.markdown('---')

# Função para carregar os dados usando yfinance
@st.cache_data
def carregar_dados(tickers, data_inicio, data_fim):
    # Função para carregar os dados usando yfinance
    dados = {}
    for ticker in tickers:
        hist = yf.Ticker(ticker + '.SA').history(start=data_inicio, end=data_fim)['Close']
        dados[ticker] = hist
    return pd.DataFrame(dados)

def calcular_performance(dados):
    # Função para calcular a performance em percentual
    if not dados.empty:
        return (dados / dados.iloc[0] - 1) * 100
    return dados

def criar_grafico(ativos_selecionados, dados):
    # Função para criar o gráfico
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
        plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro   
    )
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')

    return fig

st.subheader('Desempenho Relativo')

# Seleção de datas
data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

# Listas de tickers para cada categoria
tickers_indices = ['IBOV', 'IFNC']
tickers_commodities = ['PETR4', 'VALE3']
tickers_acoes = ['ITUB4', 'BBAS3', 'ABEV3', 'WEGE3', 'RENT3', 'JBSS3', 'ELET3']

# Dicionário de categorias
categorias = {
    'Índices': tickers_indices,
    'Commodities': tickers_commodities,
    'Ações': tickers_acoes
}

# Seleção de categoria
categoria_selecionada = st.radio('Selecione a categoria:', options=list(categorias.keys()))

# Seleção de ativos com base na categoria selecionada
ativos_selecionados = st.multiselect('Selecione:', options=categorias[categoria_selecionada], placeholder="Ativos")

# Carregar os dados
tickers = categorias[categoria_selecionada]
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
