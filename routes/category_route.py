from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from models import Category
from repositories.jwt_repository import JWTBearer
from schemas.category_schema import CategorySchema, CategoryCreateSchema
from schemas.schema import ResponseSchema
from repositories.category_repository import CategoryRepository

category = APIRouter(prefix="/categories", tags=["Category"])


@category.get("/", response_model=ResponseSchema[List[CategorySchema]])
def get_all_categories(db: Session = Depends(get_db)):
    categories = CategoryRepository.find_all(db, Category)
    return ResponseSchema.from_api_route(status_code=200, data=categories).dict(exclude_none=True)


@category.post("/", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[CategorySchema])
def create_category(category_create: CategoryCreateSchema, db: Session = Depends(get_db)):
    category_ct = Category(
        name=category_create.name,
        description=category_create.description
    )
    new_category = CategoryRepository.insert(db, category_ct)
    return ResponseSchema.from_api_route(status_code=200, data=new_category).dict(exclude_none=True)


@category.put("/{category_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[CategorySchema])
def update_category(category_id: int, category_update: CategoryCreateSchema, db: Session = Depends(get_db)):
    category_ed = CategoryRepository.find_by_id(db, Category, category_id)
    if not category_ed:
        return ResponseSchema.from_api_route(status_code=404, message="Category not found").dict(exclude_none=True)
    category_ed.name = category_update.name
    category_ed.description = category_update.description
    category_ed = CategoryRepository.update(db, category_ed)
    return ResponseSchema.from_api_route(status_code=200, data=category_ed).dict(exclude_none=True)


@category.delete("/{category_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[CategorySchema])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_ed = CategoryRepository.find_by_id(db, Category, category_id)
    if not category_ed:
        return ResponseSchema.from_api_route(status_code=404, message="Category not found").dict(exclude_none=True)
    category_ed = CategoryRepository.delete(db, category_ed)
    return ResponseSchema.from_api_route(status_code=200, data=category_ed).dict(exclude_none=True)
