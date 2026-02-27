import argparse
from ndbc_api import NdbcApi
import argparse
from geopy.geocoders import Nominatim
from sqlalchemy import create_engine
from io import StringIO
import requests
import pandas as pd
import mysql.connector
import time

def connect_sql():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="password",
                database="schemadb"
            )
            print("Connected to MySQL database successfully")
            return conn
        except Exception as e:
            print(f"Failed to connect to MySQL database: {e}")
            time.sleep(2)  # Wait 5 seconds before retrying

    raise Exception("Failed to connect to MySQL database after 10 attempts")


def extract_data():

    parser = argparse.ArgumentParser(description="Fetch data from NDBC API")                        # Create an argument parser to handle command-line arguments for station ID and mode of data to fetch
    parser.add_argument("stationID", type=str, nargs="?", default="44065", help="Station ID to fetch data for")
    parser.add_argument("year", type=str, nargs="?", default="2025", help="Year of data to fetch")

    args = parser.parse_args()                                                                      # Parse the command-line arguments and store them in 'args' value. Then pass to station_id and mode variables
    station_id = args.stationID
    year = args.year

    url = "https://www.ndbc.noaa.gov/view_text_file.php?filename={station_id}h{year}.txt.gz&dir=data/historical/stdmet/"

    response = requests.get(url.format(station_id=station_id, year=year))
    response.raise_for_status()

    text_data = response.text

    # Correct 19-column stdmet header
    columns = [
        "YY","MM","DD","hh","mm",
        "WDIR","WSPD","GST","WVHT","DPD","APD","MWD",
        "PRES","ATMP","WTMP","DEWP","VIS","PTDY","TIDE"
    ]

    df = pd.read_csv(
        StringIO(text_data),
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
    print(f"Data extracted from {station_id} in {year} and saved to CSV successfully")
    load_data_to_db(df)                                                                             # Load the fetched data into a MySQL database using the 'load_data_to_db' function defined below


def get_stations(longtiude=None, latitude=None):
    api = NdbcApi()
    if longtiude and latitude:                                                                      # If both longitude and latitude are provided, use them to find the nearest station
        lon = longtiude
        lat = latitude
    else:                                                                                           # Default longtitude and latude values if not provided
        lat = '40.368N'
        lon = '73.701W'

    nearest = api.nearest_station(lat=lat, lon=lon)                                                 # Find the nearest station to the provided latitude and longitude
    print(nearest)



def get_city_location():
    parser = argparse.ArgumentParser(description="Get the latitude and longitude of a city")        # Create an argument parser to handle command-line arguments for the city name
    parser.add_argument("city", type=str, nargs="*", default=["New", "York"], help="Name of the city to get location for")

    args = parser.parse_args()                                                                      # Parse the command-line arguments and store them in 'args' value. Then pass to city variable
    city = " ".join(args.city)

    geolocator = Nominatim(user_agent="myGeocoder")                                                 # Create a geolocator object using the Nominatim geocoding service
    location = geolocator.geocode(city)
    if location:                                                                                    # If the city is found, print its latitude and longitude to the console and return them as a tuple
        print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
        return (location.latitude, location.longitude)
    else:
        print("City not found")


def load_data_to_db(data):
    engine = create_engine("mysql+pymysql://root:password@db:3306/schemadb")
    data.to_sql('buoy_observations', con=engine, if_exists='append', index=False)                    # Load the provided data into the 'buoy_observations' table in the MySQL database using SQLAlchemy
    print("Data loaded to database successfully")


if __name__ == "__main__":
    #lat, lon = get_city_location()                                                                      # Get the latitude and longitude of the specified city
    #get_stations(0,0)
    connect_sql()                                                                                     # Connect to the MySQL database
    extract_data()