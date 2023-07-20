from typing import List

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import get_db
from models import User, UserInformation
from repositories.jwt_repository import JWTBearer
from repositories.user_repository import UserRepository, UserInformationRepository
from schemas.schema import ResponseSchema
from schemas.user_schema import UserSchema, UserAdminCreateSchema

user = APIRouter(prefix="/users", tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user.get("/", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[List[UserSchema]])
def get_all_users(db: Session = Depends(get_db)):
    users = UserRepository.find_all(db, User)
    return ResponseSchema.from_api_route(status_code=200, data=users).dict(exclude_none=True)


@user.get("/{user_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_find = UserRepository.find_by_id(db, User, user_id)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=user_find).dict(exclude_none=True)


@user.get("/role/{role}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[List[UserSchema]])
def get_user_by_role(role: str, db: Session = Depends(get_db)):
    users = UserRepository.find_by_role(db, role)
    if not users:
        return ResponseSchema.from_api_route(status_code=404, message="Users not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=users).dict(exclude_none=True)


@user.get("/email/{email}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user_find = UserRepository.find_by_email(db, email)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=user_find).dict(exclude_none=True)


@user.post("/", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def create_user(user_create: UserAdminCreateSchema, db: Session = Depends(get_db)):
    user_ct = User(
        email=user_create.email,
        hashed_password=pwd_context.hash(user_create.password),
        user_role=user_create.user_role
    )
    new_user = UserRepository.insert(db, user_ct)
    user_info = UserInformation(
        user_id=new_user.id,
        full_name=user_create.full_name,
    )
    UserInformationRepository.insert(db, user_info)
    return ResponseSchema.from_api_route(status_code=200, data=new_user).dict(exclude_none=True)


@user.put("/{user_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def update_user(user_id: int, user_update: UserAdminCreateSchema, db: Session = Depends(get_db)):
    user_find = UserRepository.find_by_id(db, User, user_id)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    user_find.email = user_update.email
    user_find.hashed_password = pwd_context.hash(user_update.password)
    user_find.user_role = user_update.user_role
    user_info = UserInformationRepository.find_by_user_id(db, user_id)
    user_info.full_name = user_update.full_name
    user_ed = UserRepository.update(db, user_find)
    return ResponseSchema.from_api_route(status_code=200, data=user_ed).dict(exclude_none=True)


@user.put("/password/{user_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def update_user_password(user_id: int, user_update: UserAdminCreateSchema, db: Session = Depends(get_db)):
    user_find = UserRepository.find_by_id(db, User, user_id)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    user_find.hashed_password = pwd_context.hash(user_update.password)
    user_ed = UserRepository.update(db, user_find)
    return ResponseSchema.from_api_route(status_code=200, data=user_ed).dict(exclude_none=True)


@user.put("/active/{user_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def update_status_active(user_id: int, db: Session = Depends(get_db)):
    user_find = UserRepository.find_by_id(db, User, user_id)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    user_find.is_active = not user_find.is_active
    user_ed = UserRepository.update(db, user_find)
    return ResponseSchema.from_api_route(status_code=200, data=user_ed).dict(exclude_none=True)


@user.delete("/{user_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if user_id == 1:
        return ResponseSchema.from_api_route(status_code=403, message="User not allowed to delete").dict(
            exclude_none=True)
    user_find = UserRepository.find_by_id(db, User, user_id)
    if not user_find:
        return ResponseSchema.from_api_route(status_code=404, message="User not found").dict(exclude_none=True)
    user_info = UserInformationRepository.find_by_user_id(db, user_id)
    UserRepository.delete(db, user_find)
    UserInformationRepository.delete(db, user_info)
    return ResponseSchema.from_api_route(status_code=200, data=user_find).dict(exclude_none=True)
