# =====================================================
# 🟦 AUTH ROUTES – API LAYER (REQUEST/RESPONSE)
# =====================================================

from flask import Blueprint, request, jsonify, current_app
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
    return jsonify({"status": "auth-service UP"}), 200


# ------------------------------------------------
# REGISTER (USER / SELLER)
# ------------------------------------------------
@auth_bp.post("/angularUser/register")
def angular_register():
    """
    Expected Payload:
    {
      "email": "user@test.com",
      "password": "12345",
      "role": "user"
    }
    """

    data = request.get_json() or {}   # 🔴 DEBUG: check incoming payload from Angular/Postman

    email = data.get("email")         # 🔴 DEBUG: should not be None
    password = data.get("password")   # 🔴 DEBUG: should not be None
    role = data.get("role", "user")   # 🔴 DEBUG: default = "user"

    # Basic validation
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    # Call service (DB insert + duplicate handling)
    resp, status = register_user(email, password, role)   # 🔴 DEBUG: F11 to step into service

    if status != 201:
        # 🔴 DEBUG: duplicate user case → expect 400 + "User already exists"
        return jsonify(resp), status

    current_app.logger.info(
        f"User registered email={email}, role={role}"
    )

    return jsonify(resp), 201


# ------------------------------------------------
# LOGIN
# ------------------------------------------------
@auth_bp.post("/angularUser/login")
def angular_login():
    """
    Expected Payload:
    {
      "email": "user@test.com",
      "password": "12345"
    }
    """

    data = request.get_json() or {}   # 🔴 DEBUG: check login payload

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    # Fetch user from DB
    user = User.query.filter_by(email=email).first()   # 🔴 DEBUG: check if user exists

    # Validate credentials
    if not user or not user.check_password(password):   # 🔴 DEBUG: wrong password / user not found
        current_app.logger.warning(
            f"Invalid login attempt email={email}"
        )
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate JWT token
    token = create_access_token(identity=str(user.id))   # 🔴 DEBUG: check token value

    return jsonify({
        "access_token": token,
        "userId": user.id,
        "role": user.role
    }), 200


# ------------------------------------------------
# PROFILE (PROTECTED ROUTE)
# ------------------------------------------------
@auth_bp.get("/profile")
@jwt_required()
def profile():
    """
    Header Required:
    Authorization: Bearer <JWT_TOKEN>
    """

    user_id = get_jwt_identity()   # 🔴 DEBUG: should return logged-in user id

    return jsonify({"user_id": user_id}), 200


# ------------------------------------------------
# LOGOUT (TOKEN BLACKLIST)
# ------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():
    """
    Header Required:
    Authorization: Bearer <JWT_TOKEN>
    """

    jti = get_jwt()["jti"]   # 🔴 DEBUG: unique token id

    db.session.add(TokenBlocklist(jti=jti))   # 🔴 DEBUG: ensure DB insert
    db.session.commit()

    return jsonify({"message": "Logged out successfully"}), 200


# =====================================================
# 🔧 DEBUG STEPS (QUICK REFERENCE)
# =====================================================

# 1. Press F5 → Start Debugging
# 2. Trigger API from Angular / Postman
# 3. Execution pauses at 🔴 lines
# 4. Use:
#    - F10 → Step Over (line by line)
#    - F11 → Step Into (go inside service)
#    - Shift + F5 → Stop Debugging

# Focus while debugging:
# ✔ Request payload (data)
# ✔ DB queries (user fetch / insert)
# ✔ Conditions (if checks)
# ✔ Token generation