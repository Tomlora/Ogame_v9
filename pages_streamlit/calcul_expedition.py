import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from streamlit_extras.metric_cards import style_metric_cards


PALIERS_EXPEDITION = [
    (10_000, '<10k'),
    (100_000, '<100k'),
    (1_000_000, '<1M'),
    (5_000_000, '<5M'),
    (25_000_000, '<25M'),
    (50_000_000, '<50M'),
    (75_000_000, '<75M'),
    (100_000_000, '<100M'),
    (float('inf'), '>100M'),
]

DICT_MAX_METAL = {
    '<10k': 40_000,
    '<100k': 500_000,
    '<1M': 1_200_000,
    '<5M': 1_800_000,
    '<25M': 2_400_000,
    '<50M': 3_000_000,
    '<75M': 3_600_000,
    '<100M': 4_200_000,
    '>100M': 5_000_000,
}

VAISSEAUX = [
    'Chasseur Léger',
    'Chasseur Lourd',
    'Croiseur',
    'Vaisseau de bataille',
    'Traqueur',
    'Bombardier',
    'Destructeur',
    'Etoile de la mort',
    'Faucheur',
    'Eclaireur',
    'Petit transporteur',
    'Grand transporteur',
    'Vaisseau de colonisation',
    'Recycleur',
    'Sonde',
]

COUT_METAL = [
    3_000, 6_000, 20_000, 45_000, 30_000, 50_000, 60_000, 5_000_000,
    85_000, 8_000, 2_000, 6_000, 10_000, 10_000, 0,
]
COUT_CRISTAL = [
    1_000, 4_000, 7_000, 15_000, 40_000, 25_000, 50_000, 4_000_000,
    55_000, 15_000, 2_000, 6_000, 20_000, 6_000, 1_000,
]
COUT_DEUT = [
    0, 0, 2_000, 0, 15_000, 15_000, 15_000, 1_000_000,
    20_000, 8_000, 0, 0, 10_000, 2_000, 0,
]
FRET_BASE = [
    50, 100, 800, 1_500, 750, 500, 2_000, 1_000_000,
    10_000, 10_000, 5_000, 25_000, 7_500, 20_000, 5,
]

RECUPERABLE_SI_PRESENT = {
    'Chasseur Léger': [
        'Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille',
        'Traqueur', 'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
        'Petit transporteur', 'Grand transporteur',
    ],
    'Chasseur Lourd': [
        'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur',
        'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
        'Grand transporteur',
    ],
    'Croiseur': [
        'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille', 'Traqueur',
        'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
    ],
    'Vaisseau de bataille': [
        'Vaisseau de bataille', 'Traqueur', 'Bombardier', 'Destructeur',
        'Faucheur', 'Eclaireur',
    ],
    'Traqueur': [
        'Vaisseau de bataille', 'Traqueur', 'Bombardier', 'Destructeur',
        'Faucheur',
    ],
    'Bombardier': ['Traqueur', 'Bombardier', 'Destructeur', 'Faucheur'],
    'Destructeur': ['Bombardier', 'Destructeur', 'Faucheur'],
    'Faucheur': ['Destructeur', 'Faucheur'],
    'Eclaireur': [
        'Croiseur', 'Vaisseau de bataille', 'Traqueur', 'Bombardier',
        'Destructeur', 'Faucheur', 'Eclaireur',
    ],
    'Petit transporteur': [
        'Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille',
        'Traqueur', 'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
        'Petit transporteur', 'Grand transporteur', 'Sonde',
    ],
    'Sonde': [
        'Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille',
        'Traqueur', 'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
        'Petit transporteur', 'Grand transporteur', 'Sonde',
    ],
    'Grand transporteur': [
        'Chasseur Léger', 'Chasseur Lourd', 'Croiseur', 'Vaisseau de bataille',
        'Traqueur', 'Bombardier', 'Destructeur', 'Faucheur', 'Eclaireur',
        'Grand transporteur',
    ],
}


def mise_en_forme_number(number):
    return f'{int(number):,}'.replace(',', ' ')


def get_palier_expedition(points_top_1):
    for index, (limite, palier) in enumerate(PALIERS_EXPEDITION):
        if points_top_1 < limite:
            return index, palier

    return len(PALIERS_EXPEDITION) - 1, PALIERS_EXPEDITION[-1][1]


def creer_table_flotte():
    return pd.DataFrame({
        'Vaisseau': VAISSEAUX,
        'Quantité': np.zeros(len(VAISSEAUX), dtype=np.int64),
    })


def calculer_expedition(
    palier,
    flotte,
    vitesse_eco,
    tech_hyperespace,
    classe_explorateur,
    bonus_res,
    bonus_vdx,
    bonus_fret_fdv,
    bonus_n3,
    taux_ferrailleur,
):
    quantites = flotte.set_index('Vaisseau')['Quantité'].astype(int)
    facteur_classe = 1.5 if classe_explorateur else 1
    facteur_eclaireur = 2 if quantites.get('Eclaireur', 0) > 0 else 1

    max_metal = int(
        DICT_MAX_METAL[palier]
        * vitesse_eco
        * facteur_classe
        * facteur_eclaireur
    )
    max_cristal = int(max_metal / 2)
    max_deut = int(max_metal / 3)

    df_res = pd.DataFrame(
        [max_metal, max_cristal, max_deut],
        index=['Metal', 'Cristal', 'Deut'],
        columns=['Ressources'],
    )
    df_res['Forme de vie'] = np.int64(df_res['Ressources'] * bonus_res)
    df_res['Forme de Vie N3'] = np.int64(
        (df_res['Ressources'] + df_res['Forme de vie']) * bonus_n3
    )
    df_res['Total'] = (
        df_res['Ressources']
        + df_res['Forme de vie']
        + df_res['Forme de Vie N3']
    )

    df_expe = pd.DataFrame({'Nombre': quantites.reindex(VAISSEAUX, fill_value=0)})
    df_expe['Recuperable'] = 'Non'

    for vaisseau_cible, vaisseaux_requis in RECUPERABLE_SI_PRESENT.items():
        if df_expe.loc[vaisseaux_requis, 'Nombre'].sum() > 0:
            df_expe.loc[vaisseau_cible, 'Recuperable'] = 'Oui'

    df_expe['cout_metal'] = COUT_METAL
    df_expe['cout_cristal'] = COUT_CRISTAL
    df_expe['cout_deut'] = COUT_DEUT
    df_expe['Structure'] = df_expe['cout_metal'] + df_expe['cout_cristal']

    bonus_fret_hyperespace = tech_hyperespace * 0.05
    df_expe['fret'] = np.array(FRET_BASE, dtype=float)
    df_expe['fret'] *= 1 + bonus_fret_hyperespace
    df_expe['fret'] *= 1 + bonus_fret_fdv
    df_expe['fret_dispo'] = df_expe['Nombre'] * df_expe['fret']

    fret_dispo = df_expe['fret_dispo'].sum()
    max_metal_with_fdv = df_res.loc['Metal', 'Total']

    # Le comportement historique est conservé : si le fret est insuffisant,
    # la valeur affichée est le fret réellement disponible et la différence
    # reste négative par rapport au maximum récupérable.
    if max_metal < fret_dispo:
        montant_max = max_metal_with_fdv
        montant_max_vsx = max_metal
    else:
        montant_max = fret_dispo
        montant_max_vsx = fret_dispo

    df_expe['Vaisseau récupérable'] = np.where(
        df_expe['Recuperable'] == 'Oui',
        np.floor(montant_max_vsx / df_expe['Structure']),
        0,
    ).astype(int)
    df_expe['Forme de vie'] = np.int64(
        np.floor(df_expe['Vaisseau récupérable'] * bonus_vdx)
    )
    df_expe['Forme de vie N3'] = np.int64(
        np.floor(df_expe['Vaisseau récupérable'] * bonus_vdx * bonus_n3)
    )
    df_expe['Total'] = np.int64(
        df_expe['Vaisseau récupérable']
        + df_expe['Forme de vie']
        + df_expe['Forme de vie N3']
    )

    df_expe['metal_total'] = (
        df_expe['cout_metal'] * df_expe['Total'] * (taux_ferrailleur / 100)
    )
    df_expe['cristal_total'] = (
        df_expe['cout_cristal'] * df_expe['Total'] * (taux_ferrailleur / 100)
    )
    df_expe['deut_total'] = (
        df_expe['cout_deut'] * df_expe['Total'] * (taux_ferrailleur / 100)
    )

    cargo_optimal = {
        'PT': int(np.ceil(max_metal_with_fdv / df_expe.loc['Petit transporteur', 'fret'])),
        'GT': int(np.ceil(max_metal_with_fdv / df_expe.loc['Grand transporteur', 'fret'])),
        'Eclaireur': int(np.ceil(max_metal_with_fdv / df_expe.loc['Eclaireur', 'fret'])),
    }

    return {
        'palier': palier,
        'df_res': df_res,
        'df_expe': df_expe,
        'fret_dispo': fret_dispo,
        'montant_max': montant_max,
        'max_metal_with_fdv': max_metal_with_fdv,
        'metal_collectable': montant_max - max_metal_with_fdv,
        'cristal_collectable': montant_max / 2 - max_metal_with_fdv / 2,
        'deut_collectable': montant_max / 3 - max_metal_with_fdv / 3,
        'cargo_optimal': cargo_optimal,
    }


def creer_figure_vaisseaux(df_expe):
    df_affiche = df_expe[df_expe['Vaisseau récupérable'] > 0]
    fig = go.Figure()
    fig.add_bar(
        x=df_affiche.index,
        y=df_affiche['Vaisseau récupérable'],
        name='Vaisseaux récupérables',
        marker_color='#0000CC',
    )
    fig.add_bar(
        x=df_affiche.index,
        y=df_affiche['Forme de vie'],
        name='Bonus Forme de vie',
        marker_color='#00BFFF',
    )
    fig.add_bar(
        x=df_affiche.index,
        y=df_affiche['Forme de vie N3'],
        name='Bonus Forme de vie N3',
        marker_color='#B0C4DE',
    )
    fig.update_layout(
        title='Quantité de vaisseaux récupérables',
        barmode='stack',
        bargap=0.15,
        legend_title_text='',
        xaxis_title='',
        yaxis_title='Quantité',
    )
    return fig


def creer_figure_ressources(df_expe):
    return go.Figure(
        data=[
            go.Pie(
                labels=['Métal', 'Cristal', 'Deutérium'],
                values=[
                    df_expe['metal_total'].sum(),
                    df_expe['cristal_total'].sum(),
                    df_expe['deut_total'].sum(),
                ],
            )
        ],
        layout=go.Layout(title='Vaisseaux convertis en ressources'),
    )


def afficher_resultat(resultat):
    montant_max = resultat['montant_max']

    st.subheader(f"Résultat — palier {resultat['palier']}")
    kpi_metal, kpi_cristal, kpi_deut = st.columns(3)
    with kpi_metal:
        st.metric(
            'Métal collectable',
            mise_en_forme_number(montant_max),
            mise_en_forme_number(resultat['metal_collectable']),
        )
    with kpi_cristal:
        st.metric(
            'Cristal collectable',
            mise_en_forme_number(montant_max / 2),
            mise_en_forme_number(resultat['cristal_collectable']),
        )
    with kpi_deut:
        st.metric(
            'Deutérium collectable',
            mise_en_forme_number(montant_max / 3),
            mise_en_forme_number(resultat['deut_collectable']),
        )

    if resultat['metal_collectable'] < 0:
        st.caption(
            'La différence négative correspond aux ressources non récupérables '
            'avec le fret actuellement disponible.'
        )

    st.subheader('Fret optimal')
    cargo_dispo, cargo_pt, cargo_gt, cargo_eclaireur = st.columns(4)
    with cargo_dispo:
        st.metric('Cargo disponible', mise_en_forme_number(resultat['fret_dispo']))
    with cargo_pt:
        st.metric(
            'Cargo optimal PT',
            f"{mise_en_forme_number(resultat['cargo_optimal']['PT'])} vaisseaux",
        )
    with cargo_gt:
        st.metric(
            'Cargo optimal GT',
            f"{mise_en_forme_number(resultat['cargo_optimal']['GT'])} vaisseaux",
        )
    with cargo_eclaireur:
        st.metric(
            'Cargo optimal Éclaireur',
            f"{mise_en_forme_number(resultat['cargo_optimal']['Eclaireur'])} vaisseaux",
        )

    tab_vaisseaux, tab_ressources, tab_details = st.tabs(
        ['Vaisseaux récupérables', 'Ressources', 'Détails du calcul']
    )

    with tab_vaisseaux:
        colonne_tableau, colonne_graphique = st.columns([1.1, 1])
        with colonne_tableau:
            df_expe_format = resultat['df_expe'][[
                'Recuperable',
                'Vaisseau récupérable',
                'Forme de vie',
                'Forme de vie N3',
                'Total',
            ]].copy()
            for colonne in [
                'Vaisseau récupérable',
                'Forme de vie',
                'Forme de vie N3',
                'Total',
            ]:
                df_expe_format[colonne] = df_expe_format[colonne].map(
                    mise_en_forme_number
                )
            st.dataframe(df_expe_format, width='stretch', height=560)
        with colonne_graphique:
            st.plotly_chart(
                creer_figure_vaisseaux(resultat['df_expe']),
                width='stretch',
            )

    with tab_ressources:
        colonne_tableau, colonne_graphique = st.columns([1.1, 1])
        with colonne_tableau:
            df_expe_copy = resultat['df_expe'].copy()
            df_expe_copy.loc['Total'] = df_expe_copy.sum(numeric_only=True)
            for colonne in ['Total', 'metal_total', 'cristal_total', 'deut_total']:
                df_expe_copy[colonne] = df_expe_copy[colonne].map(
                    mise_en_forme_number
                )
            st.dataframe(
                df_expe_copy[['Total', 'metal_total', 'cristal_total', 'deut_total']],
                width='stretch',
                height=605,
            )
        with colonne_graphique:
            st.plotly_chart(
                creer_figure_ressources(resultat['df_expe']),
                width='stretch',
            )

    with tab_details:
        st.write('Ressources maximales avant limitation par le fret')
        df_res_format = resultat['df_res'].copy()
        for colonne in ['Ressources', 'Forme de vie', 'Forme de Vie N3', 'Total']:
            df_res_format[colonne] = df_res_format[colonne].map(
                mise_en_forme_number
            )
        st.dataframe(df_res_format, width='stretch')


def afficher_comparaison(resultat_actuel, resultat_suivant):
    st.subheader('Comparaison des paliers')
    comparaison = pd.DataFrame(
        {
            'Indicateur': [
                'Métal maximal',
                'Cristal maximal',
                'Deutérium maximal',
                'Cargo optimal PT',
                'Cargo optimal GT',
                'Cargo optimal Éclaireur',
            ],
            f"Palier actuel ({resultat_actuel['palier']})": [
                resultat_actuel['max_metal_with_fdv'],
                resultat_actuel['max_metal_with_fdv'] / 2,
                resultat_actuel['max_metal_with_fdv'] / 3,
                resultat_actuel['cargo_optimal']['PT'],
                resultat_actuel['cargo_optimal']['GT'],
                resultat_actuel['cargo_optimal']['Eclaireur'],
            ],
            f"Palier suivant ({resultat_suivant['palier']})": [
                resultat_suivant['max_metal_with_fdv'],
                resultat_suivant['max_metal_with_fdv'] / 2,
                resultat_suivant['max_metal_with_fdv'] / 3,
                resultat_suivant['cargo_optimal']['PT'],
                resultat_suivant['cargo_optimal']['GT'],
                resultat_suivant['cargo_optimal']['Eclaireur'],
            ],
        }
    )
    comparaison['Différence'] = (
        comparaison.iloc[:, 2] - comparaison.iloc[:, 1]
    )
    for colonne in comparaison.columns[1:]:
        comparaison[colonne] = comparaison[colonne].map(mise_en_forme_number)
    st.dataframe(comparaison, hide_index=True, width='stretch')

    tab_actuel, tab_suivant = st.tabs([
        f"Palier actuel ({resultat_actuel['palier']})",
        f"Palier suivant ({resultat_suivant['palier']})",
    ])
    with tab_actuel:
        afficher_resultat(resultat_actuel)
    with tab_suivant:
        afficher_resultat(resultat_suivant)


def calcul_expe():
    style_metric_cards(
        background_color='#03152A',
        border_color='#0083B9',
        border_left_color='#0083B9',
        border_size_px=1,
        box_shadow=False,
        border_radius_px=0,
    )

    points_top_1 = st.session_state['top1']
    palier_actuel_index, palier_actuel = get_palier_expedition(points_top_1)
    palier_suivant = None
    points_avant_palier = None

    if palier_actuel_index < len(PALIERS_EXPEDITION) - 1:
        palier_suivant = PALIERS_EXPEDITION[palier_actuel_index + 1][1]
        limite_actuelle = PALIERS_EXPEDITION[palier_actuel_index][0]
        points_avant_palier = max(0, int(limite_actuelle - points_top_1))

    st.header('Calculateur d’expédition')
    resume_top, resume_actuel, resume_suivant = st.columns(3)
    with resume_top:
        st.metric('Points du top 1', mise_en_forme_number(points_top_1))
    with resume_actuel:
        st.metric('Palier actuel', palier_actuel)
    with resume_suivant:
        if palier_suivant is None:
            st.metric('Prochain palier', 'Palier maximal atteint')
        else:
            st.metric(
                'Prochain palier',
                palier_suivant,
                f'{mise_en_forme_number(points_avant_palier)} points restants',
                delta_color='off',
            )

    marge_gauche, contenu, marge_droite = st.columns([1, 6, 1])
    with contenu:
        with st.form('Calcul expedition', border=False):
            comparer_palier_suivant = st.toggle(
                'Comparer avec le palier suivant',
                value=False,
                disabled=palier_suivant is None,
                help=(
                    'Le calcul utilise toujours le palier actuel par défaut. '
                    'Activez cette option pour afficher simultanément le palier suivant.'
                ),
            )

            colonne_parametres, colonne_fdv = st.columns(2, gap='large')

            with colonne_parametres:
                with st.container(border=True):
                    st.subheader('Paramètres principaux')
                    tech_hyperespace = st.slider(
                        'Technologie Hyperespace', 0, 30, 1
                    )
                    classe_explorateur = st.checkbox('Classe Explorateur')
                    taux_ferrailleur = st.slider(
                        'Taux Ferrailleur (%)',
                        min_value=35,
                        max_value=100,
                        value=100,
                        help=(
                            'Impacte les ressources récupérées lorsque les '
                            'vaisseaux sont envoyés au ferrailleur.'
                        ),
                    )

            with colonne_fdv:
                with st.expander('Bonus de forme de vie', expanded=True):
                    fdv_gauche, fdv_droite = st.columns(2)
                    with fdv_gauche:
                        bonus_res = st.number_input(
                            'Bonus ressources (%)',
                            min_value=0.0,
                            value=0.0,
                            format='%.2f',
                        )
                        bonus_vdx = st.number_input(
                            'Bonus vaisseaux (%)',
                            min_value=0.0,
                            value=0.0,
                            format='%.2f',
                        )
                        bonus_am = st.number_input(
                            'Bonus antimatière (%)',
                            min_value=0.0,
                            value=0.0,
                            format='%.2f',
                            help='Conservé pour les évolutions futures du calculateur.',
                        )
                    with fdv_droite:
                        bonus_fret_fdv = st.number_input(
                            'Bonus fret (%)',
                            min_value=0.0,
                            value=0.0,
                            format='%.2f',
                        )
                        bonus_n3 = st.number_input(
                            'Bonus Tech Explorateur 3_6 (%)',
                            min_value=0.0,
                            value=0.0,
                            format='%.2f',
                            help='Saisissez 0 si la classe Explorateur n’est pas active.',
                        )

            st.subheader('Flotte envoyée')
            flotte = st.data_editor(
                creer_table_flotte(),
                hide_index=True,
                width='stretch',
                height=570,
                disabled=['Vaisseau'],
                column_config={
                    'Vaisseau': st.column_config.TextColumn(
                        'Vaisseau',
                        width='large',
                    ),
                    'Quantité': st.column_config.NumberColumn(
                        'Quantité',
                        min_value=0,
                        step=1,
                        format='%d',
                        width='small',
                    ),
                },
                key='flotte_expedition',
            )

            submitted = st.form_submit_button(
                'Calculer l’expédition',
                type='primary',
                width='stretch',
            )

    if not submitted:
        return

    flotte['Quantité'] = (
        pd.to_numeric(flotte['Quantité'], errors='coerce')
        .fillna(0)
        .clip(lower=0)
        .astype(int)
    )

    parametres_communs = {
        'flotte': flotte,
        'vitesse_eco': st.session_state['vitesse_eco'],
        'tech_hyperespace': tech_hyperespace,
        'classe_explorateur': classe_explorateur,
        'bonus_res': bonus_res / 100,
        'bonus_vdx': bonus_vdx / 100,
        'bonus_fret_fdv': bonus_fret_fdv / 100,
        'bonus_n3': bonus_n3 / 100,
        'taux_ferrailleur': taux_ferrailleur,
    }

    # Le bonus antimatière n'entre pas encore dans les résultats affichés.
    _ = bonus_am

    resultat_actuel = calculer_expedition(
        palier=palier_actuel,
        **parametres_communs,
    )

    if comparer_palier_suivant and palier_suivant is not None:
        resultat_suivant = calculer_expedition(
            palier=palier_suivant,
            **parametres_communs,
        )
        afficher_comparaison(resultat_actuel, resultat_suivant)
    else:
        afficher_resultat(resultat_actuel)
