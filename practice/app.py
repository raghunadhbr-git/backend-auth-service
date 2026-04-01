# =====================================================
# FLASK AUTH MICROSERVICE (ALL-IN-ONE PRACTICE FILE)
# Includes: Routes + Service + Model (in-memory)
# =====================================================

from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# -----------------------------
# "MODEL" (IN-MEMORY)
# -----------------------------
users = {}          # acts like DB table
blacklist = set()   # token blacklist

# -----------------------------
# "SERVICE LAYER"
# -----------------------------
def register_user(email, password, role="user"):
    if email in users:
        return {"message": "User already exists"}, 400

    hashed = hashlib.sha256(password.encode()).hexdigest()

    users[email] = {
        "password": hashed,
        "role": role,
        "id": len(users) + 1
    }

    return {"message": "User registered successfully"}, 201


# -----------------------------
# ROUTES (API)
# -----------------------------

@app.get("/")
def health():
    return jsonify({"status": "UP"}), 200


@app.post("/register")
def register():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    resp, status = register_user(email, password, role)
    return jsonify(resp), status


@app.post("/login")
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

    token = f"token-{user['id']}"

    return jsonify({
        "access_token": token,
        "userId": user["id"],
        "role": user["role"]
    }), 200


@app.get("/profile")
def profile():
    token = request.headers.get("Authorization")

    if not token or token in blacklist:
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify({"user_id": token.split("-")[-1]}), 200


@app.post("/logout")
def logout():
    token = request.headers.get("Authorization")

    if token:
        blacklist.add(token)

    return jsonify({"message": "Logged out successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True) 
