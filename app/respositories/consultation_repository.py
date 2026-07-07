from sqlalchemy.orm import Session
from app.models.consultation import Consultation

def create_consultation(
    db: Session,
    user_id: int,
    weight_kg: float,
    height_cm: float,
    age: int,
    physic_activity_id: int | None,
    goal_id: int | None,
    imc_calculated: float,
    recommended_water_ml: int,
    diagnostic_id: int,
    recommendations: list,
):
    consultation = Consultation(
      user_id=user_id,
      weight_kg=weight_kg,
      height_cm=height_cm,
      age=age,
      physic_activity_id=physic_activity_id,
      goal_id=goal_id,
      imc_calculated=imc_calculated,
      recommended_water_ml=recommended_water_ml,
      diagnostic_id=diagnostic_id,
    )
    consultation.recommendations = recommendations

    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation

def get_history_by_user(db: Session, user_id: int):
  return (
    db.query(Consultation)
    .filter(Consultation.user_id == user_id)
    .order_by(Consultation.created_at.desc())
    .all()
  )

def get_by_id(db: Session, consultation_id: int):
  return db.query(Consultation).filter(Consultation.id == consultation_id).first()
