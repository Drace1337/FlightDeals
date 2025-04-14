import requests
import os
from datetime import datetime


class AmadeusService:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.iata_endpoint = os.getenv("IATA_ENDPOINT")
        self.token_endpoint = os.getenv("TOKEN_ENDPOINT")
        self.flight_offers_endpoint = os.getenv("FLIGHT_OFFERS_ENDPOINT")
        self.token = None

    def get_token(self):
        if self.token is not None:
            return self.token
        response = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.api_secret,
            },
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def get_iata_codes(self, city_name):
        if self.token is None:
            self.token = self.get_token()
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"keyword": city_name, "subType": "AIRPORT"}
        response = requests.get(self.iata_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return [item["iataCode"] for item in response.json()["data"]]

    def search_flights(
        self, origin_iata, destination_iata, departure_date, return_date, adults
    ):
        if self.token is None:
            self.token = self.get_token()
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin_iata,
            "destinationLocationCode": destination_iata,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "currencyCode": os.getenv("CURRENCY_CODE", "EUR"),
            "max": 5,
        }
        response = requests.get(
            self.flight_offers_endpoint, headers=headers, params=params
        )
        response.raise_for_status()
        return response.json().get("data", [])
