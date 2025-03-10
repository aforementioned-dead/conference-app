def test_register_user(client):
    response = client.post("/register", json={"username": "Илон Макс", "role": "Докладчик"})
    assert response.status_code == 200
    assert response.json()["username"] == "Илон Макс"
    assert response.json()["role"] == "Докладчик"