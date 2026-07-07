from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation

def get_all_recommendations(db: Session):
    return db.query(Recommendation).all()