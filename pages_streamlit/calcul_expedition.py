import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from streamlit_extras.metric_cards import style_metric_cards


def calcul_expe():
    
    style_metric_cards(background_color='#03152A', border_color='#0083B9', border_left_color='#0083B9', border_size_px=1, box_shadow=False, border_radius_px=0)
    
    def mise_en_forme_number(number, type='int'):
        if type == 'int':
            new_number = "{:,}".format(int(number)).replace(',', ' ').replace('.', ',')
        elif type == 'float':
            new_number = "{:,}".format(number).replace(',', ' ').replace('.', ',')
        return new_number 
    
    with st.form('Calcul expedition'):
        st.subheader('Univers & Compte')
        
        # A retravailler
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
     
        st.markdown(f'Palier : **{points_top_1}** || (Points du top 1 : **{mise_en_forme_number(st.session_state["top1"])}**)')
        tech_hyperespace = st.slider('Technologie Hyperespace', 0, 30, 1)
        bonus_fret = tech_hyperespace * 0.05
        
        st.subheader('Classe')
        # Explorateur ?
        classe = st.checkbox('Classe Explorateur')
        if classe:
            classe_facteur = 1.5
        else:
            classe_facteur = 1
            
        
            
        st.subheader('Forme de vie')
        
        st.info("Pour les bonus Explorateur en détail, il faut aller dans l'onglet Calcul Bonus T3")
        
        bonus_res = st.number_input('Bonus ressources en %', 0.0, value=0.0, format='%.2f', help="10.2% s'écrit 10.2")
        bonus_vdx = st.number_input('Bonus vaisseaux en %', 0.0, value=0.0, format='%.2f', help="10.2% s'écrit 10.2")
        bonus_am = st.number_input('Bonus AM en %', 0.0, value=0.0, format='%.2f',help="10.2% s'écrit 10.2")
        bonus_fret_fdv = st.number_input('Bonus fret en %', 0.0, value=0.0, format='%.2f', help="10.2% s'écrit 10.2")
        
        bonus_res = bonus_res / 100
        bonus_vdx = bonus_vdx / 100
        bonus_am = bonus_am / 100
        bonus_fret_fdv = bonus_fret_fdv / 100
        
        st.subheader('Flotte')
        
        cle = st.number_input('Chasseur léger', 0, value=0)
        chlo = st.number_input('Chasseur lourd', 0, value=0)
        cro = st.number_input('Croiseur', 0, value=0)
        vb = st.number_input('Vaisseau de bataille', 0, value=0)
        traq = st.number_input('Traqueur', 0, value=0)
        bb = st.number_input('Bombardier', 0, value=0)
        destro = st.number_input('Destructeur', 0, value=0)
        edlm = st.number_input('Etoile de la mort', 0, value=0)
        faucheur = st.number_input('Faucheur', 0, value=0)
        eclaireur = st.number_input('Eclaireur', 0, value=0)
        pt = st.number_input('Petit transporteur', 0, value=0)
        gt = st.number_input('Grand transporteur', 0, value=0)
        vc = st.number_input('Vaisseau de colonisation', 0, value=0)
        recycleur = st.number_input('Recycleur', 0, value=0)
        sonde = st.number_input('Sonde', 0, value=0)
        
        st.subheader('Paramètres supplémentaires')
        
        taux_ferrailleur = st.slider('Taux Ferrailleur (%)', min_value=35, max_value=100, value=100, help='Ce paramètre impacte le tableau Ressources (vaisseaux), vous permettant de savoir les ressources collectables via le ferrailleur.')
        
        submitted = st.form_submit_button('Valider')
        
    if submitted:
        
        # calcul res max
        
        dict_max_metal = {'<10k' : 40000,
                     '<100k': 500000,
                     '<1M' : 1200000,
                     '<5M' : 1800000,
                     '<25M': 2400000,
                     '<50M' : 3000000,
                     '<75M' : 3600000,
                     '<100M' : 4200000 ,
                     '>100M' : 5000000}
             
        
        
        if eclaireur > 0:
            facteur_eclaireur = 2
        else:
            facteur_eclaireur = 1
        
        max_metal = int(dict_max_metal[points_top_1] * st.session_state["vitesse_eco"] * classe_facteur * facteur_eclaireur)
        max_cristal = int(max_metal / 2)
        max_deut = int(max_metal / 3)
        
        df_res = pd.DataFrame([max_metal, max_cristal, max_deut], index=['Metal', 'Cristal', 'Deut'], columns=['Ressources'])
        df_res['Forme de vie'] = np.int64(df_res['Ressources'] * bonus_res)
        df_res['Total'] = df_res['Ressources'] + df_res['Forme de vie']
        
        # calcul vaisseau
        
        df_expe = pd.DataFrame([cle, chlo, cro, vb, traq, bb, destro, edlm, faucheur, eclaireur, pt, gt, vc, recycleur, sonde], columns=['Nombre'])
        df_expe.index=['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur',
                                        'Bombardier', 'Destructeur', 'Etoile de la mort', 'Faucheur', 'Eclaireur',
                                        'Petit transporteur', 'Grand transporteur', 'Vaisseau de colonisation', 'Recycleur', 'Sonde']
        
        df_expe['Recuperable'] = 'Non'
        
        def vsx_recup(nombre_sum, vsx_target):
            if df_expe.loc[nombre_sum]['Nombre'].sum() > 0:
                for vsx in vsx_target:
                    df_expe.loc[vsx, 'Recuperable'] = 'Oui'
                
        vsx_recup(['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur', 'Petit transporteur', 'Grand transporteur'], ['Chasseur Léger'])
        vsx_recup(['Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur', 'Grand transporteur'], ['Chasseur Lourd']) 
        vsx_recup(['Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur'], ['Croiseur']) 
        vsx_recup(['Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur'], ['Vaisseau de bataille'])
        vsx_recup(['Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur'], ['Traqueur'])
        vsx_recup(['Traqueur', 'Bombardier', 'Destructeur', 'Faucheur'], ['Bombardier'])
        vsx_recup(['Bombardier', 'Destructeur', 'Faucheur'], ['Destructeur'])
        vsx_recup(['Destructeur', 'Faucheur'], ['Faucheur'])   
        vsx_recup(['Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur'], ['Eclaireur'])
        vsx_recup(['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur', 'Petit transporteur', 'Grand transporteur', 'Sonde'], ['Petit transporteur', 'Sonde'])
        vsx_recup(['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur', 
                  'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur', 'Grand transporteur'], ['Grand transporteur'])
        
        df_expe['cout_metal'] = [3000, 6000, 20000, 45000, 30000, 50000, 60000, 5000000, 85000, 8000, 2000, 6000, 10000, 10000, 0]
        df_expe['cout_cristal'] = [1000, 4000, 7000, 15000, 40000, 25000, 50000, 4000000, 55000, 15000, 2000, 6000, 20000, 6000, 1000]
        df_expe['cout_deut'] = [0, 0, 2000, 0, 15000, 15000, 15000, 1000000, 20000, 8000, 0, 0, 10000, 2000, 0]          
        df_expe['Structure'] = df_expe['cout_metal'] + df_expe['cout_cristal']
        
        df_expe['fret'] = [50, 100, 800, 1500, 750, 500, 2000, 1000000, 10000, 10000, 5000, 25000, 7500, 20000, 5]
        df_expe['fret'] = df_expe['fret'] * (1 + bonus_fret)
        df_expe['fret'] = df_expe['fret'] * (1 + bonus_fret_fdv)
        
        df_expe['fret_dispo'] = df_expe['Nombre'] * df_expe['fret']
        fret_dispo = df_expe['fret_dispo'].sum()
        
        max_metal_with_fdv = df_res.loc['Metal', 'Total']
        
        if max_metal < fret_dispo:
            montant_max = max_metal_with_fdv
            montant_max_vsx = max_metal
        else:
            montant_max = fret_dispo
            montant_max_vsx = fret_dispo
            
        print(montant_max)
        print(montant_max_vsx)
            
        df_expe['Vaisseau récupérable'] = 0
        
        df_expe['Vaisseau récupérable'] = np.where(df_expe['Recuperable'] == 'Oui',
                                                   np.floor(montant_max_vsx / df_expe['Structure']),
                                                   df_expe['Vaisseau récupérable'])
        
        df_expe['Vaisseau récupérable'] = df_expe['Vaisseau récupérable'].astype('int')
        
        df_expe['Forme de vie'] = np.int64(
            np.floor(df_expe['Vaisseau récupérable'] * bonus_vdx))
        
        df_expe['Total'] = np.int64(df_expe['Vaisseau récupérable'] + df_expe['Forme de vie'])
        
        

        
        fig = go.Figure()
        i = 0
        for vsx in ['Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur',
                                        'Bombardier', 'Destructeur', 'Etoile de la mort', 'Faucheur', 'Eclaireur',
                                        'Petit transporteur', 'Grand transporteur', 'Vaisseau de colonisation', 'Recycleur']:
            
            if i == 0:
                showlegend = True
            else:
                showlegend = False
            
            if df_expe.loc[vsx, 'Vaisseau récupérable'] > 0:
                fig.add_trace(go.Histogram(histfunc='sum',
                x=[vsx],
                y=[df_expe.loc[vsx, 'Total']],
                name='Vaisseaux récupérables',
                texttemplate="%{y}",
                marker_color = '#0000CC',
                showlegend=showlegend))

                fig.add_trace(go.Histogram(histfunc='sum',
                        x=[vsx],
                        y=[df_expe.loc[vsx, 'Forme de vie']],
                        name="Dont Bonus Forme de vie",
                        texttemplate="%{y}",
                        marker_color = '#00BFFF',
                        showlegend=showlegend))
                
                i += 1

        fig.update_layout(
            title='Quantité de vaisseaux',
            barmode="overlay",
            bargap=0.1)
        
        
        tab1, tab2 = st.tabs(['Vaisseaux', 'Ressources'])
        
        with tab1:
        
            st.subheader('Vaisseaux')
            vsx1, vsx2 = st.columns(2)
            
            with vsx1:
                df_expe_format = df_expe[['Recuperable', 'Vaisseau récupérable', 'Forme de vie', 'Total']].copy()
                
                for col in ['Vaisseau récupérable', 'Forme de vie', 'Total']:
                    df_expe_format[col] = df_expe_format[col].apply(lambda x : mise_en_forme_number(x))
                st.dataframe(df_expe_format, use_container_width=True, height=560)
            with vsx2:
                st.plotly_chart(fig)
        
        
            st.subheader('Ressources (vaisseaux)')
            
            df_expe['metal_total'] = (df_expe['cout_metal'] * df_expe['Total']) *(taux_ferrailleur / 100)
            df_expe['cristal_total'] = (df_expe['cout_cristal'] * df_expe['Total']) *(taux_ferrailleur / 100)
            df_expe['deut_total'] = (df_expe['cout_deut'] * df_expe['Total']) *(taux_ferrailleur / 100)
            vsx3, vsx4 = st.columns(2)
        
            with vsx3:
                df_expe_copy = df_expe.copy()
                df_expe_copy.loc['Total'] = df_expe_copy.sum(axis=0)
                for col in ['Total', 'metal_total', 'cristal_total', 'deut_total']:
                    df_expe_copy[col] = df_expe_copy[col].apply(lambda x : mise_en_forme_number(x))
                st.dataframe(df_expe_copy[['Total', 'metal_total', 'cristal_total', 'deut_total']], use_container_width=True, height=605)
            with vsx4:
                
                fig_ressource = go.Figure(data=[go.Pie(labels=['metal', 'cristal', 'deut'], values=[df_expe['metal_total'].sum(),
                                                                                                    df_expe['cristal_total'].sum(),
                                                                                                    df_expe['deut_total'].sum()])])
                fig_ressource.update_layout(
                title='Quantité de vaisseaux sous forme de ressources')              
                
                st.plotly_chart(fig_ressource)
        
        # Ressources
        
        with tab2:
        
            st.write('Ressources maximales')
            
            for col in ['Ressources', 'Forme de vie', 'Total']:
                df_res[col] = df_res[col].apply(lambda x : mise_en_forme_number(x))
            st.dataframe(df_res)
            
            metal_collectable = montant_max - max_metal_with_fdv
            cristal_collectable = montant_max/2 - max_metal_with_fdv/2
            deut_collectable = montant_max/3 - max_metal_with_fdv/3
            
            cargo_opti_gt = np.ceil(max_metal_with_fdv / df_expe.loc['Grand transporteur', 'fret'])
            cargo_opti_pt = np.ceil(max_metal_with_fdv / df_expe.loc['Petit transporteur', 'fret'])
            cargo_opti_eclaireur = np.ceil(max_metal_with_fdv / df_expe.loc['Eclaireur', 'fret'])
            
            
            carg1, carg2, carg3, carg4 = st.columns(4)
            
    
            
            with carg1:
                # st.metric('Cargo disponible', int(fret_dispo))
                st.metric('Cargo disponible', mise_en_forme_number(fret_dispo))
            with carg2:
                st.metric('Cargo optimal PT',f'{mise_en_forme_number(cargo_opti_pt)} vaisseaux')
            with carg3:
                st.metric('Cargo optimal GT',f'{mise_en_forme_number(cargo_opti_gt)} vaisseaux')
            with carg4:
                st.metric('Cargo optimal Eclaireur',f'{mise_en_forme_number(cargo_opti_eclaireur)} vaisseaux')
                
            
            
            kpi1, kpi2, kpi3 = st.columns(3)
            
            with kpi1:
                st.metric('Metal collectable', mise_en_forme_number(montant_max), mise_en_forme_number(metal_collectable))
            with kpi2:
                st.metric('Cristal collectable', mise_en_forme_number(montant_max/2), mise_en_forme_number(cristal_collectable))
            with kpi3:
                st.metric('Deut collectable', mise_en_forme_number(montant_max/3), mise_en_forme_number(deut_collectable))
        
        

    