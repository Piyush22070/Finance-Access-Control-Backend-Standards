from enum import Enum
from pydantic import BaseModel, EmailStr,Field, ConfigDict


class RoleEnum(str, Enum):
    Viewer = "viewer"
    Analyst = "analyst"
    Admin = "admin"


class UserBase(BaseModel):
    email : EmailStr
    role : RoleEnum 
    is_active : bool = True

class UserCreate(UserBase):
    password : str = Field(...,min_length=6)

class UserResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True) 