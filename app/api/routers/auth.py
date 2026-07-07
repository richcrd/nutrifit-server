from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.respositories.user import get_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db())):
  existing_user = get_by_email(db, data.email)

  if existing_user is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya esta registrado")

  password = hash_password(data.password)

  new_user = create_user(
    db=db,
    name=data.name,
    email=data.email,
    password=password,
    genre=data.genre
  )

  return new_user

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
  user = get_by_email(db, data.email)

  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

  valid_password = verify_password(data.password, user.password)

  if not valid_password:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

  token = create_access_token(user.id)

  return {"access_token": token, "token_type": "bearer"}
