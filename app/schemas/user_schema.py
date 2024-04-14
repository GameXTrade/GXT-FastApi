from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="Name field is required")
    email: str = Field(..., description="Email field is required")
    image: Optional[str] = Field(None, description="Optional image field")

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