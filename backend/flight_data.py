import os
import datetime
import requests

class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, file_path="Flight_Deals.xlsx") -> None:
        self._price = price
        self._origin_airport = origin_airport
        self._destination_airport = destination_airport
        self._out_date = out_date
        self._return_date = return_date
        self._file_path = file_path
        # self._tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @property
    def price(self):
        return self._price
    
    @property
    def out_date(self):
        return self._out_date
    
    @property
    def return_date(self):
        return self._return_date

    def find_cheapest_flight(self, data):
        if data is None or not data['data']:
            print("No flight data.")
            return FlightData("N/a", "N/a", "N/a", "N/a", "N/a")
            
        # Data from the first flight in the json
        first_flight = data['data'][0]
        lowest_price = float(first_flight["price"]["grandTotal"])
        origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

        # Initialize FlightData with the first flight for comparison
        cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])
            if price < lowest_price:
                lowest_price = price
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
                cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
                print(f"Lowest price to {destination} is £{lowest_price}")

        return cheapest_flight
        

