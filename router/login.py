from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import delete
from database import get_db
from models import User, RefreshToken
from datetime import datetime, timezone
from security import verify_password, create_access_token, create_refresh_token, read_token
from auth import issue_refresh_token

router = APIRouter(tags=["Login"])

@router.post("/login")
def login(form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    
    user=db.query(User).filter(User.username==form.username).first()
    if not user or not verify_password(form.password ,user.hashed_password):
        raise HTTPException(401, "Wrong name or password")
    db.execute(delete(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc)))
    refresh_token= issue_refresh_token(db, user.id)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": refresh_token,
        "token_type": "bearer",
        }

