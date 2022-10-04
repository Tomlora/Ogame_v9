import streamlit as st
import pandas as pd
import numpy as np


# https://gamewinner.fr/ogame-faq-formules.html

vitesse_base = 10000
percent_vitesse = 100


def exploration():

    
    def transformation_secondes(x):
        x = x*2
        h = x//3600
        r = x%3600
        m = int(r//60)
        s = int(r%60)
        return f'{m}:{s}'
    
    systeme = st.number_input('Système', 0, 60, 0, format='%i')
    
    df = pd.DataFrame({'Recherche' : np.arange(0,100)})
    # if systeme == 0:
    #         propre_planete = (10 + (35000 / percent_vitesse) * np.sqrt((5000 /10000)/(vitesse_base*(1+df['Recherche']/100))))/st.session_state['vitesse_allie']
    #         propre_planete = transformation_secondes(propre_planete)
    #         st.write(f'Pour sa propre planète : {propre_planete}')
    
    if systeme == 0:
        distance_planete = st.number_input('Distance planete', 1, 15, 1, format='%i')
        df['Temps (Allé)'] = (10+(35000/percent_vitesse) * np.sqrt((1000000+distance_planete*5000)/(vitesse_base*(1+df['Recherche']/100))))/st.session_state['vitesse_allie']
        df['Temps total'] = df['Temps (Allé)'].apply(transformation_secondes) 
    
    else:
        
        df['Temps (Allé)'] = (10+(35000/percent_vitesse) * np.sqrt((2700000+systeme*95000)/(vitesse_base*(1+df['Recherche']/100))))/st.session_state['vitesse_allie']
        df['Temps total'] = df['Temps (Allé)'].apply(transformation_secondes) 

    
    df = df[['Recherche', 'Temps total']]

    
    part1, part2, part3, part4, part5 = st.columns(5)

    with part1:
        st.table(df.iloc[0:10])
    with part3:
        st.table(df.iloc[10:20])
    with part5:
        st.table(df.iloc[20:30])
        
    part6, part7, part8, part9, part10 = st.columns(5)

    with part6:
        st.table(df.iloc[30:40])
    with part8:
        st.table(df.iloc[40:50])
    with part10:
        st.table(df.iloc[50:60])