from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import delete
from database import get_db
from models import User, RefreshToken
from datetime import datetime, timezone
from security import verify_password, create_access_token, create_refresh_token, read_token
from auth import issue_refresh_token, set_refresh_cookie
from ratelimit import rate_limit

router = APIRouter(tags=["Login"])
login_limit = rate_limit(5, 60)
@router.post("/login")
def login(response:Response,dependencies=[Depends(login_limit)],form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    
    user=db.query(User).filter(User.username==form.username).first()
    if not user or not verify_password(form.password ,user.hashed_password):
        raise HTTPException(401, "Wrong name or password")
    db.execute(delete(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc)))
    set_refresh_cookie(response, issue_refresh_token(db, user.id))
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        }

