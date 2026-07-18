from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.exceptions import EmailRegistered, InvalidCredentials, InvalidRefreshToken
from app.db.sessions import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.auth import TokenPair, RefreshRequest
from app.respositories.user import get_by_email, create_user
from app.respositories.refresh_token import create_refresh_token, get_by_hash, revoke, is_valid
from app.core.security import hash_password, verify_password, create_access_token, generate_refresh_token, hash_refresh_token
from app.api.response import success_response

router = APIRouter(prefix="/auth", tags=["auth"])

def issue_token_pair(db: Session, user_id: int) -> TokenPair:
  access_token = create_access_token(user_id)

  refresh_token = generate_refresh_token()
  expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_expiration_days)

  create_refresh_token(
    db=db,
    user_id=user_id,
    token_hash=hash_refresh_token(refresh_token),
    expires_at=expires_at
  )

  return TokenPair(access_token=access_token, refresh_token=refresh_token)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
  existing_user = get_by_email(db, data.email)

  if existing_user is not None:
    raise EmailRegistered()

  password = hash_password(data.password)

  new_user = create_user(
    db=db,
    name=data.name,
    email=data.email,
    password=password,
    genre=data.genre
  )

  return success_response(
    data=UserOut.model_validate(new_user).model_dump(),
    message="Usuario registrado exitosamente",
    code=status.HTTP_201_CREATED,
  )

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
  user = get_by_email(db, data.email)

  if user is None:
    raise InvalidCredentials()

  valid_password = verify_password(data.password, user.password)

  if not valid_password:
    raise InvalidCredentials()

  tokens = issue_token_pair(db, user.id)
  return success_response(
    data=tokens.model_dump(),
    message="Inicio de sesión exitoso",
  )

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
  token_hash = hash_refresh_token(data.refresh_token)
  stored_token = get_by_hash(db, token_hash)

  if not is_valid(stored_token):
    raise InvalidRefreshToken()
  
  revoke(db, stored_token)

  tokens = issue_token_pair(db, stored_token.user_id)
  return success_response(
    data=tokens.model_dump(),
    message="Token renovado exitosamente",
  )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
  token_hash = hash_refresh_token(data.refresh_token)
  stored_token = get_by_hash(db, token_hash)

  if stored_token is not None:
    revoke(db, stored_token)
