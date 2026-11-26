from pwdlib import PasswordHash
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import uuid



load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= "HS256"
access_time=15
refresh_day=10
py= PasswordHash.recommended()

def hash_password(password):
    return py.hash(password)

def verify_password(plain, hashed):
    return py.verify(plain, hashed)

def make_token(user_id, tokent_type, lifetime):
    data={
        "sub": str(user_id),
        "type": tokent_type,
        "exp":datetime.now(timezone.utc)+lifetime
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id):
    return make_token(user_id, "access", timedelta(minutes=access_time))

def create_refresh_token(user_id):
    jti= uuid.uuid4().hex
    expires= datetime.now(timezone.utc)+timedelta(days=refresh_day)
    data= {"sub": str(user_id), "type": "refresh", "jti":jti, "exp":expires}
    token= jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expires

def read_refresh_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("Not a refresh token")

    return payload
    

def read_token(token, expected_type):
    try:
        data=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if data.get("type")!=expected_type:
            return None
        return int(data["sub"])
    except(jwt.PyJWTError, KeyError, ValueError):
        return None

