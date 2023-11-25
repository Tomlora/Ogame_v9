
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import urllib.request
from datetime import timedelta

import xml.etree.ElementTree as et 

from streamlit_option_menu import option_menu
from pages_streamlit.population_et_food import pop
from pages_streamlit.reduction_cost import reduc_cost
from pages_streamlit.slot_recherche import slot
from pages_streamlit.calcul_expedition import calcul_expe
from pages_streamlit.temps_exploration import exploration
from pages_streamlit.calcul_bonus_t3 import calcul_bonus
from pages_streamlit.prod_planete import calcul_prod
from pages_streamlit.scanner_ina import inactif

try:
    st.set_page_config(
        page_title="Ogame v10",
        page_icon="📊",
        layout="wide",
    )
except:
    pass



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

st.markdown("<h1 style='text-align: center; color: white;'>Ogame v10 </h1>", unsafe_allow_html=True )

type = {0 : 'Total'}
        # 1 : 'Eco',
        # 2 : 'Research',
        # 3 : 'Militaire',
        # 4 : 'Militaire lost',
        # 5 : 'Militaire construit',
        # 6 : 'Militaire Détruit',
        # 7 : 'Honor',
        # 8 : 'FdV',
        # 9 : 'Eco FdV',
        # 10 : 'Techno FdV',
        # 11 : 'Exploration FdV'}

        
@st.cache_data
def icon(emoji:str):
    """Montre une emoji en icone de page
    
    Args:
        emoji (str): emoji à afficher, comme :":balloon:" """
        
    st.write(
        f'<span style="font-size: 50px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True
    )


@st.cache_data(show_spinner='Les ordinateurs de bords se préparent...:hourglass:', ttl=timedelta(hours=24))
def load_data():
    """_summary_

    Returns
    -------
    data
        Data des couts en ressources
    data_pop
        Data des populations en fonction du niveau du batiments
    cost_v9
        Cout des batiments v10 (fichier original)
    """
    data = pd.read_excel('data_cost.xlsx', sheet_name=0)
    data_pop = pd.read_excel('data_cost.xlsx', sheet_name=1)
    cost_v9 = pd.read_excel('cost_v9.xlsx', sheet_name=1)
    return data, data_pop, cost_v9

@st.cache_data(show_spinner='Nos ordinateurs analysent les univers...⌛', ttl=timedelta(hours=6))
def chargement_uni(type):
    # on va chercher la liste des univers
    db_liste_uni = 'https://s190-fr.ogame.gameforge.com/api/universes.xml'
    # on enregistre le fichier
    urllib.request.urlretrieve(db_liste_uni, f"./xml/liste_univers.xml")

    # on le réouvre
    df_liste_uni = pd.read_xml('./xml/liste_univers.xml')

    # on prend l'id de chaque uni. L'api fonctionne en y ajoutant l'id de l'uni en début d'url
    for num_uni in df_liste_uni['id'].values:

        db_uni = f'https://s{num_uni}-fr.ogame.gameforge.com/api/serverData.xml'
        # on enregistre
        urllib.request.urlretrieve(db_uni, f"./xml/uni/{num_uni}.xml")
         
    name_uni = []
    speed_uni = []
    speed_flotte_peace = []
    speed_flotte_war = []
    speed_flotte_holding = []
    cdr_flotte = []
    cdr_def = []
    top1 = []
    



    for num_uni in df_liste_uni['id'].values:
        # on parse le fichier xml de l'uni
        my_tree = et.parse(f'./xml/uni/{num_uni}.xml')
        # on y prend les infos qui nous intéressent.. et on les ajoute dans nos différentes listes.
        my_root = my_tree.getroot()
        name_uni.append(my_root[0].text)
        speed_uni.append(my_root[7].text)
        speed_flotte_peace.append(my_root[8].text)
        speed_flotte_war.append(my_root[9].text)
        speed_flotte_holding.append(my_root[10].text)
        cdr_flotte.append(my_root[16].text)
        cdr_def.append(my_root[17].text)
        top1.append(my_root[21].text)
        

        
    # on concatène toutes nos listes dans un dataframe
    df_univers = pd.DataFrame([df_liste_uni['id'].values, name_uni, speed_uni, speed_flotte_peace, speed_flotte_war, speed_flotte_holding, cdr_flotte, cdr_def, top1],
                            index=['id', 'Name', 'Vitesse eco', 'Vitesse allie', 'Vitesse attaque', 'Vitesse statio', 'CDR Flotte', 'CDR Def', 'Top1']).transpose()
    
    df_univers['Top1'] = df_univers['Top1'].astype('float') 
    
    for num_uni in df_liste_uni['id'].values:
        db_players = f'https://s{num_uni}-fr.ogame.gameforge.com/api/players.xml'  # une fois par jour
        db_ladder = f'https://s{num_uni}-fr.ogame.gameforge.com/api/highscore.xml?category=1&type=1' # par heure
        # category : 1 = Player, 2 = Alliance
        # On récupère la data        
        urllib.request.urlretrieve(db_players, f"xml/players_{num_uni}.xml")
    
        for key, value in type.items():
            db = f'https://s{num_uni}-fr.ogame.gameforge.com/api/highscore.xml?category=1&type={key}'
            urllib.request.urlretrieve(db, f"xml/ladder_{num_uni}_{value}.xml")
    
    
    return df_univers 
        
# on charge la data
data, data_pop, cost_v9 = load_data()
df_univers = chargement_uni(type)

# Menu sidebar
with st.sidebar:
    selected = option_menu('Menu', ['Cout v10', 'Population', 'Production', 'Scanner inactif', 'Slot recherche', 'Expedition', 'Calcul bonus T3', 'Reduction cout'],
                           icons=["currency-dollar", 'people-fill', 'file-spreadsheet', 'search', 'gear', 'send', 'kanban', 'graph-down-arrow'], menu_icon='list', default_index=0,
                           styles={
        "container": {"padding": "5!important", "background-color": "#03152A"},
        "icon": {"color": "#0083B9", "font-size": "28px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#FFFFFF"},
        "nav-link-selected": {"background-color": "#2C3845"},
    })
    
    # Variables affichées dans le sidebar, en fonction de l'univers selectionné
    st.session_state.univers = st.selectbox('Univers', df_univers['Name']) # Selection de l'univers
    st.session_state.id_univers = int(df_univers[df_univers['Name'] == st.session_state['univers']]['id'].values[0])
    st.session_state.vitesse_eco = int(df_univers[df_univers['Name'] == st.session_state['univers']]['Vitesse eco'].values[0])
    st.session_state.vitesse_allie = int(df_univers[df_univers['Name'] == st.session_state['univers']]['Vitesse allie'].values[0])
    st.session_state.top1 = int(df_univers[df_univers['Name'] == st.session_state['univers']]['Top1'].values[0])
    st.write(f'Vitesse éco : {st.session_state["vitesse_eco"]} \n \n')
    st.title('by Tomlora (v1.8) [16/11/2023]')
    


def cost_cumul(race, dat, level_act, level_max, niveau_monument_rocheux, millions:bool):
    """Calcule le cumul des couts d'un batiment ou d'une recherche

    Parameters
    ----------
    race : str
        Race ogame v9
    dat : str
        Nom du batiment
    level_act : int
        Niveau du batiment actuel
    level_max : int
        Niveau du batiment à atteindre (objectif)
    niveau_monument_rocheux : int
        Niveau du batiment mouvement rocheux

    Returns
    -------
    DataFrame
        DataFrame comportant les couts par niveau + le total pour chaque type de ressources
    """
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
        
        if millions:
            df[column] = round(df[column] / 1000,2)
        df[column] = df[column].astype(str)
        
    return df

 
if selected == 'Cout v10':    
    # title du dashboard


    st.write("Calcule le cout unitaire et cumulé d'un batiment ou d'une recherche V10")

    race = st.radio('Selectionner la race', data['Lifeform'].unique(), horizontal=True)
    type = st.radio('Batiment/Recherche', ['Batiment', 'Recherche'], horizontal=True)

    if type == 'Batiment':
        st.session_state.data_type = data[data['Type'] == 'Building']
    else:
        st.session_state.data_type = data[data['Type'] != 'Building']
        
    st.session_state.name = st.session_state['data_type'][st.session_state['data_type']['Lifeform'] == race]['Name FR'].unique()

    name = st.selectbox('Selectionner le batiment', st.session_state['name'])

    level_act = st.slider('Level actuel', 0, 90, 0 )
    level_max = st.slider('Level à atteindre', level_act, 90, 0)
    
    millions = st.checkbox('Afficher les coûts en millions', help='Si non coché, en milliers')

    if race == "Rocas" and type == 'Batiment':
        bonus_reduc = st.slider('Niveau Monument Rocheux', 0, 30, 0)
        st.write(bonus_reduc)
    else:
        bonus_reduc = 0
        
    if type == 'Recherche':
        bonus_reduc = st.slider('Centre de recherche', 0, 30, 0)
        st.session_state.centre_race = st.selectbox('Centre de recherche ', data['Lifeform'].unique())
        
        # if st.session_state['centre_race'] == 'Méca' or st.session_state['centre_race'] == 'Kaelesh':
        #     facteur = 0.25 # reduction de 0,25 par niv
        # else:
        #     facteur = 0.5 # reduction de 0,5 par niv
        
        facteur = 0.25
        
        bonus_reduc = bonus_reduc * facteur
        st.write(bonus_reduc) 
        
        

    df_cout = cost_cumul(race, name, level_act, level_max, bonus_reduc, millions)



    st.write(df_cout)

    fig = px.pie(df_cout, df_cout.index, 'Cumul', color='Cumul', color_discrete_sequence=['brown', 'cyan', 'green', 'orange'])

    st.plotly_chart(fig, theme=None)



elif selected == 'Population':
    pop(data)
    
elif selected == 'Production':
    calcul_prod(data)
    
elif selected == 'Scanner inactif':
    inactif(type)
    
elif selected == 'Reduction cout':
    reduc_cost(data)
    
elif selected == 'Slot recherche':
    slot(data, cost_v9)
    
elif selected == 'Expedition':
    calcul_expe()
    
elif selected == 'Exploration':
    exploration()
    
elif selected == 'Calcul bonus T3':
    calcul_bonus()