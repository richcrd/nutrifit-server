from pydantic import BaseModel

class DiagnosticOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class PhysicActivityOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class GoalOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RecommendationOut(BaseModel):
    id: int
    text: str
    category: str

    class Config:
        from_attributes = True
