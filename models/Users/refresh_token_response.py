from pydantic import BaseModel, Field


class Data(BaseModel):
    access_token: str = Field(validation_alias='accessToken')
    refresh_token: str = Field(validation_alias='refreshToken')


class RefreshTokenResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(validation_alias='statusCode')
    success: bool