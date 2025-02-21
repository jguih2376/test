import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.markdown('---')

# Função para carregar os dados usando yfinance
@st.cache_data
def carregar_dados(tickers, data_inicio, data_fim):
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

# Lista predefinida de tickers (ações brasileiras)
tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBAS3.SA', 'ABEV3.SA', 'WEGE3.SA', 'RENT3.SA', 'JBSS3.SA', 'ELET3.SA']

# Carregar os dados
dados = carregar_dados(tickers, data_inicio, data_fim)

# Verificar se há dados carregados antes de calcular a performance
if not dados.empty:
    dados = calcular_performance(dados)

# Criação do componente multiselect
ativos_selecionados = st.multiselect('Selecione:', options=tickers, placeholder="Ativos")

# Exibir o gráfico
if ativos_selecionados:
    fig = criar_grafico(ativos_selecionados, dados)
    st.plotly_chart(fig)
else:
    st.write('Selecione pelo menos um ativo.')

with st.expander('Seleção Adicional', expanded=True):
    opcao = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

    if opcao == 'Índices':
        indices = {'IBOV': '^BVSP',
                    'S&P500': '^GSPC',     
                    'NASDAQ': '^IXIC',
                    'FTSE100':'^FTSE',
                    'DAX':'^GDAXI',
                    'CAC40':'^FCHI',
                    'SSE Composite':'000001.SS',
                    'Nikkei225':'^N225',
                    'Merval':'^MERV'}
        with st.form(key='form_indice'):
            escolha = st.selectbox('Índice', list(indices.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = indices[escolha]

    elif opcao == 'Commodities':
        commodities = {'Ouro': 'GC=F',
                    'Prata': 'SI=F',
                    'Platinum': 'PL=F',     
                    'Cobre': 'HG=F',
                    'WTI Oil':'CL=F',
                    'Brent Oil':'BZ=F',
                    'Milho':'ZC=F',
                    'Soja':'ZS=F',
                    'Café':'KC=F'}    
        with st.form(key='form_commodities'):
            escolha = st.selectbox('Commodities', list(commodities.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = commodities[escolha]

    elif opcao == 'Ações':
        acoes = ['ALOS3.SA', 'ABEV3.SA', 'ASAI3.SA', 'AURE3.SA', 'AMOB3.SA', 'AZUL4.SA', 'AZZA3.SA', 'B3SA3.SA', 'BBSE3.SA', 'BBDC3.SA', 'BBDC4.SA', 
                'BRAP4.SA', 'BBAS3.SA', 'BRKM5.SA', 'BRAV3.SA', 'BRFS3.SA', 'BPAC11.SA', 'CXSE3.SA', 'CRFB3.SA', 'CCRO3.SA', 'CMIG4.SA', 'COGN3.SA', 
                'CPLE6.SA', 'CSAN3.SA', 'CPFE3.SA', 'CMIN3.SA', 'CVCB3.SA', 'CYRE3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENGI11.SA', 'ENEV3.SA', 
                'EGIE3.SA', 'EQTL3.SA', 'FLRY3.SA', 'GGBR4.SA', 'GOAU4.SA', 'NTCO3.SA', 'HAPV3.SA', 'HYPE3.SA', 'IGTI11.SA', 'IRBR3.SA', 'ISAE4.SA', 
                'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'KLBN11.SA', 'RENT3.SA', 'LREN3.SA', 'LWSA3.SA', 'MGLU3.SA', 'POMO4.SA', 'MRFG3.SA', 'BEEF3.SA', 
                'MRVE3.SA', 'MULT3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'RECV3.SA', 'PRIO3.SA', 'PETZ3.SA', 'PSSA3.SA', 'RADL3.SA', 'RAIZ4.SA', 
                'RDOR3.SA', 'RAIL3.SA', 'SBSP3.SA', 'SANB11.SA', 'STBP3.SA', 'SMTO3.SA', 'CSNA3.SA', 'SLCE3.SA', 'SUZB3.SA', 'TAEE11.SA', 'VIVT3.SA', 
                'TIMS3.SA', 'TOTS3.SA', 'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VAMO3.SA', 'VBBR3.SA', 'VIVA3.SA', 'WEGE3.SA', 'YDUQ3.SA']

        acoes_dict = {acao: acao for acao in acoes}

        with st.form(key='form_acoes'):
            escolha = st.selectbox('Ações', list(acoes_dict.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = acoes_dict[escolha]

