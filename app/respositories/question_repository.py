from sqlalchemy.orm import Session
from app.models.question import Question

def get_active_questions(db: Session):
    return (
        db.query(Question)
        .filter(Question.active == True)
        .order_by(Question.order_index.asc())
        .all()
    )
