import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.markdown('---')

# Função para carregar os dados usando yfinance
@st.cache_data
def carregar_dados(tickers, data_inicio, data_fim):
    if not tickers:
        return pd.DataFrame()
    dados = {}
    for ticker in tickers:
        try:
            hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
            if not hist.empty:
                dados[ticker] = hist
        except Exception as e:
            st.warning(f"Erro ao carregar {ticker}: {e}")
    return pd.DataFrame(dados)

# Função para calcular a performance em percentual
def calcular_performance(dados):
    return (dados / dados.iloc[0] - 1) * 100 if not dados.empty else dados

# Função para criar o gráfico
def criar_grafico(ativos_selecionados, dados):
    fig = go.Figure()
    for ativo in ativos_selecionados:
        if ativo in dados:
            fig.add_trace(go.Scatter(
                x=dados.index,
                y=dados[ativo],
                name=ativo,
                line=dict(width=1)
            ))
    legend_names = {ativos_selecionados[i]: list(dados.columns)[i] for i in range(len(ativos_selecionados))}
    fig.update_layout(
        title='Desempenho Relativo dos Ativos (%)',
        xaxis_title='Data',
        yaxis_title='Performance (%)',
        xaxis=dict(tickformat='%m/%Y'),
        legend_title='Ativo',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)',
        legend=dict(traceorder='normal',
                    itemsizing='trace',
                    font=dict(size=10))
    )
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')
    return fig

st.subheader('Desempenho Relativo')
opcao1 = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

indices = {'IBOV': '^BVSP', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI',
           'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}

commodities = {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platina': 'PL=F', 'Cobre': 'HG=F', 'WTI Oil': 'CL=F',
               'Brent Oil': 'BZ=F', 'Milho': 'ZC=F', 'Soja': 'ZS=F', 'Café': 'KC=F'}

acoes = ['ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4',
         'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3',
         'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3',
         'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4',
         'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3',
         'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4',
         'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3',
         'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']

acoes_dict = {acao: acao + '.SA' for acao in acoes}
col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    if opcao1 == 'Índices':
        escolha = st.multiselect('Índice', list(indices.keys()), placeholder='Ativos')
        ticker = [indices[indice] for indice in escolha]
    elif opcao1 == 'Commodities':
        escolha = st.multiselect('Commodities', list(commodities.keys()), placeholder='Ativos')
        ticker = [commodities[commodity] for commodity in escolha]
    elif opcao1 == 'Ações':
        escolha = st.multiselect('Ações', list(acoes_dict.keys()), placeholder='Ativos')
        ticker = [acoes_dict[acao] for acao in escolha]
    else:
        escolha, ticker = [], []

with col2:
    data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
with col3:
    data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

# Carregar os dados reais
dados = carregar_dados(ticker, data_inicio, data_fim)
if not dados.empty:
    fig = criar_grafico(ticker, calcular_performance(dados))
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado disponível para os tickers selecionados.")
