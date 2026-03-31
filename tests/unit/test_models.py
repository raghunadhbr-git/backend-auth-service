from app.models.user import User

def test_password_hashing():
    user = User(email="test@test.com")
    user.set_password("secret123")

    assert user.check_password("secret123")
    assert not user.check_password("wrong")