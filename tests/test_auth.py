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