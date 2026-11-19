from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import RefreshRequest
from security import verify_password, create_access_token, create_refresh_token, read_token

router = APIRouter(tags=["Refresh"])

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session=Depends(get_db)):
    user_id= read_token(data.refresh_token, "refresh")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    user=db.query(User).filter(User.id== user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
        