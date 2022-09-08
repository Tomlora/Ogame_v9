import streamlit as st
import pandas as pd

from cout_v9 import data, cost_v9

st.set_page_config(
    page_title="Recherche v9",
    page_icon="✅",
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


st.title('Choix des technologies v9')

data = data.merge(cost_v9[['Name EN', 'bonus 1 base value', 'bonus 1 max']], on='Name EN')

data_research = data[data['Type'] != 'Building'][['Name FR', 'Description FR', 'Type', 'Lifeform', 'bonus 1 base value', 'bonus 1 max']]

data_research['bonus 1 base value'] = round(data_research['bonus 1 base value'], 2)

value = st.slider('Slot', 1, 18, 1)

if value <= 6:
    niv = 1
elif value > 6 and value <= 12:
    niv = 2
else:
    niv = 3
    
pop_requise = ['0', '200.000', '300.000', '400.000', '500.000', '750.000', '1.000.000',
               '1.200.000', '3.000.000', '5.000.000', '7.000.000', '9.000.000', '11.000.000',
               '13.000.000', '26.000.000', '56.000.000', '112.000.000', '224.000.000', '448.000.000']
    
st.markdown(f'Technologie de palier {niv}')

st.markdown(f'Population de niveau {niv} requise : {pop_requise[value]}')

data_research_tri = data_research[data_research['Type'] == f'Tech {value}']

data_research_tri.drop(['Type'], axis=1, inplace=True) # on en a plus besoin

data_research_tri.columns = ['Name FR', 'Description EN', 'Race', 'Bonus par level (%)', 'Bonus Max']

st.write(data_research_tri)


url = 'https://board.fr.ogame.gameforge.com/index.php?thread/746784-tutoriel-les-formes-de-vies/'

st.markdown("Lien vers le [tutoriel ogame](%s)" % url)




