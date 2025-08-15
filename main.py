import streamlit as st
import pandas as pd

st.set_page_config(page_title='Finanças', page_icon='💰')

st.markdown("""
# Boas Vindas!

## Nosso APP Finançeiro!            

""")

# Widget de upload de dados
file_upload = st.file_uploader(label='Faça upload dos dados aqui:', type=['csv'])

# Verifica se algum arquivo foi feito upload
if file_upload:
    
    # Leitura dos dados
    df = pd.read_csv(file_upload)
    df['Data'] = pd.to_datetime(df['Data'], format = '%d/%m/%Y').dt.date

    # Exibição dos dados no App
    exp1 = st.expander('Dados Brutos')
    columns_fmt = {'Valor': st.column_config.NumberColumn('Valor', format='R$ %f')}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    # Visão Instituição
    exp2 = st.expander('Instituições')
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')

    # Abas para diferente visualizações
    tab_data, tab_history, tab_share = exp2.tabs(['Dados', 'Histórico', 'Distribuição'])
    
    # Exibe DataFrame
    with tab_data:
        st.dataframe(df_instituicao)

    # Exibe Histórico
    with tab_history:    
        st.line_chart(df_instituicao)

    # Exibe Distribuição
    with tab_share:

        # Filtro de data
        # date = st.date_input('Data para Distribuição', 
        #                     min_value=df_instituicao.index.min(),
        #                     max_value=df_instituicao.index.max())
        
        # if date not in df_instituicao.index:
        #     st.warning('Entre com uma data válida')

        # else:
        #     # Obtem a última data
        #     #last_dt = df_instituicao.sort_index().iloc[-1]
        #     st.bar_chart(df_instituicao.loc[date])
        
        
        # Filtro de data
        date = st.selectbox('Filtro Data', options=df_instituicao.index)

        # Gráfico de distribuição
        st.bar_chart(df_instituicao.loc[date])
