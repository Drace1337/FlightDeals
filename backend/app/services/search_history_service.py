from app.models import SearchHistory
from app.extensions import db
from datetime import datetime, timezone

def save_search_history(user_id, search_data):
    history = SearchHistory(
        user_id=user_id,
        origin=search_data['origin'],
        destination=search_data['destination'],
        departure_date=datetime.strptime(search_data['departure_date'], "%Y-%m-%d").date(),
        return_date=datetime.strptime(search_data['return_date'], "%Y-%m-%d").date(),
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(history)
    db.session.commit()
    return history

def get_user_history(user_id):
    return SearchHistory.query.filter_by(user_id=user_id).order_by(SearchHistory.created_at.desc()).all()