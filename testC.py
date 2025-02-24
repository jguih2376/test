import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

st.title('📉 Análise Histórica')

st.subheader('Retorno Mensal')
with st.expander('...', expanded=True):
    opcao = st.radio('Selecione:', ['Índices', 'Ações', 'Commodities'])

    with st.form(key='form_ativo'):
        if opcao == 'Índices':
            indices = {
                'IBOV': '^BVSP', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE',
                'DAX': '^GDAXI', 'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225',
                'Merval': '^MERV'
            }
            escolha = st.selectbox('', list(indices.keys()), index=0)
            ticker = indices[escolha]

        elif opcao == 'Commodities':
            commodities = {
                'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platina': 'PL=F', 'Cobre': 'HG=F',
                'WTI Oil': 'CL=F', 'Brent Oil': 'BZ=F', 'Gasolina': 'RB=F', 'Gás Natural': 'NG=F',
                'Gado Vivo': 'LE=F', 'Porcos Magros': 'HE=F',  # Corrigido
                'Milho': 'ZC=F', 'Soja': 'ZS=F', 'Cacau': 'CC=F', 'Café': 'KC=F'
            }
            escolha = st.selectbox('', list(commodities.keys()))
            ticker = commodities[escolha]

        elif opcao == 'Ações':
            acoes = [
                'ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 
                'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 
                'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 
                'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'EQTL3', 'FLRY3', 
                'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 'ITSA4', 
                'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 
                'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 
                'PSSA3', 'RADL3', 'RAIZ4', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 
                'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 
                'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3'
            ]
            acoes_dict = {acao: acao + '.SA' for acao in acoes}
            escolha = st.selectbox('', list(acoes_dict.keys()))
            ticker = acoes_dict[escolha]

        analisar = st.form_submit_button('Analisar')

    if analisar:
        data_inicial = '1999-12-01'
        data_final = '2030-12-31'

        # Baixa os dados do Yahoo Finance
        dados = yf.download(ticker, start=data_inicial, end=data_final, interval="1mo")

        if not dados.empty:
            retornos = dados['Close'].pct_change().dropna()
            retornos = retornos.reset_index()
            retornos['Year'] = retornos['Date'].dt.year
            retornos['Month'] = retornos['Date'].dt.month

            tabela_retornos = retornos.pivot(index='Year', columns='Month', values='Close')
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                       'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            tabela_retornos['Anual'] = (1 + tabela_retornos).prod(axis=1) - 1  # Ajustado

            # Heatmap
            fig, ax = plt.subplots(figsize=(12, 9))
            cmap = sns.color_palette('RdYlGn', as_cmap=True)
            sns.heatmap(
                tabela_retornos.drop(columns='Anual'), cmap=cmap, annot=True, fmt='.2%',
                center=0, vmax=retornos.max().max(), vmin=retornos.min().min(),
                linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax
            )
            ax.set_title(f'Heatmap Retorno Mensal - {escolha}', fontsize=18)
            st.pyplot(fig)

            # Exibir tabela de retornos
            st.write(tabela_retornos)

            # Estatísticas
            stats = tabela_retornos.describe().T
            stats['Positivos'] = tabela_retornos.gt(0).sum() / tabela_retornos.count()
            stats['Negativos'] = tabela_retornos.le(0).sum() / tabela_retornos.count()

            # Heatmap estatístico
            fig, ax = plt.subplots(figsize=(12, 2))
            sns.heatmap(stats[['mean', '50%', 'max', 'min']].T, cmap=cmap, annot=True, fmt='.2%',
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            st.pyplot(fig)

        else:
            st.error("Erro ao buscar os dados. Verifique o ticker ou tente novamente mais tarde.")
