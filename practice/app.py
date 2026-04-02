# =====================================================
# FLASK AUTH MICROSERVICE (ALL-IN-ONE PRACTICE FILE)
# Includes: Routes + Service + Model (in-memory)
# DEBUG VERSION (ADD PRINTS)
# =====================================================

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity, get_jwt
)
import hashlib


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    jwt = JWTManager(app)

    # -----------------------------
    # "MODEL" (IN-MEMORY)
    # -----------------------------
    users = {}          # acts like DB table
    blacklist = set()   # token blacklist


    auth_bp = Blueprint("auth", __name__)

    # -----------------------------
    # REGISTER
    # -----------------------------
    @auth_bp.post("/angularUser/register")
    def register():
        data = request.get_json()
        print("🔍 Incoming Register Data:", data)

        email = data.get("email")
        password = data.get("password")

        print("📩 Email:", email)
        print("🔑 Password:", password)

        if email in users:
            print("❌ Duplicate user")
            return jsonify({"message": "User already exists"}), 400

        hashed = hashlib.sha256(password.encode()).hexdigest()
        print("🔐 Hashed Password:", hashed)

        users[email] = {"password": hashed, "id": len(users) + 1}

        print("✅ User Stored:", users)

        return jsonify({"message": "User registered successfully"}), 201

    # -----------------------------
    # LOGIN
    # -----------------------------
    @auth_bp.post("/angularUser/login")
    def login():
        data = request.get_json()
        print("🔍 Login Data:", data)

        email = data.get("email")
        password = data.get("password")

        user = users.get(email)
        print("👤 User Found:", user)

        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        hashed = hashlib.sha256(password.encode()).hexdigest()

        print("🔐 Hashed Input:", hashed)

        if user["password"] != hashed:
            print("❌ Password mismatch")
            return jsonify({"message": "Invalid email or password"}), 401

        token = create_access_token(identity=str(user["id"]))
        print("🎟️ Token Generated:", token)

        return jsonify({"access_token": token}), 200

    # -----------------------------
    # PROFILE
    # -----------------------------
    @auth_bp.get("/profile")
    @jwt_required()
    def profile():
        user_id = get_jwt_identity()
        print("👤 Logged in user:", user_id)

        return jsonify({"user_id": user_id}), 200

    # -----------------------------
    # LOGOUT
    # -----------------------------
    @auth_bp.post("/logout")
    @jwt_required()
    def logout():
        jti = get_jwt()["jti"]
        print("🚫 Blacklisting token:", jti)

        blacklist.add(jti)
        return jsonify({"message": "Logged out"}), 200

    @jwt.token_in_blocklist_loader
    def check(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
    
