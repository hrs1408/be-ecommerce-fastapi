from typing import List, Optional

from pydantic import BaseModel

from schemas.product_schema import ProductSchema


class CategoryCreateSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str
    products: Optional[List[ProductSchema]]

    class Config:
        orm_mode = True
