from pydantic import BaseModel, Field


class Data(BaseModel):
    __v: int
    _id: str
    country_code: str = Field(validation_alias='countryCode')
    created_at: str = Field(validation_alias='createdAt')
    first_name: str = Field(validation_alias='firstName')
    last_name: str = Field(validation_alias='lastName')
    owner: str
    phone_number: str = Field(validation_alias='phoneNumber')
    updated_at: str = Field(validation_alias='updatedAt')


class UpdateProfileResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(validation_alias='statusCode')
    success: bool
