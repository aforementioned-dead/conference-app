from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в менеджер конференций"}


def test_create_room(client):
    response = client.post("/rooms", json={"name": "Основная комната"})
    assert response.status_code == 200
    assert response.json()["name"] == "Основная комната"


def test_schedule_by_room(client):
    client.post("/rooms", json={"name": "Основная комната"})
    client.post("/presentations", json={
        "title": "Моя первая презентация",
        "description": "Я очень волнуюсь (правда)",
        "presenter": "Илон Макс"
    })
    client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:00:00",
        "end_time": "2025-01-16T11:00:00"
    })
    response = client.get("/schedule-by-room")
    assert response.status_code == 200
    assert "Основная комната" in response.json()
    assert len(response.json()["Основная комната"]) == 1


def test_time_slot_overlap(client):
    client.post("/rooms", json={"name": "Основная комната"})
    client.post("/presentations", json={
        "title": "Моя первая презентация",
        "description": "Я очень волнуюсь (правда)",
        "presenter": "Илон Макс"
    })
    client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:00:00",
        "end_time": "2025-01-16T11:00:00"
    })
    response = client.post("/schedules", json={
        "room_id": 1,
        "presentation_id": 1,
        "start_time": "2025-01-16T10:30:00",
        "end_time": "2025-01-16T11:30:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Это время уже занято другой презентацией. Пожалуйста, выберите другое время!"