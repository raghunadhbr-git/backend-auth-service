# Import pytest framework (used for writing and running tests)
import pytest

# Import your Flask app factory function
from app import create_app


# Fixture = reusable setup for tests
# This creates a test client to simulate API requests
@pytest.fixture
def client():
    app = create_app()          # Create Flask app instance
    return app.test_client()    # Return test client (fake browser)


# ---------------------------
# TEST: Register a new user
# ---------------------------
def test_register_user(client):
    # Send POST request to register endpoint
    res = client.post("/api/v1/auth/angularUser/register", json={
        "email": "user@test.com",
        "password": "12345"
    })

    # Expect success (201 = Created)
    assert res.status_code == 201


# ---------------------------
# TEST: Duplicate registration
# ---------------------------
def test_duplicate_register(client):
    # First registration (should succeed)
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })

    # Second registration with same email
    res = client.post("/api/v1/auth/angularUser/register", json={
        "email": "dup@test.com",
        "password": "12345"
    })

    # Expect failure (400 = Bad Request)
    assert res.status_code == 400


# ---------------------------
# TEST: Login user
# ---------------------------
def test_login_user(client):
    # Register user first
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "login@test.com",
        "password": "12345"
    })

    # Attempt login
    res = client.post("/api/v1/auth/angularUser/login", json={
        "email": "login@test.com",
        "password": "12345"
    })

    # Expect success (200 = OK)
    assert res.status_code == 200


# ---------------------------
# TEST: Invalid login
# ---------------------------
def test_invalid_login(client):
    # Try logging in with wrong credentials
    res = client.post("/api/v1/auth/angularUser/login", json={
        "email": "wrong@test.com",
        "password": "wrong"
    })

    # Expect unauthorized (401)
    assert res.status_code == 401


# ---------------------------
# TEST: Profile without token
# ---------------------------
def test_profile_requires_auth(client):
    # Access profile without authentication
    res = client.get("/api/v1/auth/profile")

    # Expect unauthorized (401)
    assert res.status_code == 401


# ---------------------------
# TEST: Profile with valid token
# ---------------------------
def test_profile_with_token(client):
    # Register user
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "p@test.com",
        "password": "12345"
    })

    # Login to get token
    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "p@test.com",
        "password": "12345"
    })

    # Extract JWT token from response
    token = login.json["access_token"]

    # Access protected route with token
    res = client.get("/api/v1/auth/profile", headers={
        "Authorization": f"Bearer {token}"   # Send token in header
    })

    # Expect success
    assert res.status_code == 200


# ---------------------------
# TEST: Logout
# ---------------------------
def test_logout(client):
    # Register user
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "l@test.com",
        "password": "12345"
    })

    # Login user
    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "l@test.com",
        "password": "12345"
    })

    # Get token
    token = login.json["access_token"]

    # Logout request
    res = client.post("/api/v1/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    # Expect success
    assert res.status_code == 200


# ---------------------------
# TEST: Token invalid after logout
# ---------------------------
def test_token_invalid_after_logout(client):
    # Register user
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "x@test.com",
        "password": "12345"
    })

    # Login
    login = client.post("/api/v1/auth/angularUser/login", json={
        "email": "x@test.com",
        "password": "12345"
    })

    # Get token
    token = login.json["access_token"]

    # Logout (invalidate token)
    client.post("/api/v1/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    # Try accessing protected route again
    res = client.get("/api/v1/auth/profile", headers={
        "Authorization": f"Bearer {token}"
    })

    # Expect unauthorized (token should not work anymore)
    assert res.status_code == 401


# ---------------------------
# HOW TO RUN TESTS
# ---------------------------

# Run this in terminal:
# pytest practice/test_app.py -v

# -v = verbose (shows each test result clearly)
