from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    image: str = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    ...

class User(UserBase):
    id: int
    is_verified: bool = False
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str
    image: Optional[str]
    is_verified: bool = False

    class Config:
        from_attributes = True