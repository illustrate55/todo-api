"""Тесты работы с задачами и изоляция пользователей"""

def get_auth_headers(client, username, password="password123"):
    """Вспомогательная функция: регистрирует юзера и возвращает заголовки с токеном"""
    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post("/auth/login", data={"username": username, "password": password})
    
    # Добавим проверку, чтобы видеть в консоли, если логин вдруг не удался
    assert response.status_code == 200, f"Login failed for {username}: {response.json()}"
    
    token = response.json()["access_token"]
    # ИСПРАВЛЕНО: Authorization (с буквой h)
    return {"Authorization": f"Bearer {token}"}


def test_create_task_unauthorized(client):
    """Проверяем, что без токена создать задачу нельзя"""
    response = client.post("/tasks", json={"title": "Task without auth"})
    assert response.status_code == 401


def test_create_and_get_tasks(client):
    """Проверяем создание и получение задач для одного юзера"""
    # ИСПРАВЛЕНО: Используем пароль по умолчанию "password123"
    headers = get_auth_headers(client, "alice")

    res = client.post("/tasks", json={"title": "Купить хлеб"}, headers=headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Купить хлеб"
    assert res.json()["position"] == 1

    res = client.get("/tasks", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["title"] == "Купить хлеб"


def test_task_isolation(client):
    """Проверяем, что Alice и Bob не видят задачи друг друга"""
    # ИСПРАВЛЕНО: Используем пароль по умолчанию "password123"
    headers_alice = get_auth_headers(client, "alice")
    headers_bob = get_auth_headers(client, "bob")

    # Алиса создает задачу
    client.post("/tasks", json={"title": "Секрет Алисы"}, headers=headers_alice)

    # Боб смотрит свои задачи - должен увидеть пустой список
    res = client.get("/tasks", headers=headers_bob)
    assert res.status_code == 200
    assert res.json() == []

    # Боб пытается удалить задачу Алисы (position 1)
    # ИСПРАВЛЕНО: /tasks/1 вместо /tasksk/1
    res = client.delete("/tasks/1", headers=headers_bob)
    assert res.status_code == 404  # 404, потому что у Боба нет задачи с position 1