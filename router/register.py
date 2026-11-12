from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import Usercreate, Userread
from security import hash_password

router = APIRouter(tags=["Register"])
@router.post("/register", response_model= Userread)
def register(name:Usercreate, db: Session=Depends(get_db)):
    taken=db.query(User).filter(User.username==name.username).first()
    if taken:
        raise HTTPException(status_code=400, detail="username is taken")
    user=User(name=name.name, username= name.username, hashed_password=hash_password(name.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

