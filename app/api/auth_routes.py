# =====================================================
# 🟦 AUTH ROUTES – API LAYER (REQUEST/RESPONSE)
# =====================================================

from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from ..services.auth_service import register_user
from ..extensions import db
from ..models.token_blacklist import TokenBlocklist
from ..models.user import User

auth_bp = Blueprint("auth", __name__)


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------
@auth_bp.get("/")
def health():
    current_app.logger.info(f"[REQ:{g.request_id}] Health check called")
    return jsonify({"status": "auth-service UP"}), 200


# ------------------------------------------------
# REGISTER
# ------------------------------------------------
@auth_bp.post("/angularUser/register")
def angular_register():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        current_app.logger.warning(f"[REQ:{g.request_id}] Missing email/password")
        return jsonify({"message": "email and password required"}), 400

    resp, status = register_user(email, password, role)

    if status != 201:
        current_app.logger.warning(f"[REQ:{g.request_id}] Duplicate user {email}")
        return jsonify(resp), status

    current_app.logger.info(
        f"[REQ:{g.request_id}] User registered email={email}, role={role}"
    )

    return jsonify(resp), 201


# ------------------------------------------------
# LOGIN
# ------------------------------------------------
@auth_bp.post("/angularUser/login")
def angular_login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        current_app.logger.warning(
            f"[REQ:{g.request_id}] Invalid login {email}"
        )
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    current_app.logger.info(
        f"[REQ:{g.request_id}] Login success user_id={user.id}"
    )

    return jsonify({
        "access_token": token,
        "userId": user.id,
        "role": user.role
    }), 200


# ------------------------------------------------
# PROFILE
# ------------------------------------------------
@auth_bp.get("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    current_app.logger.info(
        f"[REQ:{g.request_id}] Profile accessed user_id={user_id}"
    )

    return jsonify({"user_id": user_id}), 200


# ------------------------------------------------
# LOGOUT
# ------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():

    jti = get_jwt()["jti"]

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    current_app.logger.info(
        f"[REQ:{g.request_id}] Logout success"
    )

    return jsonify({"message": "Logged out successfully"}), 200


# =====================================================
# 🔧 DEBUG STEPS (UPDATED)
# =====================================================

# 1. Trigger API (Angular/Postman)
# 2. Check logs:
#    logs/auth.log
# 3. Observe:
#    [REQ:<ID>] same for entire request
# 4. Use ID to trace full flow
