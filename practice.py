import streamlit as st
import pandas as pd
import numpy as np
import time


st.header('Startup Dashboard')

# st.sidebar("Sidebar")

st.subheader('Data')

df = pd.read_csv('startup_funding.csv')
st.dataframe(df)
# st.write(df.columns)
# for i in df.columns:
#     st.write(df[i].dtype)

st.metric('Total',df['Sr No'].count(),str(df['Sr No'].sum()))

col1,col2 = st.columns(2)
with col1:
    st.image('ss1.png')
with col2:
    st.video('https://www.youtube.com/watch?v=74SnvbQYgx8')

    


st.echo('Hello')
st.warning('Hello')
st.success('Hello')
st.info('Hello')


# bar = st.progress(0)
# for i in range(0,100):
#     time.sleep(1)
#     bar.progress(i)


nums = st.number_input('Age')
date = st.date_input('Enter Reg Date')

email= st.text_input('Enter Email')
password = st.text_input('Enter password',type='password')

gender = st.selectbox('Select Anyone', ['M','F'])

add = st.button('Click here')
if add:
    if email == 'mohsin@gmail.com' and password == '123':
        st.success('Logged In')
        st.balloons()
        st.write(gender)
    else:
        st.error('Login Failed')


file = st.file_uploader('Upload a csv filr')
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())