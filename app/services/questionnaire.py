from sqlalchemy.orm import Session

from app.models.catalog import PhysicActivity, Goal
from app.models.question import Question
from app.respositories.question_repository import get_active_questions
from app.schemas.question import QuestionOut, QuestionOptionOut

CATALOG_MODELS = {
    "physic_activity": PhysicActivity,
    "goal": Goal,
}

def get_questionnaire(db: Session) -> list[QuestionOut]:
    questions = get_active_questions(db)
    return [build_question_out(db, question) for question in questions]

def build_question_out(db: Session, question: Question) -> QuestionOut:
    options = None

    if question.catalog_source is not None:
        catalog_model = CATALOG_MODELS[question.catalog_source]
        catalog_items = db.query(catalog_model).all()
        options = [QuestionOptionOut(id=item.id, label=item.name) for item in catalog_items]
    
    return QuestionOut(
        field=question.field,
        label=question.label,
        type=question.type,
        required=question.required,
        options=options,
    )
