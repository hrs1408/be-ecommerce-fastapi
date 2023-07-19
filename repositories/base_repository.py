from typing import TypeVar, Generic

from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository():
    @staticmethod
    def find_all(db: Session, model: Generic[T]):
        return db.query(model).all()

    @staticmethod
    def find_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).first()

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()
