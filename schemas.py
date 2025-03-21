from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class TokenData(BaseModel):
    email: EmailStr

class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=100000)
