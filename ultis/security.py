from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from config import ALGORITHM, SECRET_KEY
from repositories.jwt_repository import JWTBearer


async def get_current_user(token: str = Depends(JWTBearer())) -> int:
    """
    Decode JWT token to get sub => return sub
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )

        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return int(payload.get('sub'))
