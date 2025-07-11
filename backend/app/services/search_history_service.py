from app.models import SearchHistory
from app.extensions import db
from datetime import datetime, timezone

def save_search_history(user_id, search_data):
    """    Save the search history for a user.
    Args:
        user_id (int): The ID of the user.
        search_data (dict): The search data to be saved.
    """
    history = SearchHistory(
        user_id=user_id,
        origin=search_data['origin'],
        destination=search_data['destination'],
        departure_date=search_data['departure_date'],
        return_date=search_data['return_date'],
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(history)
    db.session.commit()
    return history.id

def get_user_history(user_id):
    """    Retrieve the search history for a user.
    Args:
        user_id (int): The ID of the user.
    """
    return SearchHistory.query.filter_by(user_id=user_id).order_by(SearchHistory.created_at.desc()).all()