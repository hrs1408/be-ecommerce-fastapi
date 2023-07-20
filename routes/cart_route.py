from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from models import Cart, User, CartItem
from repositories.cart_repository import CartRepository, CartItemRepository
from repositories.user_repository import UserRepository
from schemas.cart_item_schema import CartItemSchema
from schemas.cart_schema import CartSchema, PutProductToCartSchema, CartItemUpdateQuantitySchema
from schemas.schema import ResponseSchema
from ultis.security import get_current_user

cart = APIRouter(prefix="/carts", tags=["Cart"])


@cart.get("/", response_model=ResponseSchema[CartSchema])
def get_cart_by_user_id(sub: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).id
    cart_exits = CartRepository.find_by_user_id(db, user_id)
    if not cart_exits:
        new_cart = Cart(
            user_id=user_id,
        )
        cart_ct = CartRepository.insert(db, new_cart)
        return ResponseSchema.from_api_route(status_code=200, data=cart_ct).dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=cart_exits).dict(exclude_none=True)


@cart.post("/", response_model=ResponseSchema[CartItemSchema])
def insert_product_to_cart(data_in: PutProductToCartSchema, sub: int = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).id
    if not user_id:
        return ResponseSchema.from_api_route(status_code=404, data="User not found").dict(exclude_none=True)
    cart_exits = CartRepository.find_by_user_id(db, user_id)
    if not cart_exits:
        new_cart = Cart(
            user_id=user_id,
        )
        cart_ct = CartRepository.insert(db, new_cart)
        cart_item = CartItem(
            cart_id=cart_ct.id,
            product_id=data_in.product_id,
            quantity=data_in.quantity
        )
        CartItemRepository.insert(db, cart_item)
        return ResponseSchema.from_api_route(status_code=200, data=new_cart).dict(exclude_none=True)
    cart_item = CartItem(
        cart_id=cart_exits.id,
        product_id=data_in.product_id,
        quantity=data_in.quantity
    )
    response = CartItemRepository.insert(db, cart_item)
    CartRepository.update(db, cart_exits)
    return ResponseSchema.from_api_route(status_code=200, data=response).dict(exclude_none=True)


@cart.delete("/{cart_item_id}", response_model=ResponseSchema)
def delete_cart_item(cart_item_id: int, sub: int = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).id
    cart = CartRepository.find_by_user_id(db, user_id)
    if not cart:
        return ResponseSchema.from_api_route(status_code=404, data="Cart not found").dict(exclude_none=True)
    cart_item = CartItemRepository.find_by_id(db, CartItem, cart_item_id)
    if not cart_item:
        return ResponseSchema.from_api_route(status_code=404, data="Cart item not found").dict(exclude_none=True)
    CartItemRepository.delete(db, cart_item)
    return ResponseSchema.from_api_route(status_code=200, data="Delete successfully").dict(exclude_none=True)


@cart.put("/{cart_item_id}", response_model=ResponseSchema[CartItemSchema])
def update_cart_item(cart_item_id: int, data: CartItemUpdateQuantitySchema, sub: int = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    user_id = UserRepository.find_by_id(db, User, sub).id
    cart = CartRepository.find_by_user_id(db, user_id)
    if not cart:
        return ResponseSchema.from_api_route(status_code=404, data="Cart not found").dict(exclude_none=True)
    cart_item = CartItemRepository.find_by_id(db, CartItem, cart_item_id)
    if not cart_item:
        return ResponseSchema.from_api_route(status_code=404, data="Cart item not found").dict(exclude_none=True)
    cart_item.quantity = data.quantity
    CartItemRepository.update(db, cart_item)
    return ResponseSchema.from_api_route(status_code=200, data=cart_item).dict(exclude_none=True)
