def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json == {"message": "Hello from Flask"}

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {"status": "healthy"}

def test_random_number(client):
    res = client.get("/random")
    assert res.status_code == 200
    assert "random_number" in res.json
    assert isinstance(res.json["random_number"], int)
    assert 1 <= res.json["random_number"] < 100