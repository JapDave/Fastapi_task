from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .database import get_db, get_user_by_token


def authenticate_token(
    authorization: str | None = Header(default=None),
    token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    # Preserve the assessment token header while supporting Bearer auth.
    if authorization:
        scheme, _, credential = authorization.partition(" ")
        if scheme.lower() != "bearer" or not credential:
            raise HTTPException(status_code=401, detail="Invalid token")
        token = credential
    user = get_user_by_token(token, db) if token else None
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user.id
