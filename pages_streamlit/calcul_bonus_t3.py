import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards

def mise_en_forme_number(number, type='int'):
        if type == 'int':
            new_number = "{:,}".format(int(number)).replace(',', ' ').replace('.', ',')
        elif type == 'float':
            new_number = "{:,}".format(number).replace(',', ' ').replace('.', ',')
        return new_number 


def calcul_bonus_t3_total_explo(cumul_t1, cumul_t2, cumul_t3, niveau_race, explorateur:bool, niveau_metro, vitesse_uni:bool):
    bonus_race = 1 + niveau_race/1000
    
    if explorateur:
        bonus_expe = 1.5
    else:
        bonus_expe = 1
        
    bonus_metro = niveau_metro * 0.5 / 100
    # bonus = ((cumul_t1 + cumul_t2) * 0.2 + cumul_t3 * 0.2 * st.session_state["vitesse_eco"] * bonus_expe) * bonus_race
    if vitesse_uni:
        bonus = bonus_expe * st.session_state["vitesse_eco"] * (1+0.2/100 * (cumul_t1 + cumul_t2) * (bonus_race + bonus_metro)) * (1+0.2/100 * cumul_t3 * (bonus_race + bonus_metro))
    else:
         bonus = bonus_expe * 1 * (1+0.2/100 * (cumul_t1 + cumul_t2) * (bonus_race + bonus_metro)) * (1+0.2/100 * cumul_t3 * (bonus_race + bonus_metro))
    
    # 0.2 correspond au bonus de la techno
    return round(bonus,3) 

def calcul_bonus_t3_unitaire_explo(niveau_t3, niveau_race, explorateur:bool, niveau_metro):
    bonus_race = 1 + niveau_race / 1000
    if explorateur:
        bonus_expe = 1.5
    else:
        bonus_expe = 1
    bonus_metro = niveau_metro * 0.5 / 100
    bonus = (niveau_t3 * 0.2) * st.session_state["vitesse_eco"] * bonus_expe * (bonus_race + bonus_metro)
    return round(bonus,3) 


def calcul_bonus_collecteur(bonus_prod, niveau_t3):
    return round((bonus_prod * (1 + 0.2/100 * niveau_t3 * 1.1)) * 100 ,3)


def calcul_bonus():
    style_metric_cards(background_color='#03152A', border_color='#0083B9', border_left_color='#0083B9', border_size_px=1, box_shadow=False, border_radius_px=0)
    
    st.title('Calcul bonus T3')
    
    type_calcul = st.radio('Type de calcul', ['Explorateur', 'Collecteur'], horizontal=True)
    
    if type_calcul == 'Explorateur':
        explorateur = st.checkbox('Bonus Explorateur ?')
        niv_race = st.slider('Niveau Race', 0, 100, 0)
        niv_metro = st.slider('Niveau Metropolis', 0, 100, 0)
        
        tab_unitaire, tab_total = st.tabs(['Unitaire', 'Total'])
        
        
        with tab_unitaire:
            
            value_techno_t3 = st.slider('Niveau de la techno T3.6', 0, 100, 0)
            
            bonus_unitaire = calcul_bonus_t3_unitaire_explo(value_techno_t3, niv_race, explorateur, niv_metro)
            
            st.metric('Bonus unitaire', bonus_unitaire)
            
        with tab_total:
        
            value_techno_t1_cumul = st.slider('Cumul de la techno T1.5', 0, 700, 0)
            value_techno_t2_cumul = st.slider('Cumul de la techno T2.5', 0, 700, 0)
            value_techno_t3_cumul = st.slider('Cumul de la techno T3.6', 0, 700, 0)
            vitesse_uni = st.checkbox("Inclure la vitesse de l'univers directement dans le calcul", value=True, help="Si coché, la vitesse de l'univers est inséré dans le calcul. Il faut donc inscrire dans les ressources obtenues, l'équivalent sur un x1 eco")
            
            bonus_total = calcul_bonus_t3_total_explo(value_techno_t1_cumul, value_techno_t2_cumul, value_techno_t3_cumul,  niv_race, explorateur, niv_metro, vitesse_uni)
            
            st.metric('Bonus total', bonus_total)
        
            st.subheader('Conséquence Exploration')
            
            eclaireur = st.checkbox('Eclaireur ?')
            
            if eclaireur:
                bonus_eclaireur = 2
            else:
                bonus_eclaireur = 1
                
            if explorateur:
                bonus_expe = 1.5
            else:
                bonus_expe = 1
                
            if st.session_state['top1'] > 100000000:
                points_top_1 = '>100M'
            if st.session_state['top1'] < 100000000:
                points_top_1 = '<100M'
            if st.session_state['top1'] < 75000000:
                points_top_1 = '<75M'
            if st.session_state['top1'] < 50000000:
                points_top_1 = '<50M'
            if st.session_state['top1'] < 25000000:
                points_top_1 = '<25M'
            if st.session_state['top1'] < 5000000:
                points_top_1 = '<5M'
            if st.session_state['top1'] < 1000000:
                points_top_1 = '<1M'
            if st.session_state['top1'] < 100000:
                points_top_1 = '<100k'                        
            if st.session_state['top1'] < 10000:
                points_top_1 = '<10k'
                
            dict_max_metal = {'<10k' : 40000,
                        '<100k': 500000,
                        '<1M' : 1200000,
                        '<5M' : 1800000,
                        '<25M': 2400000,
                        '<50M' : 3000000,
                        '<75M' : 3600000,
                        '<100M' : 4200000 ,
                        '>100M' : 5000000}
            
            max_metal = int(dict_max_metal[points_top_1]) * st.session_state["vitesse_eco"] * bonus_expe * bonus_eclaireur
        
            metal = st.number_input('Metal', 1, int(max_metal), 1, format='%i', help='Ressource obtenue sur une expédition')
            cristal = st.number_input('Cristal ', 1, round(max_metal / 2), 1, format='%i', help='Ressource obtenue sur une expédition')
            deut = st.number_input('Deut ', 1, round(max_metal / 3), 1, format='%i', help='Ressource obtenue sur une expédition')
            
            metal_total = round(metal * bonus_eclaireur * bonus_total)
            cristal_total = round(cristal * bonus_eclaireur * bonus_total)
            deut_total = round(deut * bonus_eclaireur * bonus_total)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric('Metal', mise_en_forme_number(metal_total), help='Avec les bonus')
            
            with col2:
                st.metric('Cristal', mise_en_forme_number(cristal_total), help='Avec les bonus')
                
            with col3:
                st.metric('Deut', mise_en_forme_number(deut_total), help='Avec les bonus')
                
    elif type_calcul == 'Collecteur':
        
        value_techno_t1_cumul_collecteur = st.slider('Cumul de la techno T3.6', 0, 700, 0)
        

        bonus_prod = 25/100

        bonus_fret_energie = 10/100
            
        bonus_total_prod = calcul_bonus_collecteur(bonus_prod, value_techno_t1_cumul_collecteur)
        bonus__total_autre = calcul_bonus_collecteur(bonus_fret_energie, value_techno_t1_cumul_collecteur)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric('Bonus Production', bonus_total_prod)
        
        with col2:
            st.metric('Bonus Fret/Energie', bonus__total_autre)