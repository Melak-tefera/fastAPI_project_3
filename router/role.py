from database import get_db
from models import User
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas import Rolechange
from auth import require_admin

router = APIRouter(tags=["role"])

@router.get("/admin/users")
def list_users(db: Session=Depends(get_db), admin: User= Depends(require_admin)):
    users = db.query(User).filter(User.role=="user").order_by(User.id).all()
    return [{"id": u.id, "name": u.name, "role": u.role } for u in users] 


@router.put("/admin/users/{user_id}/role")
def change_role(user_id:int, data:Rolechange, db: Session=Depends(get_db), admin: User=Depends(require_admin)):
    user= db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == admin.id:
        raise HTTPException(400, "You cannot change your own role")
    user.role = data.role
    db.commit()
    return {"id": user.id, "name": user.name, "role": user.role}
    
    