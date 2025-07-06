from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.extensions import db
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login a user."""

    if not request.is_json:
        return jsonify({"message": "No data provided"}), 400

    data = request.get_json() 

    if not data:
        return jsonify({"message": "Email and password are required"}), 400
    
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 401

    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout a user."""
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    """Register a new user."""

    if not request.is_json:
        return jsonify({"message": "No data provided"}), 400


    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid input"}), 400

    name = data.get("name")
    email = data.get("email") 
    password = data.get("password")
    if not email or not password or not name:
        return jsonify({"message": "Email, name and password are required"}), 400

    existing_email = User.query.filter_by(email=email).first()
    existing_name = User.query.filter_by(name=name).first()
    if existing_email:
        return jsonify({"message": "User with such email already exists"}), 409
    if existing_name:
        return jsonify({"message": "User with such name already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

