from typing import List

from pydantic import BaseModel


class Data(BaseModel):
    __v: int
    _id: str
    category: str
    createdAt: str
    description: str
    mainImage: str
    name: str
    owner: str
    price: int
    stock: int
    subImages: List[str]
    updatedAt: str


class CreateProductResponse(BaseModel):
    data: Data
    message: str
    statusCode: int
    success: bool
