from typing import Optional, List

from pydantic import BaseModel

from schemas.image_schema import ImageSchema


class ProductCreateSchema(BaseModel):
    name: str
    price: float
    description: str
    category_id: int


class ProductBase(BaseModel):
    name: str
    price: float
    description: str


class ProductSchema(ProductBase):
    id: int
    category_id: int
    images: Optional[List[ImageSchema]]

    class Config:
        orm_mode = True
