from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.search_history_service import save_search_history
from services.amadeus_service import get_access_token, get_iata_codes, search_flights

search_bp = Blueprint('search', __name__)


@search_bp.route("/iata", methods=["POST"])
@jwt_required()
def get_iata():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    token = get_access_token()
    iata_codes = get_iata_codes(token, city)

    return jsonify(iata_codes), 200


@search_bp.route("/flights", methods=["POST"])
@jwt_required()
def search_flights_route():
    data = request.get_json()
    token = get_access_token()
    offers = search_flights(token, data)

    return jsonify(offers), 200


@search_bp.route("/save", methods=["POST"])
@jwt_required()
def save_search_route():
    data = request.get_json()
    user_id = get_jwt_identity()

    try:
        search_id = save_search_history(user_id, data)
        return jsonify({"message": "Search saved", "id": search_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
