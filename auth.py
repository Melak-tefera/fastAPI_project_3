
from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from security import read_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    user_id = read_token(token=token, expected_type="access")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Bad or expired token")
    user= db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="user no longer exists")
    
    return user

def require_admin(current_user: User= Depends(get_current_user)):
    if current_user.role !="admin":
        raise HTTPException(status_code="403", detail="admins only")
    return current_user
