from functools import wraps
from fastapi import HTTPException
from starlette.requests import Request
from services import AuthSvc


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_svc = AuthSvc()
        request: Request = kwargs.get("request")
        token = request.headers.get("Authorization").replace("Bearer ", "")
        db = kwargs.get("db")
        user = auth_svc.verify_token(token, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        request.state.user = user
        return func(*args, **kwargs)

    return wrapper

