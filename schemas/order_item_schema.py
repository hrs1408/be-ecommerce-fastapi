from pydantic import BaseModel


class OrderItemSchemaBase(BaseModel):
    product_id: int
    order_id: int
    quantity: int


class OrderItemSchema(OrderItemSchemaBase):
    id: int

    class Config:
        orm_mode = True
