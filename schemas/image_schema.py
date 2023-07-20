from pydantic import BaseModel


class ImageCreateSchema(BaseModel):
    file_path: str
    file_name: str
    product_id: int


class ImageBase(BaseModel):
    file_path: str
    file_name: str


class ImageSchema(ImageBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True
