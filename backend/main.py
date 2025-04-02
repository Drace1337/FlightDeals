#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
import os
import time
import datetime
import pandas as pd


data_manager = DataManager()
sheet_manager = data_manager.get_destination_data()
flight_search = FlightSearch()



# Free tokens out so can't use this code
# sheety_headers = {
#     "Authorization": "Basic RHJhY2U6ZmxpZ2h0ZGVhbHo="
# }
# sheety_endpoint = f"https://api.sheety.co/{os.environ["SHEETY_USERNAME"]}/{os.environ["SHEETY_PROJECT_NAME"]}/{os.environ["SHEET_NAME"]}"

# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = flight_search.get_destination_code(row["city"])
#         time.sleep(2)
# print(f'sheet_data: {sheet_data}')



file_path = "Flight_Deals.xlsx" 
sheet_data = pd.read_excel(file_path).to_dict(orient="records")

for row in sheet_data:
    if row["IATA Code"] == "":
        row["IATA Code"] = flight_search.get_destination_code(row["City"])
        time.sleep(2)

print(f'sheet_data: {sheet_data}')


data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

tomorrow = datetime.datetime.now() + datetime.timedelta(days=(6*30))
six_month_from_today = datetime.datetime.now() + datetime.timedelta(days=(9 * 30))

departure_date = input("Enter the departure date (YYYY-MM-DD): ")
return_date = input("Enter the return date (YYYY-MM-DD): ")



data_manager.update_lowest_prices(departure_date, return_date)

# for destination in sheet_data:
#     print(f"Getting flights for {destination['City']}...")
#     flights = flight_search.check_flights(
#         os.environ["DEPARTURE_AIRPORT_IATA"],
#         destination["IATA Code"],
#         from_time=departure_date,
#         to_time=return_date
#     )
#     cheapest_flight = flight_data.find_cheapest_flight(flights)
#     print(f"{destination['City']}: £{cheapest_flight.price}")
#     print(f"Deportation date: {cheapest_flight.out_date}")
#     print(f"Return date: {cheapest_flight.return_date}")
#     # Slowing down requests to avoid rate limit
#     time.sleep(2)

city_from = input("Enter the city you are travelling from (in English): ")
iata_from = flight_search.get_destination_code(city_from)
if iata_from == "N/a":
    print("No airport code found.")
    exit()
city_to = input("Enter the city you want to travel to (in English): ")
iata_to = flight_search.get_destination_code(city_to)
if iata_to == "N/a":
    print("No airport code found.")
    exit()


flights = flight_search.check_flights(
    os.environ["DEPARTURE_AIRPORT_IATA"],
    iata_to,
    from_time=departure_date,
    to_time=return_date
)