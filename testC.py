import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.markdown('---')

@st.cache_data
def carregar_dados(tickers, data_inicio, data_fim):
    if not tickers:
        return pd.DataFrame()
    
    dados = yf.download(tickers, start=data_inicio, end=data_fim)['Adj Close']
    
    # Se apenas um ativo for selecionado, garantir que seja DataFrame
    if isinstance(dados, pd.Series):
        dados = dados.to_frame()
    
    return dados

def calcular_performance(dados):
    return ((dados / dados.iloc[0]) - 1) * 100 if not dados.empty else dados

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
        xaxis=dict(tickformat='%Y'),
        legend_title='Ativo',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)' ,
        heigth=600
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
        escolha = st.multiselect('Índice', list(indices.keys()), placeholder='Selecione ativos')
        ticker = [indices[indice] for indice in escolha]

    elif opcao1 == 'Commodities':
        escolha = st.multiselect('Commodities', list(commodities.keys()), placeholder='Selecione ativos')
        ticker = [commodities[commodity] for commodity in escolha]

    elif opcao1 == 'Ações':
        escolha = st.multiselect('Ações', list(acoes_dict.keys()), placeholder='Selecione ativos')
        ticker = [acoes_dict[acao] for acao in escolha]

with col2:
    data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date())
with col3:
    data_fim = st.date_input('Data de término', pd.to_datetime('today').date())

# Verificar se há ativos selecionados antes de carregar os dados
if ticker:
    dados = carregar_dados(ticker, data_inicio, data_fim)
    
    if not dados.empty:
        fig = criar_grafico(ticker, calcular_performance(dados))
        st.plotly_chart(fig)
    else:
        st.warning("Nenhum dado disponível para os ativos selecionados.")
else:
    st.info("Selecione ao menos um ativo para exibir o gráfico.")
