from pwdlib import PasswordHash
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone



load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= "HS256"

py= PasswordHash.recommended()

def hash_password(password):
    return py.hash(password)

def verify_password(plain, hashed):
    return py.verify(plain, hashed)

def create_token(user_id):
    data={
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc)+ timedelta(minutes=30)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

