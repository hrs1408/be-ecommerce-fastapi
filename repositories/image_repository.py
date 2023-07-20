from sqlalchemy.orm import Session

from models import Image
from repositories.base_repository import BaseRepository


class ImageRepository(BaseRepository):
    @staticmethod
    def find_by_product_id(db: Session, product_id):
        return db.query(Image).filter(Image.product_id == product_id).all()

    @staticmethod
    def insert_list(db: Session, images):
        db.add_all(images)
        db.commit()
        db.refresh(images)
        return images
