import requests
import json
import argparse
from pprint import pprint
import sys
from datetime import datetime


class FlightSearchAPITester:
    """
    Test utility to check JSON responses from the flight search backend API
    """

    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def register_user(self, name, email, password):
        """Register a test user"""
        print(f"\n=== Registering user: {email} ===")

        endpoint = f"{self.base_url}/auth/register"
        data = {"name": name, "email": email, "password": password}

        response = requests.post(endpoint, json=data, headers=self.headers)

        print(f"Status code: {response.status_code}")
        if response.status_code == 201:
            print("User registered successfully")
            return True
        else:
            print(f"Registration failed: {response.json()}")
            return False

    def login(self, email, password):
        """Login and get JWT token"""
        print(f"\n=== Logging in user: {email} ===")

        endpoint = f"{self.base_url}/auth/login"
        data = {"email": email, "password": password}

        response = requests.post(endpoint, json=data, headers=self.headers)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers["Authorization"] = f"Bearer {self.token}"
            print("Login successful - JWT token obtained")
            return True
        else:
            print(f"Login failed: {response.json()}")
            return False

    def get_iata_codes(self, city):
        """Test the /search/iata endpoint"""
        print(f"\n=== Getting IATA codes for city: {city} ===")

        # Test GET method
        endpoint = f"{self.base_url}/search/iata"
        params = {"city": city}

        print("Testing GET request...")
        response = requests.get(endpoint, params=params, headers=self.headers)

        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} IATA codes")
            print("\nResponse structure:")
            if data:
                print(json.dumps(data[0], indent=2))
            else:
                print("No IATA codes found")
            return data
        else:
            print(f"Request failed: {response.json()}")
            return None

    def search_flights(
        self, origin, destination, departure_date, return_date=None, adults=1
    ):
        """Test the /search/flights endpoint"""
        print(f"\n=== Searching flights ===")
        print(f"From: {origin} To: {destination}")
        print(f"Departure: {departure_date} Return: {return_date}")
        print(f"Adults: {adults}")

        endpoint = f"{self.base_url}/search/flights"
        data = {
            "origin_iata": origin,
            "destination_iata": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": adults,
        }

        # Test POST method
        print("Testing POST request...")
        response = requests.post(endpoint, json=data, headers=self.headers)

        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            flight_data = response.json()
            print(f"Found {len(flight_data)} flight offers")

            if flight_data:
                print("\nResponse structure:")
                # Print a formatted sample of the first flight offer
                formatted_sample = json.dumps(flight_data[0], indent=2)
                # Limit output if it's too large
                if len(formatted_sample) > 1000:
                    print(
                        formatted_sample[:1000]
                        + "...\n(Response truncated for readability)"
                    )
                else:
                    print(formatted_sample)

                # Check for key elements in flight offers
                self._analyze_flight_offer_structure(flight_data[0])
            else:
                print("No flight offers found")

            return flight_data
        else:
            print(
                f"Request failed: {response.json() if response.content else 'No content'}"
            )
            return None

    def save_search(self, origin, destination, departure_date, return_date):
        """Test the /search/save endpoint"""
        print(f"\n=== Saving search ===")

        endpoint = f"{self.base_url}/search/save"
        data = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
        }

        response = requests.post(endpoint, json=data, headers=self.headers)

        print(f"Status code: {response.status_code}")
        if response.status_code == 201:
            print(f"Search saved successfully: {response.json()}")
            return response.json()
        else:
            print(
                f"Save failed: {response.json() if response.content else 'No content'}"
            )
            return None

    def get_search_history(self):
        """Test the /history endpoint"""
        print(f"\n=== Getting search history ===")

        endpoint = f"{self.base_url}/history/"

        response = requests.get(endpoint, headers=self.headers)

        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            history = response.json()
            print(f"Found {len(history)} search history entries")

            if history:
                print("\nHistory entry structure:")
                print(json.dumps(history[0], indent=2))
            else:
                print("No history entries found")

            return history
        else:
            print(
                f"Request failed: {response.json() if response.content else 'No content'}"
            )
            return None

    def _analyze_flight_offer_structure(self, offer):
        """Analyze and print important fields in a flight offer"""
        print("\nKey flight offer information:")

        try:
            # Try to extract common fields
            print(f"Offer ID: {offer.get('id', 'N/A')}")

            if "price" in offer:
                print(
                    f"Price: {offer['price'].get('total', 'N/A')} {offer['price'].get('currency', 'N/A')}"
                )

            if "itineraries" in offer and offer["itineraries"]:
                segments = offer["itineraries"][0].get("segments", [])
                if segments:
                    departure = segments[0].get("departure", {})
                    arrival = segments[-1].get("arrival", {})

                    print(
                        f"Departure: {departure.get('iataCode', 'N/A')} at {departure.get('at', 'N/A')}"
                    )
                    print(
                        f"Arrival: {arrival.get('iataCode', 'N/A')} at {arrival.get('at', 'N/A')}"
                    )

            # Count how many segments/flights in the offer
            segments_count = sum(
                len(itinerary.get("segments", []))
                for itinerary in offer.get("itineraries", [])
            )
            print(f"Total segments: {segments_count}")

            # Check if it's a direct flight or has connections
            if segments_count == len(offer.get("itineraries", [])):
                print("Flight type: Direct flight")
            else:
                print("Flight type: Has connections")

        except Exception as e:
            print(f"Error analyzing offer structure: {e}")


def main():
    parser = argparse.ArgumentParser(description="Test Flight Search API Responses")
    parser.add_argument(
        "--url", default="http://localhost:5000", help="Base URL of the API"
    )
    parser.add_argument(
        "--email", default="apitest@example.com", help="Email for authentication"
    )
    parser.add_argument(
        "--password", default="testpassword", help="Password for authentication"
    )
    parser.add_argument(
        "--name", default="APITester", help="Name for user registration"
    )
    parser.add_argument("--origin", default="SYD", help="Origin IATA code")
    parser.add_argument("--destination", default="BKK", help="Destination IATA code")
    parser.add_argument(
        "--city", default="Sydney", help="City to search for IATA codes"
    )

    # Generate default dates (current date + 30 days for departure, + 37 days for return)
    from datetime import timedelta

    today = datetime.now()
    default_departure = (today.replace(day=1) + timedelta(days=62)).strftime("%Y-%m-%d")
    default_return = (today.replace(day=1) + timedelta(days=69)).strftime("%Y-%m-%d")

    parser.add_argument(
        "--departure", default=default_departure, help="Departure date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--return",
        dest="return_date",
        default=default_return,
        help="Return date (YYYY-MM-DD)",
    )

    args = parser.parse_args()

    tester = FlightSearchAPITester(base_url=args.url)

    # Try to register (may fail if user already exists)
    tester.register_user(args.name, args.email, args.password)

    # Login is required for all the API tests
    if not tester.login(args.email, args.password):
        print("Login failed. Cannot proceed with API tests.")
        sys.exit(1)

    # Test IATA code search
    iata_results = tester.get_iata_codes(args.city)

    # If we got IATA results, use the first one for flight search
    origin = args.origin
    if iata_results and len(iata_results) > 0:
        origin = iata_results[0]["iataCode"]
        print(f"Using {origin} from search results as origin")

    # Test flight search
    flight_results = tester.search_flights(
        origin=origin,
        destination=args.destination,
        departure_date=args.departure,
        return_date=args.return_date,
    )

    # Test saving a search
    if flight_results:
        tester.save_search(
            origin=origin,
            destination=args.destination,
            departure_date=args.departure,
            return_date=args.return_date,
        )

    # Test getting search history
    tester.get_search_history()


if __name__ == "__main__":
    main()
