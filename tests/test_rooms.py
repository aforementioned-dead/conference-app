def test_create_room(client):
    response = client.post("/rooms", json={"name": "Основная комната"})
    assert response.status_code == 200
    assert response.json()["name"] == "Основная комната"


def test_update_room(client):
    response_create = client.post("/rooms", json={"name": "Тестовая комната"})
    assert response_create.status_code == 200
    created_room = response_create.json()

    updated_data = {"name": "Обновленная тестовая комната"}
    response_update = client.put(f"/rooms/{created_room['id']}", json=updated_data)
    assert response_update.status_code == 200
    updated_room = response_update.json()

    assert updated_room["id"] == created_room["id"]
    assert updated_room["name"] == updated_data["name"]


def test_delete_room(client):
    response_create = client.post("/rooms", json={"name": "Тестовая комната"})
    assert response_create.status_code == 200
    created_room = response_create.json()

    response_delete = client.delete(f"/rooms/{created_room['id']}")
    assert response_delete.status_code == 200

    response_get = client.get(f"/rooms/{created_room['id']}")
    assert response_get.status_code == 404