from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken

def create_refresh_token(db: Session, user_id: int, token_hash: str, expires_at: datetime):
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token

def get_by_hash(db: Session, token_hash: str):
    return db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

def revoke(db: Session, refresh_token: RefreshToken):
    refresh_token.revoked = True
    db.commit()

def is_valid(refresh_token: RefreshToken) -> bool:
    if refresh_token is None:
        return False
    if refresh_token.revoked:
        return False
    if refresh_token.expires_at < datetime.now(timezone.utc):
        return False
    return True
