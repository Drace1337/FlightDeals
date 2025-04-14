from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_history_service import save_search_history
from app.services.amadeus_service import AmadeusService
from datetime import datetime
from flask import current_app

search_bp = Blueprint("search", __name__)
amadeus_service = AmadeusService()


# @search_bp.route("/iata", methods=["GET", "POST"])
# @jwt_required()
# def get_iata():

#     if request.method == "GET":
#         city = request.args.get("city")
#     else:
#         data = request.get_json()
#         city = data.get("city")

#     if not city:
#         return jsonify({"error": "City is required"}), 400

#     token = amadeus_service.get_token()
#     iata_codes = amadeus_service.get_iata_codes(token, city)

#     return jsonify(iata_codes), 200

@search_bp.route("/iata", methods=["GET", "POST"])
@jwt_required()
def get_iata():
    current_app.logger.info("Request JSON: %s", request.get_json())

    if request.method == "GET":
        city = request.args.get("city")
    else:
        data = request.get_json()
        city = data.get("city")

    print("CITY:", city)

    if not city:
        return jsonify({"error": "City is required"}), 400

    token = amadeus_service.get_token()
    iata_codes = amadeus_service.get_iata_codes(token, city)

    return jsonify(iata_codes), 200


@search_bp.route("/flights", methods=["POST"])
@jwt_required()
def search_flights_route():
    data = request.get_json()
    token = amadeus_service.get_token()
    offers = amadeus_service.search_flights(token, data)

    return jsonify(offers), 200


@search_bp.route("/save", methods=["POST"])
@jwt_required()
def save_search_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    user_id = get_jwt_identity()
    current_app.logger.info("JWT user_id: %s", user_id)
    current_app.logger.info("DATA: %s", data)

    try:
        # konwersja dat ze stringa na date
        data["departure_date"] = datetime.strptime(
            data["departure_date"], "%Y-%m-%d"
        ).date()
        data["return_date"] = datetime.strptime(data["return_date"], "%Y-%m-%d").date()

        search_id = save_search_history(user_id, data)
        return jsonify({"message": "Search saved", "id": search_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
