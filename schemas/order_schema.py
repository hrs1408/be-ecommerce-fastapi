from typing import List, Optional

from pydantic import BaseModel

from schemas.order_item_schema import OrderItemSchema


class OrderSchemaBase(BaseModel):
    user_id: int
    total: float
    status: str


class OrderSchema(OrderSchemaBase):
    id: int
    order_items: Optional[List[OrderItemSchema]]

    class Config:
        orm_mode = True
