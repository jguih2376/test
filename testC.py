import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.write('---')
# Título da página
st.subheader("Desempenho Relativo dos Ativos")

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
def criar_grafico(ativos_selecionados, dados, normalizado=True, legenda_dict=None):
    fig = go.Figure()
    for ativo in ativos_selecionados:
        nome_ativo = legenda_dict.get(ativo, ativo)  # Usa a chave do dicionário para o nome
        # Dados normalizados ou brutos
        y_data = calcular_performance(dados)[ativo] if normalizado else dados[ativo]

        # Adicionando linha do gráfico
        fig.add_trace(go.Scatter(
            x=dados.index,
            y=y_data,
            name=nome_ativo,  # Utiliza a chave do dicionário na legenda
            mode='lines',  # Apenas a linha
            line=dict(width=1)
        ))

        # Adicionando bolinha no último ponto
        fig.add_trace(go.Scatter(
            x=[dados.index[-1]],  # Último ponto do gráfico
            y=[y_data.iloc[-1]],  # Último valor
            mode='markers',
            marker=dict(size=5, color='red', symbol='circle'),
            name=f'{nome_ativo} - Último Preço',
            showlegend=False
        ))

    # Ajustando a data do eixo X para intervalo de 1 ano
    fig.update_layout(
        title=f"{'Desempenho Relativo (%)' if normalizado else 'Preço dos Ativos'}",
        yaxis_title='Performance (%)' if normalizado else 'Preço',
        xaxis=dict(
            tickformat='%Y',  # Exibe o ano
            tickmode='array',  # Define um modo de marcação personalizada
            tickvals=dados.index[::252],  # Marca um ponto a cada 252 dias (aproximadamente 1 ano de pregão)
        ),
        legend_title='Ativos',
        legend_orientation='h',
        plot_bgcolor='rgba(211, 211, 211, 0.15)',
        height=600,
        margin=dict(r=10)  # Ajusta a margem à direita
    )
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')

    return fig

# Opções de seleção para ativos
indices = {'IBOV': '^BVSP','EWZ':'EWZ', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI',
        'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}

commodities = {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platinum': 'PL=F', 'Cobre': 'HG=F', 'WTI Oil':'CL=F', 'Brent Oil':'BZ=F',
            'Gasolina':'RB=F', 'Gás Natural':'NG=F', 'Gado Vivo':'LE=F', 'Porcos Magros':'LE=F', 'Milho':'ZC=F',
            'Soja':'ZS=F', 'Cacau':'CC=F', 'Café':'KC=F'}

acoes = ["PETR4", "VALE3","ITUB4", "BBAS3", "BBDC4", "RAIZ4","PRIO3", "VBBR3", "CSAN3", "UGPA3", "BPAC11", "SANB11",
        "GGBR4", "CSNA3", "USIM5", "JBSS3", "ABEV3", "MRFG3", "BRFS3", "BEEF3", "ELET3", "NEOE3", "CPFE3", "ENGI11",
        "EQTL3", "SUZB3", "KLBN11", "DTEX3", "RANI3", "MRFG3", "CYRE3", "MRVE3", "EZTC3", "CVCB3", "TRIS3", "WEGE3", "B3SA3"]

acoes_dict = {acao: acao + '.SA' for acao in acoes}

# Layout para selecionar os ativos e definir o período dentro do expander
with st.expander('...', expanded=True):
    # Seleção de opções
    opcao1 = st.selectbox('Selecione:', ['Índices', 'Ações', 'Commodities'])
    with st.form(key='meu_form'):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            if opcao1 == 'Índices':
                escolha = st.multiselect('', list(indices.keys()), placeholder='Índices')
                ticker = [indices[indice] for indice in escolha]
                legenda_dict = {v: k for k, v in indices.items()}  # Inverte o dicionário para a legenda

            elif opcao1 == 'Commodities':
                escolha = st.multiselect('', list(commodities.keys()), placeholder='Commodities')
                ticker = [commodities[commodity] for commodity in escolha]
                legenda_dict = {v: k for k, v in commodities.items()}  # Inverte o dicionário para a legenda

            elif opcao1 == 'Ações':
                escolha = st.multiselect('', list(acoes_dict.keys()), placeholder='Ações')
                ticker = [acoes_dict[acao] for acao in escolha]
                legenda_dict = {v: k for k, v in acoes_dict.items()}  # Inverte o dicionário para a legenda

        with col2:
            data_inicio = st.date_input('Data de início', pd.to_datetime('2020-01-01').date(), format='DD/MM/YYYY')

        with col3:
            data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

        # Adicionando o checkbox para desempenho percentual
        normalizado = st.checkbox("Exibir desempenho percentual", value=True)

        # Submissão do formulário
        submit_button = st.form_submit_button(label='Gerar Gráfico')

    # Carregar os dados reais e mostrar o gráfico quando o botão for pressionado
    if submit_button and ticker:

        dados = carregar_dados(ticker, data_inicio, data_fim)
        if not dados.empty:
            fig = criar_grafico(ticker, dados, normalizado, legenda_dict)
            st.plotly_chart(fig)
            df_valorizacao = calcular_valorizacao(dados)
            st.dataframe(df_valorizacao)
        else:
            st.warning("Nenhum dado disponível para os tickers selecionados.")