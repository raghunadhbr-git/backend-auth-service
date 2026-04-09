# =====================================================
# FILE: test_auth_layered.py
# Pytest for layered auth app
# Pytest for layered auth app debug
# =====================================================

import pytest
# from auth_app_layered import create_app
from auth_app_layered_debug import create_app


# Fixture
@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


# ---------------------------
# REGISTER
# ---------------------------
def test_register_user(client):
    res = client.post("/api/v1/auth/angularUser/register", json={
        "email": "user@test.com",
        "password": "12345"
    })
    assert res.status_code == 201


def test_duplicate_register(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })

    res = client.post("/api/v1/auth/angularUser/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })

    assert res.status_code == 400


# ---------------------------
# LOGIN
# ---------------------------
def test_login_user(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "login@test.com",
        "password": "12345"
    })

    res = client.post("/api/v1/auth/angularUser/login", json={
        "email": "login@test.com",
        "password": "12345"
    })

    assert res.status_code == 200


def test_invalid_login(client):
    res = client.post("/api/v1/auth/angularUser/login", json={
        "email": "wrong@test.com",
        "password": "wrong"
    })

    assert res.status_code == 401


# ---------------------------
# PROFILE
# ---------------------------
def test_profile_requires_auth(client):
    res = client.get("/api/v1/auth/profile")
    assert res.status_code == 401


def test_profile_with_token(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "p@test.com",
        "password": "12345"
    })

    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "p@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    res = client.get("/api/v1/auth/profile", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


# ---------------------------
# LOGOUT
# ---------------------------
def test_logout(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "l@test.com",
        "password": "12345"
    })

    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "l@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    res = client.post("/api/v1/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


def test_token_invalid_after_logout(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "x@test.com",
        "password": "12345"
    })

    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "x@test.com",
        "password": "12345"
    })

    token = login.json["access_token"]

    client.post("/api/v1/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    res = client.get("/api/v1/auth/profile", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 401


# =====================================================
# HOW TO RUN TESTS
# =====================================================
# pytest .\practice\test_auth_both.py -v