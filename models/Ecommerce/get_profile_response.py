from pydantic import BaseModel, Field


class Data(BaseModel):
    _id: str
    first_name: str = Field(validation_alias='firstName')
    last_name: str = Field(validation_alias='lastName')
    country_code: str = Field(validation_alias='countryCode')
    phone_number: str = Field(validation_alias='phoneNumber')
    owner: str
    created_at: str = Field(validation_alias='createdAt')
    updated_at: str = Field(validation_alias='updatedAt')
    __v: int


class GetProfileResponse(BaseModel):
    status_code: int = Field(validation_alias='statusCode')
    data: Data
    message: str
    success: bool
