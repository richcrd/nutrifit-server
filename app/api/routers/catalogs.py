from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.models.catalog import PhysicActivity, Goal, Diagnostic
from app.schemas.catalog import PhysicActivityOut, GoalOut, DiagnosticOut
from app.api.response import success_response

router = APIRouter(prefix="/catalogs", tags=["catalogs"])

@router.get("/physic-activity")
def list_physic_activity(db: Session = Depends(get_db)):
  activities = db.query(PhysicActivity).all()
  return success_response(
    data=[PhysicActivityOut.model_validate(a).model_dump() for a in activities],
    message="Actividades físicas obtenidas correctamente",
  )

@router.get("/goals")
def list_goals(db: Session = Depends(get_db)):
    goals = db.query(Goal).all()
    return success_response(
        data=[GoalOut.model_validate(g).model_dump() for g in goals],
        message="Metas obtenidas correctamente",
    )

@router.get("/diagnostics")
def list_diagnostics(db: Session = Depends(get_db)):
    diagnostics = db.query(Diagnostic).all()
    return success_response(
        data=[DiagnosticOut.model_validate(d).model_dump() for d in diagnostics],
        message="Diagnósticos obtenidos correctamente",
    )
