from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Boolean, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

recommendations_rule = Table(
    "recommendations_rule",
    Base.metadata,
    Column("rule_id", Integer, ForeignKey("rules.id"), primary_key=True),
    Column("recommendation_id", Integer, ForeignKey("catalog_recommendations.id"), primary_key=True),
)

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    field = Column(String(50), nullable=False)
    operator = Column(String(10), nullable=False)
    min_value = Column(Numeric, nullable=False)
    max_value = Column(Numeric, nullable=True)
    diagnostic_id = Column(Integer, ForeignKey("catalog_diagnostics.id"), nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)

    diagnostic = relationship("Diagnostic")
    recommendations = relationship("Recommendation", secondary=recommendations_rule)
