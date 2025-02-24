import streamlit as st
import plotly.graph_objects as go
from bcb import sgs
import requests

@st.cache_data
def get_data():
    try:
        # Tentando obter dados do Banco Central (SGS)
        dolar = sgs.get({'Dólar': 10813}, start='2000-01-01')
        dolar_atual = dolar.iloc[-1].values[0]
        
        selic = sgs.get({'Selic': 432}, start='2000-01-01')
        selic_atual = selic.iloc[-1].values[0]
        
        ipca = sgs.get({'IPCA': 13522}, start='2000-01-01')
        ipca_atual = ipca.iloc[-1].values[0]

        # Calcular juros real
        juros_real = ((1 + selic_atual) / (1 + ipca_atual)) - 1
        
        return selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual
    
    except requests.exceptions.RequestException as e:
        st.error(f"Ocorreu um erro ao tentar obter os dados: {e}")
        return None  # Ou algum valor de fallback, dependendo da lógica
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None  # Ou algum valor de fallback


st.title("🏛️ Estatística Monetária")

# Obtendo dados com cache
result = get_data()
if result:
    selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual = result
else:
    st.stop()  # Se não obter os dados, interrompe a execução

col1, col2 = st.columns([5, 1])

with col1:
    # Criando gráfico interativo da Selic
    fig_selic = go.Figure()
    fig_selic.add_trace(go.Scatter(x=selic.index, y=selic['Selic'], mode='lines'))
    fig_selic.add_trace(go.Scatter(x=[selic.index[-1]], y=[selic_atual], mode='markers', marker=dict(color='red', size=5)))

    fig_selic.update_layout(
        title='Taxa de Juros SELIC',
        title_x=0.4, 
        yaxis_title='Taxa de Juros (%)',
        showlegend=False,
        plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro
    )
    fig_selic.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False,  range=[0, fig_selic.data[0]['y'].max() * 1.1])
    fig_selic.update_xaxes(showgrid=False, zeroline=False)

    # Adicionando anotação para destacar o valor atual
    fig_selic.add_annotation(
        x=selic.index[-1], 
        y=selic_atual,
        text=f'{selic_atual:.2f}%',
        showarrow=True,
        arrowhead=0,
        ax=20,
        ay=-40,
        bordercolor='yellow'
    )
    
    # Criando gráfico interativo do IPCA
    fig_ipca = go.Figure()
    fig_ipca.add_trace(go.Scatter(x=ipca.index, y=ipca['IPCA'], mode='lines'))
    fig_ipca.add_trace(go.Scatter(x=[ipca.index[-1]], y=[ipca_atual], mode='markers', marker=dict(color='red', size=5)))

    fig_ipca.update_layout(
        title='IPCA Acumulado 12M',
        title_x=0.4, 
        yaxis_title='IPCA acumulado (%)',
        showlegend=False,
        plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro
    )
    fig_ipca.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False, range=[0, fig_ipca.data[0]['y'].max() * 1.1])
    fig_ipca.update_xaxes(showgrid=False, zeroline=False)

    # Adicionando anotação para destacar o valor atual
    fig_ipca.add_annotation(
        x=ipca.index[-1], 
        y=ipca_atual,
        text=f'{ipca_atual:.2f}%',
        showarrow=True,
        arrowhead=0,
        ax=20,
        ay=-40,
        bordercolor='yellow'
    )

    # Exibindo os gráficos com o Streamlit
    st.plotly_chart(fig_selic)
    st.plotly_chart(fig_ipca)

with col2:
    st.write('')
    st.write('')

    # Exibindo o iframe com alinhamento ajustado
    iframe_code = """
    <div style="text-align: center; padding: 10px; font-family: sans-serif;">
        <span style="font-size: 16px; font-weight: bold; display: block; margin-bottom: 8px; color: white;">Mundo</span>
        <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
        src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
        header_bg=ffffff&header_text=FFFFFF&force_lang=12" align="center"></iframe>
    </div>
    """
    st.components.v1.html(iframe_code, height=180)

with col1:
    # Criando gráfico interativo do Dólar
    fig_dolar = go.Figure()

    # Linha do dólar ao longo do tempo
    fig_dolar.add_trace(go.Scatter(
        x=dolar.index, 
        y=dolar['Dólar'], 
        mode='lines',
        width=1),
        name="Cotação do Dólar"
    )

    # Ponto final destacado
    fig_dolar.add_trace(go.Scatter(
        x=[dolar.index[-1]], 
        y=[dolar_atual], 
        mode='markers', 
        marker=dict(color='red', size=8),
        name="Última cotação"
    ))

    # Layout do gráfico
    fig_dolar.update_layout(
        title='💵 Cotação do Dólar',
        title_x=0.4,  # Centraliza melhor o título
        yaxis_title='Valor em R$',
        showlegend=False,
        plot_bgcolor='rgba(211, 211, 211, 0.15)',  # Fundo mais claro para facilitar leitura
    )

    # Ajustes nos eixos
    fig_dolar.update_yaxes(
        showgrid=True, 
        gridwidth=0.1, 
        gridcolor='gray',
        griddash='dot', 
        zeroline=False,  
        range=[dolar['Dólar'].min() * 0.9, dolar['Dólar'].max() * 1.1]  # Ajuste dinâmico do eixo Y
    )

    fig_dolar.update_xaxes(showgrid=False, zeroline=False)

    # Adicionando anotação para destacar o valor atual
    fig_dolar.add_annotation(
        x=dolar.index[-1], 
        y=dolar_atual,
        text=f'R${dolar_atual:.2f}',
        showarrow=True,
        arrowhead=0,
        ax=20,
        ay=-40,
        bordercolor='yellow'
    )

    st.plotly_chart(fig_dolar)
