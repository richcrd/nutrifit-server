from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import DiagnosticNotFound
from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.models.catalog import Goal, PhysicActivity
from app.schemas.consultation import ConsultationCreate, ConsultationOut
from app.schemas.question import QuestionOut
from app.services.inference_engine import process_consultation
from app.services.questionnaire import get_questionnaire
from app.respositories.consultation_repository import create_consultation, get_history_by_user
from app.api.response import success_response

router = APIRouter(prefix="/consultations", tags=["consultations"])

@router.get("/questions")
def get_questions_consultation(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    questions = get_questionnaire(db)
    return success_response(
        data=[QuestionOut.model_validate(q).model_dump() for q in questions],
        message="Preguntas obtenidas correctamente",
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_consulta_nutricional(
    data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    result = process_consultation(
        db=db,
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        age=data.age,
        genre=current_user.genre,
    )

    if result["diagnostic"] is None:
        raise DiagnosticNotFound()

    if data.goal_id is not None:
        if not db.query(Goal).filter(Goal.id == data.goal_id).first():
            raise HTTPException(status_code=400, detail=f"goal_id={data.goal_id} no existe en catálogo de metas")

    if data.physic_activity_id is not None:
        if not db.query(PhysicActivity).filter(PhysicActivity.id == data.physic_activity_id).first():
            raise HTTPException(status_code=400, detail=f"physic_activity_id={data.physic_activity_id} no existe en catálogo de actividades")

    saved_consultation = create_consultation(
        db=db,
        user_id=current_user.id,
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        age=data.age,
        physic_activity_id=data.physic_activity_id,
        goal_id=data.goal_id,
        imc_calculated=result["imc_calculated"],
        recommended_water_ml=result["recommended_water_ml"],
        diagnostic_id=result["diagnostic"].id,
        recommendations=result["recommendations"],
    )

    return success_response(
        data=ConsultationOut.model_validate(saved_consultation).model_dump(mode="json"),
        message="Consulta nutricional creada exitosamente",
        code=status.HTTP_201_CREATED,
    )


@router.get("")
def obtener_mi_historial(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    history = get_history_by_user(db, current_user.id)
    return success_response(
        data=[ConsultationOut.model_validate(c).model_dump(mode="json") for c in history],
        message="Historial obtenido correctamente",
    )
