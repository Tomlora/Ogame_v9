import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from cout_v9 import data, data_pop, cost_v9

st.set_page_config(
    page_title="Reduction cost v9",
    page_icon="👨",
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

# Fonction

def calcul_pop_max(base_value:int, factor:float, level:int, bonus_logement:float, marchand:bool=False):
    pop_max = base_value * pow(factor, level) * (level + 1)

    bonus_bat = pop_max * bonus_logement
    if marchand:
        classe_marchand = pop_max * 0.1
    else:
        classe_marchand = 0
        
    total_pop = pop_max + bonus_bat + classe_marchand
    return total_pop

def conso_nourriture(base_value:int, factor:float, level:int, reduc_conso:float, vitesse_uni:int):
    conso = (base_value * pow(factor, level) * (level + 1))*vitesse_uni
    
    conso = conso * (1-reduc_conso)
    
    return conso

def prod_nourriture(base_value:int, factor:float, level:int, bonus_production:float, vitesse_uni:int):
    
    prod = (base_value * pow(factor, level) * (level + 1))*vitesse_uni
    bonus_prod = prod * bonus_production
    
    prod = prod + bonus_prod
    
    return prod

def ratio_nourri(prod, conso):
    
    return prod/conso

def pop_max_nourri(total_pop, ratio_nourri):
    
    return total_pop * ratio_nourri
    

# Préparation data

# title du dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Ogame v9 </h1>", unsafe_allow_html=True )
st.subheader('by Tomlora (v1)')

st.write("Calcule les statistiques de la population en fonction des différents critères")


st.session_state.race = st.selectbox('Selectionner la race', data['Lifeform'].unique())
level_residence = st.slider('Niveau résidence', 0,90,0)
level_ferme = st.slider('Niveau production food', 0, 90, 0)

vitesse_uni = st.slider('Vitesse economique', 1, 8, 1 )
marchand = st.checkbox('Classe alliance marchand ?')

if st.session_state['race'] == 'Humain':
    base_value_pop_max = 210
    factor_pop_max = 1.21
    
    base_value_conso = 9
    factor_conso = 1.15
    
    base_value_prod = 10
    factor_prod = 1.14
    
    reduc_conso_name = 'Réserve alimentaire'
    reduc_conso = st.slider(reduc_conso_name, 0, 80, 0 )
    reduc_conso_value = reduc_conso / 100 # pourcentage
    
    st.write(reduc_conso_value)
    
    bonus_logement_name = "Tour d'habitation"
    bonus_logement = st.slider(bonus_logement_name, 0, 80 , 0)
    factor_logement = 1.5
    bonus_logement_value = bonus_logement * factor_logement / 100
    
    st.write(bonus_logement_value)

    bonus_prod_name = "Labo de biotechnologie"
    bonus_prod = st.slider(bonus_prod_name,0, 80, 0)
    factor_bonus = 5
    bonus_prod_value = bonus_prod * factor_bonus / 100
    
    st.write(bonus_prod_value)
    
elif st.session_state['race'] == 'Méca':
    
    base_value_pop_max = 500
    factor_pop_max = 1.205
    
    base_value_conso = 22
    factor_conso = 1.15
    
    base_value_prod = 23
    factor_prod = 1.12
    
    reduc_conso = 0
    reduc_conso_value = 0
    
    bonus_logement_name = 'Atelier de montage'
    bonus_logement = st.slider(bonus_logement_name, 0, 80 , 0)
    factor_logement = 2
    bonus_logement_value = bonus_logement * factor_logement/100
    
    st.write(bonus_logement_value)
    
    bonus_prod_name = 'Chaine de prod de micropuce'
    bonus_prod = st.slider(bonus_prod_name,0, 80, 0)
    factor_bonus = 2
    bonus_prod_value = bonus_prod * factor_bonus/100
    
    st.write(bonus_prod_value)
    
elif st.session_state['race'] == 'Kaelesh':
    
    base_value_pop_max = 250
    factor_pop_max = 1.21
    
    base_value_conso = 11
    factor_conso = 1.15
    
    base_value_prod = 12
    factor_prod = 1.14
    
    reduc_conso_name = 'Convecteur AM'
    reduc_conso = st.slider(reduc_conso_name, 0, 80, 0 )
    reduc_conso_value = reduc_conso / 100 # pourcentage
    
    st.write(reduc_conso_value)
    
    bonus_logement_name = 'Accélérateur par chrysalide'
    bonus_logement = st.slider(bonus_logement_name, 0, 80 , 0)
    factor_logement = 2
    bonus_logement_value = bonus_logement * factor_logement/100
    
    st.write(bonus_logement_value)
    
    bonus_prod = 0    
    bonus_prod_value = 0
    
elif st.session_state['race'] == 'Rocas':
    
    base_value_pop_max = 150
    factor_pop_max = 1.216
    
    base_value_conso = 5
    factor_conso = 1.15
    
    base_value_prod = 6
    factor_prod = 1.14
    
    reduc_conso = 0
    reduc_conso_value = 0
    
    bonus_logement = 0
    bonus_logement_value = 0
    
    bonus_prod = 0
    bonus_prod_value = 0
    


st.subheader('Population')

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    pop_max = calcul_pop_max(base_value_pop_max, factor_pop_max, level_residence, bonus_logement_value, marchand)
    st.metric(label='Pop max', value='{:,}'.format(int(pop_max)).replace(',','.'))
    
with kpi2:
    conso = conso_nourriture(base_value_conso, factor_conso, level_residence, reduc_conso_value, vitesse_uni)
    st.metric(label='Conso nourriture', value='{:,}'.format(int(conso)).replace(',','.'))
    
with kpi3:
    prod = prod_nourriture(base_value_prod, factor_prod, level_ferme, bonus_prod_value, vitesse_uni)
    st.metric(label='Production alimentaire', value='{:,}'.format(int(prod)).replace(',','.'))
    
kpi4, kpi5 = st.columns(2)

with kpi4:
    try:
        ratio_nourriture = ratio_nourri(prod, conso)
    except ZeroDivisionError:
        ratio_nourriture = 0
    st.metric('Ratio population nourri', value=f'{round(ratio_nourriture*100,2)}%')
    
with kpi5:
    try:
        pop_max_nourri_possible = pop_max_nourri(pop_max, ratio_nourriture)
    except ZeroDivisionError:
        pop_max_nourri_possible = 0
    st.metric('Population max nourri', value='{:,}'.format(int(pop_max_nourri_possible)).replace(',','.'))
    
    
if ratio_nourriture < 1:
    with st.expander('Informations supplémentaires'):
        prod_next = prod_nourriture(base_value_prod, factor_prod, level_ferme + 1, bonus_prod_value, vitesse_uni)
        ratio_nourriture_next = ratio_nourri(prod_next, conso)
        st.write(f'Avec un niveau de ferme en plus, tu produiras assez pour {round(ratio_nourriture_next*100,2)}% de la population')
        
        if reduc_conso != 0:
            reduc_conso_value_next = (reduc_conso + 1 ) / 100
            conso_next = conso_nourriture(base_value_conso, factor_conso, level_residence, reduc_conso_value_next, vitesse_uni)
            ratio_nourriture_next2 = ratio_nourri(prod, conso_next)
            st.write(f'Avec un niveau de {reduc_conso_name} supplémentaire, tu produiras assez pour {round(ratio_nourriture_next2*100,2)}% de la population')
        
        if bonus_prod !=0:
            bonus_prod_value_next = (bonus_prod + 1) * factor_bonus / 100
            bonus_next2 = prod_nourriture(base_value_prod, factor_prod, level_ferme, bonus_prod_value_next, vitesse_uni)
            ratio_nourriture_next3 = ratio_nourri(bonus_next2, conso)
            st.write(f'Avec un niveau de {bonus_prod_name} supplémentaire, tu produiras assez pour {round(ratio_nourriture_next3*100,2)}% de la population ')
        

with st.expander('Population N2/N3'):
    batiment_n2 = st.slider('Batiment N2', 0, 60, 0)
    batiment_n3 = st.slider('Batiment N3', 0, 60, 0)
    
    prop_n2 = int(pop_max_nourri_possible) * (batiment_n2 / 100)
    prop_n3 = int(prop_n2) * (batiment_n3 / 100)
    
    fig = px.pie(names=['N1', 'N2', 'N3'], values=[int(pop_max_nourri_possible), int(prop_n2), int(prop_n3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
    
    st.write(fig)
    
