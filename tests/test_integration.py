def test_health_and_random(client):
    health_res = client.get("/health")
    assert health_res.status_code == 200
    assert health_res.json["status"] == "healthy"

    random_res = client.get("/random")
    assert random_res.status_code == 200
    assert "random_number" in random_res.json
