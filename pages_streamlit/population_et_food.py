import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards




def pop(data):


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

    def conso_nourriture(base_value:int, factor:float, level:int, reduc_conso:float):
        conso = (base_value * pow(factor, level) * (level + 1))* st.session_state["vitesse_eco"]
        
        conso = conso * (1-reduc_conso)
        
        return conso

    def prod_nourriture(base_value:int, factor:float, level:int, bonus_production:float):
        
        prod = (base_value * pow(factor, level) * (level + 1)) * st.session_state["vitesse_eco"]
        bonus_prod = prod * bonus_production
        
        prod = prod + bonus_prod
        
        return prod

    def ratio_nourri(prod, conso):
        return prod/conso

    def pop_max_nourri(total_pop, ratio_nourri):
        
        return total_pop * ratio_nourri
    
    
    def format_number(number):
        return '{:,}'.format(int(number)).replace(',','.')
        


    st.write("Calcule les statistiques de la population en fonction des différents critères")


    race = st.radio('Selectionner la race.', data['Lifeform'].unique(), horizontal=True)
    level_residence = st.slider('Niveau résidence', 0,90,0)
    level_ferme = st.slider('Niveau production food', 0, 90, 0)

    marchand = st.checkbox('Classe alliance marchand ?')

# -------------------- Parametres --------------------

    if race == 'Humain':
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
        
    elif race == 'Méca':
        
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
        
    elif race == 'Kaelesh':
        
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
        
    elif race == 'Rocas':
        
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
        
# --------------------------------------------------

    st.subheader('Population')
    
    style_metric_cards(background_color='#03152A', border_color='#0083B9', border_left_color='#0083B9', border_size_px=1, box_shadow=False, border_radius_px=0)

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        pop_max = calcul_pop_max(base_value_pop_max, factor_pop_max, level_residence, bonus_logement_value, marchand)
        st.metric(label='Pop max', value=format_number(pop_max))
        
    with kpi3:
        conso = conso_nourriture(base_value_conso, factor_conso, level_residence, reduc_conso_value)
        st.metric(label='Conso nourriture', value=format_number(conso))
        
    with kpi2:
        prod = prod_nourriture(base_value_prod, factor_prod, level_ferme, bonus_prod_value)
        st.metric(label='Production alimentaire', value=format_number(prod), delta=int(prod)-int(conso))
        
    kpi4, kpi5 = st.columns(2)

    with kpi4:
        try:
            ratio_nourriture = ratio_nourri(prod, conso)
        except ZeroDivisionError:
            ratio_nourriture = 0
        st.metric('Ratio population nourri', value=f'{round(ratio_nourriture*100,2)}%', delta=round(ratio_nourriture*100-100,2))
        
    with kpi5:
        try:
            pop_max_nourri_possible = pop_max_nourri(pop_max, ratio_nourriture)
        except ZeroDivisionError:
            pop_max_nourri_possible = 0
        st.metric('Population max nourri', value=format_number(pop_max_nourri_possible), delta=format_number(int(pop_max_nourri_possible)-int(pop_max)))
        
        
    if ratio_nourriture < 1:
        with st.expander('Informations supplémentaires'):
            prod_next = prod_nourriture(base_value_prod, factor_prod, level_ferme + 1, bonus_prod_value)
            ratio_nourriture_next = ratio_nourri(prod_next, conso)
            st.write(f'Avec un niveau de ferme en plus, tu produiras assez pour {round(ratio_nourriture_next*100,2)}% de la population')
            
            if reduc_conso != 0:
                reduc_conso_value_next = (reduc_conso + 1 ) / 100
                conso_next = conso_nourriture(base_value_conso, factor_conso, level_residence, reduc_conso_value_next)
                ratio_nourriture_next2 = ratio_nourri(prod, conso_next)
                st.write(f'Avec un niveau de {reduc_conso_name} supplémentaire, tu produiras assez pour {round(ratio_nourriture_next2*100,2)}% de la population')
            
            if bonus_prod !=0:
                bonus_prod_value_next = (bonus_prod + 1) * factor_bonus / 100
                bonus_next2 = prod_nourriture(base_value_prod, factor_prod, level_ferme, bonus_prod_value_next)
                ratio_nourriture_next3 = ratio_nourri(bonus_next2, conso)
                st.write(f'Avec un niveau de {bonus_prod_name} supplémentaire, tu produiras assez pour {round(ratio_nourriture_next3*100,2)}% de la population ')
            

    with st.expander('Population N2/N3'):
        batiment_n2 = st.slider('Batiment N2', 0, 60, 0)
        batiment_n3 = st.slider('Batiment N3', 0, 60, 0)
        
        def graph_popN2N3(pop):
        
            prop_n2 = int(pop) * (batiment_n2 / 100)
            prop_n3 = int(prop_n2) * (batiment_n3 / 100)
            
            fig = px.pie(names=['N1', 'N2', 'N3'], values=[int(pop), int(prop_n2), int(prop_n3)])
            fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
            
            return fig
        
        if ratio_nourriture <= 1: # Lorsque la conso dépasse 100% , on s'arrête à la limite de la population totale. Sinon, on prend le max nourri.
            fig = graph_popN2N3(pop_max_nourri_possible)
        else:
            fig = graph_popN2N3(pop_max)
            
        st.plotly_chart(fig)
    
