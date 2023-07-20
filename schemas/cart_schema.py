from typing import Optional, List

from pydantic import BaseModel

from schemas.cart_item_schema import CartItemSchema


class CartCreateSchema(BaseModel):
    user_id: int


class PutProductToCartSchema(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdateQuantitySchema(BaseModel):
    quantity: int

class CartSchemaBase(BaseModel):
    user_id: int


class CartSchema(CartSchemaBase):
    id: int
    cart_items: Optional[List[CartItemSchema]]

    class Config:
        orm_mode = True
