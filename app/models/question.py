from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    field = Column(String(50), nullable=False, unique=True)
    label = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)
    catalog_source = Column(String(50), nullable=True)
    required = Column(Boolean, nullable=False, default=True)
    order_index = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
