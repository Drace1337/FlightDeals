import requests
import os
from datetime import datetime


class AmadeusService:
    def __init__(self):
        """Initialize the AmadeusService with API credentials and endpoints.
        The API credentials and endpoints are expected to be set as environment variables.
        """
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.iata_endpoint = os.getenv("IATA_ENDPOINT")
        self.token_endpoint = os.getenv("TOKEN_ENDPOINT")
        self.flight_offers_endpoint = os.getenv("FLIGHT_OFFERS_ENDPOINT")
        self.token = None

    def get_token(self):
        """        Retrieve an access token from the Amadeus API using client credentials.
        This method caches the token to avoid unnecessary requests.
        Returns:
            str: Access token for the Amadeus API
        """
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
        """
        Get IATA codes for airports in a given city

        Args:
            city_name (str): Name of the city to search for

        Returns:
            list: List of dictionaries containing airport information including IATA codes
        """
        if self.token is None:
            self.token = self.get_token()

        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "keyword": city_name,
            "include": "AIRPORTS",
            "max": 10,  
        }

        response = requests.get(self.iata_endpoint, headers=headers, params=params)
        response.raise_for_status()

        
        results = []
        for item in response.json().get("data", []):
            if "iataCode" in item:
                results.append(
                    {
                        "iataCode": item["iataCode"],
                        "name": item.get("name", ""),
                        "cityName": item.get("address", {}).get("cityName", ""),
                        "countryName": item.get("address", {}).get("countryName", ""),
                    }
                )

        return results

    def search_flights(
        self, origin_iata, destination_iata, departure_date, return_date, adults
    ):
        """        Search for flights based on provided parameters
        Args:
            origin_iata (str): IATA code of the origin airport
            destination_iata (str): IATA code of the destination airport
            departure_date (str): Departure date in YYYY-MM-DD format
            return_date (str): Return date in YYYY-MM-DD format
            adults (int): Number of adult passengers
        """
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
