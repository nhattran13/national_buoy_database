import streamlit as st
import pandas as pd
from ndbc_api import NdbcApi
import os 

def show_map(): #station_id is defined in the main function
    api = NdbcApi()
    stations_df = api.stations()

    selected_row = stations_df.loc[stations_df['Station'] == station_id]
    lat = selected_row['Lat'].values[0]
    lon = selected_row['Lon'].values[0]

    #Create a small DataFrame for st.map
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.subheader(f"Current Location: Station {station_id}")
    st.map(map_data)


def show_buoy_info(): #buoy_df and cwind_df are defined in the main function
    st.title("⚓ National Buoy Real-Time Monitor")

    col1, col2, col3, col4 = st.columns([4, 4, 4, 4])
    latest = buoy_df.iloc[-1]
    prev = buoy_df.iloc[-25]

    col1.metric(f"Air Temp on {latest['observation_time'].date()}", f"{latest['atmp']}°F", f"{round(latest['atmp'] - prev['atmp'], 1)}°F")
    col2.metric(f"Wind Speed on {latest['observation_time'].date()}", f"{latest['wspd']} kts")
    col3.metric(f"Pressure on {latest['observation_time'].date()}", f"{latest['pres']} in")
    col4.metric(f"Wind Direction on {latest['observation_time'].date()}", f"{latest['wdir'] }°")

    #Trend charts
    st.subheader(f"24-Hour Temperature Trend on {latest['observation_time'].date()}")
    st.line_chart(buoy_df.set_index('observation_time')[['atmp', 'wtmp']].iloc[-25:])

    st.subheader(f"Wind & Gust Activity on {latest['observation_time'].date()}")
    st.area_chart(cwind_df.set_index('observation_time')[['wspd', 'gst']].iloc[-25:])




if __name__ == "__main__":
    st.set_page_config(page_title="NDBC Buoy Monitor", layout="wide")

    #Set global variables
    buoy_df = pd.read_sql("SELECT * FROM buoy_observations LIMIT 1000", con=f"mysql+pymysql://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@db:3306/{os.environ.get('MYSQL_DATABASE')}")
    cwind_df = pd.read_sql("SELECT * FROM cwind LIMIT 1000", con=f"mysql+pymysql://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@db:3306/{os.environ.get('MYSQL_DATABASE')}")
    station_id = buoy_df['station_id'].iloc[0]

    show_map()
    show_buoy_info()
