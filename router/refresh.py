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
    parsed = rea
        