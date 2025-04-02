import os
import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self) -> None:
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self._token = self._get_new_token()

    def get_destination_code(self, city_name):
        print(f"Getting destination code for {city_name}")
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        response = requests.get(url=os.environ["IATA_ENDPOINT"], headers=headers, params=query)
        print(f"Status code: {response.status_code}, Airport IATA code: {response.text}")
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}")
            return "N/a"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}")
            return "Not found"

        return code
    

    def _get_new_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }

        response = requests.post(url=os.environ["TOKEN_ENDPOINT"], headers=headers, data=body)

        print(f"Your token is {response.json()['access_token']}")
        print(f"Expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time, #.strftime("%Y-%m-%d"),
            "returnDate": to_time, #.strftime("%Y-%m-%d"),
            "currencyCode": os.environ["CURRENCY_CODE"],
            "adults": 2,
            "max": 10
        }
        response = requests.get(url=os.environ["FLIGHT_OFFERS_ENDPOINT"], headers=headers, params=query)

        if response.status_code != 200:
            print(f'check_flights() response code: {response.status_code}')
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()
    

        