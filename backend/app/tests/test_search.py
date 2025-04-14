from unittest.mock import patch

@patch("services.amadues_service.get_iata_codes")
@patch("services.amadues_service.get_access_token")
def test_get_iata(mock_token, mock_iata, client, auth_headers):
    mock_token.return_value = "mock_token"
    mock_iata.return_value = {"city":"PAR", "airports":["CDG", "ORY"]}

    res = client.post("/search/iata", json={"city": "Paris"}, headers=auth_headers)
    assert res.status_code == 200
    assert "airports" in res.get_json()