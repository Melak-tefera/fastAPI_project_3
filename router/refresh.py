from fastapi import APIRouter, Depends, HTTPException,Request, Response,status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import User, RefreshToken
from auth import issue_refresh_token, revoke_all, get_current_user, set_refresh_cookie, clear_refresh_cookie
from security import verify_password, create_access_token, create_refresh_token, read_refresh_token, read_token

router = APIRouter(tags=["Refresh"])

@router.post("/refresh")
def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token cookie",
        )

    try:
        payload = read_refresh_token(token)
    except jwt.ExpiredSignatureError:
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except jwt.InvalidTokenError:
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    user_id = payload.get("sub")
    if not  user_id:
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has no subject",
        )
        

    access_token = create_access_token(
        user_id
    )

    # Optional but recommended: rotate the refresh token
    new_refresh_token, new_jti, new_expires = create_refresh_token(
        user_id
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,      # True in production
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24 * 7,
    )

    return {"access_token": access_token, "token_type": "bearer"}
    

@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("refresh_token")

    if not token:
        response.delete_cookie("refresh_token", path="/")
        return {"message": "Already logged out"}

    try:
        parsed = read_refresh_token(token)
    except jwt.ExpiredSignatureError:
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except jwt.InvalidTokenError:
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Revoke the refresh token/session here
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Logged out"}

@router.post("/logout-all")
def logout_all(response: Response,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    revoke_all(db, current_user.id)
    clear_refresh_cookie(response)
    return {"message": "Logged out everywhere"}
