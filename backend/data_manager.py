import os
import requests
import pandas as pd
import time
from flight_search import FlightSearch
from flight_data import FlightData

from dotenv import load_dotenv

load_dotenv()


flight_search = FlightSearch()
flight_data = FlightData(
  price="N/A",
  origin_airport="N/A",
  destination_airport="N/A", 
  out_date="N/A",
  return_date="N/A"
)

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, file_path="Flight_Deals.xlsx") -> None:
        # self._user = os.environ["SHEETY_USERNAME"]
        # self._password = os.environ["SHEETY_PASSWORD"]
        # self.sheety_headers = {"Authorization": os.environ["SHEETY_HEADER"]}
        self._file_path = file_path
        self.destination_data = {}

    # Code for sheety:
    # def get_destination_data(self):
    #     response = requests.get(url=f"https://api.sheety.co/{self._user}/{os.environ["SHEETY_PROJECT_NAME"]}/{os.environ["SHEET_NAME"]}", headers=self.sheety_headers)
    #     data = response.json()
    #     self.destination_data = data["prices"]
    #     return self.destination_data
    
    # def update_destination_codes(self):
    #     for city in self.destination_data:
    #         new_data = {
    #             "price": {
    #                 "iataCode": city["iataCode"]
    #             }
    #         }
    #         response = requests.put(url=f"https://api.sheety.co/{self._user}/{os.environ["SHEETY_PROJECT_NAME"]}/{os.environ["SHEET_NAME"]}/{city['id']}", headers=self.sheety_headers, json=new_data)
    #         print(response.text)

    # Code for pandas:
    def get_destination_data(self):
        sheet_data = pd.read_excel(self._file_path).to_dict(orient="records")
        self.destination_data = sheet_data
        return self.destination_data
    
    def update_destination_codes(self):
        df = pd.read_excel(self._file_path)
        for index, row in df.iterrows():
            if row["IATA Code"] == "":
                df.at[index, "IATA Code"] = flight_search.get_destination_code(row["City"])
                time.sleep(2)
        df.to_excel(self._file_path, index=False)
        print("Destination codes updated.")

    def update_lowest_prices(self, departure_date, return_date):
        df = pd.read_excel(self._file_path)
        for index, row in df.iterrows():
            print(f"Getting flights for {row['City']}...")
            flights = flight_search.check_flights(
                os.environ["DEPARTURE_AIRPORT_IATA"],
                row["IATA Code"],
                from_time=departure_date,
                to_time=return_date
            )
            cheapest_flight = flight_data.find_cheapest_flight(flights)
            print(f"{row['City']}: £{cheapest_flight.price}")
            print(f"Departure date: {cheapest_flight.out_date}")
            print(f"Return date: {cheapest_flight.return_date}")

            # Aktualizacja wartości w DataFrame
            df.at[index, "Lowest Price"] = cheapest_flight.price
            time.sleep(2)

        # Zapisanie zmian do pliku
        df.to_excel(self._file_path, index=False)
        print("Updated lowest prices and saved to file.")