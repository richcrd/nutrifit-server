from annotated_types import Timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    genre = Column(String(1), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
