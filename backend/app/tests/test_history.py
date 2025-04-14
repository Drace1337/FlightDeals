def test_search_save_and_history(client, auth_headers):
    search_data = {
        "origin": "CDG",
        "destination": "JFK",
        "departure_date": "2025-06-01",
        "return_date": "2025-06-10"
    }

    res = client.post("/search/save", json=search_data, headers=auth_headers)
    assert res.status_code == 201

    res = client.get("/history/", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)