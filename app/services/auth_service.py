# =====================================================
# 🟦 AUTH SERVICE – BUSINESS LOGIC + DB HANDLING
# =====================================================

from flask import current_app, g
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.extensions import db


def register_user(email: str, password: str, role: str = "user"):

    try:
        user = User(email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(
            f"[REQ:{g.request_id}] User created id={user.id}, email={user.email}"
        )

        return {
            "message": "User registered successfully",
            "role": user.role
        }, 201

    except IntegrityError:
        db.session.rollback()

        current_app.logger.warning(
            f"[REQ:{g.request_id}] Duplicate user {email}"
        )

        return {
            "message": "User already exists"
        }, 400
