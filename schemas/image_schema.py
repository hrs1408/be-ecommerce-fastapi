from pydantic import BaseModel


class ImageBase(BaseModel):
    url: str


class ImageSchema(ImageBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True
