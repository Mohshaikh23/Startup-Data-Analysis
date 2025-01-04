import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from programs import general_analysis,load_investor,load_startups

st.set_page_config(page_title="Startup Analysis",layout="wide")


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Anlaysis Type',
                 ['Overall Analysis',
                  'Investor Profile',
                  'Startup Analysis'],
                  placeholder='Select one')


df= pd.read_csv('Startup_clean.csv')

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    general_analysis()

elif option == 'Startup Analysis':
    st.title('Startup Analysis')
    startup = st.sidebar.selectbox('Select Startup',sorted(df['Startup'].unique().tolist()))
    btn1= st.sidebar.button('Find startup')
    if btn1:
        load_startups(startup)

else:
    st.title('Investor Profile')
    Investor = st.sidebar.selectbox('Select Startup',sorted(set(df.Investors.str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor')
    if btn2:
        load_investor(Investor)


st.markdown(
    '''
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    ''',unsafe_allow_html=True)
