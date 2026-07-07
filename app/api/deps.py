from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.exceptions import UserNotFound
from app.db.sessions import get_db
from app.core.security import decode_token
from app.respositories.user import get_by_id

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido o expirado")

    user_id_str = payload.get("sub")

    if user_id_str is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    user = get_by_id(db, int(user_id_str))

    if user is None:
      raise UserNotFound()

    return user
