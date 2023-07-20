import os
from typing import List

from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.orm import Session

from config import get_db
from models import Image
from repositories.image_repository import ImageRepository
from schemas.image_schema import ImageSchema
from schemas.schema import ResponseSchema

media = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@media.post("/upload/{product_id}", response_model=ResponseSchema[ImageSchema])
def upload_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_name = file.filename
    with open(os.path.join("medias", file_name), "wb") as buffer:
        buffer.write(file.file.read())
    image = Image(
        file_name=file_name,
        file_path=os.path.join("http://127.0.0.1:8000", "medias", file_name),
        product_id=product_id,
    )
    new_image = ImageRepository.insert(db, image)
    return ResponseSchema.from_api_route(status_code=200, data=new_image).dict(exclude_none=True)


@media.post("/upload/{product_id}/list", response_model=ResponseSchema[List[ImageSchema]])
def upload_image_list(product_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    images = []
    for file in files:
        file_name = file.filename
        with open(os.path.join("medias", file_name), "wb") as buffer:
            buffer.write(file.file.read())
        image = Image(
            file_name=file_name,
            file_path=os.path.join("http://127.0.0.1:8000", "medias", file_name),
            product_id=product_id,
        )
        images.append(image)
        ImageRepository.insert(db, image)
    return ResponseSchema.from_api_route(status_code=200, data=images).dict(exclude_none=True)
