import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.markdown('---')

# Função para carregar os dados usando yfinance
@st.cache_data(ttl=600)  # Cache atualizado a cada 10 min
def carregar_dados(tickers, data_inicio, data_fim):
    if not tickers:
        return pd.DataFrame()
    
    dados = {}
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
        dados[ticker] = hist
    
    return pd.DataFrame(dados).dropna()  # Remove valores NaN

def calcular_performance(dados):
    if not dados.empty:
        return (dados / dados.iloc[0] - 1) * 100
    return dados

def criar_grafico(ativos_selecionados, dados, normalizado=True, legenda_dict=None):
    fig = go.Figure()
    for ativo in ativos_selecionados:
        nome_ativo = legenda_dict.get(ativo, ativo)  # Usa a chave do dicionário para o nome
        fig.add_trace(go.Scatter(
            x=dados.index,
            y=calcular_performance(dados)[ativo] if normalizado else dados[ativo],
            name=nome_ativo,  # Utiliza a chave do dicionário na legenda
            line=dict(width=1)
        ))

    fig.update_layout(
        title=f"{'Desempenho Relativo (%)' if normalizado else 'Preço dos Ativos'}",
        xaxis_title='Data',
        yaxis_title='Performance (%)' if normalizado else 'Preço',
        xaxis=dict(tickformat='%m/%Y'),
        legend_title='Ativo',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)'
    )
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')

    return fig

st.subheader('Desempenho Relativo')

opcao1 = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

indices = {'IBOV': '^BVSP', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI', 
        'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}

commodities = {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platina': 'PL=F', 'Cobre': 'HG=F', 'WTI Oil': 'CL=F', 
            'Brent Oil': 'BZ=F', 'Milho': 'ZC=F', 'Soja': 'ZS=F', 'Café': 'KC=F'}


acoes = [
    "PETR3", "PETR4", "VALE3", "ITUB3", "ITUB4", "BBDC3", "BBDC4", 
    "ABEV3", "BBAS3", "B3SA3", "SANB11", "WEGE3", "BPAC11", "SUZB3", 
    "GGBR4", "ELET3", "ELET6", "RENT3", "JBSS3", "MGLU3"
]


acoes_dict = {acao: acao + '.SA' for acao in acoes}

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    if opcao1 == 'Índices':
        escolha = st.multiselect('Índice', list(indices.keys()), placeholder='Ativos')
        ticker = [indices[indice] for indice in escolha]
        legenda_dict = {v: k for k, v in indices.items()}  # Inverte o dicionário para a legenda

    elif opcao1 == 'Commodities':
        escolha = st.multiselect('Commodities', list(commodities.keys()), placeholder='Ativos')
        ticker = [commodities[commodity] for commodity in escolha]
        legenda_dict = {v: k for k, v in commodities.items()}  # Inverte o dicionário para a legenda

    elif opcao1 == 'Ações':
        escolha = st.multiselect('Ações', list(acoes_dict.keys()), placeholder='Ativos')
        ticker = [acoes_dict[acao] for acao in escolha]
        legenda_dict = {v: k for k, v in acoes_dict.items()}  # Inverte o dicionário para a legenda

with col2:
    data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
with col3:
    data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

# Opção para visualizar valores normalizados ou brutos
normalizado = st.checkbox("Exibir desempenho percentual", value=True)

# Carregar os dados reais
if ticker:
    dados = carregar_dados(ticker, data_inicio, data_fim)
    if not dados.empty:
        fig = criar_grafico(ticker, dados, normalizado, legenda_dict)
        st.plotly_chart(fig)
    else:
        st.warning("Nenhum dado disponível para os tickers selecionados.")
else:
    st.info("Selecione pelo menos um ativo para exibir os dados.")
