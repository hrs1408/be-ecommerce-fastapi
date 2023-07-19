from typing import Dict, Optional, TypeVar, Generic, Any

from fastapi_pagination.bases import AbstractParams, RawParams
from fastapi_responseschema import AbstractResponseSchema, SchemaAPIRoute
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


# Build your "Response Schema"
class ResponseMetadata(BaseModel):
    error: Optional[bool]
    message: Optional[str]


class ResponseSchema(AbstractResponseSchema[T], Generic[T]):
    data: T
    meta: Optional[ResponseMetadata]
    status_code: int

    @classmethod
    def from_exception(cls, reason, status_code, message: str = "Error", **others):
        return cls(
            data=reason,
            status_code=status_code,
            meta=ResponseMetadata(error=status_code >= 400, message=message)
        )

    @classmethod
    def from_api_route(
            cls, data: Any, status_code: int, description: Optional[str] = None, **others
    ):
        return cls(
            data=data,
            status_code=status_code,
            meta=ResponseMetadata(error=status_code >= 400, message=description)
        )


# Create an APIRoute
class Route(SchemaAPIRoute):
    response_schema = ResponseSchema


class Params(BaseModel, AbstractParams):
    size: Optional[int] = 10
    page: Optional[int] = 1
    is_full: bool = False
    search: Optional[str]

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * self.page,
        )
