from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.schemas.consultation import ConsultationCreate, ConsultationOut
from app.services.inference_engine import process_consultation
from app.respositories.consultation_repository import create_consultation, get_history_by_user

router = APIRouter(prefix="/consultations", tags=["consultations"])

@router.post("", response_model=ConsultationOut, status_code=status.HTTP_201_CREATED)
def crear_consulta_nutricional(
    data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user()),
):
    result = process_consultation(
        db=db,
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        age=data.age,
        genre=current_user.sexo,
    )

    if result["diagnostic"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se encontro un diagnostico para los datos proporcionados",
        )

    saved_consultation = create_consultation(
        db=db,
        user_id=current_user.id,
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        age=data.age,
        physic_activity_id=data.physic_activity_id,
        goal_id=data.goal_id,
        imc_calculated=result["imc_calculated"],
        recommended_water_ml=result["recommended_water_imc"],
        diagnostic_id=result["diagnostic"].id,
        recommendations=result["recommendations"],
    )

    return saved_consultation


@router.get("", response_model=list[ConsultationOut])
def obtener_mi_historial(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user()),
):
    return get_history_by_user(db, current_user.id)
