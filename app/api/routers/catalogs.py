from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.models.catalog import PhysicActivity, Goal, Diagnostic
from app.schemas.catalog import PhysicActivityOut, GoalOut, DiagnosticOut

router = APIRouter(prefix="/catalogs", tags=["catalogs"])

@router.get("/physic-activity", response_model=list[PhysicActivityOut])
def list_physic_activity(db: Session = Depends(get_db)):
  return db.query(PhysicActivity).all()

@router.get("/goals", response_model=list[GoalOut])
def list_goals(db: Session = Depends(get_db)):
    return db.query(Goal).all()


@router.get("/diagnostics", response_model=list[DiagnosticOut])
def list_diagnostics(db: Session = Depends(get_db)):
    return db.query(Diagnostic).all()
