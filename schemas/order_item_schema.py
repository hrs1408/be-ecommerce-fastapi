from pydantic import BaseModel


class OrderItemSchemaBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemSchema(OrderItemSchemaBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True
