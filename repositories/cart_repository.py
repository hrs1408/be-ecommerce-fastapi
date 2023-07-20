from sqlalchemy.orm import Session

from models import Cart
from repositories.base_repository import BaseRepository


class CartRepository(BaseRepository):
    @staticmethod
    def find_by_user_id(db: Session, user_id):
        return db.query(Cart).filter(Cart.user_id == user_id).first()


class CartItemRepository(BaseRepository):
    @staticmethod
    def find_by_cart_id(db: Session, cart_id):
        return db.query(Cart).filter(Cart.cart_id == cart_id).first()
