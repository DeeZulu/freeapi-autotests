from typing import Any, List, Optional

from pydantic import BaseModel, Field


class MainImage(BaseModel):
    _id: str
    local_path: str = Field(..., alias='localPath')
    url: str


class SubImage(BaseModel):
    _id: str
    local_path: str = Field(..., alias='localPath')
    url: str


class Product(BaseModel):
    __v: int
    _id: str
    category: str
    created_at: str = Field(..., alias='createdAt')
    description: str
    main_image: MainImage = Field(..., alias='mainImage')
    name: str
    owner: str
    price: int
    stock: int
    sub_images: List[SubImage] = Field(..., alias='subImages')
    updated_at: str = Field(..., alias='updatedAt')


class Data(BaseModel):
    has_next_page: bool = Field(..., alias='hasNextPage')
    has_prev_page: bool = Field(..., alias='hasPrevPage')
    limit: int
    next_page: Optional[int] = Field(default=None, alias='nextPage')
    page: int
    prev_page: Any = Field(..., alias='prevPage')
    products: List[Product]
    serial_number_start_from: int = Field(..., alias='serialNumberStartFrom')
    total_pages: int = Field(..., alias='totalPages')
    total_products: int = Field(..., alias='totalProducts')


class GetAllProductsResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(..., alias='statusCode')
    success: bool