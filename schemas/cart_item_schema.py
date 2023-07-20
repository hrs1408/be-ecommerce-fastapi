from typing import Optional

from pydantic import BaseModel

from schemas.product_schema import ProductSchema


class CartItemSchemaBase(BaseModel):
    product_id: int
    cart_id: int
    quantity: int


class CartItemSchema(CartItemSchemaBase):
    id: int
    product: Optional[ProductSchema]

    class Config:
        orm_mode = True
