from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, User
from schemas import Createpost, Readpost
from auth import get_current_user

router= APIRouter(tags=["Posts"])
@router.post("/posts", response_model=Readpost)
def create_post(data:Createpost, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    post= Post(tile=data.title, user_id= current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/posts", response_model=list[Readpost])
def my_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.user_id == current_user.id).first()
    return post