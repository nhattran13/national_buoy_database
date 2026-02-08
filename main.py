import argparse
from ndbc_api import NdbcApi
import argparse
from geopy.geocoders import Nominatim



def extract_data():
    api = NdbcApi()

    parser = argparse.ArgumentParser(description="Fetch data from NDBC API")                        # Create an argument parser to handle command-line arguments for station ID and mode of data to fetch
    parser.add_argument("stationID", type=str, nargs="?", default="44065", help="Station ID to fetch data for")
    parser.add_argument("mode", type=str, nargs="?", default="stdmet", choices=["adcp", "cdwind", "ocean", "spec", "supl", "swden", "swdir", "swdir2", "swr1", "swr2" , "stdmet"], help="Mode of data to fetch")

    args = parser.parse_args()                                                                     # Parse the command-line arguments and store them in 'args' value. Then extract to stationID and modes variables
    stationID = args.stationID
    modes = args.mode
    
    test_station = api.station(station_id=stationID, as_df=False)                                   # Fetch station information for the specified station ID and print it to the console
    data=api.get_data(station_id=stationID, mode=modes, as_df=True)
    print(data)

    data.to_csv(f"{stationID}_{modes}_data.csv", index=False)                                       # Save the fetched data to a CSV file named using the station ID and mode




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
    extract_data()