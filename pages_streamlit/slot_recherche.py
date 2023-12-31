import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import numpy as np

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)  # set column width  
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def slot(data, cost_v9):

    st.subheader('Choix des technologies v10')

    data = data.merge(cost_v9[['Name EN', 'bonus 1 base value', 'bonus 1 max']], on='Name EN')

    data_research = data[data['Type'] != 'Building'][['Name FR', 'Description FR', 'Type', 'Lifeform', 'bonus 1 base value', 'bonus 1 max']]

    data_research['bonus 1 base value'] = round(data_research['bonus 1 base value'], 2)

    value = st.slider('Slot', 1, 18, 1)

    if value <= 6:
        niv = 1
        ecart_tech = value
    elif value > 6 and value <= 12:
        niv = 2
        ecart_tech = value - 6
    else:
        niv = 3
        ecart_tech = value - 12
        
    pop_requise = ['0', '200.000', '300.000', '400.000', '500.000', '750.000', '1.000.000',
                '1.200.000', '3.000.000', '5.000.000', '7.000.000', '9.000.000', '11.000.000',
                '13.000.000', '26.000.000', '56.000.000', '112.000.000', '224.000.000', '448.000.000']
        
    st.markdown(f'Technologie {niv}.{ecart_tech} (Palier {niv})')

    st.markdown(f'Population de niveau {niv} requise : {pop_requise[value]}')

    data_research_tri = data_research[data_research['Type'] == f'Tech {value}']

    data_research_tri.drop(['Type'], axis=1, inplace=True) # on en a plus besoin

    data_research_tri.columns = ['Name FR', 'Description FR', 'Race', 'Bonus par level (%)', 'Bonus Max']

    st.write(data_research_tri)


    url = 'https://board.fr.ogame.gameforge.com/index.php?thread/746784-tutoriel-les-formes-de-vies/'

    st.markdown("Lien vers le [tutoriel ogame](%s)" % url)
    
    st.write('------------------')
    
    with st.expander('Faire son choix'):
        race = st.radio('Race', data_research['Lifeform'].unique(), horizontal=True)
            
        # Filtre sur le niveau des recherches    
        col1, col2, col3 = st.columns(3)
        niv1 = col1.checkbox('Tech niveau 1', value=True)
        niv2 = col2.checkbox('Tech niveau 2', value=True)
        niv3 = col3.checkbox('Tech niveau 3', value=True)
            
        range_slot = []
            
        if niv1 == True:
            range_slot += list(range(1,7))
        if niv2 == True:
            range_slot += list(range(7,13))
        if niv3 == True:
            range_slot += list(range(13,19))
            
        with st.form('Formulaire'):
            
            liste_tech = [st.selectbox(f'Slot {number}', data_research[data_research['Type'] == f'Tech {number}']['Name FR']) for number in range_slot]

            submitted = st.form_submit_button('Valider')
            
        if submitted:
                
                tech_all = liste_tech
                df_selected = data_research[data_research['Name FR'].isin(tech_all)]
                
                # on calcule le nombre d'artefacts nécessaires
                def niveau(x):
                    if x in [f'Tech {niv}' for niv in range(0,7)]:
                        return 1
                    elif x in [f'Tech {niv}' for niv in range(7,13)]:
                        return 2
                    elif x in [f'Tech {niv}' for niv in range(13,19)]:
                        return 3
                
                # niveau de la recherche, qui permettra d'évaluer le nombre d'artefacts
                df_selected['Niveau'] = df_selected['Type'].apply(lambda x : niveau(x))
                              
                cout_dict = {1 : 200, 2: 400, 3: 600}

                df_selected['Cout_artefact'] = df_selected['Niveau'].apply(lambda x : cout_dict[x])
                
                # si c'est notre race, cela coutera 0
                df_selected['Cout_artefact'] = np.where(df_selected['Lifeform'] == race, 0, df_selected['Cout_artefact'])
                
                # total
                cout_arte = df_selected['Cout_artefact'].sum()
                
                # On sort sur les tech
                df_selected['sort'] = df_selected['Type'].str.extract('(\d+)', expand=False).astype(int)
                df_selected.sort_values('sort',inplace=True, ascending=True)
                df_selected = df_selected.drop('sort', axis=1)
                
                
                # df_selected.sort_values(['Type'], inplace=True)
                
                st.dataframe(df_selected, use_container_width=True)
                
                st.write('Par race')
                
                st.write(df_selected['Lifeform'].value_counts())
                
                st.info(f'Cela coutera {cout_arte} artefacts.')
                
                # download
                
                df_download = to_excel(df_selected)
                

                st.download_button('Télécharger mes choix au format Excel', data=df_download, file_name='recherches_selected.xlsx')
                


