"""Тесты авторизации"""
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json = {"username": "testuser", "password": "secret123"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "testuser"}


def test_register_dublicate_username(client):
    client.post("/auth/register", json={"username": "testuser", "password": "secret123"})
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "anotherpass"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_login_success(client):
    client.post("/auth/register", json={"username": "testuser", "password": "secret123"})
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "testuser", "password": "secret123"})
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_get_current_user(client):
    client.post("/auth/register", json={"username": "meuser", "password": "password123"})
    response = client.post("/auth/login", data={"username": "meuser", "password": "password123"})
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/users/me", headers=headers)

    assert res.status_code == 200
    assert res.json()["username"] == "meuser"
    assert "id" in res.json()


def test_refresh_token_flow(client):
    client.post("/auth/register", json={"username": "refuser", "password": "password123"})
    login_res = client.post("/auth/login", data={"username": "refuser", "password": "password123"})
    
    tokens = login_res.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    
    # Обновляем токен
    refresh_res = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    
    # Старый refresh-токен больше не должен работать
    bad_res = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert bad_res.status_code == 401