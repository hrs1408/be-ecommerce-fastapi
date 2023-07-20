from sqlalchemy.orm import Session

from models import Product
from repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    @staticmethod
    def find_by_name(db: Session, name):
        return db.query(Product).filter(Product.name == name).first()

    @staticmethod
    def find_by_category_id(db: Session, category_id):
        return db.query(Product).filter(Product.category_id == category_id).all()
