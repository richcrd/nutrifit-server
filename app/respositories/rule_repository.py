from sqlalchemy.orm import Session
from app.models.rule import Rule

def get_active_rules(db: Session):
    return (
        db.query(Rule)
        .filter(Rule.active == True)
        .order_by(Rule.priority.asc())
        .all()
    )