import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ambev Horas App", page_icon="img/dnc_logo.jpg", layout="wide")

# -- Side page -- #

st.sidebar.title('Parameters to beings imputed in the model')

SK_269 = st.sidebar.number_input(label='SK_269', value=10)
BDM_350 = st.sidebar.number_input(label='BDM_350', value=1000)
SK_350 = st.sidebar.number_input(label='SK_350', value=1000)
BC_350 = st.sidebar.number_input(label='BC_350', value=10)
OR_350 = st.sidebar.number_input(label='OR_350', value=900)
BUD350_SL = st.sidebar.number_input(label='BUD350_SL', value=10)
BUDSIX = st.sidebar.number_input(label='BUDSIX', value=10)
BUD12 = st.sidebar.number_input(label='BUD12', value=800)
BUDSIX_EX = st.sidebar.number_input(label='BUDSIX_EX', value=5)
BUD12_EX = st.sidebar.number_input(label='BUD12_EX', value=5)
BEL473 = st.sidebar.number_input(label='BEL473', value=1000)
BUD473 = st.sidebar.number_input(label='BUD473', value=10)
BUD_473_EX = st.sidebar.number_input(label='BUD_473_EX', value=5)

# -- Model -- #
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def prediction():
    df_input = pd.DataFrame([{
        'SK_269':SK_269, 'BDM_350':BDM_350, 
        'SK_350':SK_350, 'BC_350':BC_350, 
        'OR_350':OR_350, 'BUD350_SL':BUD350_SL,
        'BUDSIX':BUDSIX, 'BUD12':BUD12,
        'BUDSIX_EX':BUDSIX_EX, 'BUD12_EX':BUD12_EX, 
        'BEL473':BEL473, 'BUD473':BUD473, 'BUD_473_EX':BUD_473_EX, 
        }])
    prediction = model.predict(df_input)[0]
    return prediction
    
# -- Main page -- #

st.title('Horas Extras Pack 511')

predicted_class = prediction()
st.write(predicted_class)