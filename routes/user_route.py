from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from models import User
from repositories.user_repository import UserRepository
from schemas.schema import ResponseSchema
from schemas.user_schema import UserSchema

user = APIRouter(prefix="/users", tags=["users"])


@user.get("/", response_model=ResponseSchema[List[UserSchema]])
def get_all_users(db: Session = Depends(get_db)):
    users = UserRepository.find_all(db, User)
    return ResponseSchema.from_api_route(status_code=200, data=users).dict(exclude_none=True)
