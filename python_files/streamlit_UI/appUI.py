import streamlit as st
import pandas as pd
import os 

def export_data():


    df = pd.read_sql("SELECT * FROM buoy_observations LIMIT 10", con=f"mysql+pymysql://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@db:3306/{os.environ.get('MYSQL_DATABASE')}")
    st.write(f"This is the data from buoy observations in standard mode of station {df['station_id'].iloc[0]}:")
    df.drop(columns=["station_id"], inplace=True)  # Drop the 'id' column from the DataFrame
  
    st.dataframe(df, hide_index=True)  # Display the DataFrame in Streamlit without the index column

    df = pd.read_sql("SELECT * FROM cwind LIMIT 10", con=f"mysql+pymysql://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@db:3306/{os.environ.get('MYSQL_DATABASE')}")
    st.write(f"This is the data from buoy observations in cwind mode of station {df['station_id'].iloc[0]}:")
    df.drop(columns=["station_id"], inplace=True)  # Drop the 'id' column from the DataFrame

    st.dataframe(df, hide_index=True)  # Display the DataFrame in Streamlit without the index column
    st.line_chart(df, x="observation_time", y=["wspd", "wdir"]) 

if __name__ == "__main__":
    export_data()
