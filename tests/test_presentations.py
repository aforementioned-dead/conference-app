def test_create_presentation(client):
    client.post("/users", json={"username": "Илон Макс", "role": "Докладчик"})
    response = client.post("/presentations", json={
        "title": "Моя первая презентация",
        "description": "Я очень волнуюсь (правда)",
        "presenter": "Илон Макс"
    }, headers={"user-id": "1"})
    
    assert response.status_code == 200
    assert response.json()["title"] == "Моя первая презентация"