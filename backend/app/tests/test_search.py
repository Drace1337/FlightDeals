from unittest.mock import patch


@patch("app.routes.search_routes.amadeus_service.get_token", return_value="mocked_token")
@patch("app.routes.search_routes.amadeus_service.get_iata_codes", return_value=["JFK"])
def test_get_iata(mock_get_iata_codes, mock_get_token, client, auth_headers):
    res = client.get("/search/iata?city=New+York", headers=auth_headers)
    print("RESPONSE JSON:", res.get_json())

    assert res.status_code == 200
    assert res.get_json() == ["JFK"]
