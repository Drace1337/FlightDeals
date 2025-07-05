from flask import Blueprint, jsonify, request
from app.services.search_history_service import get_user_history

history_bp = Blueprint('history', __name__)

@history_bp.route("", methods=["GET", "OPTIONS"])
def get_history():
    if request.method == "OPTIONS":
        return '', 200

    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    try:
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        history = get_user_history(user_id)
        return jsonify([entry.to_dict() for entry in history]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

