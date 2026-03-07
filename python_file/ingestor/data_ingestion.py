from io import StringIO
from time import time
import pandas as pd
import requests
from sqlalchemy import create_engine

def data_ingest(station_id, year):
    extract_std_data(station_id, year)                                                                             # Call the function to extract standard meteorological data for the specified station and year
    extract_cwind_data(station_id, year)                                                                             # Call the function to extract cwind data for the specified station and year



def extract_std_data(station_id, year):                                                             #extract stdmet data    

    for i in range(10):
        try:
            url_std = "https://www.ndbc.noaa.gov/view_text_file.php?filename={station_id}h{year}.txt.gz&dir=data/historical/stdmet/"

            response = requests.get(url_std.format(station_id=station_id, year=year))
            response.raise_for_status()

            std_data = response.text
            break
        except Exception as e:
            print(f"Failed to fetch STDMET data: {e}")
            time.sleep(2)  # Wait 5 seconds before retrying

    # Correct 19-column stdmet header
    columns = [
        "YY","MM","DD","hh","mm",
        "WDIR","WSPD","GST","WVHT","DPD","APD","MWD",
        "PRES","ATMP","WTMP","DEWP","VIS","PTDY","TIDE"
    ]

    df = pd.read_csv(
        StringIO(std_data),
        sep=r"\s+",
        names=columns,
        comment="#",
        engine="python",   # <-- important for whitespace parsing
        na_values=["MM"]
    )

    df["station_id"] = station_id
    # Build timestamp as string instead of datetime
    df["observation_time"] = (
        df["YY"].astype(int).astype(str).str.zfill(4) + "-" +
        df["MM"].astype(int).astype(str).str.zfill(2) + "-" +
        df["DD"].astype(int).astype(str).str.zfill(2) + " " +
        df["hh"].astype(int).astype(str).str.zfill(2) + ":" +
        df["mm"].astype(int).astype(str).str.zfill(2) + ":00"
    )
    df = df.drop(columns=["YY", "MM", "DD", "hh", "mm"])

    df.to_csv(f"{station_id}h{year}.csv", index=False)
    print(f"STDMET data extracted from {station_id} in {year} and saved to CSV successfully")
    load_stdmet_to_db(df)                                                                             # Load the fetched data into a MySQL database using the 'load_data_to_db' function defined below



def extract_cwind_data(station_id, year):                                                             #extract cwind data
    for i in range(10):
        try:
            url_cwind = "https://www.ndbc.noaa.gov/view_text_file.php?filename={station_id}c{year}.txt.gz&dir=data/historical/cwind/"

            response = requests.get(url_cwind.format(station_id=station_id, year=year))
            response.raise_for_status()

            cwind_data = response.text
            break
        except Exception as e:
            print(f"Failed to fetch CWIND data: {e}")
            time.sleep(2)  # Wait 5 seconds before retrying

    # Correct 19-column cwind header
    columns = [
        "YY","MM","DD","hh","mm",
        "WDIR","WSPD","GDR","GST","GTIME"
    ]

    df = pd.read_csv(
        StringIO(cwind_data),
        sep=r"\s+",
        names=columns,
        comment="#",
        engine="python",   # <-- important for whitespace parsing
        na_values=["MM"]
    )

    df["station_id"] = station_id
    # Build timestamp as string instead of datetime
    df["observation_time"] = (
        df["YY"].astype(int).astype(str).str.zfill(4) + "-" +
        df["MM"].astype(int).astype(str).str.zfill(2) + "-" +
        df["DD"].astype(int).astype(str).str.zfill(2) + " " +
        df["hh"].astype(int).astype(str).str.zfill(2) + ":" +
        df["mm"].astype(int).astype(str).str.zfill(2) + ":00"
    )
    df = df.drop(columns=["YY", "MM", "DD", "hh", "mm"])


    df.to_csv(f"{station_id}c{year}.csv", index=False)
    print(f"CWIND data extracted from {station_id} in {year} and saved to CSV successfully")
    load_cwind_to_db(df)                                                                             # Load the fetched data into a MySQL database using the 'load_data_to_db' function defined below


def load_stdmet_to_db(data):
    engine = create_engine("mysql+pymysql://root:password@db:3306/buoy_db")
    data.to_sql('buoy_observations', con=engine, if_exists='append', index=False)                    # Load the provided data into the 'buoy_observations' table in the MySQL database using SQLAlchemy
    print("Data loaded to database successfully")


def load_cwind_to_db(data):
    engine = create_engine("mysql+pymysql://root:password@db:3306/buoy_db")
    data.to_sql('cwind', con=engine, if_exists='append', index=False)                    # Load the provided data into the 'cwind' table in the MySQL database using SQLAlchemy
    print("Data loaded to database successfully")