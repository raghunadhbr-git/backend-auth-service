# =====================================================
# FILE: auth_app_layered.py
# Single-file BUT layered structure inside
# Route → Service → Model (Interview Ready)
# =====================================================

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity, get_jwt
)
import hashlib


# =====================================================
# APP FACTORY
# =====================================================
def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    jwt = JWTManager(app)

    # =====================================================
    # MODEL LAYER (DB Simulation - In Memory)
    # =====================================================
    users = {}        # {email: {id, password}}
    blacklist = set() # token blacklist

    def create_user(email, hashed_password):
        users[email] = {
            "id": len(users) + 1,
            "password": hashed_password
        }
        return users[email]

    def get_user(email):
        return users.get(email)


    # =====================================================
    # SERVICE LAYER (Business Logic)
    # =====================================================
    def register_service(email, password):
        # Input: email(str), password(str)
        # Output: JSON response

        if email in users:
            return {"message": "User already exists"}, 400

        hashed = hashlib.sha256(password.encode()).hexdigest()

        create_user(email, hashed)

        return {"message": "User registered successfully"}, 201


    def login_service(email, password):
        user = get_user(email)

        if not user:
            return {"message": "Invalid email or password"}, 401

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if user["password"] != hashed:
            return {"message": "Invalid email or password"}, 401

        token = create_access_token(identity=str(user["id"]))

        return {"access_token": token}, 200


    def profile_service():
        user_id = get_jwt_identity()
        return {"user_id": user_id}, 200


    def logout_service():
        jti = get_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Logged out"}, 200


    # JWT blocklist check
    @jwt.token_in_blocklist_loader
    def check(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist


    # =====================================================
    # ROUTE LAYER (Controller)
    # =====================================================
    auth_bp = Blueprint("auth", __name__)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    
    # ---------------------------
    # HEALTH CHECK (ROOT LEVEL)
    # ---------------------------
    @app.get("/")
    def health_root():
        return jsonify({
            "status": "UP",
            "service": "auth-service"
        }), 200


    # ---------------------------
    # HEALTH CHECK (EXPLICIT)
    # ---------------------------
    @app.get("/health")
    def health():
        return jsonify({
            "status": "UP",
            "service": "auth-service"
        }), 200

    # -------- REGISTER --------
    @auth_bp.post("/angularUser/register")
    def register():
        # JSON request → Python dict
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        # Call service
        response, status = register_service(email, password)

        # dict → JSON response
        return jsonify(response), status


    # -------- LOGIN --------
    @auth_bp.post("/angularUser/login")
    def login():
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        response, status = login_service(email, password)

        return jsonify(response), status


    # -------- PROFILE --------
    @auth_bp.get("/profile")
    @jwt_required()
    def profile():
        response, status = profile_service()
        return jsonify(response), status


    # -------- LOGOUT --------
    @auth_bp.post("/logout")
    @jwt_required()
    def logout():
        response, status = logout_service()
        return jsonify(response), status


    # =====================================================
    # FLOW SUMMARY (IMPORTANT FOR INTERVIEW)
    # =====================================================
    # Client (JSON request)
    #   ↓
    # Route Layer (request.get_json())
    #   ↓
    # Service Layer (business logic, hashing, validation)
    #   ↓
    # Model Layer (users dict / blacklist set)
    #   ↓
    # Service returns dict
    #   ↓
    # Route converts dict → JSON (jsonify)
    #   ↓
    # Client receives response

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    return app


# Run app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


# =====================================================
# HOW TO RUN
# =====================================================
# python auth_app_layered.py