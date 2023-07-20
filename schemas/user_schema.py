from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, root_validator


class UserCreateSchema(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    confirm_password: str

    @root_validator()
    def validate_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if (password != confirm_password):
            raise HTTPException(status_code=400, detail="Password and confirm password not match")
        if password is None or (password.length == 0) or (password == ''):
            raise HTTPException(status_code=400, detail="Password is required")
        if password and len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        return values


class UserInformationBase(BaseModel):
    full_name: str
    phone_number: Optional[str]
    address: Optional[str]
    dob: Optional[str]


class UserInformationSchema(UserInformationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    user_role: str
    is_active: bool
    user_information: Optional[UserInformationSchema]

    class Config:
        orm_mode = True
