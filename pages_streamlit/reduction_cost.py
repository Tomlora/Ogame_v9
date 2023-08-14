import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# from cout_v9 import data, data_pop, cost_v9



def reduc_cost(data):

    def cost_cumul(race, dat, level_act, level_max, niveau_monument_rocheux, millions:bool):
        
        level_act = level_act + 1
        
        tri = data[data['Name FR'] == dat]
        
        level_list = []
        metal = []
        crystal = []
        deut = []
            
        for level in range(level_act, level_max+1):
            level_list.append(str(level))
            metal.append(round(tri[f'metal cost {level}'].values[0] * (1-niveau_monument_rocheux/100),1))
            crystal.append(round(tri[f'crystal cost {level}'].values[0] * (1-niveau_monument_rocheux/100),1))
            deut.append(round(tri[f'deut cost {level}'].values[0] * (1-niveau_monument_rocheux/100),1))
            
        level_list.append('Cumul')    
        metal.append(round(np.sum(metal),1))
        crystal.append(round(np.sum(crystal),1))
        deut.append(round(np.sum(deut),1))
        
        df = pd.DataFrame([metal, crystal, deut], columns=level_list, index=['Metal', 'Crystal', 'Deut'])
        
        if millions:
            df = df / 1000
                
        return df


    st.write('Calcule les réductions de coût en fonction des batiments montés')

    st.subheader('Batiment/Recherche visé')

    race = st.radio('Selectionner la race de la planète', data['Lifeform'].unique(), horizontal=True)

    if race == "Rocas":
        type = st.radio('Batiment/Recherche', ['Batiment', 'Recherche'], horizontal=True)
    else:
        type = st.radio('Batiment/Recherche', ['Recherche'], horizontal=True)
        
    if type == 'Batiment':
        st.session_state.data_type = data[data['Type'] == 'Building']
    else:
        st.session_state.data_type = data[data['Type'] != 'Building']
        
    liste_data = st.session_state['data_type'][st.session_state['data_type']['Lifeform'] == race]['Name FR'].unique()

    name = st.selectbox('Selectionner le batiment', liste_data)

    level_act = st.slider('Level actuel', 0, 90, 0 )
    level_max = st.slider('Level à atteindre', level_act, 90, 0)

    st.subheader('Batiment de réduction')

    if race == "Rocas" and type == 'Batiment':
        bonus_reduc_f = st.slider('Niveau Monument Rocheux', 0, 30, 0)
    else:
        bonus_reduc_f = 0
        
    if type == 'Recherche':
        bonus_reduc = st.slider('Centre de recherche', 0, 30, 0)
        st.session_state.centre_race = st.radio('Centre de recherche ', data['Lifeform'].unique(), horizontal=True)
        
        if st.session_state['centre_race'] == 'Méca' or st.session_state['centre_race'] == 'Kaelesh':
            facteur = 0.25 # reduction de 0,25 par niv
        else:
            facteur = 0.5 # reduction de 0,5 par niv
        
        bonus_reduc_f = bonus_reduc * facteur 
        
    millions = st.checkbox('Afficher les coûts en millions', value=False, key=None, help='Si non coché, en milliers')   

    df_cout_mini = cost_cumul(race, name, level_act, level_max, bonus_reduc_f, millions)
    df_cout = cost_cumul(race, name, level_act, level_max, 0, millions)

    df_diff = df_cout_mini - df_cout

    for column in df_diff.columns:
        if millions:
            df_diff[column] = round(df_diff[column],1)
        else:
            df_diff[column] = round(df_diff[column],3)
        df_diff[column] = df_diff[column].astype(str)

    st.subheader('Différence de coût')

    st.write(df_diff)

    with st.expander('Voir cout du batiment de réduction'):
        if race == "Rocas" and type == 'Batiment':
            st.write(cost_cumul(race, 'Monument rocheux', 0, bonus_reduc_f, 0, millions))
        
        else:
            dict_labo = {'Humain' : 'Centre de recherche ',
                        'Méca' : 'Centre de recherche en robotique ',
                        'Kaelesh' : 'Salle à vortex ',
                        'Rocas' : 'Centre technologique runique '}
            
            labo = dict_labo[st.session_state['centre_race']]
            
            
            st.write(cost_cumul(st.session_state['centre_race'], labo, 0, bonus_reduc, 0, millions))
        