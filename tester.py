from app import app  

# Creates a test client to make requests to the app
client = app.test_client()
client.testing = True

def test_balance_endpoint():
    # Sends a GET request to the app's endpoint
    response = client.get('/balance')  

    assert response.status_code == 200
    assert response.get_json() == {"DANNON": 1000,"UNILEVER" : 0, "MILLER COORS": 5300}

def test_add_endpoint():
    # Sends a POST request to the app's endpoint
    response1 = client.post('/add', json=
        {"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
    )
    response2 = client.post('/add', json=
        { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" }
    )
    response3 = client.post('/add', json=
        { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" }
    )
    response4 = client.post('/add', json=
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" }
    )
    response5 = client.post('/add', json=
        { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
    )

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert response4.status_code == 200
    assert response5.status_code == 200

def test_spend_endpoint():
    # Sends a POST request to the app's endpoint
    response = client.post('/spend', json=
        { "points": 5000 }
    )
    assert response.status_code == 200


if __name__ == '__main__':
    # Runs the tests
    test_add_endpoint()
    test_spend_endpoint()
    test_balance_endpoint()