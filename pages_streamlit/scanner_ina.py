import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def inactif(type):


    print(st.session_state.id_univers)
    
    df_players = pd.read_xml(f'xml/players_{st.session_state.id_univers}.xml')
    
    mapping = {'a' : 'admin',
            'v' : 'mv',
            'i' : 'inactif',
            'I' : 'inactif',
            None: 'actif'}
    
    df_players['status'] = df_players['status'].replace(mapping)

    df_players.drop('alliance', axis=1, inplace=True)

    for value in type.values():
        df = pd.read_xml(f'xml/ladder_{st.session_state.id_univers}_{value}.xml')
        if len(df.columns) == 3:
            df.columns = [f'position_{value}', 'id', f'points_{value}']
        else:
            df.columns = [f'position_{value}', 'id', f'points_{value}', "ships"]
        df_players = pd.merge(df_players, df, on='id')
        
    df_players.sort_values('position_Total', ascending=True, inplace=True)

    df_ina = df_players[df_players['status'] == 'inactif']

    df_ina.drop('id', axis=1, inplace=True)

    df_ina.set_index('position_Total', inplace=True)

    # df
    
    points_mini = st.number_input('Nombre de points minimum', min_value=50000, max_value=int(df_ina['points_Total'].max()), value=50000)
    
    df_ina_filter = df_ina[df_ina['points_Total'] >= points_mini]
    st.subheader(f'Inactifs : {df_ina_filter.shape[0]}')
    st.dataframe(df_ina_filter, use_container_width=True, height=df_ina_filter.shape[0] * 35)
    
    df_download = to_excel(df_ina_filter)
    
    st.download_button('Télécharger', data=df_download, file_name=f'inactif_{st.session_state.univers}.xlsx')
    

