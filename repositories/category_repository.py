from models import Category
from repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    @staticmethod
    def find_by_name(db, name):
        return db.query(Category).filter(Category.name == name).first()
