from typing import List

from pydantic import BaseModel, Field

class ImageModel(BaseModel):
    id: str = Field(alias="_id")
    url: str
    local_path: str = Field(alias="localPath")

class Data(BaseModel):
    __v: int
    _id: str
    category: str
    created_at: str = Field(..., alias='createdAt')
    description: str
    main_image: ImageModel = Field(..., alias='mainImage')
    name: str
    owner: str
    price: int
    stock: int
    sub_images: List[ImageModel] = Field(..., alias='subImages')
    updated_at: str = Field(..., alias='updatedAt')


class CreateProductResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(..., alias='statusCode')
    success: bool