from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_history_service import get_user_history

history_bp = Blueprint('history', __name__)


@history_bp.route("/", methods=["GET"])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()

    try:
        history = get_user_history(user_id)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
