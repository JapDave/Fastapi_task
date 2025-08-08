from fastapi import Depends,HTTPException,Header
from .database import get_db, get_user_by_token
from sqlalchemy.orm import Session

def authenticate_token(token: str = Header(None),  db: Session = Depends(get_db)):
    user = get_user_by_token(token, db)
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user.id

# def get_current_user(token: str = Depends(authenticate_token)):
#     user = get_user_by_token(token)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return user.id