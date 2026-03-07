import argparse
from ndbc_api import NdbcApi
from geopy.geocoders import Nominatim
from data_ingestion import data_ingest
from connect_sql import connect_sql


def data_parse():
    parser = argparse.ArgumentParser(description="Connect to MySQL database")        # Create an argument parser to handle command-line arguments for the station ID and year
    parser.add_argument("rootPassword", type=str, nargs="?", default="password", help="Root password")
    parser.add_argument("databaseName", type=str, nargs="?", default="buoy_db", help="Database name")
    parser.add_argument("stationID", type=str, nargs="?", default="44065", help="Station ID to fetch data for")
    parser.add_argument("year", type=str, nargs="?", default="2025", help="Year of data to fetch")


    args = parser.parse_args()                                                                      # Parse the command-line arguments and store them in 'args' value. Then pass to root_password and database_name variables
    root_password = args.rootPassword
    database_name = args.databaseName
    station_id = args.stationID
    year = args.year

    connect_sql(root_password, database_name)                                                                      # Connect to the MySQL database using the 'connect_sql' function defined in 'connect_sql.py'
    data_ingest(station_id, year)                                                                                      # Fetch data from the NDBC API and load it into a MySQL database


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





if __name__ == "__main__":
    #lat, lon = get_city_location()                                                                      # Get the latitude and longitude of the specified city
    #get_stations(0,0)
    data_parse()                                                                                      # Parse the command-line arguments and fetch the data for the specified station and year