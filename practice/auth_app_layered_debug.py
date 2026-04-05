# =====================================================
# FILE: auth_app_layered_debug.py
# DEBUG VERSION (Where to put breakpoints + what to inspect)
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

    # =====================================================
    # MODEL LAYER
    # =====================================================
    users = {}
    blacklist = set()

    def create_user(email, hashed_password):
        # 🔴 DEBUG POINT (MODEL - CREATE)
        print("MODEL: Creating user", email)

        users[email] = {
            "id": len(users) + 1,
            "password": hashed_password
        }

        # 👉 Inspect in debugger:
        # users dict → should contain new user
        return users[email]

    def get_user(email):
        # 🔴 DEBUG POINT (MODEL - READ)
        print("MODEL: Fetching user", email)

        return users.get(email)


    # =====================================================
    # SERVICE LAYER
    # =====================================================
    def register_service(email, password):
        # 🔴 DEBUG POINT (SERVICE ENTRY)
        print("SERVICE: Register called")

        # 👉 Inspect:
        # email = "user@test.com"
        # password = "12345"

        if email in users:
            return {"message": "User already exists"}, 400

        hashed = hashlib.sha256(password.encode()).hexdigest()

        # 👉 Inspect:
        # hashed → long string (same for same password)

        create_user(email, hashed)

        return {"message": "User registered successfully"}, 201


    def login_service(email, password):
        # 🔴 DEBUG POINT
        print("SERVICE: Login called")

        user = get_user(email)

        # 👉 Inspect:
        # user = {"id": 1, "password": "hashed_value"}

        if not user:
            return {"message": "Invalid email or password"}, 401

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if user["password"] != hashed:
            return {"message": "Invalid email or password"}, 401

        token = create_access_token(identity=str(user["id"]))

        # 👉 Inspect:
        # token = JWT string

        return {"access_token": token}, 200


    def profile_service():
        # 🔴 DEBUG POINT
        print("SERVICE: Profile called")

        user_id = get_jwt_identity()

        # 👉 Inspect:
        # user_id = "1"

        return {"user_id": user_id}, 200


    def logout_service():
        # 🔴 DEBUG POINT
        print("SERVICE: Logout called")

        jti = get_jwt()["jti"]

        # 👉 Inspect:
        # jti = unique token id

        blacklist.add(jti)

        return {"message": "Logged out"}, 200


    # JWT BLOCKLIST CHECK
    @jwt.token_in_blocklist_loader
    def check(jwt_header, jwt_payload):
        # 🔴 DEBUG POINT (VERY IMPORTANT)
        print("JWT CHECK:", jwt_payload["jti"])

        return jwt_payload["jti"] in blacklist


    # =====================================================
    # ROUTE LAYER
    # =====================================================
    auth_bp = Blueprint("auth", __name__)

    @auth_bp.post("/angularUser/register")
    def register():
        # 🔴 DEBUG POINT (ROUTE ENTRY)
        print("ROUTE: Register API hit")

        data = request.get_json()

        # 👉 Inspect:
        # data = {"email": "...", "password": "..."}

        email = data.get("email")
        password = data.get("password")

        response, status = register_service(email, password)

        return jsonify(response), status


    @auth_bp.post("/angularUser/login")
    def login():
        # 🔴 DEBUG POINT
        print("ROUTE: Login API hit")

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        response, status = login_service(email, password)

        return jsonify(response), status


    @auth_bp.get("/profile")
    @jwt_required()
    def profile():
        # 🔴 DEBUG POINT
        print("ROUTE: Profile API hit")

        response, status = profile_service()

        return jsonify(response), status


    @auth_bp.post("/logout")
    @jwt_required()
    def logout():
        # 🔴 DEBUG POINT
        print("ROUTE: Logout API hit")

        response, status = logout_service()

        return jsonify(response), status


    # =====================================================
    # HEALTH CHECK
    # =====================================================
    @app.get("/")
    def health_root():
        return jsonify({"status": "UP"}), 200

    @app.get("/health")
    def health():
        return jsonify({"status": "UP"}), 200


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


# =====================================================
# SAMPLE DEBUG FLOW (VERY IMPORTANT)
# =====================================================

# 👉 Example: REGISTER
# Request:
# {
#   "email": "user@test.com",
#   "password": "12345"
# }

# FLOW:
# ROUTE → register()
#   ↓
# SERVICE → register_service()
#   ↓
# MODEL → create_user()
#   ↓
# BACK → SERVICE
#   ↓
# BACK → ROUTE → response


# 👉 Example: LOGIN
# ROUTE → login()
#   ↓
# SERVICE → login_service()
#   ↓
# MODEL → get_user()
#   ↓
# TOKEN GENERATED
#   ↓
# RESPONSE


# =====================================================
# 🧠 DEBUGGING STRATEGY (INTERVIEW GOLD)
# =====================================================

# 1. Start at ROUTE (entry point)
# 2. Step Into → SERVICE
# 3. Step Into → MODEL
# 4. Step Out → SERVICE
# 5. Step Out → ROUTE → RESPONSE

# Use VS Code:
# F9 → breakpoint
# F10 → step over
# F11 → step into


# =====================================================
# 🔍 WHAT TO INSPECT
# =====================================================

# ROUTE:
# - data (incoming JSON)

# SERVICE:
# - email, password
# - hashed password
# - token

# MODEL:
# - users dict

# JWT:
# - jti (token id)