from asyncio import set_child_watcher
from re import sub
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from cost_v9 import data, data_pop, cost_v9

st.set_page_config(
    page_title="Reduction cost v9",
    page_icon="✅",
    layout="wide",
)


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div.block-container{padding-top:2rem;}
  
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def cost_cumul(race, dat, level_act, level_max, niveau_monument_rocheux):
    
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
            
    return df

 
    
# title du dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Ogame v9 </h1>", unsafe_allow_html=True )
st.subheader('by Tomlora (v1)')

st.subheader('Batiment/Recherche visé')

st.session_state.race = st.selectbox('Selectionner la race', data['Lifeform'].unique())

if st.session_state['race'] == "Rock´tal":
    st.session_state.type = st.selectbox('Batiment/Recherche', ['Batiment', 'Recherche'])
else:
    st.session_state.type = st.selectbox('Batiment/Recherche', ['Recherche'])
    
if st.session_state['type'] == 'Batiment':
    st.session_state.data_type = data[data['Type'] == 'Building']
else:
    st.session_state.data_type = data[data['Type'] != 'Building']
    
st.session_state.name = st.session_state['data_type'][st.session_state['data_type']['Lifeform'] == st.session_state.race]['Name FR'].unique()

name = st.selectbox('Selectionner le batiment', st.session_state['name'])

level_act = st.slider('Level actuel', 0, 59, 0 )
level_max = st.slider('Level à atteindre', level_act, 59, 0)

st.subheader('Batiment de réduction')

if st.session_state['race'] == "Rock´tal" and st.session_state['type'] == 'Batiment':
    bonus_reduc_f = st.slider('Niveau Monument Rocheux', 0, 30, 0)
else:
    bonus_reduc_f = 0
    
if st.session_state['type'] == 'Recherche':
    bonus_reduc = st.slider('Centre de recherche', 0, 30, 0)
    st.session_state.centre_race = st.selectbox('Centre de recherche ', data['Lifeform'].unique())
    
    if st.session_state['centre_race'] == 'Mecha' or st.session_state['centre_race'] == 'Kaelesh':
        facteur = 0.25 # reduction de 0,25 par niv
    else:
        facteur = 0.5 # reduction de 0,5 par niv
    
    bonus_reduc_f = bonus_reduc * facteur 
    
    

df_cout_mini = cost_cumul(st.session_state['race'], name, level_act, level_max, bonus_reduc_f)
df_cout = cost_cumul(st.session_state['race'], name, level_act, level_max, 0)

df_diff = df_cout_mini - df_cout

for column in df_diff.columns:
    df_diff[column] = round(df_diff[column],3)
    df_diff[column] = df_diff[column].astype(str)

st.subheader('Différence de coût')

st.write(df_diff)

with st.expander('Voir cout du batiment de réduction'):
    if st.session_state['race'] == "Rock´tal" and st.session_state['type'] == 'Batiment':
        st.write(cost_cumul(st.session_state['race'], 'Mégalithe', 0, bonus_reduc_f, 0))
    
    else:
        dict_labo = {'Human' : 'Centre de recherche ',
                     'Mecha' : 'Centre de recherche en robotique ',
                     'Kaelesh' : 'Chambre vortex ',
                     'Rock´tal' : 'Rune Technologium '}
        
        labo = dict_labo[st.session_state['centre_race']]
        
        
        st.write(cost_cumul(st.session_state['centre_race'], labo, 0, bonus_reduc, 0))
        