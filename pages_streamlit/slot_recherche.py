import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

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
        with st.form('Formulaire'):
            tech1 = st.selectbox('Slot 1', data_research[data_research['Type'] == f'Tech 1']['Name FR'])
            tech2 = st.selectbox('Slot 2', data_research[data_research['Type'] == f'Tech 2']['Name FR'])
            tech3 = st.selectbox('Slot 3', data_research[data_research['Type'] == f'Tech 3']['Name FR'])
            tech4 = st.selectbox('Slot 4', data_research[data_research['Type'] == f'Tech 4']['Name FR'])
            tech5 = st.selectbox('Slot 5', data_research[data_research['Type'] == f'Tech 5']['Name FR'])
            tech6 = st.selectbox('Slot 6', data_research[data_research['Type'] == f'Tech 6']['Name FR'])
            tech7 = st.selectbox('Slot 7', data_research[data_research['Type'] == f'Tech 7']['Name FR'])
            tech8 = st.selectbox('Slot 8', data_research[data_research['Type'] == f'Tech 8']['Name FR'])
            tech9 = st.selectbox('Slot 9', data_research[data_research['Type'] == f'Tech 9']['Name FR'])
            tech10 = st.selectbox('Slot 10', data_research[data_research['Type'] == f'Tech 10']['Name FR'])
            tech11 = st.selectbox('Slot 11', data_research[data_research['Type'] == f'Tech 11']['Name FR'])
            tech12 = st.selectbox('Slot 12', data_research[data_research['Type'] == f'Tech 12']['Name FR'])
            tech13 = st.selectbox('Slot 13', data_research[data_research['Type'] == f'Tech 13']['Name FR'])
            tech14 = st.selectbox('Slot 14', data_research[data_research['Type'] == f'Tech 14']['Name FR'])
            tech15 = st.selectbox('Slot 15', data_research[data_research['Type'] == f'Tech 15']['Name FR'])
            tech16 = st.selectbox('Slot 16', data_research[data_research['Type'] == f'Tech 16']['Name FR'])
            tech17 = st.selectbox('Slot 17', data_research[data_research['Type'] == f'Tech 17']['Name FR'])
            tech18 = st.selectbox('Slot 18', data_research[data_research['Type'] == f'Tech 18']['Name FR'])
            
            submitted = st.form_submit_button('Valider')
            
        if submitted: # tout à faire
                tech_all = [tech1, tech2, tech3, tech4, tech5, tech6, tech7, tech8, tech9, tech10, tech11, tech12, tech13, tech14, tech15, tech16, tech17, tech18]
                
                df_selected = data_research[data_research['Name FR'].isin(tech_all)]
                
                # On sort sur les tech
                df_selected['sort'] = df_selected['Type'].str.extract('(\d+)', expand=False).astype(int)
                df_selected.sort_values('sort',inplace=True, ascending=True)
                df_selected = df_selected.drop('sort', axis=1)
                
                
                # df_selected.sort_values(['Type'], inplace=True)
                
                st.dataframe(df_selected)
                
                st.write('Par race')
                
                st.write(df_selected['Lifeform'].value_counts())
                
                # download
                
                df_download = to_excel(df_selected)
                

                st.download_button('Télécharger mes choix au format Excel', data=df_download, file_name='recherches_selected.xlsx')
                


