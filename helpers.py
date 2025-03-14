from functools import wraps

from fastapi import HTTPException
from sqlalchemy.orm import Session
import jwt
import datetime
from datetime import timedelta
import hashlib

from starlette.requests import Request

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from models import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return db.query(User).filter(User.email == email).first()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        token = request.headers.get("Authorization").replace("Bearer ", "")
        db = kwargs.get("db")
        user = verify_token(token, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        request.state.user = user
        return func(*args, **kwargs)

    return wrapper

