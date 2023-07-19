from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=8, max_length=32)


class TokenResponse(BaseModel):
    token_type: str
    access_token: str
    access_token_expires: datetime
    refresh_token: str
    refresh_token_expires: datetime


class AccessToken(BaseModel):
    token_type: str
    access_token: str
    access_token_expires: datetime


class RefreshToken(BaseModel):
    refresh_token: str
    refresh_token_expires: datetime
    sub: Optional[str]


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    sub: Optional[str]
