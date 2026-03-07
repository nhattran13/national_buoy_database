import streamlit as st
import pandas as pd

def export_data():
    st.write("Here's our first attempt at using data to create a table:")
    df = pd.read_sql("SELECT * FROM buoy_observations LIMIT 10", con="mysql+pymysql://root:password@db:3306/buoy_db")

    st.write(df)

    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)


export_data()