# =====================================================
# 🟦 AUTH SERVICE – BUSINESS LOGIC + DB HANDLING
# =====================================================

from flask import current_app
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.extensions import db


def register_user(email: str, password: str, role: str = "user"):
    """
    Handles:
    - User creation
    - Password hashing
    - Duplicate handling (race condition safe)
    """

    try:
        user = User(
            email=email,
            role=role
        )

        # Secure password hashing
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(
            f"User created id={user.id}, email={user.email}"
        )

        return {
            "message": "User registered successfully",
            "role": user.role
        }, 201

    except IntegrityError:
        # Handles duplicate email / race condition
        db.session.rollback()

        return {
            "message": "User already exists"
        }, 400