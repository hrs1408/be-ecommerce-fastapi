from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from models import User, OrderItem, Order
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository, OrderItemRepository
from repositories.user_repository import UserRepository
from schemas.order_schema import OrderSchema
from schemas.schema import ResponseSchema
from ultis.security import get_current_user

order = APIRouter(prefix="/orders", tags=["Order"])


@order.get("/", response_model=ResponseSchema[List[OrderSchema]])
def get_order_by_user(sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).user_id
    orders = OrderRepository.find_by_user_id(db, user_id)
    if not orders:
        return ResponseSchema.from_api_route(status_code=404, message="Order not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=orders).dict(exclude_none=True)


@order.get("/{order_id}", response_model=ResponseSchema[OrderSchema])
def get_order_by_id(order_id: int, sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).user_id
    order = OrderRepository.find_by_id(db, order_id)
    if not order:
        return ResponseSchema.from_api_route(status_code=404, message="Order not found").dict(exclude_none=True)
    if order.user_id != user_id:
        return ResponseSchema.from_api_route(status_code=403, message="Permission denied").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=order).dict(exclude_none=True)


@order.post("/", response_model=ResponseSchema[OrderSchema])
def create_order(sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    total = 0
    user_id = UserRepository.find_by_id(db, User, sub).user_id
    order = Order(
        user_id=user_id,
        total=0,
        status="pending",
    )
    order_ct = OrderRepository.insert(db, order)
    cart_user = CartRepository.find_by_user_id(db, user_id)
    if not cart_user:
        return ResponseSchema.from_api_route(status_code=404, message="Cart not found").dict(exclude_none=True)
    cart_items = cart_user.cart_items
    for cart_item in cart_items:
        item = OrderItem(
            order_id=order_ct.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )
        total += cart_item.product.price * cart_item.quantity
        OrderItemRepository.insert(db, item)
    order_ct.total = total
    OrderRepository.update(db, order_ct)
    return ResponseSchema.from_api_route(status_code=200, data=order).dict(exclude_none=True)


@order.delete("/{order_id}", response_model=ResponseSchema[OrderSchema])
def delete_order(order_id: int, sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).user_id
    order = OrderRepository.find_by_id(db, order_id)
    if not order:
        return ResponseSchema.from_api_route(status_code=404, message="Order not found").dict(exclude_none=True)
    if order.user_id != user_id:
        return ResponseSchema.from_api_route(status_code=403, message="Permission denied").dict(exclude_none=True)
    OrderRepository.delete(db, order_id)
    return ResponseSchema.from_api_route(status_code=200, message="Delete order successfully").dict(exclude_none=True)


@order.put("/{order_id}", response_model=ResponseSchema[OrderSchema])
def update_status_order(order_id: int, status: str, sub: int = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).user_id
    order = OrderRepository.find_by_id(db, order_id)
    if not order:
        return ResponseSchema.from_api_route(status_code=404, message="Order not found").dict(exclude_none=True)
    if order.user_id != user_id:
        return ResponseSchema.from_api_route(status_code=403, message="Permission denied").dict(exclude_none=True)
    order.status = status
    OrderRepository.update(db, order)
    return ResponseSchema.from_api_route(status_code=200, data=order).dict(exclude_none=True)
