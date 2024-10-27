from flask import Flask, jsonify, request
from flask_cors import cross_origin, CORS
from pymongo import MongoClient
from jose import jwt
from functools import wraps
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_IDENTIFIER = os.getenv("API_IDENTIFIER")
ALGORITHMS = os.getenv("ALGORITHMS")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client['auth_database']
users_collection = db['users']

# Helper function to get the token from the Authorization header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Exception("Authorization header is missing")
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Exception("Token not found")
    elif len(parts) > 2:
        raise Exception("Authorization header must be Bearer token")
    return parts[1]

# Auth0 JWT verification decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        try:
            jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = requests.get(jwks_url).json()
            payload = jwt.decode(token, jwks, algorithms=[ALGORITHMS], audience=API_IDENTIFIER)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.JWTError:
            return jsonify({"error": "Invalid token"}), 401
        return f(payload, *args, **kwargs)
    return decorated

# Signup endpoint (creates a new Auth0 user and saves to MongoDB)
@app.route('/signup', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Use Auth0 Management API to create a new user
    auth0_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials"
    }

    # Get Auth0 Management API token
    auth_response = requests.post(auth0_url, headers=headers, json=payload)
    mgmt_token = auth_response.json().get("access_token")

    # Create user
    if mgmt_token:
        user_url = f"https://{AUTH0_DOMAIN}/api/v2/users"
        user_headers = {
            "authorization": f"Bearer {mgmt_token}",
            "content-type": "application/json"
        }
        user_payload = {
            "email": email,
            "password": password,
            "connection": "Username-Password-Authentication"
        }
        user_response = requests.post(user_url, headers=user_headers, json=user_payload)
        new_user = user_response.json()

        # Save user data in MongoDB
        user_data = {
            "auth0_id": new_user.get("user_id"),
            "email": email,
            "created_at": new_user.get("created_at")
        }
        users_collection.insert_one(user_data)

        return jsonify({"message": "User created successfully", "user": user_data}), 201
    else:
        return jsonify({"error": "Failed to get Auth0 Management API token"}), 500

# Login endpoint (authenticates user with Auth0)
@app.route('/login', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    auth_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "password",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": API_IDENTIFIER,
        "username": username,
        "password": password,
        "scope": "openid profile email"
    }
    response = requests.post(auth_url, json=payload)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Failed to authenticate"}), response.status_code

# Protected route (requires valid Auth0 token)
@app.route('/protected', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def protected_route(payload):
    auth0_id = payload["sub"]
    user = users_collection.find_one({"auth0_id": auth0_id})

    if user:
        return jsonify({"message": "This is a protected route.", "user": {"email": user["email"], "auth0_id": user["auth0_id"]}}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
