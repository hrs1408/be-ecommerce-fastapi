from fastapi import Depends, APIRouter

from repositories.jwt_repository import JWTBearer

testRoute = APIRouter(
    tags=["Test Route"],
    dependencies=[Depends(JWTBearer())],
    prefix="/testRoute"
)


@testRoute.get("/testRoute")
def test():
    return {"message": "Hello World"}
