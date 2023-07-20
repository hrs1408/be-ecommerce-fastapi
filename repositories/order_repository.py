from sqlalchemy.orm import Session

from models import Order
from repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    @staticmethod
    def find_by_user_id(db: Session, user_id):
        return db.query(Order).filter(Order.user_id == user_id).first()


class OrderItemRepository(BaseRepository):
    @staticmethod
    def find_by_order_id(db: Session, order_id):
        return db.query(Order).filter(Order.order_id == order_id).first()
