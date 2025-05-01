from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("", methods=["GET"])
@jwt_required()
def get_profile():
    """ "Get user profile information."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return (
            jsonify(
                {
                    "email": user.email,
                    "name": user.name,
                }
            ),
            200,
        )
    return jsonify({"message": "User not found"}), 404


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update user profile information."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if "email" in data and data["email"] != user.email:
        existing_email = User.query.filter_by(email=data["email"]).first()
        if existing_email:
            return jsonify({"message": "User with such email already exists"}), 409
        user.email = data["email"]
    if "name" in data and data["name"] != user.name:
        existing_name = User.query.filter_by(name=data["name"]).first()
        if existing_name:
            return jsonify({"message": "User with such name already exists"}), 409
        user.name = data["name"]

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@profile_bp.route("/password", methods=["PUT"])
@jwt_required()
def update_password():
    """Update user password."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not all(key in data for key in ["current_password", "new_password"]):
        return jsonify({"message": "Current and new password are required"}), 400
    
    if not check_password_hash(user.password, data["current_password"]):
        return jsonify({"message": "Current password is incorrect"}), 401
    
    user.password = generate_password_hash(data["new_password"])
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200