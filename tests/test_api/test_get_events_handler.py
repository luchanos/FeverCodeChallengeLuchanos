async def test_ping(client):
    resp = client.post("/ping/")
    assert resp.status_code == 200
