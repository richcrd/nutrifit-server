from pydantic import BaseModel

class QuestionOptionOut(BaseModel):
    id: int
    label: str

class QuestionOut(BaseModel):
    field: str
    label: str
    type: str
    required: bool
    options: list[QuestionOptionOut] | None = None

    class Config:
        from_attributes = True
