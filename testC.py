import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="MarketView - Análise de Ativos", layout="wide")

st.subheader("📊 Desempenho Histórico dos Ativos")

# Cache para carregar os dados históricos (atualiza a cada 10 minutos)
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

    # Converter index do DataFrame para datetime, garantindo compatibilidade
    dados.index = pd.to_datetime(dados.index)

    # Converter data_inicio para Timestamp para evitar erro de comparação
    data_inicio_dt = pd.to_datetime(data_inicio)

    # Filtrar o primeiro dado disponível a partir da data selecionada
    dados_filtrados = dados[dados.index >= data_inicio_dt]
    
    if not dados_filtrados.empty:
        preco_inicio = dados_filtrados.iloc[0]
        df_var['Desde Data Selecionada (%)'] = ((dados.iloc[-1] / preco_inicio) - 1) * 100
    else:
        df_var['Desde Data Selecionada (%)'] = None  # Se não houver dados, evita erro

    df_var['1 Dia (%)'] = ((dados.iloc[-1] / dados.iloc[-2]) - 1) * 100 if len(dados) > 1 else None
    df_var['1 Semana (%)'] = ((dados.iloc[-1] / dados.iloc[-5]) - 1) * 100 if len(dados) > 5 else None
    df_var['1 Mês (%)'] = ((dados.iloc[-1] / dados.iloc[-21]) - 1) * 100 if len(dados) > 21 else None
    df_var['1 Ano (%)'] = ((dados.iloc[-1] / dados.iloc[0]) - 1) * 100 if len(dados) > 1 else None

    return df_var.round(2)

# Função para criar o gráfico de desempenho
def criar_grafico(ativos_selecionados, dados, normalizado=True, legenda_dict=None):
    fig = go.Figure()
    for ativo in ativos_selecionados:
        nome_ativo = legenda_dict.get(ativo, ativo)  # Usa a chave do dicionário para o nome
        y_data = ((dados[ativo] / dados[ativo].iloc[0]) - 1) * 100 if normalizado else dados[ativo]

        fig.add_trace(go.Scatter(
            x=dados.index,
            y=y_data,
            name=nome_ativo,
            mode='lines',
            line=dict(width=1.5)
        ))

        # Adicionando marcador no último ponto
        fig.add_trace(go.Scatter(
            x=[dados.index[-1]],
            y=[y_data.iloc[-1]],
            mode='markers',
            marker=dict(size=6, color='red'),
            showlegend=False
        ))

    fig.update_layout(
        title=f"{'Desempenho Relativo (%)' if normalizado else 'Preço dos Ativos'}",
        yaxis_title='Performance (%)' if normalizado else 'Preço',
        xaxis=dict(tickformat='%Y', tickvals=dados.index[::252]),
        legend_title='Ativos',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)',
        height=600,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    fig.update_yaxes(showgrid=True, gridcolor='gray', gridwidth=0.5, griddash='dot')

    return fig

# Lista de ativos disponíveis
indices = {'IBOV': '^BVSP', 'EWZ':'EWZ', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'DAX': '^GDAXI'}
commodities = {'Ouro': 'GC=F', 'Petróleo Brent': 'BZ=F', 'Milho': 'ZC=F', 'Café': 'KC=F'}
acoes = ["PETR4", "VALE3", "ITUB4", "BBAS3", "BBDC4"]
acoes_dict = {acao: acao + '.SA' for acao in acoes}

# Layout de seleção
with st.expander("Selecione os ativos e o período", expanded=True):
    opcao1 = st.selectbox('Escolha a classe de ativos:', ['Índices', 'Ações', 'Commodities'])
    
    with st.form(key='selecao_ativos'):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            if opcao1 == 'Índices':
                escolha = st.multiselect('Selecione os índices:', list(indices.keys()), placeholder='Índices')
                ticker = [indices[indice] for indice in escolha]
                legenda_dict = {v: k for k, v in indices.items()}

            elif opcao1 == 'Commodities':
                escolha = st.multiselect('Selecione as commodities:', list(commodities.keys()), placeholder='Commodities')
                ticker = [commodities[commodity] for commodity in escolha]
                legenda_dict = {v: k for k, v in commodities.items()}

            elif opcao1 == 'Ações':
                escolha = st.multiselect('Selecione as ações:', list(acoes_dict.keys()), placeholder='Ações')
                ticker = [acoes_dict[acao] for acao in escolha]
                legenda_dict = {v: k for k, v in acoes_dict.items()}

        with col2:
            data_inicio = st.date_input('Data de início', pd.to_datetime('2020-01-01').date())

        with col3:
            data_fim = st.date_input('Data de término', pd.to_datetime('today').date())

        normalizado = st.checkbox("Exibir desempenho percentual", value=True)
        submit_button = st.form_submit_button(label='Gerar Gráfico')

if submit_button and ticker:
    dados = carregar_dados(ticker, data_inicio, data_fim)

    if not dados.empty:
        fig = criar_grafico(ticker, dados, normalizado, legenda_dict)
        st.plotly_chart(fig)

        df_valorizacao = calcular_valorizacao(dados, data_inicio)
        st.dataframe(df_valorizacao)

    else:
        st.warning("Nenhum dado disponível para os tickers selecionados.")
