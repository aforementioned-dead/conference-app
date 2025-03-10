def test_schedule_by_room(client):
    client.post("/users", json={"username": "Илон Макс", "role": "Докладчик"})
    client.post("/presentations", json={
        "title": "Моя первая презентация",
        "description": "Я очень волнуюсь (правда)",
        "presenter": "Илон Макс"
    }, headers={"user-id": "1"})
    client.post("/rooms", json={"name": "Основная комната"})
    client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:00:00",
        "end_time": "2025-01-16T11:00:00"
    }, headers={"user-id": "1"})
    
    response = client.get("/schedule-by-room")
    assert response.status_code == 200
    assert "Основная комната" in response.json()
    assert len(response.json()["Основная комната"]) == 1

def test_time_slot_overlap(client):
    client.post("/rooms", json={"name": "Основная комната"})
    client.post("/users", json={"username": "Илон Макс", "role": "Докладчик"})
    client.post("/presentations", json={
        "title": "Моя первая презентация",
        "description": "Я очень волнуюсь (правда)",
        "presenter": "Илон Макс"
    }, headers={"user-id": "1"})
    
    client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:00:00",
        "end_time": "2025-01-16T11:00:00"
    }, headers={"user-id": "1"})

    response = client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:30:00",
        "end_time": "2025-01-16T11:30:00"
    }, headers={"user-id": "1"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Это время уже занято другой презентацией. Пожалуйста, выберите другое время!"