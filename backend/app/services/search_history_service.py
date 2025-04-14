from app.models import db, SearchHistory
from datetime import datetime, timezone

def save_search_history(user_id, search_data):
    history = SearchHistory(
        user_id=user_id,
        origin_city=search_data['origin_city'],
        destination_city=search_data['destination_city'],
        origin_iata=search_data['origin_iata'],
        destination_iata=search_data['destination_iata'],
        departure_date=search_data['departure_date'],
        return_date=search_data['return_date'],
        passengers=search_data['passengers'],
        price=search_data.get('price'),
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(history)
    db.session.commit()
    return history

def get_user_history(user_id):
    return SearchHistory.query.filter_by(user_id=user_id).order_by(SearchHistory.created_at.desc()).all()