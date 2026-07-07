from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Diagnostic(Base):
    __tablename__ = "catalog_diagnostics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

class PhysicActivity(Base):
    __tablename__ = "catalog_physic_activity"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    calorie_factor = Column(Integer,nullable=True)

class Goal(Base):
    __tablename__ = "catalog_goals"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
