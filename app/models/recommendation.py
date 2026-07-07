from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Recommendation(Base):
    __tablename__ = "catalog_recommendations"

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    