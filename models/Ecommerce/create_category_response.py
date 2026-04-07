from pydantic import BaseModel, Field


class Data(BaseModel):
    __v: int
    _id: str
    created_at: str = Field(alias='createdAt')
    name: str
    owner: str
    updated_at: str = Field(alias='updatedAt')


class CreateCategoryResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(alias='statusCode')
    success: bool
