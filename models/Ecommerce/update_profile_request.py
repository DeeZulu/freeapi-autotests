from typing import Optional

from pydantic import BaseModel, Field


class UpdateProfileRequest(BaseModel):
    country_code: str | Optional = Field(validation_alias='countryCode')
    first_name: str| Optional = Field(validation_alias='firstName')
    last_name: str| Optional = Field(validation_alias='lastName')
    phone_number: str| Optional = Field(validation_alias='phoneNumber')
