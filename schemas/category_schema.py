from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, root_validator

from schemas.product_schema import ProductSchema


class CategoryCreateSchema(BaseModel):
    name: str
    description: Optional[str]

    @root_validator()
    def validate_name(cls, values):
        name = values.get('name')
        if name is None or (len(name) == 0) or (name == ''):
            raise HTTPException(status_code=400, detail="Name is required")
        return values


class CategorySchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    products: Optional[List[ProductSchema]]

    class Config:
        orm_mode = True
