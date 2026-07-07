from datetime import datetime
from pydantic import BaseModel

from app.schemas.catalog import DiagnosticOut, RecommendationOut

class ConsultationCreate(BaseModel):
    weight_kg: float
    height_cm: float
    age: int
    physic_activity_id: int | None = None
    goal_id: int | None = None

class ConsultationOut(BaseModel):
    id: int
    weight_kg: float
    height_cm: float
    age: int
    imc_calculated: float
    recommended_water_ml: int
    diagnostic: DiagnosticOut
    recommendations: list[RecommendationOut]
    created_at: datetime

    class Config:
        from_attributes = True
