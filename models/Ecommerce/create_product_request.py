from typing import List

from pydantic import BaseModel, Field, ConfigDict


class CreateProductRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    category: str
    description: str
    main_image: str = Field(alias='mainImage')
    name: str
    price: str
    stock: str
    sub_images: List[str] = Field(alias='subImages')
