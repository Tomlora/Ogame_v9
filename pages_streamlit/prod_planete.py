import pandas as pd 
import streamlit as st
import numpy as np

from streamlit_extras.colored_header import colored_header


def calcul_prod(data):
    
    st.info("Suppose que l'énergie soit à 100%")
    
    def prod_metal(niveau_metal, vitesse_eco):
        return round(30 * niveau_metal * pow(1.1, niveau_metal)*vitesse_eco)

    def prod_cristal(niveau_cristal, vitesse_eco):
        return round(20 * niveau_cristal * pow(1.1, niveau_cristal)*vitesse_eco)

    def prod_deut(niveau_deut, vitesse_eco, temp_max):
        return round((10 * niveau_deut * pow(1.1, niveau_deut)) * (1.44-0.004*temp_max))*vitesse_eco

    # Humains
    
    def fusion_haute_energie(prod_metal, niveau_bat):
        return round(prod_metal * (0.015 * niveau_bat))

    def extraction_fusion(prod_cristal, prod_deut, niveau_bat):
        return round(prod_cristal * (0.015 * niveau_bat)),  round(prod_deut * (0.015 * niveau_bat))

    # Roctas
    def fusion_magnetique(prod_metal, niveau_bat):
        return round(prod_metal * (0.02 * niveau_bat))
    
    def chambre_disruption(prod_cristal, niveau_bat):
        return round(prod_cristal * (0.02 * niveau_bat))

    def synthoniseur_deut(prod_deut, niveau_bat):
        return round(prod_deut * (0.02 * niveau_bat))

    def calcul_plasma(metal, cristal, deut, niv_plasma):
        metal = round(metal * (0.01 * niv_plasma))
        cristal = round(cristal * (0.0066 * niv_plasma))
        deut = round(deut * (0.0033 * niv_plasma))
        return metal, cristal, deut

    def calcul_geologue(metal, cristal, deut):
        metal = round(metal * 0.1)
        cristal = round(cristal * 0.1)
        deut = round(deut * 0.1)
        return metal, cristal, deut

    def calcul_conseil_officier(metal, cristal, deut):
        metal = round(metal * 0.02)
        cristal = round(cristal * 0.02)
        deut = round(deut * 0.02)
        return metal, cristal, deut

    def classe_collecteur(metal, cristal, deut):
        metal = round(metal * 0.25)
        cristal = round(cristal * 0.25)
        deut = round(deut * 0.25)
        return metal, cristal, deut
    
    def prod_foreuse(metal, cristal, deut, foreuse, bonus_collector):
        metal = round((metal * foreuse * bonus_collector) / 100)
        cristal = round((cristal * foreuse * bonus_collector) / 100)
        deut = round((deut * foreuse * bonus_collector) / 100)
        return metal, cristal, deut
        

    def classe_marchand(metal, cristal, deut):
        metal = round(metal * 0.05)
        cristal = round(cristal * 0.05)
        deut = round(deut * 0.05)
        return metal, cristal, deut


    def bonus_recherches_fdv(metal, cristal, deut, bonus_metal, bonus_cristal, bonus_deut):
        bonus_metal = bonus_metal / 100 
        bonus_cristal = bonus_cristal / 100
        bonus_deut = bonus_deut / 100
        
        metal = round(metal * bonus_metal)
        cristal = round(cristal * bonus_cristal)
        deut = round(deut * bonus_deut)
        return metal, cristal, deut
    
    
    def calcul_objets(prod, ratio):
        return round(prod * (ratio / 100))
    
    st.title('Calcul production')
    
    pos_planete = st.radio('Position planète', [i for i in range(1,16)], 0, horizontal=True)
    vitesse_eco = st.session_state["vitesse_eco"]
    temp_max = st.number_input('Température max', -200, 1000, 0, format='%i')
    
    
    # st.subheader('Mines')
    
    colored_header('Mines', description='', color_name='green-70')
    
    
    niveau_metal = st.slider('Niveau mine de métal', 0, 60, 0, format='%i')
    niveau_cristal = st.slider('Niveau mine de cristal', 0, 60, 0, format='%i')
    niveau_deut = st.slider('Niveau synthétiseur de deut', 0, 60, 0, format='%i')
    
    
    
    # ---------- Mine
    
    
    
    if pos_planete in [6,10]:
        bonus_metal = 1.17
    elif pos_planete in [7,9]:
        bonus_metal = 1.23
    elif pos_planete == 8:
        bonus_metal = 1.35
    else:  
        bonus_metal = 1

    mine_metal = round(prod_metal(niveau_metal, vitesse_eco) * bonus_metal)
    
    
    if pos_planete == 1:
        bonus_cristal = 1.4
    elif pos_planete == 2:
        bonus_cristal = 1.3
    elif pos_planete == 3:
        bonus_cristal = 1.2
    else:
        bonus_cristal = 1
    
    mine_cristal = round(prod_cristal(niveau_cristal, vitesse_eco) * bonus_cristal)
    
    mine_deut = round(prod_deut(niveau_deut, vitesse_eco, temp_max))
    
    
    # Batiments Formes de Vie
    
    colored_header('Batiment Formes de Vie', description='', color_name='green-70')
    
    race = st.radio('Selectionner la race.', data['Lifeform'].unique(), horizontal=True)
    
    if race == 'Humain':
        niveau_fusion_magnetique = st.slider('Niveau Fusion à haute energie', 0, 60, 0, format='%i', help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        niveau_extraction_fusion = st.slider('Niveau Extraction Fusion', 0, 60, 0, format='%i',help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        
        metal_bats_fdv = fusion_haute_energie(mine_metal, niveau_fusion_magnetique)
        cristal_bats_fdv, deut_bats_fdv = extraction_fusion(mine_cristal, mine_deut, niveau_extraction_fusion)

        
    elif race == 'Méca':
        niveau_synthoniseur = st.slider('Niveau synthoniseur à haut rendement', 0, 60, 0, format='%i', help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        
        metal_bats_fdv = 0
        cristal_bats_fdv = 0
        deut_bats_fdv = synthoniseur_deut(mine_deut, niveau_synthoniseur)

        
    elif race == 'Kaelesh':
        metal_bats_fdv = 0
        cristal_bats_fdv = 0
        deut_bats_fdv = 0

        
    elif race == 'Rocas':
        niveau_fusion_magnetique = st.slider('Niveau Fusion Magnetique', 0, 60, 0, format='%i', help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        niveau_raffinerie_cristaux = st.slider('Niveau Raffinerie de cristaux', 0, 60, 0, format='%i', help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        niveau_synthoniseur_deut = st.slider('Niveau synthoniseur de deut', 0, 60, 0, format='%i', help='Possibilité de laisser vide en mettant le total de Bonus de prod ci-dessous')
        
        
        metal_bats_fdv = fusion_magnetique(mine_metal, niveau_fusion_magnetique)
        cristal_bats_fdv = chambre_disruption(mine_cristal, niveau_raffinerie_cristaux)
        deut_bats_fdv = synthoniseur_deut(mine_deut, niveau_synthoniseur_deut)
        

    # Technologies
    
    colored_header('Technologies', description='', color_name='green-70')
    
    niveau_plasma = st.slider('Niveau plasma', 0, 60, 0, format='%i')
    
    metal_plasma, cristal_plasma, deut_plasma = calcul_plasma(mine_metal, mine_cristal, mine_deut, niveau_plasma)
    
    colored_header('Bonus Technologies Formes de Vie', description='', color_name='green-70')
    
    metal_recherches_fdv_bonus = st.number_input('Bonus métal', 0.0, 200.0, 0.0, format='%f', help='Il ne faut pas prendre en compte les bonus batiments si les champs Batiments FdV ont été remplis')
    cristal_recherches_fdv_bonus = st.number_input('Bonus cristal', 0.0, 200.0, 0.0, format='%f', help='Il ne faut pas prendre en compte les bonus batiments si les champs Batiments FdV ont été remplis')
    deut_recherches_fdv_bonus = st.number_input('Bonus deut', 0.0, 200.0, 0.0, format='%f', help='Il ne faut pas prendre en compte les bonus batiments si les champs Batiments FdV ont été remplis')
    
    
    metal_recherches_fdv, cristal_recherches_fdv, deut_recherches_fdv = bonus_recherches_fdv(mine_metal, mine_cristal, mine_deut,
                         metal_recherches_fdv_bonus, cristal_recherches_fdv_bonus, deut_recherches_fdv_bonus)
    
    
    # Officiers
    
    colored_header('Officiers et Classes', description='', color_name='green-70')
    
    geologue = st.checkbox('Geologue')
    
    if geologue:
        metal_geo, cristal_geo, deut_geo = calcul_geologue(mine_metal, mine_cristal, mine_deut)
    else:
        metal_geo, cristal_geo, deut_geo = 0, 0, 0
        
    conseil_officier = st.checkbox('Conseil officier')
    
    if conseil_officier:
        metal_conseil, cristal_conseil, deut_conseil = calcul_conseil_officier(mine_metal, mine_cristal, mine_deut)
    else:
        metal_conseil, cristal_conseil, deut_conseil = 0, 0, 0
        
    collecteur = st.checkbox('Classe collecteur')
    
    if collecteur:
        metal_collecteur, cristal_collecteur, deut_collecteur = classe_collecteur(mine_metal, mine_cristal, mine_deut)
        bonus_collector = 0.03
    else:
        metal_collecteur, cristal_collecteur, deut_collecteur = 0, 0, 0
        bonus_collector = 0.02
        
    nb_foreuse = st.number_input('Nombre de foreuses', 0, 2000, 0, format='%i')
    
    metal_foreuse, cristal_foreuse, deut_foreuse = prod_foreuse(mine_metal, mine_cristal, mine_deut, nb_foreuse, bonus_collector)
        
    marchand = st.checkbox('Classe Alliance marchand')
    
    if marchand:
        metal_marchand, cristal_marchand, deut_marchand = classe_marchand(mine_metal, mine_cristal, mine_deut)
    else:
        metal_marchand, cristal_marchand, deut_marchand = 0, 0, 0
        
    colored_header('Objets', description='', color_name='orange-70')    
    with st.expander('Boosters'):
            
        value_booster = [0, 10, 20, 30, 40]
        ratio_metal = st.radio('Booster metal', value_booster, 0, horizontal=True)
        ratio_cristal = st.radio('Booster cristal', value_booster, 0, horizontal=True)
        ratio_deut = st.radio('Booster deut', value_booster, 0, horizontal=True)
            
        metal_objets = calcul_objets(mine_metal, ratio_metal)
        cristal_objets = calcul_objets(mine_cristal, ratio_cristal)
        deut_objets = calcul_objets(mine_deut, ratio_deut)

    
    # Construction DataFrame
    
    df = pd.DataFrame([[mine_metal, mine_cristal, mine_deut],
                       [metal_bats_fdv, cristal_bats_fdv, deut_bats_fdv],
                       [metal_plasma, cristal_plasma, deut_plasma],
                       [metal_objets, cristal_objets, deut_objets],
                       [metal_geo, cristal_geo, deut_geo],
                       [metal_conseil, cristal_conseil, deut_conseil],
                       [metal_foreuse, cristal_foreuse, deut_foreuse],
                       [metal_collecteur, cristal_collecteur, deut_collecteur],
                       [metal_marchand, cristal_marchand, deut_marchand],
                       [metal_recherches_fdv, cristal_recherches_fdv, deut_recherches_fdv],],
                      index=['Mines', 'Batiments FdV', 'Plasma', 'Objets',
                             'Geologue', 'Conseil officiers', 'Foreuse', 'Collecteur', 'Classe Marchand', 'Recherches FdV'], 
                      columns=['Metal', 'Cristal', 'Deut'])
    
    df.loc['Total Heure'] = df.sum(axis=0)
    df.loc['Total Jour'] = df.loc['Total Heure'] * 24
    df.loc['Total Semaine'] = df.loc['Total Jour'] * 7
    
    df = df.replace(',', ' ')
    
    colored_header('Production', description='', color_name='yellow-70')
        
    st.dataframe(df, use_container_width=True)
    
    colored_header('Production de Flotte', description='', color_name='yellow-70')
    
    with st.expander('Production'):
        
        df_vsx = pd.DataFrame(index=['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur',
                                        'Bombardier', 'Destructeur', 'Etoile de la mort', 'Faucheur', 'Eclaireur',
                                        'Petit transporteur', 'Grand transporteur', 'Vaisseau de colonisation', 'Recycleur', 'Sonde'])
        
        df_vsx['cout_metal'] = [3000, 6000, 20000, 45000, 30000, 50000, 60000, 5000000, 85000, 8000, 2000, 6000, 10000, 10000, 0]
        df_vsx['cout_cristal'] = [1000, 4000, 7000, 15000, 40000, 25000, 50000, 4000000, 55000, 15000, 2000, 6000, 20000, 6000, 1000]
        df_vsx['cout_deut'] = [0, 0, 2000, 0, 15000, 15000, 15000, 1000000, 20000, 8000, 0, 0, 10000, 2000, 0]  
        
        df_vsx['cout_metal'] = np.ceil(df.loc['Total Heure', 'Metal'] / df_vsx['cout_metal']) 
        df_vsx['cout_cristal'] = np.ceil(df.loc['Total Heure', 'Cristal'] / df_vsx['cout_cristal']) 
        df_vsx['cout_deut'] = np.ceil(df.loc['Total Heure', 'Deut'] / df_vsx['cout_deut'])
        
        df_vsx['Par Heure'] = df_vsx[['cout_metal', 'cout_cristal', 'cout_deut']].min(axis=1)
        df_vsx['Par jour'] = df_vsx['Par Heure'] * 24
        df_vsx['Par Semaine'] = df_vsx['Par jour'] * 7
    
        st.dataframe(df_vsx[['Par Heure', 'Par jour', 'Par Semaine']], use_container_width=True)