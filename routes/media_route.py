import os
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.orm import Session, sessionmaker

from config import get_db
from models import Image, FileData
from repositories.file_repository import FileRepository
from repositories.image_repository import ImageRepository
from schemas.image_schema import ImageSchema, ImageCreateSchema
from schemas.schema import ResponseSchema

media = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@media.post("/upload/{product_id}", response_model=ResponseSchema[ImageSchema])
def upload_file(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_data = FileData(
        file_name=file.filename,
        file_path=os.path.join(os.getcwd(), "uploads", file.filename),
        content_type=file.content_type,
        file=file.file.read()
    )
    file_data_ct = FileRepository.insert(db, file_data)
    image_ct = Image(
        product_id=product_id,
        file_name=file_data_ct.id,
        file_path=file_data_ct.file_path,
    )
    new_image = ImageRepository.insert(db, image_ct)
    return ResponseSchema.from_api_route(status_code=200, data=new_image).dict(exclude_none=True)