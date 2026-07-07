from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.util import deprecated

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(password_plain: str, password_hash: str) -> bool:
  return pwd_context.verify(password_plain, password_hash)

def create_access_token(user_id: int) -> str:
  expiration = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
  token_data = {"sub": str(user_id), "exp": expiration}
  token = jwt.encode(token_data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
  return token

def decode_token(token: str):
  try:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    return payload
  except JWTError:
    return None
