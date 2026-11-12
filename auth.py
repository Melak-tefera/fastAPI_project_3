import jwt
from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from security import SECRET_KEY, ALGORITHM

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    try:
        data= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(data["sub"])
    except:
        raise HTTPException(401, "Bad or expired token")
    user= db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(401, "User no longer exists")
    return user