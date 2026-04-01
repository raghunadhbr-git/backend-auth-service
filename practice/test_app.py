import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()


def test_register_user(client):
    res = client.post("/register", json={
        "email": "user@test.com",
        "password": "12345"
    })
    assert res.status_code == 201


def test_duplicate_register(client):
    client.post("/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })
    res = client.post("/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })
    assert res.status_code == 400


def test_login_user(client):
    client.post("/register", json={
        "email": "login@test.com",
        "password": "12345"
    })
    res = client.post("/login", json={
        "email": "login@test.com",
        "password": "12345"
    })
    assert res.status_code == 200


def test_invalid_login(client):
    res = client.post("/login", json={
        "email": "wrong@test.com",
        "password": "wrong"
    })
    assert res.status_code == 401


def test_profile_requires_auth(client):
    res = client.get("/profile")
    assert res.status_code == 401


def test_profile_with_token(client):
    client.post("/register", json={
        "email": "p@test.com",
        "password": "12345"
    })
    login = client.post("/login", json={
        "email": "p@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    res = client.get("/profile", headers={"Authorization": token})
    assert res.status_code == 200


def test_logout(client):
    client.post("/register", json={
        "email": "l@test.com",
        "password": "12345"
    })
    login = client.post("/login", json={
        "email": "l@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    res = client.post("/logout", headers={"Authorization": token})
    assert res.status_code == 200


def test_token_invalid_after_logout(client):
    client.post("/register", json={
        "email": "x@test.com",
        "password": "12345"
    })
    login = client.post("/login", json={
        "email": "x@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    client.post("/logout", headers={"Authorization": token})

    res = client.get("/profile", headers={"Authorization": token})
    assert res.status_code == 401 
