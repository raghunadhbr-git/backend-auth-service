# =====================================================
# 🔥 FINAL INTERVIEW VERSION (DATA STRUCTURES CLEAR)
# =====================================================

from flask import Flask, Blueprint, request, jsonify   # request → dict, jsonify → JSON
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity, get_jwt
)
import hashlib


# =====================================================
# 🟩 APP FACTORY (FUNCTION)
# Input: None
# Output: Flask app object
# =====================================================
def create_app():

    app = Flask(__name__)   # app → object

    app.config["JWT_SECRET_KEY"] = "super-secret-key"   # config → dict-like

    jwt = JWTManager(app)   # jwt → object

    # =====================================================
    # 🟪 "MODELS" (IN-MEMORY)
    # =====================================================
    users = {}        # dict → {email: {password, id}}
    blacklist = set() # set → store revoked tokens

    # =====================================================
    # 🟦 ROUTES (API LAYER)
    # =====================================================
    auth_bp = Blueprint("auth", __name__)   # object


    # -----------------------------------------------------
    # 🟢 REGISTER
    # Input: JSON → dict
    # Output: JSON → dict
    # -----------------------------------------------------
    @auth_bp.post("/angularUser/register")
    def register():

        data = request.get_json()  
        # data → dict (JSON from Postman)

        email = data.get("email")       # string
        password = data.get("password") # string
        role = data.get("role", "user") # string

        if not email or not password:
            return jsonify({"message": "email required"}), 400  
            # return → (dict, int)

        if email in users:
            return jsonify({"message": "User exists"}), 400  
            # dict + status

        # password hashing
        hashed = hashlib.sha256(password.encode()).hexdigest()  
        # hashed → string

        # store in dict
        users[email] = {
            "password": hashed,   # string
            "role": role,         # string
            "id": len(users) + 1  # int
        }

        return jsonify({"message": "User registered"}), 201  
        # return → JSON


    # -----------------------------------------------------
    # 🟢 LOGIN
    # Input: dict (email, password)
    # Output: dict (token, id, role)
    # -----------------------------------------------------
    @auth_bp.post("/angularUser/login")
    def login():

        data = request.get_json()   # dict

        email = data.get("email")       # string
        password = data.get("password") # string

        user = users.get(email)   # dict OR None

        if not user:
            return jsonify({"message": "Invalid"}), 401

        hashed = hashlib.sha256(password.encode()).hexdigest()

        if user["password"] != hashed:
            return jsonify({"message": "Invalid"}), 401

        token = create_access_token(identity=str(user["id"]))  
        # token → string

        return jsonify({
            "access_token": token,  # string
            "userId": user["id"],   # int
            "role": user["role"]    # string
        }), 200


    # -----------------------------------------------------
    # 🟢 PROFILE (PROTECTED)
    # Input: Header → string token
    # Output: dict
    # -----------------------------------------------------
    @auth_bp.get("/profile")
    @jwt_required()
    def profile():

        user_id = get_jwt_identity()  
        # string (decoded from token)

        return jsonify({"user_id": user_id}), 200  
        # dict


    # -----------------------------------------------------
    # 🟢 LOGOUT
    # Input: token
    # Output: dict
    # -----------------------------------------------------
    @auth_bp.post("/logout")
    @jwt_required()
    def logout():

        jti = get_jwt()["jti"]  
        # jti → string (token id)

        blacklist.add(jti)  
        # set add

        return jsonify({"message": "Logged out"}), 200


    # -----------------------------------------------------
    # 🔴 TOKEN CHECK
    # Input: jwt_payload → dict
    # Output: bool
    # -----------------------------------------------------
    @jwt.token_in_blocklist_loader
    def check(jwt_header, jwt_payload):

        return jwt_payload["jti"] in blacklist  
        # returns True/False


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    return app   # Flask object


# =====================================================
# ▶️ RUN.PY EQUIVALENT
# =====================================================
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
"""
# This below explains like a final revision sheet for interviews, 
# focusing on data structures and data types used in the code. 
# It is meant to be a quick reference guide 
# for understanding the flow of data through the application, 
# the types of data being handled, and how they are structured.
"""
    
    
"""
🎯 🧠 FINAL UNDERSTANDING
DATA STRUCTURES USED
| Layer       | Data Structure       |
| ----------- | -------------------- |
| Request     | dict                 |
| Response    | dict → JSON          |
| Users DB    | dict                 |
| Token store | set                  |
| Model       | class (real project) |
| Token       | string               |
| Return      | tuple (dict, status) |

🔥 ONE LINE MEMORY

👉
dict → API, string → input, set → blacklist, object → app

💯 FINAL

👉 This is your ultimate revision file before interview
👉 Covers:
✔ Routes
✔ Service logic
✔ Models concept
✔ Data structures
✔ Input/output

🔥 DONE BRO
👉 Now you are FULLY READY
"""    

"""
🔥 — here is your FINAL INTERVIEW TABLE (everything in one place)
👉 Save this — gold revision 💯
________________________________________
📊 🔥 FINAL DATA FLOW TABLE

| Step | Layer                        | What Happens            | Input Type | Processing Type | Output Type | Data Structures |
| ---- | ---------------------------- | ----------------------- | ---------- | --------------- | ----------- | --------------- |
| 1    | Client (Postman/Angular)     | Sends request           | JSON       | —               | —           | dict (JSON)     |
| 2    | Route (`request.get_json()`) | Reads data              | dict       | —               | dict        | dict            |
| 3    | Extract Fields               | email, password         | string     | —               | string      | string          |
| 4    | Validation                   | check empty / duplicate | string     | if condition    | bool        | —               |
| 5    | Service Logic                | hash password           | string     | string          | string      | string          |
| 6    | Store Data                   | save user               | dict       | dict            | dict        | dict (users DB) |
| 7    | Login Check                  | compare password        | string     | string          | bool        | —               |
| 8    | Token Creation               | JWT generate            | string     | string          | string      | string          |
| 9    | Protected Route              | decode token            | string     | string          | string      | string          |
| 10   | Logout                       | store token id          | string     | set add         | set         | set (blacklist) |
| 11   | Response                     | return result           | dict       | tuple           | JSON        | dict            |
| 12   | Final Output                 | send to client          | JSON       | —               | JSON        | dict            |

🎯 🔥 SUPER SIMPLE VERSION
| Category   | Used                          |
| ---------- | ----------------------------- |
| Input      | dict (JSON)                   |
| Processing | string, bool                  |
| Storage    | dict (users), set (blacklist) |
| Output     | dict → JSON                   |
| Return     | tuple (dict, status)          |

🧠 🔥 ONE LINE MEMORY (MOST IMPORTANT)

👉
“dict → input/output, string → data, set → logout, tuple → response”

💯 FINAL INTERVIEW ANSWER

👉 If asked:

“What data structures are used?”

Say:

“We mainly use dictionaries for request and response handling, strings for user data and tokens, sets for token blacklist, and tuples for returning responses with status codes.”

🔥 DONE BRO
👉 This is your ultimate revision sheet
"""