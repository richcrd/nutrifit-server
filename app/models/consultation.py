from sqlalchemy import Column, ForeignKey, Integer, Numeric, DateTime, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.rule import recommendations_rule

recommendations_consultation = Table(
    "recommendations_consultation",
    Base.metadata,
    Column("consultation_id", Integer, ForeignKey("consultations.id"), primary_key=True),
    Column("recommendation_id", Integer, ForeignKey("catalog_recommendations.id"), primary_key=True),
)

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight_kg = Column(Numeric, nullable=False)
    height_cm = Column(Numeric, nullable=False)
    age = Column(Integer, nullable=False)
    physic_activity_id = Column(Integer, ForeignKey("catalog_physic_activity.id"), nullable=True)
    goal_id = Column(Integer, ForeignKey("catalog_goals.id"), nullable=True)

    imc_calculated = Column(Numeric, nullable=False)
    recommended_water_ml = Column(Integer, nullable=False)
    diagnostic_id = Column(Integer, ForeignKey("catalog_diagnostics.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    diagnostic = relationship("Diagnostic")
    physic_activity = relationship("PhysicActivity")
    goal = relationship("Goal")
    recommendations = relationship("Recommendation", secondary=recommendations_consultation)
