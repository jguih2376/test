import streamlit as st
import plotly.graph_objects as go
from bcb import sgs

@st.cache_data
def get_data():
    selic = sgs.get({'Selic': 432}, start='2000-01-01')
    selic_atual = selic.iloc[-1].values[0]
    ipca = sgs.get({'IPCA': 13522}, start='2000-01-01')
    ipca_atual = ipca.iloc[-1].values[0]
    
    # Calculando juros reais
    juros_reais = selic - ipca
    juros_reais_atual = juros_reais.iloc[-1].values[0]
    
    return selic, selic_atual, ipca, ipca_atual, juros_reais, juros_reais_atual

def app():
    st.title("Estatística Monetária")

    # Obtendo dados com cache
    selic, selic_atual, ipca, ipca_atual, juros_reais, juros_reais_atual = get_data()

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
            plot_bgcolor='rgba(211, 211, 211, 0.15)'
        )
        fig_selic.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False, range=[0, fig_selic.data[0]['y'].max() * 1.1])
        fig_selic.update_xaxes(showgrid=False, zeroline=False)

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
            xaxis_title='Data',
            showlegend=False,
            plot_bgcolor='rgba(211, 211, 211, 0.15)'
        )
        fig_ipca.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False, range=[0, fig_ipca.data[0]['y'].max() * 1.1])
        fig_ipca.update_xaxes(showgrid=False, zeroline=False)

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

        # Criando gráfico do Juro Real
        fig_juros_reais = go.Figure()
        fig_juros_reais.add_trace(go.Scatter(x=juros_reais.index, y=juros_reais.iloc[:, 0], mode='lines'))
        fig_juros_reais.add_trace(go.Scatter(x=[juros_reais.index[-1]], y=[juros_reais_atual], mode='markers', marker=dict(color='red', size=5)))

        fig_juros_reais.update_layout(
            title='Juro Real (SELIC - IPCA)',
            title_x=0.4, 
            yaxis_title='Juro Real (%)',
            xaxis_title='Data',
            showlegend=False,
            plot_bgcolor='rgba(211, 211, 211, 0.15)'
        )
        fig_juros_reais.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False, range=[juros_reais.iloc[:, 0].min() * 1.1, juros_reais.iloc[:, 0].max() * 1.1])
        fig_juros_reais.update_xaxes(showgrid=False, zeroline=False)

        fig_juros_reais.add_annotation(
            x=juros_reais.index[-1], 
            y=juros_reais_atual,
            text=f'{juros_reais_atual:.2f}%',
            showarrow=True,
            arrowhead=0,
            ax=20,
            ay=-40,
            bordercolor='yellow'
        )

        # Exibindo os gráficos no Streamlit
        st.plotly_chart(fig_selic)
        st.plotly_chart(fig_ipca)
        st.plotly_chart(fig_juros_reais)

    with col2:
        st.write('')
        st.write('')

        iframe_code = """
        <div style="text-align: center; padding: 10px; font-family: sans-serif;">
            <span style="font-size: 16px; font-weight: bold; display: block; margin-bottom: 8px; color: white;">Mundo</span>
            <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
            src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
            header_bg=ffffff&header_text=FFFFFF&force_lang=12" align="center"></iframe>
        </div>
        """
        
        st.components.v1.html(iframe_code, height=180)
