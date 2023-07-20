from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from config import get_db
from models import User, UserInformation
from repositories.jwt_repository import JWTRepository, JWTBearer
from repositories.user_repository import UserRepository, UserInformationRepository
from schemas.auth_schema import TokenResponse, LoginRequest
from schemas.schema import ResponseSchema
from schemas.user_schema import UserCreateSchema, UserSchema
from ultis.security import get_current_user

auth = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth.post("/register", response_model=ResponseSchema[TokenResponse])
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    is_email_already_exist = UserRepository.find_by_email(db, user.email)
    if is_email_already_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
    )
    new_user = UserRepository.insert(db, new_user)
    user_info = UserInformation(
        user_id=new_user.id,
        full_name=user.full_name,
    )
    UserInformationRepository.insert(db, user_info)
    token_response = JWTRepository.update_refresh_token(db, new_user)
    return ResponseSchema.from_api_route(data=token_response, status_code=status.HTTP_201_CREATED).dict(
        exclude_none=True)


@auth.post("/login", response_model=ResponseSchema[TokenResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = UserRepository.find_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token_response = JWTRepository.update_refresh_token(db, user)
    return ResponseSchema.from_api_route(data=token_response, status_code=status.HTTP_200_OK).dict(
        exclude_none=True)


@auth.get("/me", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[UserSchema])
def me(sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UserRepository.find_by_id(db, User, sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ResponseSchema.from_api_route(data=user, status_code=status.HTTP_200_OK).dict(
        exclude_none=True
    )


@auth.get("/refresh-token", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[TokenResponse])
def refresh_token(sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UserRepository.find_by_id(db, User, sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_response = JWTRepository.update_refresh_token(db, user)
    return ResponseSchema.from_api_route(data=token_response, status_code=status.HTTP_200_OK).dict(
        exclude_none=True
    )

