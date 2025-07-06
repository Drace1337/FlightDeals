import json
import pytest
from unittest.mock import patch, MagicMock

class TestSearchRoutes:
    """Tests for the search routes in search_routes.py"""

    mock_iata_response_get = [
        {
            "iataCode": "WAW",
            "name": "Warsaw Chopin Airport",
            "cityName": "Warsaw",
            "countryName": "Poland",
        },
        {
            "iataCode": "WMI",
            "name": "Warsaw Modlin Airport",
            "cityName": "Warsaw",
            "countryName": "Poland",
        },
    ]

    mock_iata_response_post = [
        {
            "iataCode": "BER",
            "name": "Berlin Brandenburg Airport",
            "cityName": "Berlin",
            "countryName": "Germany",
        }
    ]

    mock_flights_response = {
        "data": [
            {
                "id": "1",
                "source": "GDS",
                "instantTicketingRequired": False,
                "price": {"currency": "EUR", "total": "350.50"},
            }
        ]
    }

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_get_iata_get_success(self, mock_get_amadeus_service, client, auth_headers):
        """Test getting IATA codes using GET method."""
        mock_service_instance = MagicMock()
        mock_service_instance.get_iata_codes.return_value = self.mock_iata_response_get
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.get("/search/iata?city=Warsaw", headers=auth_headers)

        assert response.status_code == 200
        assert json.loads(response.data) == self.mock_iata_response_get
        mock_service_instance.get_iata_codes.assert_called_once_with("Warsaw")

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_get_iata_post_success(self, mock_get_amadeus_service, client, auth_headers):
        """Test getting IATA codes using POST method."""
        mock_service_instance = MagicMock()
        mock_service_instance.get_iata_codes.return_value = self.mock_iata_response_post
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.post(
            "/search/iata",
            data=json.dumps({"city": "Berlin"}),
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert json.loads(response.data) == self.mock_iata_response_post
        mock_service_instance.get_iata_codes.assert_called_once_with("Berlin")

    def test_get_iata_missing_city(self, client, auth_headers):
        """Test getting IATA codes without providing city parameter."""
        response = client.get("/search/iata", headers=auth_headers)

        assert response.status_code == 400
        assert json.loads(response.data) == {"error": "City parameter is required"}

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_get_iata_service_error(self, mock_get_amadeus_service, client, auth_headers):
        """Test handling of service errors when getting IATA codes."""
        mock_service_instance = MagicMock()
        mock_service_instance.get_iata_codes.side_effect = Exception("API connection error")
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.get("/search/iata?city=Warsaw", headers=auth_headers)

        assert response.status_code == 500
        assert json.loads(response.data) == {"error": "API connection error"}

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_search_flights_get_success(self, mock_get_amadeus_service, client, auth_headers):
        """Test searching for flights using GET method."""
        mock_service_instance = MagicMock()
        mock_service_instance.search_flights.return_value = self.mock_flights_response
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.get(
            "/search/flights?origin_iata=WAW&destination_iata=BER&departure_date=2023-06-01&return_date=2023-06-10&adults=1",
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert json.loads(response.data) == self.mock_flights_response
        mock_service_instance.search_flights.assert_called_once_with(
            "WAW", "BER", "2023-06-01", "2023-06-10", 1
        )

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_search_flights_post_success(self, mock_get_amadeus_service, client, auth_headers):
        """Test searching for flights with POST request."""
        mock_service_instance = MagicMock()
        mock_service_instance.search_flights.return_value = self.mock_flights_response
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.post(
            "/search/flights",
            data=json.dumps(
                {
                    "origin_iata": "WAW",
                    "destination_iata": "BER",
                    "departure_date": "2023-06-01",
                    "return_date": "2023-06-10",
                    "adults": 1,
                }
            ),
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert json.loads(response.data) == self.mock_flights_response
        mock_service_instance.search_flights.assert_called_once_with(
            "WAW", "BER", "2023-06-01", "2023-06-10", 1
        )

    def test_search_flights_missing_params(self, client, auth_headers):
        """Test searching for flights with missing required parameters."""
        response = client.get("/search/flights?origin_iata=WAW", headers=auth_headers)

        assert response.status_code == 400
        assert "Missing required parameters" in json.loads(response.data)["error"]

    def test_search_flights_invalid_adults(self, client, auth_headers):
        """Test searching for flights with invalid adults parameter."""
        response = client.get(
            "/search/flights?origin_iata=WAW&destination_iata=BER&departure_date=2023-06-01&adults=invalid",
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert json.loads(response.data) == {"error": "adults must be a valid number"}

    @patch("app.routes.search_routes.get_amadeus_service")
    def test_search_flights_service_error(self, mock_get_amadeus_service, client, auth_headers):
        """Test handling of service errors when searching for flights."""
        mock_service_instance = MagicMock()
        mock_service_instance.search_flights.side_effect = Exception("API connection error")
        mock_get_amadeus_service.return_value = mock_service_instance

        response = client.get(
            "/search/flights?origin_iata=WAW&destination_iata=BER&departure_date=2023-06-01",
            headers=auth_headers,
        )

        assert response.status_code == 500
        assert json.loads(response.data) == {"error": "API connection error"}

    @patch("app.routes.search_routes.save_search_history")
    @patch("app.routes.search_routes.get_jwt_identity")
    def test_save_search_success(self, mock_get_jwt_identity, mock_save_search_history, client, auth_headers):
        """Test saving search history successfully."""
        mock_get_jwt_identity.return_value = "1"
        mock_save_search_history.return_value = 42

        payload = {
            "departure_date": "2023-06-01",
            "return_date": "2023-06-10",
            "origin_iata": "WAW",
            "destination_iata": "BER",
            "adults": 1,
        }

        response = client.post(
            "/search/save",
            data=json.dumps(payload),
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert json.loads(response.data) == {"message": "Search saved", "id": 42}
        mock_save_search_history.assert_called_once()

    def test_save_search_no_data(self, client, auth_headers):
        """Test saving search with no data provided."""
        response = client.post("/search/save", data='{}', headers=auth_headers)

        assert response.status_code == 400
        assert json.loads(response.data) == {"error": "No data provided"}

    @patch("app.routes.search_routes.save_search_history")
    @patch("app.routes.search_routes.get_jwt_identity")
    def test_save_search_invalid_date_format(self, mock_get_jwt_identity, mock_save_search_history, client, auth_headers):
        """Test saving search with invalid date format."""
        mock_get_jwt_identity.return_value = "1"

        payload = {
            "departure_date": "invalid-date",
            "return_date": "2023-06-10",
            "origin_iata": "WAW",
            "destination_iata": "BER",
            "adults": 1,
        }

        response = client.post(
            "/search/save",
            data=json.dumps(payload),
            headers=auth_headers,
        )

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        mock_save_search_history.assert_not_called()
