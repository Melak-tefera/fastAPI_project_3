
from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from models import User, RefreshToken
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from security import read_token , create_refresh_token, read_refresh_token

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

def issue_refresh_token(db:Session, user_id:int):
    token, jti, expires= create_refresh_token(user_id)
    db.add(RefreshToken(jti=jti, user_id=user_id, expires=expires))
    db.commit()
    return token

def revoke_all(db: Session, user_id: int):
    db.execute(update(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .values(revoked=True))
    db.commit()
