from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection string
MONGO_CONNECTION_STRING = "mongodb+srv://hack24teambreakers:B8R2o6C7DayfaQ92@fdhck24.2riz5.mongodb.net/hck24gm?retryWrites=true&w=majority&appName=FDHCK24&serverSelectionTimeoutMS=30000&connectTimeoutMS=30000"

# Create a MongoClient object
client = MongoClient(MONGO_CONNECTION_STRING)

# Access the database
db = client.hck24gm

# Access a collection
users_collection = db.users

@app.route('/')
def home():
    return "Welcome to the User Management API"

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    if not user_data or 'username' not in user_data or 'password' not in user_data:
        return jsonify({"error": "Invalid user data"}), 400
    
    # In a real application, you should hash the password here
    new_user = {
        "username": user_data['username'],
        "password": user_data['password']
    }
    
    result = users_collection.insert_one(new_user)
    return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    if not user_data:
        return jsonify({"error": "No data provided"}), 400
    
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_data}
    )
    
    if result.modified_count:
        return jsonify({"message": "User updated"})
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))