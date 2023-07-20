from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from models import Product
from repositories.jwt_repository import JWTBearer
from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductSchema, ProductCreateSchema
from schemas.schema import ResponseSchema

product = APIRouter(prefix="/products", tags=["Products"])


@product.get("/", response_model=ResponseSchema[List[ProductSchema]])
def get_all_products(db: Session = Depends(get_db)):
    products = ProductRepository.find_all(db, Product)
    if not products:
        return ResponseSchema.from_api_route(status_code=404, message="Products not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=products).dict(exclude_none=True)


@product.get("/{product_id}", response_model=ResponseSchema[ProductSchema])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product_find = ProductRepository.find_by_id(db, Product, product_id)
    if not product_find:
        return ResponseSchema.from_api_route(status_code=404, message="Product not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=product_find).dict(exclude_none=True)


@product.get("/{product_name}", response_model=ResponseSchema[ProductSchema])
def get_product_by_name(product_name: str, db: Session = Depends(get_db)):
    product_find = ProductRepository.find_by_name(db, product_name)
    if not product_find:
        return ResponseSchema.from_api_route(status_code=404, message="Product not found").dict(exclude_none=True)
    return ResponseSchema.from_api_route(status_code=200, data=product_find).dict(exclude_none=True)


@product.post("/", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[ProductSchema])
def create_product(product_create: ProductCreateSchema, db: Session = Depends(get_db)):
    product_ct = Product(
        name=product_create.name,
        description=product_create.description,
        price=product_create.price,
        category_id=product_create.category_id
    )
    new_product = ProductRepository.insert(db, product_ct)
    return ResponseSchema.from_api_route(status_code=200, data=new_product).dict(exclude_none=True)


@product.put("/{product_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[ProductSchema])
def update_product(product_id: int, product_update: ProductCreateSchema, db: Session = Depends(get_db)):
    product_ed = ProductRepository.find_by_id(db, Product, product_id)
    if not product_ed:
        return ResponseSchema.from_api_route(status_code=404, message="Product not found").dict(exclude_none=True)
    product_ed.name = product_update.name
    product_ed.description = product_update.description
    product_ed.price = product_update.price
    product_ed.category_id = product_update.category_id
    product_ed = ProductRepository.update(db, product_ed)
    return ResponseSchema.from_api_route(status_code=200, data=product_ed).dict(exclude_none=True)


@product.delete("/{product_id}", dependencies=[Depends(JWTBearer())], response_model=ResponseSchema[ProductSchema])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_del = ProductRepository.find_by_id(db, Product, product_id)
    if not product_del:
        return ResponseSchema.from_api_route(status_code=404, message="Product not found").dict(exclude_none=True)
    product_del = ProductRepository.delete(db, product_del)
    return ResponseSchema.from_api_route(status_code=200, data=product_del).dict(exclude_none=True)
