from ndbc_api import NdbcApi
import csv

api = NdbcApi()

stationID = input("Enter station ID: ")
modes= input(f"Enter mode from available modes {api.get_modes()}: ")

test_station = api.station(station_id=stationID, as_df=False)
data=api.get_data(station_id=stationID, mode=modes, as_df=True)
print(data)

data.to_csv(f"{stationID}_{modes}_data.csv", index=False)