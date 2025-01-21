from fastapi.testclient import TestClient
from app.main import app
#from fastapi import Header

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
    client.post("/users", json={"username": "Илон Макс",
                                "role": "Докладчик"})
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
    client.post("users", json={"username": "Илон Макс", "role": "Докладчик"})
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


def test_update_room(client, test_db):
    response_create = client.post("/rooms", json={"name": "Тестовая комната"})
    assert response_create.status_code == 200
    created_room = response_create.json()

    updated_data = {"name": "Обновленная тестовая комната"}
    response_update = client.put(f"/rooms/{created_room['id']}", json=updated_data)
    assert response_update.status_code == 200
    updated_room = response_update.json()

    assert updated_room["id"] == created_room["id"]
    assert updated_room["name"] == updated_data["name"]


def test_delete_room(client, test_db):
    response_create = client.post("/rooms", json={"name": "Обновленная тестовая комната"})
    assert response_create.status_code == 200
    created_room = response_create.json()

    response_delete = client.delete(f"/rooms/{created_room['id']}")
    assert response_delete.status_code == 200

    response_get = client.get(f"/rooms/{created_room['id']}")
    assert response_get.status_code == 404