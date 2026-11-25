from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User, RefreshToken
from auth import issue_refresh_token, revoke_all, get_current_user
from schemas import RefreshRequest
from security import verify_password, create_access_token, create_refresh_token, read_refresh_token, read_token

router = APIRouter(tags=["Refresh"])

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session=Depends(get_db)):
    parsed = read_refresh_token(data.refresh_token)
    if parsed is None:
        raise HTTPException(401, "invalid or expired refresh token")
    user_id, jti= parsed
    saved = db.query(RefreshToken).filter(RefreshToken.jti==jti).first()
    if saved is None:
        raise HTTPException(401, "Invalid or expired refresh token")
    
    if saved.revoked:
    # An already-used token came back: somebody has a copy.
    # Cancel every refresh token this user has.
        revoke_all(db, user_id)
        raise HTTPException(401, "Refresh token was already used. Please log in again.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(401, "user no longer exists")
    saved.revoked=True
    new_refresh = issue_refresh_token(db, user.id)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": new_refresh,
        "token_type": "bearer",
        }
    
@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    parsed = read_refresh_token(data.refresh_token)
    if parsed is not None:
        saved = db.scalar(select(RefreshToken).where(RefreshToken.jti == parsed[1]))
    if saved:
        saved.revoked = True
    db.commit()
    return {"message": "Logged out"}
@router.post("/logout-all")
def logout_all(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    revoke_all(db, current_user.id)
    return {"message": "Logged out everywhere"}

