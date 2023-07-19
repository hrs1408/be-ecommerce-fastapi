import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from models import User
from repositories.user_repository import UserRepository
from schemas.auth_schema import AccessToken, RefreshToken, TokenResponse


class JWTRepository:
    @staticmethod
    def create_access_token(user: User, data: Optional[dict] = None,
                            expires_delta: Optional[timedelta] = None):
        to_encode = data.copy() if data else {}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        to_encode.update({"sub": user.id})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return AccessToken(access_token=encode_jwt, access_token_expires=expire, token_type="bearer")

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return RefreshToken(refresh_token=encoded_jwt, refresh_token_expires=expire)

    @staticmethod
    def decode_access_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_time = datetime.utcnow()
            return decode_token if datetime.utcfromtimestamp(decode_token["exp"]) >= current_time else None
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid access token")

    @staticmethod
    def decode_refresh_token(token: str):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_time = datetime.utcnow()
            return decoded_token if datetime.utcfromtimestamp(decoded_token["exp"]) >= current_time else None
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def update_refresh_token(db: Session, user: User):
        access_token = JWTRepository.create_access_token(user)
        refresh_token_sub = str(uuid.uuid4())
        refresh_token = JWTRepository.create_refresh_token({'sub': refresh_token_sub})

        user.refresh_token_sub = refresh_token_sub
        UserRepository.update(db, user)

        return TokenResponse(
            token_type="bearer",
            access_token=access_token.access_token,
            access_token_expires=access_token.access_token_expires,
            refresh_token=refresh_token.refresh_token,
            refresh_token_expires=refresh_token.refresh_token_expires
        )


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication schema.")
            if self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str):
        is_token_valid: bool = False
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithm=[ALGORITHM])
        except:
            payload = None

        if payload:
            is_token_valid = True
        return is_token_valid
