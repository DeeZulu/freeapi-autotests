from typing import Optional

from pydantic import BaseModel, Field


class UpdateProfileRequest(BaseModel):

    country_code: Optional[str] = Field(default=None, alias='countryCode')
    first_name: Optional[str] = Field(default=None, alias='firstName')
    last_name: Optional[str] = Field(default=None, alias='lastName')
    phone_number: Optional[str] = Field(default=None, alias='phoneNumber')
