# =====================================================
# FULL AUTH APP (JWT + BLUEPRINT)
# =====================================================

from flask import Flask
from flask_jwt_extended import JWTManager

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
import hashlib

# -----------------------------
# APP FACTORY
# -----------------------------
def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    jwt = JWTManager(app)

    # In-memory DB
    users = {}
    blacklist = set()

    auth_bp = Blueprint("auth", __name__)

    # -----------------------------
    # HEALTH
    # -----------------------------
    @auth_bp.get("/")
    def health():
        return jsonify({"status": "UP"}), 200

    # -----------------------------
    # REGISTER
    # -----------------------------
    @auth_bp.post("/angularUser/register")
    def register():
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not email or not password:
            return jsonify({"message": "email and password required"}), 400

        if email in users:
            return jsonify({"message": "User already exists"}), 400

        hashed = hashlib.sha256(password.encode()).hexdigest()

        users[email] = {
            "password": hashed,
            "role": role,
            "id": len(users) + 1
        }

        return jsonify({"message": "User registered successfully"}), 201

    # -----------------------------
    # LOGIN
    # -----------------------------
    @auth_bp.post("/angularUser/login")
    def login():
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")

        user = users.get(email)

        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if user["password"] != hashed:
            return jsonify({"message": "Invalid email or password"}), 401

        token = create_access_token(identity=str(user["id"]))

        return jsonify({
            "access_token": token,
            "userId": user["id"],
            "role": user["role"]
        }), 200

    # -----------------------------
    # PROFILE (JWT REQUIRED)
    # -----------------------------
    @auth_bp.get("/profile")
    @jwt_required()
    def profile():
        user_id = get_jwt_identity()
        return jsonify({"user_id": user_id}), 200

    # -----------------------------
    # LOGOUT (BLACKLIST)
    # -----------------------------
    @auth_bp.post("/logout")
    @jwt_required()
    def logout():
        jti = get_jwt()["jti"]
        blacklist.add(jti)
        return jsonify({"message": "Logged out successfully"}), 200

    # -----------------------------
    # BLOCKLIST CHECK
    # -----------------------------
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    return app


# -----------------------------
# RUN
# -----------------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)