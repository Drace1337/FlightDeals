from unittest.mock import patch


from app.routes.search_routes import amadeus_service


@patch(
    "app.services.amadeus_service.AmadeusService.get_iata_codes", return_value=["JFK"]
)
@patch(
    "app.services.amadeus_service.AmadeusService.get_token", return_value="mocked_token"
)
def test_get_iata(mock_get_token, mock_get_iata_codes, client, auth_headers):
    headers = {"Authorization": auth_headers["Authorization"]}

    res = client.get("/search/iata", query_string={"city": "Warsaw"}, headers=headers)

    assert res.status_code == 200
    assert res.get_json() == ["JFK"]
    mock_get_iata_codes.assert_called_with("Warsaw")
