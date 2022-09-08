from asyncio import set_child_watcher
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from streamlit_option_menu import option_menu
from pages_streamlit.population_et_food import pop
from pages_streamlit.reduction_cost import reduc_cost
from pages_streamlit.slot_recherche import slot

st.set_page_config(
    page_title="Ogame v9",
    page_icon="📊",
    layout="wide",
)



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div.block-container{padding-top:2rem;}

div[role="listbox"] ul {
    background-color: #1E90FF;
}
 
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("<h1 style='text-align: center; color: white;'>Ogame v9 </h1>", unsafe_allow_html=True )


@st.cache
def load_data():
    data = pd.read_excel('data_cost.xlsx', sheet_name=0)
    data_pop = pd.read_excel('data_cost.xlsx', sheet_name=1)
    cost_v9 = pd.read_excel('cost_v9.xlsx', sheet_name=1)
    return data, data_pop, cost_v9

data, data_pop, cost_v9 = load_data()

with st.sidebar:
    selected = option_menu('Menu', ['Cout v9', 'Population', 'Reduction cout', 'Slot recherche'],
                           icons=["currency-dollar", 'people-fill', 'kanban', 'gear'], menu_icon='list', default_index=0,
                           styles={
        "container": {"padding": "5!important", "background-color": "#03152A"},
        "icon": {"color": "#0083B9", "font-size": "28px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#FFFFFF"},
        "nav-link-selected": {"background-color": "#2C3845"},
    })
    st.write('----------------')
    st.write('by Tomlora (v1.1)')
    


def cost_cumul(race, dat, level_act, level_max, niveau_monument_rocheux):
    
    level_act = level_act + 1
    
    tri = data[data['Name FR'] == dat]
    
    level_list = []
    metal = []
    crystal = []
    deut = []
    energy = []
        
    for level in range(level_act, level_max+1):
        level_list.append(str(level))
        metal.append(round(tri[f'metal cost {level}'].values[0],1) * (1-niveau_monument_rocheux/100))
        crystal.append(round(tri[f'crystal cost {level}'].values[0],1) * (1-niveau_monument_rocheux/100))
        deut.append(round(tri[f'deut cost {level}'].values[0],1) * (1-niveau_monument_rocheux/100))
        energy.append(round(tri[f'energy cost {level}'].values[0],1))
        
        
    level_list.append('Cumul')    
    metal.append(round(np.sum(metal),1))
    crystal.append(round(np.sum(crystal),1))
    deut.append(round(np.sum(deut),1))
    energy.append(round(np.sum(energy),1))
    
    df = pd.DataFrame([metal, crystal, deut, energy], columns=level_list, index=['Metal', 'Crystal', 'Deut', 'Energy'])
    
    for column in df.columns:
        df[column] = round(df[column], 3)
        df[column] = df[column].astype(str)
        
    return df

 
if selected == 'Cout v9':    
    # title du dashboard


    st.write("Calcule le cout unitaire et cumulé d'un batiment ou d'une recherche V9")

    st.session_state.race = st.selectbox('Selectionner la race', data['Lifeform'].unique())
    st.session_state.type = st.selectbox('Batiment/Recherche', ['Batiment', 'Recherche'])

    if st.session_state['type'] == 'Batiment':
        st.session_state.data_type = data[data['Type'] == 'Building']
    else:
        st.session_state.data_type = data[data['Type'] != 'Building']
        
    st.session_state.name = st.session_state['data_type'][st.session_state['data_type']['Lifeform'] == st.session_state.race]['Name FR'].unique()

    name = st.selectbox('Selectionner le batiment', st.session_state['name'])

    level_act = st.slider('Level actuel', 0, 90, 0 )
    level_max = st.slider('Level à atteindre', level_act, 90, 0)

    if st.session_state['race'] == "Rocas" and st.session_state['type'] == 'Batiment':
        bonus_reduc = st.slider('Niveau Monument Rocheux', 0, 30, 0)
        st.write(bonus_reduc)
        st.write('Note : En attente de la confirmation de GameForge sur la prise en compte du centre des minéraux. En conséquence, il y a un léger écart concernant les deux premiers batiments')
    else:
        bonus_reduc = 0
        
    if st.session_state['type'] == 'Recherche':
        bonus_reduc = st.slider('Centre de recherche', 0, 30, 0)
        st.session_state.centre_race = st.selectbox('Centre de recherche ', data['Lifeform'].unique())
        
        if st.session_state['centre_race'] == 'Méca' or st.session_state['centre_race'] == 'Kaelesh':
            facteur = 0.25 # reduction de 0,25 par niv
        else:
            facteur = 0.5 # reduction de 0,5 par niv
        
        bonus_reduc = bonus_reduc * facteur
        st.write(bonus_reduc) 
        
        

    df_cout = cost_cumul(st.session_state['race'], name, level_act, level_max, bonus_reduc)



    st.write(df_cout)

    fig = px.pie(df_cout, df_cout.index, 'Cumul', color='Cumul', color_discrete_sequence=['brown', 'cyan', 'green', '#FF7F00'])

    st.write(fig)


elif selected == 'Population':
    pop(data)
    
elif selected == 'Reduction cout':
    reduc_cost(data)
    
elif selected == 'Slot recherche':
    slot(data, cost_v9)