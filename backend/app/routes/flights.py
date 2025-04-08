from flask import Blueprint, request, jsonify
from app import db
from app.models.search_history import SearchHistory
from app.models.user import User

flights_bp = Blueprint('flights', __name__)

def to_dict(self):
    return {
        'id': self.id,
        'origin': self.origin,
        'destination': self.destination,
        'departure_date': self.departure_date.isoformat(),
        'return_date': self.return_date.isoformat(),
        'created_at': self.created_at.isoformat(),
        'user_id': self.user_id,
    }

@flights_bp.route('/save', methods=['POST'])
def save_search():
    data= request.get_json()
    criteria = SearchHistory(
        origin=data['origin'],
        destination=data['destination'],
        departure_date=data['departure_date'],
        return_date=data['return_date'],
        user_id=data['user_id']
    )
    db.session.add(criteria)
    db.session.commit()
    return jsonify({"message": "Search saved successfully"}), 201

@flights_bp.route('/history/<int:user_id>', methods=['GET'])
def get_search_history(user_id):
    history = SearchHistory.query.filter_by(user_id=user_id).all()
    return jsonify([h.to_dict() for h in history]), 200