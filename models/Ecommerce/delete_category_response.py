from pydantic import BaseModel, Field


class DeletedCategory(BaseModel):
    __v: int
    id: str = Field(..., alias='_id')
    created_at: str = Field(..., alias='createdAt')
    name: str
    owner: str
    updated_at: str = Field(..., alias='updatedAt')


class Data(BaseModel):
    deleted_category: DeletedCategory = Field(..., alias='deletedCategory')


class DeleteCategoryResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(..., alias='statusCode')
    success: bool