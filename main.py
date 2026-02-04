from ndbc_api import NdbcApi
api = NdbcApi()
#print(api.station(station_id=44065, as_df=True))
print(api.get_modes())
test_station = api.station(station_id=44065, as_df=False)
data=api.get_data(station_id='44065', mode="stdmet", as_df=True)
print(data)