from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_history_service import save_search_history
from app.services.amadeus_service import AmadeusService
from datetime import datetime
from flask import current_app

search_bp = Blueprint("search", __name__)
amadeus_service = None


def init_amadeus_service(service):
    """
    Initialize the AmadeusService and store it in the Flask app context.
    This allows the service to be accessed globally within the app.
    """
    current_app.extensions["amadeus_service"] = service

def get_amadeus_service():
    """
    Retrieve the AmadeusService instance from the Flask app context.
    This function is used to access the AmadeusService throughout the application.
    Returns:
        AmadeusService: The initialized AmadeusService instance.
    """
    return current_app.extensions.get("amadeus_service")


@search_bp.route("/iata", methods=["GET", "POST"])
@jwt_required()
def get_iata():
    """
    Route to get IATA codes for airports in a given city

    Expected query parameter (GET) or JSON (POST):
    - city: Name of the city to search for

    Returns:
        JSON: List of dictionaries containing airport information including IATA codes
    """
    try:
        if request.method == "GET":
            city = request.args.get("city")
        else:  
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
            city = data.get("city")

        if not city:
            return jsonify({"error": "City parameter is required"}), 400

        iata_codes = get_amadeus_service().get_iata_codes(city)

        return jsonify(iata_codes), 200
    except Exception as e:
        current_app.logger.error(f"Error getting IATA codes: {str(e)}")
        return jsonify({"error": str(e)}), 500


@search_bp.route("/flights", methods=["GET", "POST"])
@jwt_required()
def search_flights_route():
    """
    Route to search for flights based on provided parameters

    Expected JSON body:
    {
        "origin_iata": "SYD",
        "destination_iata": "BKK",
        "departure_date": "2023-05-02",
        "return_date": "2023-05-10",
        "adults": 1
    }

    Returns:
        JSON: Flight offers matching the search criteria
    """
    if request.method == "GET":
        origin_iata = request.args.get("origin_iata")
        destination_iata = request.args.get("destination_iata")
        departure_date = request.args.get("departure_date")
        return_date = request.args.get("return_date")
        adults = request.args.get("adults", 1)
    else:  
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        origin_iata = data.get("origin_iata")
        destination_iata = data.get("destination_iata")
        departure_date = data.get("departure_date")
        return_date = data.get("return_date")
        adults = data.get("adults", 1)

    if not all([origin_iata, destination_iata, departure_date]):
        return (
            jsonify(
                {
                    "error": "Missing required parameters: origin_iata, destination_iata, departure_date"
                }
            ),
            400,
        )

    try:
        adults = int(adults)

        offers = get_amadeus_service().search_flights(
            origin_iata, destination_iata, departure_date, return_date, adults
        )

        return jsonify(offers), 200
    except ValueError:
        return jsonify({"error": "adults must be a valid number"}), 400
    except Exception as e:
        current_app.logger.error(f"Error searching flights: {str(e)}")
        return jsonify({"error": str(e)}), 500


@search_bp.route("/save", methods=["POST"])
@jwt_required()
def save_search_route():
    """
    Route to save a flight search history entry for the authenticated user.
    Expected JSON body:
    {
        "origin_iata": "SYD",
        "destination_iata": "BKK",
        "departure_date": "2023-05-02",
        "return_date": "2023-05-10",
        "adults": 1
    }
    Returns:
        JSON: Confirmation message and search ID if successful
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    user_id = int(get_jwt_identity())
    current_app.logger.info("JWT user_id: %s", user_id)
    current_app.logger.info("DATA: %s", data)

    try:
        data["departure_date"] = datetime.strptime(
            data["departure_date"], "%Y-%m-%d"
        ).date()
        data["return_date"] = datetime.strptime(data["return_date"], "%Y-%m-%d").date()

        search_id = save_search_history(user_id, data)
        return jsonify({"message": "Search saved", "id": search_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
