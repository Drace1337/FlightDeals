import json
import pytest
from unittest.mock import patch, MagicMock

from app.services.amadeus_service import AmadeusService


class TestSearchRoutes:
    """Tests for the search routes in search_routes.py"""

    # Tests for get_iata route
    @patch.object(AmadeusService, "get_iata_codes")
    def test_get_iata_get_success(self, mock_get_iata_codes, client, auth_headers):
        """Test successful GET request to /iata endpoint."""
        # Mock data
        mock_response = [
            {
                "iataCode": "SYD",
                "name": "Sydney Kingsford Smith International Airport",
                "cityName": "Sydney",
                "countryName": "Australia",
            },
            {
                "iataCode": "SWZ",
                "name": "Sydney Airport",
                "cityName": "Sydney",
                "countryName": "Australia",
            },
        ]

        mock_get_iata_codes.return_value = mock_response

        # Make request
        response = client.get("/search/iata?city=Sydney", headers=auth_headers)

        # Assertions
        assert response.status_code == 200
        assert json.loads(response.data) == mock_response
        mock_get_iata_codes.assert_called_once_with("Sydney")

    @patch.object(AmadeusService, "get_iata_codes")
    def test_get_iata_post_success(self, mock_get_iata_codes, client, auth_headers):
        """Test successful POST request to /iata endpoint."""
        # Mock data
        mock_response = [
            {
                "iataCode": "BKK",
                "name": "Suvarnabhumi International Airport",
                "cityName": "Bangkok",
                "countryName": "Thailand",
            }
        ]

        mock_get_iata_codes.return_value = mock_response

        # Make request
        response = client.post(
            "/search/iata", data=json.dumps({"city": "Bangkok"}), headers=auth_headers
        )

        # Assertions
        assert response.status_code == 200
        assert json.loads(response.data) == mock_response
        mock_get_iata_codes.assert_called_once_with("Bangkok")

    def test_get_iata_missing_city(self, client, auth_headers):
        """Test error handling when city parameter is missing."""
        # Make request without city parameter
        response = client.get("/search/iata", headers=auth_headers)

        # Assertions
        assert response.status_code == 400
        assert json.loads(response.data) == {"error": "City parameter is required"}

    @patch.object(AmadeusService, "get_iata_codes")
    def test_get_iata_service_error(self, mock_get_iata_codes, client, auth_headers):
        """Test error handling when service throws an exception."""
        # Mock exception
        mock_get_iata_codes.side_effect = Exception("API connection error")

        # Make request
        response = client.get("/search/iata?city=Sydney", headers=auth_headers)

        # Assertions
        assert response.status_code == 500
        assert json.loads(response.data) == {"error": "API connection error"}

    # Tests for search_flights_route
    @patch.object(AmadeusService, "search_flights")
    def test_search_flights_get_success(
        self, mock_search_flights, client, auth_headers
    ):
        """Test successful GET request to /flights endpoint."""
        # Mock data
        mock_response = {
            "data": [
                {
                    "id": "1",
                    "source": "GDS",
                    "instantTicketingRequired": False,
                    "price": {"currency": "USD", "total": "1200.20"},
                }
            ]
        }

        mock_search_flights.return_value = mock_response

        # Make request
        response = client.get(
            "/search/flights?origin_iata=SYD&destination_iata=BKK&departure_date=2023-05-02&return_date=2023-05-10&adults=1",
            headers=auth_headers,
        )

        # Assertions
        assert response.status_code == 200
        assert json.loads(response.data) == mock_response
        mock_search_flights.assert_called_once_with(
            "SYD", "BKK", "2023-05-02", "2023-05-10", 1
        )

    @patch.object(AmadeusService, "search_flights")
    def test_search_flights_post_success(
        self, mock_search_flights, client, auth_headers
    ):
        """Test successful POST request to /flights endpoint."""
        # Mock data
        mock_response = {
            "data": [
                {
                    "id": "1",
                    "source": "GDS",
                    "instantTicketingRequired": False,
                    "price": {"currency": "USD", "total": "1200.20"},
                }
            ]
        }

        mock_search_flights.return_value = mock_response

        # Make request
        response = client.post(
            "/search/flights",
            data=json.dumps(
                {
                    "origin_iata": "SYD",
                    "destination_iata": "BKK",
                    "departure_date": "2023-05-02",
                    "return_date": "2023-05-10",
                    "adults": 1,
                }
            ),
            headers=auth_headers,
        )

        # Assertions
        assert response.status_code == 200
        assert json.loads(response.data) == mock_response
        mock_search_flights.assert_called_once_with(
            "SYD", "BKK", "2023-05-02", "2023-05-10", 1
        )

    def test_search_flights_missing_params(self, client, auth_headers):
        """Test error handling when required parameters are missing."""
        # Make request with missing parameters
        response = client.get("/search/flights?origin_iata=SYD", headers=auth_headers)

        # Assertions
        assert response.status_code == 400
        assert "Missing required parameters" in json.loads(response.data)["error"]

    def test_search_flights_invalid_adults(self, client, auth_headers):
        """Test error handling when adults parameter is invalid."""
        # Make request with invalid adults parameter
        response = client.get(
            "/search/flights?origin_iata=SYD&destination_iata=BKK&departure_date=2023-05-02&adults=invalid",
            headers=auth_headers,
        )

        # Assertions
        assert response.status_code == 400
        assert json.loads(response.data) == {"error": "adults must be a valid number"}

    @patch.object(AmadeusService, "search_flights")
    def test_search_flights_service_error(
        self, mock_search_flights, client, auth_headers
    ):
        """Test error handling when service throws an exception."""
        # Mock exception
        mock_search_flights.side_effect = Exception("API connection error")

        # Make request
        response = client.get(
            "/search/flights?origin_iata=SYD&destination_iata=BKK&departure_date=2023-05-02",
            headers=auth_headers,
        )

        # Assertions
        assert response.status_code == 500
        assert json.loads(response.data) == {"error": "API connection error"}
