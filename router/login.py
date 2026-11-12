from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User

from security import verify_password, create_access_token, create_refresh_token, read_token

router = APIRouter(tags=["Login"])

@router.post("/login")
def login(form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    
    user=db.query(User).filter(User.username==form.username).first()
    if not user or  verify_password(form.password ,user.hashed_password):
        raise HTTPException(401, "Wrong name or password")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
        }

